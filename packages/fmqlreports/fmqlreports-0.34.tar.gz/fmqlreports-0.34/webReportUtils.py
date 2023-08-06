#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter

import numpy
import math

from fmqlutils.cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, SCHEMA_LOCN_TEMPL, DATA_LOCN_TEMPL, DATARF_LOCN_TEMPL, TMPWORKING_LOCN_TEMPL
from fmqlutils.schema.reduceReportTypes import TYPEREDUCE_LOCN_TEMPL
from fmqlutils.reporter.reportUtils import MarkdownTable

"""
Site
"""
SITE_DIR_TEMPL = "/data/vista/{}/ReportSite/" 

TOP_MD_TEMPL = """---
layout: default
title: {}
---

# {}

"""

def dtdd(dt, dd):
    return "{}\n:    {}\n\n".format(dt, dd)
    
"""
Hide need to include DATA_LOCN_TEMPL and SCHEMA
"""
def filteredResultIterator(stationNo, flTyp, useRF=False, startAtReply=""):
    locn = DATARF_LOCN_TEMPL.format(stationNo) if useRF else DATA_LOCN_TEMPL.format(stationNo)
    return FilteredResultIterator(locn, flTyp, startAtReply=startAtReply)
    
def loadSelectTypes(stationNo):
    return  json.load(open(SCHEMA_LOCN_TEMPL.format(stationNo) + "SELECT_TYPES.json"))

# ############################### Stat Utils #########################

"""
Shows off key stats with a little (obvious) stats observations

https://docs.scipy.org/doc/numpy/user/

TODO: more on numpy (ie/ go through it as go through books)
"""
def reportKeyStats(kstats):
    print("Count Values: {}".format(kstats["count"]))
    mn = kstats["mean"]
    print("Mean: {}".format(mn))
    M = kstats["median"]
    print("Median (M): {}".format(M))
    if M > mn:
        print("\t... M bigger than Mean so data skews left")
    elif M < mn:
        print("\t... M smaller than Mean so data skews right")
    print("Standard Deviation (s): {}".format(kstats["std"]))
    print("\treflect skew of min {} and max {}".format(kstats["min"], kstats["max"]))
    print("IQR: {}".format(kstats["iqr"]))                                                   
    print("\tbetween 1st ({}) and 3rd ({}) quartiles".format(kstats["quartileOne"], kstats["quartileThree"]))
    if "olt" in kstats:
        print("Outliers below", kstats["olt"])
    print("Outliers above\n", kstats["oht"])
    
"""
Key stats for distribution of values

min, max
Quartile: 1, 2 (Median), 3 for data-spread
... "five-number summary" ideal for data w/ outliers and a 'box-and-whisker' plot 
... Quartiles divide a rank-ordered data set into four equal parts at 25, 50, 75
percentiles
IQR
... "midspread" - best at spread if outliers
olt < (Q1-1.5*IQR)
oht > Q3+1.5*IQR
... for key outliers: < are lows, > are highs. Only present if > max, < min
mean
std
... for symm distributions with no outliers where five numbers don't kick in

TODO: consider <span class='yellowIt'>{:.2f}%</span> and numpy.around or
roundFloat (see below)

oht: 1.5 == "inner fences"
major outliers: Q3 + 3*IQR == "outer fences" ... need name for this.

Note: this is 'Univariate method' (See: https://www.kdnuggets.com/2017/01/3-methods-deal-outliers.html / 'Minkowski error' etc)

https://en.wikipedia.org/wiki/Outlier (Tukey's fences)
- above: Q3 + K(Q3-Q1) where K is 1.5 and K = 3 is "far out"
- below: Q1 - K(Q1-Q3)
ie/ K times Quartile. Fences for box plots.
"""
def keyStats(values):
    quartileOne = numpy.percentile(values, 25)
    median = numpy.percentile(values, 50)
    quartileThree = numpy.percentile(values, 75)
    # get variance in middle 50% of data
    # numpy.subtract(*numpy.percentile(values, [75, 25]))
    iqr = quartileThree - quartileOne # interquartile range    
    oht = quartileThree + (1.5 * iqr) # Outlier High above this
    cntValsGTOHT = sum(1 for val in values if val > oht) 
    ohto = quartileThree + (3 * iqr) # idea of "outer fence": TODO: get name
    cntValsGTOHTO = sum(1 for val in values if val > ohto) 
    stats = {"total": sum(val for val in values), "count": len(values), "min": numpy.min(values), "quartileOne": quartileOne, "median": median, "quartileThree": quartileThree, "max": numpy.max(values), "iqr": iqr, "oht": oht, "ohto": ohto, "mean": numpy.mean(values), "std": numpy.std(values)}
    olt = quartileOne - (1.5 * iqr) # Outlier Low below this
    if int(olt) > 0: # only olt if > 0 ie/ negative ie/ all acceptable
        stats["olt"] = olt
    """
    Own: should show outliers? only go into outliers if big ie/ if pretty smooth 
    """
    stats["hasOutliers"] = True if stats["max"] - stats["oht"] > stats["median"] else False
    if cntValsGTOHT:
        stats["gtoht"] = cntValsGTOHT
    if cntValsGTOHTO:
        stats["gtohto"] = cntValsGTOHTO
    return stats
    
"""
Use typically for byValueCount off typer or a Counter

    "a": 1
    "b": 2
    "c": 1
    
-----> [a, b, b, c]

and can pass into kstats if forceInt

Note: forceInt is for the measured values which may be integers but
are in string form.
"""
def flattenFrequencyDistribution(freqDistrib, forceInt=True):
    freqDistribFlat = []
    for entry in freqDistrib:
        f = [int(entry) if forceInt else entry for i in range(int(freqDistrib[entry]))]
        freqDistribFlat.extend(f)
    return freqDistribFlat
    
"""
New Stats to expand:

- (basic) and relative (percent/ration) frequency distribution ie/ cnt occurrences
        from collections import Counter
        Counter([...]) ... 
  ... put relatives into a stacked bar chart
  ... conditional => a number of freq distribs, one each per condition (ex/ for PDFs, WSs)
- bar (or a pie) to histogram: when # of distict values too big then go to histogram
- null hypothesis/expected frequencies: variables unrelated (type of image and WS?)
  - https://www.spss-tutorials.com/chi-square-independence-test/
"""

"""
- cumulative frequencies add as go (https://www.spss-tutorials.com/frequency-distribution-what-is-it/) ... no good for nominals ("French" or "PDF") but for good/better/best ...
  ie age of patients  ... https://www.wyzant.com/resources/lessons/math/statistics_and_probability/averages/cumulative_frequency_percentiles_and_quartiles
  ... A cumulative frequency graph, also known as an Ogive
  ... good site for stuff.
  ... cumulative freq can be used to gen quartiles
"""        

"""
Clustering, numpy has it (ntlk uses it - but mainly see intelligent web book)
... k ... and clumping 'users' or ... based on similarity/distance.
"""

"""
after excel, try matplotlib, networkx 
"""
    
# ############################ Simple Report Utils #################

def roundFloat(no):
    no = no.round(2)
    if no.is_integer():
        return int(no)
    return no
    
# ############################ Plot Utils ##########################

"""
Crude Example of Graph

import matplotlib.pyplot as plt

See: https://python-graph-gallery.com/120-line-chart-with-matplotlib/ and
https://matplotlib.org/gallery/index.html

    plot([2007, 2008, 2009, 2010], [1, 2, 3, 4])

"""
def plot(xs, ys):

    import matplotlib.pyplot as plt
    plt.plot(xs, ys, "ro")
    plt.xlabel("Time")
    plt.ylabel("Ibs")
    plt.show()
            
# ######################### Reduce Users ###########################

"""
Returns Users, Indexed 

Note: RF part ie/ 200 into DataRF will move out of here. Tmp index
maker for any type (including RF types) will become one simple utility.

TODO: go to lookup by IEN as simpler
"""
def reduce200(stationNo, onlyUsers=None, forceNew=False):

    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "userReduction.json"
    
    if not forceNew:
        try:
            infosByRef = json.load(open(jsnFl))
        except:
            pass
        else:
            return infosByRef

    print("First time through, creating index by id for Users (200) for {}".format(stationNo))
    
    dataLocn = DATA_LOCN_TEMPL.format(stationNo)
    resourceIter = FilteredResultIterator(dataLocn, "200")
    infosByRef = {}
    cnt = 0
    for resource in resourceIter:
        cnt += 1
                
        if cnt % 1000 == 0:
            print("Processed another 1000 users - now at {:,}".format(len(infosByRef)))
        
        if onlyUsers and resource["_id"] not in onlyUsers:
            continue
        
        userId = "{} [{}]".format(resource["label"], resource["_id"])
                
        info = {"hasProps": sorted([key for key in resource.keys() if key not in set(["_id", "label", "type"])])}
        
        if "creator" in resource:
            if resource["creator"]["id"] == "200-0":
                info["is_created_by_0"] = True
            else:
                createdId = "{} [{}]".format(resource["creator"]["label"], resource["creator"]["id"])
                info["creator"] = createdId
        
        if "date_entered" in resource:
            info["date_entered"] = resource["date_entered"]["value"]
            
        if "title" in resource:
            info["title"] = resource["title"]["label"] # it's a pointer
            
        if "ssn" in resource:
            info["ssn"] = resource["ssn"]
            
        # used for lookup BEFORE SSN in setup. goes with subject_organizations etc
        if "secid" in resource:
            info["secid"] = resource["secid"]
            if "subject_organization" in resource and resource["subject_organization"] != "Department Of Veterans Affairs":
                raise Exception("Expected Subject Org for sec id to always be VA!")
            
        if "termination_date" in resource:
            info["termination_date"] = resource["termination_date"]["value"]
        if "termination_reason" in resource:
            info["termination_reason"] = resource["termination_reason"] 
            
        if "network_username" in resource:
            info["network_username"] = resource["network_username"]   

        # Consider "first sign on"
        if "visited_from" in resource:
            finalVisitedTime = None
            visitedFroms = {}
            for i, mresource in enumerate(resource["visited_from"]):
                if "visited_from" in mresource: 
                    visitedFrom = re.sub(r'[^\d]+', '', mresource["visited_from"])
                    duzAtHomeSite = mresource["duz_at_home_site"] if "duz_at_home_site" in mresource else ""
                    siteName = mresource["site_name"] if "site_name" in mresource else ""
                    siteId = ":".join([visitedFrom, duzAtHomeSite, siteName])
                    details = None
                    if "first_visit" in mresource or "last_visited" in mresource:
                        details = {}
                        if "first_visit" in mresource:
                            details["first"] = mresource["first_visit"]["value"]
                        if "last_visited" in mresource:
                            details["last"] = mresource["last_visited"]["value"]                            
                    visitedFroms[siteId] = details
            if len(visitedFroms):
                info["signed_on_froms"] = visitedFroms
        if "last_signon_date_time" in resource:
            info["last_signon_date_time"] = resource["last_signon_date_time"]["value"]
                
        if "network_username" in resource:
            info["network_username"] = resource["network_username"] 
            
        if "user_class" in resource:
            if len(resource["user_class"]) > 1:
                raise Exception("Expected only one user class assertion - ie/ singleton multiple")
            info["user_class"] = [uci["user_class"]["label"] for uci in resource["user_class"]][0]
            
        if "file_manager_access_code" in resource and resource["file_manager_access_code"] == "@":
            info["has_fileman_programmer_access"] = True
                
        if "primary_menu_option" in resource:
            info["primary_menu_option"] = resource["primary_menu_option"]["label"]
                
        if "secondary_menu_options" in resource:
            smos = set() # allows for dups with crude SMO addition
            for smo in resource["secondary_menu_options"]:
                if not re.match(r'\d+$', smo["secondary_menu_options"]["label"]):
                    smos.add(smo["secondary_menu_options"]["label"])
            if len(smos):
                info["secondary_menu_options"] = sorted(list(smos))
            
        if "delegated_options" in resource:
            dos = set()
            for delo in resource["delegated_options"]:
                if not re.match(r'\d+$', delo["delegated_options"]["label"]):
                    dos.add(delo["delegated_options"]["label"])
            if len(dos):                   
                info["delegated_options"] = sorted(list(dos))
            
        if "keys" in resource:
            keys = set() 
            for key in resource["keys"]:
                if not re.match(r'\d+$', key["key"]["label"]):
                    keys.add(key["key"]["label"])
            if len(keys):
                info["keys"] = sorted(list(keys))   
                
        if "preferred_editor" in resource: # for REMOTE user checks
            info["preferred_editor"] = resource["preferred_editor"]["label"]
            
        if "terminal_type_last_used" in resource:
            info["terminal_type_last_used"] = resource["terminal_type_last_used"]["label"] 
        
        infosByRef[userId] = info 
    
    print("Serializing and Returning Index of {:,} Users (200)".format(cnt))

    json.dump(infosByRef, open(jsnFl, "w"), indent=4)
    
    return infosByRef
    
# ############################ Reduce Patient ########################

def reduce2(stationNo, forceNew=False):

    jsnFl = TMPWORKING_LOCN_TEMPL.format(stationNo) + "patientReduction.json"
    
    if not forceNew:
        try:
            infosByIEN = json.load(open(jsnFl))
        except:
            pass
        else:
            return infosByIEN

    print("First time through, creating patient entered reduction for {}".format(stationNo))
    sys.stdout.flush()
    
    dataLocn = DATA_LOCN_TEMPL.format(stationNo)
    resourceIter = FilteredResultIterator(dataLocn, "2")
    infosByIEN = {}
    PROPS_TO_TAKE = set([
        "name", 
        "sex", 
        "date_of_birth", 
        "social_security_number", 
        
        "who_entered_patient", 
        "date_entered_into_file", 
        
        "city", 
        "state", 
        "zip_code", 
        
        "period_of_service", 
        
        "date_of_death", 
        "death_entered_by", 
        
        "primary_eligibility_code", 
        "combat_service_indicated", 
        
        "preferred_facility", 
        
        # TODO: expand these - ensure all id's used by VA/C are in here
        "integration_control_number", 
        "subscription_control_number", # 774 entries for CIRN (see if sync file
        "full_icn"    
    ])
    for resource in resourceIter:
        patientIEN = resource["_id"].split("-")[1]
        info = {"ien": patientIEN}
        for prop in PROPS_TO_TAKE:
            if prop in resource:
                if isinstance(resource[prop], list):
                    raise Exception("Not reducing multiples of 2")
                if isinstance(resource[prop], dict):
                    if "value" in resource[prop]:
                        info[prop] = resource[prop]["value"]
                    else:
                        info[prop] = resource[prop]["label"]
                else: 
                    info[prop] = resource[prop]
        infosByIEN[patientIEN] = info
        if len(infosByIEN) % 1000 == 0:
            print("Processed another 1000 patients - now at {:,}".format(len(infosByIEN)))
            sys.stdout.flush()
    
    print("Serializing and Returning Index of {:,} Users (2)".format(len(infosByIEN)))
    sys.stdout.flush()

    json.dump(infosByIEN, open(jsnFl, "w"), indent=4)
    
    return infosByIEN
    
# ############################ Reduce Location (44) ###########################

"""
Like other "anchor file" reductions, preludes to more formal reframes (RF) that
split out different types of key data into distinct types AND establishes a
lookup 

<----- will see if AppointmentHospitalLocation can be a sub class or split out appt info

Note: allows RF take - right now that RF is just the result of extracting the
44.001 and other multiples.
"""
def reduce44(stationNo, useRF=False, forceNew=False): 

    """
                for litProp in ["patient_friendly_name", "physical_location", "length_of_appointment", "default_appointment_type"]: # includes enum
                if litProp not in resource:
                    continue
                red[litProp] = resource[litProp]
            for dtProp in ["inactivate_date", "reactivate_date"]:
                if dtProp not in resource:
                    continue
                red[dtProp] = resource[dtProp]["value"]
            for refProp in ["stop_code_number", "institution", "division", "type_extension", "default_provider"]:
                if refProp not in resource:
                    continue
                    
    Add mult of provider (list) etc and the letter props
    """
    pass

    # TODO: out of custom reports
    
# ############################ Simple Reusable MD Makers ###############################

def mdFilesOfDomain(stationNo, domainName, bottomFileNo, beyondFileNo, usedFiles):

    selectTypes = loadSelectTypes(stationNo)

    fileTypeInfos = [typeInfo for typeInfo in selectTypes["results"] if "number" in typeInfo and float(typeInfo["number"]) >= bottomFileNo and float(typeInfo["number"]) < beyondFileNo and "count" in typeInfo]
     
    mu = """There are <span class="yellowIt">{:,}</span> files in the system dedicated to the _{}_ ...
    
""".format(len(fileTypeInfos), domainName)
    
    tbl = MarkdownTable(["Name", "\#", "Count"])
    for typeInfo in fileTypeInfos:
        tbl.addRow([
                "__{}__".format(typeInfo["name"]) if typeInfo["name"] in usedFiles else typeInfo["name"], 
            typeInfo["number"], 
            typeInfo["count"]
    ])
    mu += tbl.md() + "\n\n"
        
    return mu
    
# ######################### Simple Type Utils ########################

class PropertyCounter:
    
    def __init__(self):
        self.__counts = Counter()
        self.__countResources = 0
            
    def resourceProperties(self, props):
        for prop in props:
            self.__counts[prop] += 1
        self.__countResources += 1
            
    def mandatories(self):
        return sorted([prop for prop in self.__counts if self.__counts[prop] == self.__countResources]) 
            
    def optionalCounts(self):
        return dict((prop, self.__counts[prop]) for prop in self.__counts if self.__counts[prop] < self.__countResources) 
