#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import re
import json
from collections import OrderedDict, Counter
from datetime import datetime
import logging

from .. import VISTA_DATA_BASE_DIR
from ..cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, BASE_LOCN_TEMPL, DATA_LOCN_TEMPL
from reduceReportType import TypeReducer, SubTypeReducer, reportReductions, DEFAULT_FORCE_COUNT_PTER_TYPES, isValidDayForm

DATAREDUCTION_LOCN_TEMPL = BASE_LOCN_TEMPL + "DataReductions/"
TYPEREDUCE_LOCN_TEMPL = DATAREDUCTION_LOCN_TEMPL + "Types/"
REPORTS_LOCN_TEMPL = BASE_LOCN_TEMPL + "Reports/"
TYPEREPORT_LOCN_TEMPL = REPORTS_LOCN_TEMPL + "Types/"

"""
As command, fmqltyper

Same pattern as v2er, cacher, using 
- [a] /data/vista/{STATIONNO}/... locations for reductions and reports and 
- [b] taking a configuration from the location the runtime runs from. 
- [c] that 'local' location is usually just a place for these configurations
- [d] onAndAfterDay/upToDay rely on create property and if set, want a "reductionLabel" to differentiate them

TODO:
- try yaml config https://pyyaml.org/wiki/PyYAMLDocumentation as can embed code 
easily ie/ include custom filters/enhancers inline so no need for custom ie/ can't
now invoke dynamically in command line
- for now, using print, not logging. May move over to one pattern 
"""

def reduceReportTypes(stationNumber, types, dataLocnTempl, forceRedo=False, createDate={}, reductionLabel="", subTypeProps={}, forceCountPointerTypesExtra={}, forceCountProperties={}, onAndAfterDay="", upToDay="", countDateMonth=False, countDateMonthFor=[], customEnhancers={}):

    start = datetime.now()
    
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)    
    ch = logging.StreamHandler(sys.stdout)
    format = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(format)
    log.addHandler(ch)
    
    # Used to ensure 
    def ensureLocation(locn):
        if not os.path.isdir(locn):
            os.mkdir(locn)
        return locn
    ensureLocation(DATAREDUCTION_LOCN_TEMPL.format(stationNumber))
    ensureLocation(REPORTS_LOCN_TEMPL.format(stationNumber))
                    
    typesAndDates = dict((typId, createDate[typId] if typId in createDate else "") for typId in types)
    
    if onAndAfterDay:
        if not isValidDayForm(onAndAfterDay):
            raise Exception("Invalid 'on and after day': {}".format(onAndAfterDay))

    if upToDay:
        if not isValidDayForm(upToDay):
            raise Exception("Invalid 'up to day': {}".format(upToDay))
            
    if (upToDay or onAndAfterDay) and reductionLabel == "":
        raise Exception("You must name the reduction ('reductionLabel') for time limited ('onAndAfterDay'/'upToDay') reductions")
        
    def getCreateDay(resource, createDateProp):
        value = resource[createDateProp]["value"] if "value" in resource[createDateProp] else resource[createDateProp]["label"]
        dayValue = value.split("T")[0] # using lex comp on ISO‑8601 form as fastest
        if not isValidDayForm(dayValue):
            log.debug("Can't get create day as its date has invalid value: {}".format(dayValue))
            return None
        return dayValue
            
    logging.info("About to reduce (and report) on {} types, starting at {} [PID {}]".format(len(typesAndDates), start, os.getpid()))

    count = 0 # allow for 0 - no i defined
    filtered = 0      
    dataLocn = dataLocnTempl.format(stationNumber)  
    for i, typId in enumerate(sorted(typesAndDates, key=lambda x: float(re.sub(r'\_', '.', x))), 1):
        startTyp = start if len(types) == 1 else datetime.now()
            
        reductionLocn = ensureLocation(TYPEREDUCE_LOCN_TEMPL.format(stationNumber))
        redFFL = "{}/{}{}Reduction.json".format(reductionLocn, typId, reductionLabel)
        
        if forceRedo == False and os.path.isfile(redFFL):
            logging.info("Not reducing (and reporting) {} as already exists and NOT forceredo".format(typId))
            continue

        logging.info("Reducing (and reporting) {}".format(typId))
        
        startAtReply = ""
        if onAndAfterDay:
            if not re.search(r'RF', dataLocn):
                store = FMQLReplyStore(dataLocn)
                startAtReply = store.firstReplyFileOnOrAfterCreateDay(typId, typesAndDates[typId], onAndAfterDay)
                if startAtReply == "":
                    logging.info("** Exiting: can't find Reply to start at on and after day {}, create property {}".format(onAndAfterDay, typesAndDates[typId]))
                    break
                logging.debug("Start Efficiency: configuring Iterator for on and after time: on or after day {}, create property {}, starting at reply {}".format(onAndAfterDay, typesAndDates[typId], startAtReply))
            else:
                logging.debug("No Start Efficiency: taking first Reply and ignoring onAndAfterDay as walking reformed (RF) data which is usually from out of order multiples")
        resourceIter = FilteredResultIterator(dataLocn, typId, isOrdered=False, startAtReply=startAtReply)
        fcpts = DEFAULT_FORCE_COUNT_PTER_TYPES
        if typId in forceCountPointerTypesExtra:
            fcpts.extend(forceCountPointerTypesExtra[typId])
        fcps = forceCountProperties[typId] if typId in forceCountProperties else []
        countDateMonthType = True if (countDateMonth or typId in countDateMonthFor) else False
        if typId in subTypeProps: 
            if isinstance(subTypeProps[typId], list):
                stps = subTypeProps[typId]
            else:
                stps = [subTypeProps[typId]]
            logging.info("Subtyping by '{}'".format("-".join(stps)))
            rtr = SubTypeReducer(typId, createDateProp=typesAndDates[typId], subTypeProps=stps, forceCountPointerTypes=fcpts, forceCountProperties=fcps, countDateMonth=countDateMonthType)
        else:
            rtr = TypeReducer(typId, createDateProp=typesAndDates[typId], forceCountPointerTypes=fcpts, forceCountProperties=fcps, countDateMonth=countDateMonthType)
        customEnhancer = None
        if typId in customEnhancers:
            customEnhancer = customEnhancers[typId]
            
        msgThres = 50000 
        upToDayStopped = False 
        filtered = Counter()  
        for i, resource in enumerate(resourceIter, 1):
            count += 1
            filteredSoFar = sum(filtered[c] for c in filtered)
            if i % msgThres == 0:
                logging.debug("Checked {} more resources for total of {:,}, sub type reducers {:,}, so far filtered {:,}, now in reply {} - {}".format(msgThres, i, rtr.subTypeReducerCount(), filteredSoFar, resourceIter.currentReplyFile(), datetime.now() - start))
            idProp = "id" if "id" in resource else "_id"
            if customEnhancer:
                resource = customEnhancer.enhance(resource)
                if not resource:
                    filtered["CUSTOM"] += 1
                    continue
            # Allows for out of order too
            if onAndAfterDay or upToDay:
                if typesAndDates[typId] not in resource:
                    filtered["NOCREATEDATE"] += 1
                    continue
                createDay = getCreateDay(resource, typesAndDates[typId])
                if not createDay:
                    filtered["BADCREATEDATE"] += 1
                    continue
                if onAndAfterDay and createDay < onAndAfterDay:
                    filtered["LTONAFTER"] += 1
                    continue
                # Can't efficiently cut out as start for appt can go on (ie/ not ordered)
                if upToDay and createDay >= upToDay:
                    filtered["GTEUPTO"] += 1
                    continue 
            rtr.transform(resource)
            
        pattData = rtr.reductions()
        for red in pattData:
            red["_stationNumber"] = stationNumber
            if reductionLabel:
                red["_label"] = reductionLabel
                            
        json.dump(pattData, open(redFFL, "w")) 
     
        reportLocn = ensureLocation(TYPEREPORT_LOCN_TEMPL.format(stationNumber))
        reportReductions(pattData, "{}/{}{}Report.txt".format(reportLocn, typId, reductionLabel))
        
        if len(filtered):
            filteredMU = "/".join(["{} [{}]".format(reason, filtered[reason]) for reason in filtered])
            logging.info("Finished after {:,} resources of {} in {} at {}, {:,} explicitly filtered with {}".format(count, typId, datetime.now() - startTyp, datetime.now(), sum(filtered[c] for c in filtered), filteredMU))
        else:
            logging.info("Finished after {:,} resources of {} in {} at {}".format(count, typId, datetime.now() - startTyp, datetime.now()))
            
    if len(types) > 1:
        logging.info("Finished {} types at {} in {}".format(len(types), datetime.now(), datetime.now() - start))

# ############################# Driver ####################################

"""
Form of configs

    {
        "stationNumber": "999",
        "types": ["2"],
        "createDateByType": {"2": "date_entered_into_file" },
        "forceRedo": False
    }
    
"""
def main():

    if len(sys.argv) < 2:
        print "need to specify configuration ex/ {VISTAAB}.json - exiting"
        return

    configBase = sys.argv[1].split(".")[0]

    if not os.path.isfile("{}.json".format(configBase)):
        print "No config file {}.json - exiting".format(configBase)
        return

    config = json.load(open("{}.json".format(configBase)), object_pairs_hook=OrderedDict)

    if "stationNumber" not in config:
        print "No station number in configuration - exiting"
        return
    stationNumber = config["stationNumber"]
    
    dataLocnTempl=DATA_LOCN_TEMPL if "dataLocationTemplate" not in config else config["dataLocationTemplate"] # allows RF override etc. May nix just for that option?

    # "types": [], "createDateByType": {"{TYPE}": "{creation_date_property}" ...}
    # ... if don't set "types" then all types will be used
    if "types" not in config or len(config["types"]) == 0:
        dataLocn = dataLocnTempl.format(stationNumber)    
        print "Typing ALL available data as no subset specified"
        types = FMQLReplyStore(dataLocn).availableTypes()
    else:
        types = config["types"]
            
    reduceReportTypes(
        stationNumber, 
        types,
        dataLocnTempl=dataLocnTempl,
        forceRedo=(True if ("forceRedo" in config and config["forceRedo"] == True) else False),
        subTypeProps=(config["subTypeProps"] if "subTypeProps" in config else {}),
        createDate=({} if "createDate" not in config else config["createDate"]), 
        onAndAfterDay=(config["onAndAfterDay"] if "onAndAfterDay" in config else ""),
        upToDay=(config["upToDay"] if "upToDay" in config else ""),
        reductionLabel=(config["reductionLabel"] if "reductionLabel" in config else ""),
        countDateMonth=(True if "countDateMonth" in config and config["countDateMonth"] else False),
        countDateMonthFor=(config["countDateMonthFor"] if "countDateMonthFor" in config else []),
        forceCountProperties=(config["forceCountProperties"] if "forceCountProperties" in config else {}), 
        forceCountPointerTypesExtra=(config["forceCountPointerTypesExtra"] if "forceCountPointerTypesExtra" in config else {})
    )
        
if __name__ == "__main__":
    main()
    
