#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import re
import json
from collections import OrderedDict, defaultdict, Counter
from datetime import datetime
import logging

from ..cacher.cacherUtils import DATA_LOCN_TEMPL, DATARF_LOCN_TEMPL
from reduceReportTypes import TYPEREDUCE_LOCN_TEMPL
from reduceReportType import DEFAULT_MAX_NOMINAL_VALUES

"""
Expect 1 ALL (returned first) and many sub's with one or more properties. Note
that may have > that number of properties in split. 'expectSubTypeProperty' 
enforces the minimum.
"""
def splitTypeDatas(stationNo, typ, reductionLabel="", expectSubTypeProperties=[], expectSubTypeProperty=""):
    if expectSubTypeProperty: # for backward compatibility
        expectSubTypeProperties = [expectSubTypeProperty]
    typeDatas = json.load(open(TYPEREDUCE_LOCN_TEMPL.format(stationNo) + "{}{}Reduction.json".format(typ, reductionLabel)))
    if isinstance(typeDatas, dict): # old and dictionary only of ALL
        return typeDatas, []
    allTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" not in typeData]
    if len(allTypeDatas):
        if len(allTypeDatas) != 1:
            raise Exception("Expect one and only one ALL type data in a type data list")
    allTypeData = allTypeDatas[0]
    subTypeDatas = [typeData for typeData in typeDatas if "_subTypeId" in typeData]
    if len(subTypeDatas) and len(expectSubTypeProperties):
        subTypeProps = set(subTypeDatas[0]["_subTypeId"].split(":")[0].split("-"))
        if subTypeProps != set(expectSubTypeProperties):
            raise Exception("Expect sub type prop(s) \"{}\" but st has \"{}\"".format(":".join(sorted(expectSubTypeProperties)), subTypeDatas[0]["_subTypeId"]))
    elif expectSubTypeProperty:
        raise Exception("No sub type datas but expect {} as sub type property".format(expectSubTypeProperty))
    return allTypeData, subTypeDatas
    
"""
Combine sub types to broader criteria (including no criteria)
"""
def combineSubTypes(sts, subTypePropsSubset=[], forceCountProps=[]):
    def makeWantedSubTypeId(st, propsWanted):
        propsWanted = sorted(propsWanted)
        pieces = st["_subTypeId"].split(":")
        props = pieces[0].split("-")
        if len(set(propsWanted) - set(props)):
            raise Exception("Expect props wanted to be subset of those in st")
        allValues = [pieces[i] for i in range(1, len(pieces))]
        values = []
        for i, prop in enumerate(props):
            if prop in propsWanted:
                values.append(allValues[i])
        return "{}:{}".format("-".join(propsWanted), ":".join(values))
    stsBySTIdWanted = defaultdict(list)
    # ALL or broader groups
    if len(subTypePropsSubset):
        try:
            makeWantedSubTypeId(sts[0], subTypePropsSubset)
        except:
            raise Exception("Can't combine as subtype properties wanted aren't all in sts")
        for st in sts:
            stIdWanted = makeWantedSubTypeId(st, subTypePropsSubset)
            stsBySTIdWanted[stIdWanted].append(st)
    else:
        stsBySTIdWanted["ALL"] = sts
    createDateProp = "" if "_createDateProp" not in sts[0] else sts[0]["_createDateProp"]
    csts = []
    for stIdWanted in sorted(stsBySTIdWanted):
        # only prop kept  
        cst = OrderedDict([("_subTypeId", stIdWanted), ("_total", 0)])
        if createDateProp:
            cst["_createDateProp"] = createDateProp
        csts.append(cst)
        """
        For now, not taking 'rangeTypes', "firstCreateDate" or "range" and not
        the reduction of LIST ie/ just the counters and counts
        """
        for st in stsBySTIdWanted[stIdWanted]:
            cst["_total"] += st["_total"]
            for prop in st:
                if re.match(r'_', prop):
                    continue
                if prop not in cst:
                    cst[prop] = dict((field, st[prop][field]) for field in st[prop] if field in ["count", "type", "byValueCount", "byWeekDay"])
                    continue
                cst[prop]["count"] += st[prop]["count"]
                # merge counter only if in cst already; otherwise ignore. If not in st
                # then remove from cst ie/ either all with prop have cntType or no merge
                for cntType in ["byValueCount", "byWeekDay"]:
                    if cntType in cst[prop]:
                        if cntType in st[prop]: 
                            cst[prop][cntType] = Counter(cst[prop][cntType]) + Counter(st[prop][cntType])
                            # can get huge - ex IPs in user etc (typer does the same)
                            if prop not in forceCountProps and len(cst[prop][cntType]) > DEFAULT_MAX_NOMINAL_VALUES:
                                del cst[prop][cntType]
                        else: # only delete from cst if another st with prop has none
                            del cst[prop][cntType]
    return csts
    
"""
Check Data: array of fileType and what's needed (array)
... ALL | TYPE | {REDUCTIONLABEL}

Ex/ [{"fileType": "3_081", "check": "TYPE"}]
"""
def checkDataPresent(stationNumber, dataToCheck):
    hasAll = True
    for dataInfo in dataToCheck:
        ftyp = dataInfo["fileType"]
        if not isinstance(dataInfo["check"], list):
            dataInfo["check"] = [dataInfo["check"]]
        checked = {}
        for toCheck in dataInfo["check"]:
            if re.match("ALL", toCheck):
                if toCheck == "ALL":
                    # note: doesn't check completeness. One will do!
                    fl = DATA_LOCN_TEMPL.format(stationNumber) + "{}-0.zip".format(ftyp)
                elif toCheck == "ALLRF":
                    fl = DATARF_LOCN_TEMPL.format(stationNumber) + "{}-0.zip".format(ftyp)
                else:
                    raise Exception("ALL options are ALL|ALLRF")
                if not os.path.isfile(fl):
                    checked[toCheck] = False
                    hasAll = False
                else:
                    checked[toCheck] = True
                continue
            reductionLabel = toCheck if toCheck != "TYPE" else ""
            fl = TYPEREDUCE_LOCN_TEMPL.format(stationNumber) + "{}{}Reduction.json".format(ftyp, reductionLabel)
            if not os.path.isfile(fl):
                checked[toCheck] = False
                hasAll = False
            else:
                checked[toCheck] = True
        del dataInfo["check"]
        dataInfo["checked"] = checked
    return hasAll, dataToCheck
    
"""
Convenience function for manipulating type reductions

Note: no need for singleValueCount as if singleValue => red[prop]["count"] has value
"""
def singleValue(typeRed, prop, ifMissingValue=""):
    if prop not in typeRed:
        if ifMissingValue:
            return ifMissingValue
        raise Exception("Unexpected missing property {} of reduction".format(prop))
    if not ("byValueCount" in typeRed[prop] and len(typeRed[prop]["byValueCount"].keys()) == 1):
        raise Exception("Unexpected > 1 value for prop {} of reduction".format(prop))
    return typeRed[prop]["byValueCount"].keys()[0]
    
"""
mu a bvc

Note: forceShowCount is to allow an ST BVC use to force a count for
a single value if count < total
"""
def muBVC(bvc, separator=", ", forceShowCount=False, countOnlyIfOver=-1):
    def labelKey(k):
        if re.search(r' \[', k):
            return k.split(" [")[0]
        if not re.search(r':', k):
            return k
        return k.split(":")[1]
    if len(bvc) == 1:
        k = bvc.keys()[0]
        if not forceShowCount:
            return labelKey(k)
        return "{} [{:,}]".format(labelKey(k), bvc[k]) 
    if countOnlyIfOver != -1 and len(bvc) > countOnlyIfOver:
        return "{:,}".format(len(bvc))
    mu = separator.join(["{} [{:,}]".format(labelKey(k), bvc[k]) for k in sorted(bvc, key=lambda x: bvc[x], reverse=True)])
    return mu
    
def muBVCOfSTProp(st, prop, separator=", ", addNotSet=True):
    if prop not in st:
        return "" # don't say NOTSET - just leave blank
    valueInfo = st[prop]
    if "byValueCount" not in valueInfo:
        raise Exception("Value missing BVC")
    bvc = valueInfo["byValueCount"]
    if addNotSet and st[prop]["count"] < st["_total"]:
        bvc["NOTSET"] = st["_total"] - st[prop]["count"]
    return muBVC(bvc, separator, st["_total"] != st[prop]["count"])
    