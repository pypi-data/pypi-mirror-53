#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime
import numpy

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from fmqlutils.schema.reduceTypeUtils import splitTypeDatas, checkDataPresent, singleValue
from ..webReportUtils import TOP_MD_TEMPL, SITE_DIR_TEMPL, keyStats, roundFloat, reduce200
from userClassifier import UserClassifier, couldBeMachineSSN, enforceLOA

"""
Basic User Type Summary/Overview

Requires:
- 3.081 (Type Reduction by User: YR1 unless 'smallSOSet')
- 200 (All/Indexed-reduce200)
- ... Will move to require image logs too to round out

Note: smallSOSet setup for case where only have small sample of SOs (ie/ take all)
"""

def webReportUser(stationNo, deidentify=False, smallSOSet=False):

    print("Preparing to make user report for {}{} - loading data ...".format(stationNo, " [DEIDENTIFY]" if deidentify else ""))

    allThere, details = checkDataPresent(stationNo, [
        {"fileType": "3_081", "check": "YR1" if not smallSOSet else "TYPE"},
        {"fileType": "200", "check": "ALL"} # Index
    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    mu = TOP_MD_TEMPL.format("{} Users".format(stationNo), "Users")

    userInfoByUserRef = reduce200(stationNo)    
    type3_081, st3_081s = splitTypeDatas(stationNo, "3_081", reductionLabel="" if smallSOSet else "YR1", expectSubTypeProperty="user")
    st3_081ByUserRef = dict((singleValue(st, "user"), st) for st in st3_081s if "user" in st)
    
    userClassifier = UserClassifier(stationNo, userInfoByUserRef, type3_081, st3_081ByUserRef)
    print("Classifying Users ...")
    classification = userClassifier.classify()
    print("... Classification complete")

    overallFirstSODate = type3_081["_firstCreateDate"].split("T")[0]
    overallLastSODate = type3_081["_lastCreateDate"].split("T")[0]
        
    BLURB_TEMPL = """Of the <span class='yellowIt'>{:,}</span> users known to the system, a minority <span class='yellowIt'>{}</span> ("__Active Users__") signed in between {} and {}, {}.

Most Active Users are real people but there are "__Machine Users__" for specialized VA batch applications or applications which manage end users themselves.

"""

    mu += BLURB_TEMPL.format(
        len(userInfoByUserRef),
        reportAbsAndPercent(len(classification["activeUserRefs"]), len(userInfoByUserRef)),
        overallFirstSODate, 
        overallLastSODate,
        "the period for which sign on logs are available" if smallSOSet else "the most recent year for which data is available"
    )  

    if deidentify:
        mu += "__DE-IDENTIFIED__: the names and national identifiers of real (Non-Machine) end users have been scrubbed from this report. VistA-specific IENs are left to identify such users for those with access to the system.\n\n"

    tbl = MarkdownTable(["Type", "Count"])
    tbl.addRow([
        "Total Users (200 entries)", 
        len(userInfoByUserRef)
    ])
    tbl.addRow([
        "Active Users (3.081s for period)", 
        reportAbsAndPercent(len(classification["activeUserRefs"]), len(userInfoByUserRef))
    ])
    tbl.addRow([
        "Active Proxy Users", 
        len(classification["activeProxyUserRefs"])
    ])  
    tbl.addRow([
        "Active Non Proxy, Machine Users", 
        len(classification["activeNonProxyMachineUserRefs"])
    ])
    tbl.addRow([
        "Active Remote Users", 
        reportAbsAndPercent(len(classification["activeRemoteUserRefs"]), len(classification["activeUserRefs"]))
    ])
    tbl.addRow([
        "Active Local Users", 
        reportAbsAndPercent(len(classification["activeLocalUserRefs"]), len(classification["activeUserRefs"]))
    ])
    tbl.addRow([
        "Sign ons (3.081 entries for period)", 
        type3_081["_total"]
    ])
    # "Remote Sign ons"
    mu += tbl.md() + "\n\n"
    
    mu += webReportPostmaster(
        classification["postmasterUserRef"],
        userInfoByUserRef[classification["postmasterUserRef"]],
        type3_081["_total"],
        st3_081ByUserRef[classification["postmasterUserRef"]],
        classification["warningsByUserRef"][classification["postmasterUserRef"]] if classification["postmasterUserRef"] in classification["warningsByUserRef"] else []
    )
        
    mu += webReportDoDUser(
        classification["dodUserRef"],
        userInfoByUserRef[classification["dodUserRef"]],
        type3_081["_total"],
        st3_081ByUserRef[classification["dodUserRef"]],
        classification["warningsByUserRef"][classification["dodUserRef"]] if classification["dodUserRef"] in classification["warningsByUserRef"] else [],
        deidentify
    )
    
    mu += webReportProxyUsers(
        classification["activeProxyUserRefs"], 
        classification["warningsByUserRef"],
        userInfoByUserRef,
        st3_081ByUserRef,
        type3_081["_total"]
    )

    mu += webReportNonProxyMachineUsers(
        classification["activeNonProxyMachineUserRefs"], 
        classification["warningsByUserRef"],
        userInfoByUserRef,
        type3_081["_total"],
        st3_081ByUserRef
    )

    mu += webReportRemoteUsers(
        classification["activeRemoteUserRefs"],
        classification["warningsByUserRef"],
        len(classification["activeUserRefs"]), 
        userInfoByUserRef, 
        type3_081["_total"], 
        st3_081ByUserRef,
        classification["remoteExcludeReasonCount"], 
        deidentify
    )
        
    mu += webReportLocalUsers(
        classification["activeLocalUserRefs"], 
        classification["warningsByUserRef"],
        len(classification["activeUserRefs"]), 
        userInfoByUserRef, 
        type3_081["_total"], 
        st3_081ByUserRef,
        deidentify
    )

    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    reportFile = userSiteDir + ("user.md" if not deidentify else "userDeId.md")
    print("Writing report {}".format(reportFile))
    open(reportFile, "w").write(mu)

"""
Proxy Users

Classifier enforces CONNECTOR PROXY, AV presence and LOA 2

TO ADD:
- workstation_name pattern (ie/ form of TCP Connect)
- forced_close on SO %

Refs: <----- TODO: make explicit in report
https://github.com/vistadataproject/RPCDefinitionToolkit/issues/44
- EDIS - Emergency Department Integration Software (EDIS) https://www.va.gov/vdl/documents/Clinical/Emergency_Dept_Integration_Software/edp_2_1_1_tm.pdf (SPOK: CONNECTOR,EDIS?)
- AVS may be After Visit Summary
- The VistALink Connector Proxy User is an entry on your VistA NEW PERSON file that the PATS application and other web-based applications use to connect to your VistA site. For the PATS application, there will be one data center located in Falling Waters, VA and a second fail-over data center in Hines, IL. A VistALink connector proxy user needs to be set up on your VistA server for the Falling Waters data center and also for the Hines data center.
  (SPOK: VISTALINK,EMC HINES)
- RTLS: "application proxy user 'VIAASERVICE,RTLS APPLICATION PROXY' will be created automatically."
- VPS: 
  (SPOK: CONNECT,VPS)
- Fee Basis Claims System (FBCS) application
- CPGATEWAY,USER: The CP Gateway Service is composed of two subsystems ... via the RPC Broker to retrieve the HL7 message ... Vendor CIS for Clinical Procedures and VistA

Note: tied up with vistalink and two step of connector (with station number
lookup) and then switch to local user <------------ see if two step means two sign ons?
"""
def webReportProxyUsers(activeProxyUserRefs, warningsByUserRef, userInfoByUserRef, st3_081ByUserRef, totalSignOns):

    totalProxySignOnCount = sum(st3_081ByUserRef[userRef]["_total"] for userRef
 in activeProxyUserRefs)
    mu = "There are <span class='yellowIt'>{:,}</span> active Proxy Machine Users (user_class is \"CONNECTOR PROXY\") with <span class='yellowIt'>{}</span> signons. All user records have _access_, _verify_ and lack a social while their signons have _LOA_ 2 and don't have \"remote_...\" properties (ie/ CPRS-like combo) ...\n\n".format(len(activeProxyUserRefs), reportAbsAndPercent(totalProxySignOnCount, totalSignOns))
    tbl = MarkdownTable(["Name [IEN]", "Entered", "PMO", "SMOs", "Keys", "SignOns", "Period", "\# IPs", "Unexpected"])
    for userRef in sorted(activeProxyUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True):
        userInfo = userInfoByUserRef[userRef] 
        st = st3_081ByUserRef[userRef]
        userRefMU = "__{}__ [{}]".format(userRef.split(" [200-")[0], userRef.split("[200-")[1][:-1]) 
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        ipMU = len(st["ipv4_address"]["byValueCount"]) if len(st["ipv4_address"]["byValueCount"]) > 1 else "__{}__".format(singleValue(st, "ipv4_address"))
        unexpectedMU = "" if userRef not in warningsByUserRef else "/".join(warningsByUserRef[userRef])
        tbl.addRow([
            userRefMU,
            userInfo["date_entered"], 
            pmoMU,
            smosMU,
            keysMU,
            reportAbsAndPercent(st["_total"], totalProxySignOnCount),
            muSignOnPeriod(st),
            ipMU,
            unexpectedMU
        ])
    mu += tbl.md() + "\n\n"
        
    return mu
    
"""
Off Key Words BUT Not the DoD User (| Postmaster) 

Expects: machine SSN, visited_from, NO remote_app, LOA 2 (usually), no PMO or keys

Note:
- no PMO or Keys as none specified (in VCB)
- not enforcing LOA 2 as see 200, 2001 combos where first is 1 and then move to 2
- showing remote_user_ien as apparently fixed
- NOT enforcing no remote_app as one CVIX has VISTAWEB login in VCB

CVIX remote_user_ien seems to have a fixed IEN
CVIX_MHVUSER_SSNIEN = "200:412864" # expect 2001 too and 2006_95's >> sign ons
CVIX_USER_SSNIEN = "200:217122" # expect 2001 too; 2006_95 << sign ons 
...
and fixed IP and LOA 1 usually
"""
def webReportNonProxyMachineUsers(activeNonProxyMachineUserRefs, warningsByUserRef, userInfoByUserRef, totalSignOns, st3_081ByUserRef):

    totalNonProxyMachineSignOnCount = sum(st3_081ByUserRef[userRef]["_total"] for userRef in activeNonProxyMachineUserRefs)
    mu = "Besides the _DoD User_, there are <span class='yellowIt'>{:,}</span> active Non-Proxy Machine Users with <span class='yellowIt'>{}</span> signons. These users appear in most VistAs under fabricated social security numbers ...\n\n".format(
        len(activeNonProxyMachineUserRefs), 
        reportAbsAndPercent(totalNonProxyMachineSignOnCount, totalSignOns)
    )

    # To add: workstation_name - take first part? ipv4_address    
    tbl = MarkdownTable(["Name [IEN]", "Entered", "SSN", "SMOs", "SignOns", "Period", "Remote IEN(s)", "Remote Station Id(s)", "\# IPs", "Unexpected"])
    for userRef in sorted(activeNonProxyMachineUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True):
        userInfo = userInfoByUserRef[userRef]
        st = st3_081ByUserRef[userRef]
        userRefMU = "__{}__ [{}]".format(userRef.split(" [200-")[0], userRef.split("[200-")[1][:-1]) 
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        ipMU = len(st["ipv4_address"]["byValueCount"]) if len(st["ipv4_address"]["byValueCount"]) > 1 else "__{}__".format(singleValue(st, "ipv4_address"))
        unexpectedMU = "" if userRef not in warningsByUserRef else "/".join(warningsByUserRef[userRef])
        tbl.addRow([
            userRefMU,
            userInfo["date_entered"],
            "__{}__".format(userInfo["ssn"]) if "ssn" in userInfo else "",
            smosMU,
            reportAbsAndPercent(st["_total"], totalNonProxyMachineSignOnCount),
            muSignOnPeriod(st),
            # NO remote app?
            "/".join(st["remote_user_ien"]["byValueCount"].keys()) if "remote_user_ien" in st else "",
            "/".join(st["remote_station_id"]["byValueCount"].keys()) if "remote_station_id" in st else "",
            ipMU,
            unexpectedMU      
        ])
    mu += tbl.md() + "\n\n"
    return mu
    
"""
FIRST: exceed and nix
- https://github.com/vistadataproject/RPCDefinitionToolkit/blob/master/Reporters/Users/reportRemoteUsersE.py
- bseEntries = [entry for entry in entries if "remote_app" in entry] etc in
https://github.com/vistadataproject/DataExtractNSync/blob/master/RPCSessionTests/reportUsersAndLogins.py

TODO: needs more
- JLV vs other - see IPs in fmrepo's util
  ... JLV with DoD Ids
  ie/ DoD JLV
  ie/ may show REAL dod ids => de-identify
- non station id/ien combo (need from custom run on SO!) ie/ X:1 in particular
"""
def webReportDoDUser(userRef, userInfo, totalSignons, st, warnings, deidentify):
    
    mu = "One special non proxy, machine user is used for JLV DoD access and by a number of other applications ...\n\n"
    
    tbl = MarkdownTable(["Property", "Value"])
    
    userRefMU = "__{}__ [{}]".format(userRef.split(" [200-")[0], userRef.split("[200-")[1][:-1]) 
    tbl.addRow(["Name \[IEN\]", userRefMU])
    tbl.addRow(["Date Entered", userInfo["date_entered"]])
    tbl.addRow(["SSN", "__{}__".format(userInfo["ssn"])])
    pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
    tbl.addRow(["SMOs", smosMU])
    
    tbl.addRow(["Sign ons", reportAbsAndPercent(st["_total"], totalSignons)])
    tbl.addRow(["Sign on period", muSignOnPeriod(st)])
    noRemoteStationIds = len(st["remote_station_id"]["byValueCount"])
    tbl.addRow(["Remote Station Ids", noRemoteStationIds])
    
    if len(warnings):
        tbl.addRow(["Unexpected", "/".join(warnings)])
    
    mu += tbl.md() + "\n\n"
    return mu
        
def webReportPostmaster(userRef, userInfo, totalSignons, st, warnings):

    mu = "Every VistA has __Postmaster__, (one of) the first user in the system ...\n\n"
    
    tbl = MarkdownTable(["Property", "Value"])
    
    userRefMU = "__{}__ [{}]".format(userRef.split(" [200-")[0], userRef.split("[200-")[1][:-1]) 
    tbl.addRow(["Name \[IEN\]", userRefMU])
    tbl.addRow(["Date Entered", userInfo["date_entered"]])
    pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
    if pmoMU:
        tbl.addRow(["PMO", pmoMU])
    if smosMU:
        tbl.addRow(["SMOs", smosMU])
    if keysMU:
        tbl.addRow(["Keys", keysMU])
    
    tbl.addRow(["Sign ons", reportAbsAndPercent(st["_total"], totalSignons)])
    tbl.addRow(["Sign on period", muSignOnPeriod(st)])
    
    if len(warnings):
        tbl.addRow(["Unexpected", "/".join(warnings)])
    
    mu += tbl.md() + "\n\n"
    return mu
    
"""
TODO:
- more on VPR SMO ... split em out
- by APP ie/ CAPRI et al + ENFORCE [classifier] on loa 1/2 (3 for local?) ie/ break JLV vs others in separate tables (fuller report)
- manilla called out; 200 too?

fmrepo/user/catag (move over)
- 
- JLV
    "ipv4_addresses": set(JLV_INVA_IPS).union(set(JLV_INVA_EXTRA_IPS)),
            "level_of_assurance": "1",
            "workstation_name": "10"
    and CC JLV
    (besides DoD JLV)
"""
def webReportRemoteUsers(activeRemoteUserRefs, warningsByUserRef, totalActiveUsers, userInfoByUserRef, totalSignOns, st3_081ByUserRef, remoteExcludeReasonCount, deidentify):

    remoteSignOnCountsByUserRef = dict((userRef, st3_081ByUserRef[userRef]["_total"]) for userRef in activeRemoteUserRefs)
    totalRemoteSignOns = sum(remoteSignOnCountsByUserRef[userRef] for userRef in remoteSignOnCountsByUserRef)
    totalTriplerRemoteSignOns = sum(remoteSignOnCountsByUserRef[userRef] for userRef in remoteSignOnCountsByUserRef if "459" in st3_081ByUserRef[userRef]["remote_station_id"]["byValueCount"])
    kstats = keyStats(remoteSignOnCountsByUserRef.values())
    
    mu = """Remote users dominate in every VistA - <span class='yellowIt'>{}</span> - but account for less sign ons - <span class='yellowIt'>{}</span> - than their numbers suggest. The median number of sign ons per remote user is <span class='yellowIt'>{:,}</span>.

The following shows the top 50 Remote Users. Note that users from station __459__ (_Hawaii, Tripler_) are JLV test users and account for <span class='yellowIt'>{}</span> of the remote logins.

""".format(
        reportAbsAndPercent(len(activeRemoteUserRefs), totalActiveUsers),
        reportAbsAndPercent(totalRemoteSignOns, totalSignOns),
        roundFloat(kstats["median"]),
        reportAbsAndPercent(totalTriplerRemoteSignOns, totalRemoteSignOns)
    )

    def muRemoteIds(st): # points to need for custom combine of sno:ien
        stationIdVC = st["remote_station_id"]["byValueCount"]
        # Could happen but ? ... TODO: force IEN count 
        if "byValueCount" not in st["remote_user_ien"]:
            return ""
        ienVC = st["remote_user_ien"]["byValueCount"]
        if len(stationIdVC) == 1:
            return "{}:{}".format(stationIdVC.keys()[0], ienVC.keys()[0])
        if len(ienVC) == 1:
            return "{}:{}".format("/".join(stationIdVC.keys()), ienVC.keys()[0])
        # TODO: match counts in both to assemble id
        return ""

    tbl = MarkdownTable(["Name [IEN]", "Entered", "SSN", "Remote Id(s)", "SignOns", "Period", "Remote Apps", "Options", "Unexpected"])
    for i, userRef in enumerate(sorted(activeRemoteUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True), 1):
        if i > 50:
            break
        userInfo = userInfoByUserRef[userRef] 
        name = userRef.split(" [200-")[0]
        userRefMU = "__{}__ [{}]".format(
            name if not deidentify else re.sub(r'[A-Za-z]', "X", name),
            userRef.split("[200-")[1][:-1]
        ) 
        ssnMU = "" if "ssn" not in userInfo else (userInfo["ssn"] if not deidentify else re.sub(r'\d', 'X', userInfo["ssn"]))
        st = st3_081ByUserRef[userRef]
        # May put VPR in bold later as JLV indicator
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        remote_app_count = st["remote_app"]["byValueCount"] if "remote_app" in st else {}
        no_remote_app_count = st["_total"] if "remote_app" not in st else st["_total"] - st["remote_app"]["count"]
        if no_remote_app_count:
            remote_app_count["UNIDENTIFIED"] = no_remote_app_count
        remoteAppMU = ", ".join(["{} ({})".format(remote_app.split(" [")[0], remote_app_count[remote_app]) for remote_app in sorted(remote_app_count, key=lambda x: remote_app_count[x], reverse=True)])
        unexpectedMU = "" if userRef not in warningsByUserRef else "/".join(warningsByUserRef[userRef])
        tbl.addRow([
            userRefMU,
            userInfo["date_entered"],
            ssnMU,
            muRemoteIds(st),
            reportAbsAndPercent(st["_total"], totalRemoteSignOns),
            muSignOnPeriod(st),
            remoteAppMU,
            smosMU,
            unexpectedMU
        ])
    mu += tbl.md() + "\n\n"
    return mu

"""
TODO: exclude from remote on MAND_PROPS and ALLOWED_PROPS as opposed to 0's ie/ 0's in here PLUS station_no in locals
"""
def webReportLocalUsers(activeLocalUserRefs, warningsByUserRef, totalActiveUsers, userInfoByUserRef, totalSignOns, st3_081ByUserRef, deidentify):

    # TODO: markup local users - include title and show mix
    totalLocalSignOns = sum(st3_081ByUserRef[userRef]["_total"] for userRef in activeLocalUserRefs)
    mu = "There are <span class='yellowIt'>{}</span> active Local Users with <span class='yellowIt'>{}</span> signons.\n\n".format(reportAbsAndPercent(len(activeLocalUserRefs), totalActiveUsers), reportAbsAndPercent(totalLocalSignOns, totalSignOns))
    
    SUPERUSER_KEYS = ["XUMGR"] # removing XUPROG
    superUserRefs = set(userRef for userRef in activeLocalUserRefs if "keys" in userInfoByUserRef[userRef] and len(set(SUPERUSER_KEYS).intersection(set(userInfoByUserRef[userRef]["keys"]))))
    
    mu += "<span class='yellowIt'>{:,}</span> Local Users are __Superusers__ (those with key {}) ...\n\n".format(len(superUserRefs), "|".join(SUPERUSER_KEYS))
    
    tbl = MarkdownTable(["Name [IEN]", "Entered", "Title", "SSN", "SignOns", "Sign On Period", "PMO", "SMOs", "Keys"])
    for userRef in sorted(superUserRefs, key=lambda x: st3_081ByUserRef[x]["_total"], reverse=True):
        name = userRef.split(" [200-")[0]
        userRefMU = "__{}__ [{}]".format(
            name if not deidentify else re.sub(r'[A-Za-z]', "X", name),
            userRef.split("[200-")[1][:-1]
        )
        userInfo = userInfoByUserRef[userRef]
        ssnMU = "" if "ssn" not in userInfo else (userInfo["ssn"] if not deidentify else re.sub(r'\d', 'X', userInfo["ssn"]))
        st = st3_081ByUserRef[userRef]
        pmoMU, smosMU, keysMU = muOptionsNKeys(userInfo)
        unexpectedMU = "" if userRef not in warningsByUserRef else "/".join(warningsByUserRef[userRef])
        tbl.addRow([
            userRefMU,
            userInfo["date_entered"],
            userInfo["title"] if "title" in userInfo else "",
            ssnMU,
            reportAbsAndPercent(st["_total"], totalLocalSignOns),
            muSignOnPeriod(st),
            pmoMU,
            smosMU,
            keysMU,
            unexpectedMU
        ])
    mu += tbl.md() + "\n\n"
        
    return mu
   
# TODO: change to calc length formally in case of gaps 
def muSignOnPeriod(st):

    if len(st["date_time"]["byValueCount"]) == 13:
        soPeriodMU = "EVERY MONTH"
    elif st["date_time"]["firstCreateDate"].split("T")[0] == st["date_time"]["lastCreateDate"].split("T")[0]:
        soPeriodMU = st["date_time"]["lastCreateDate"].split("T")[0]
    else:
        soPeriodMU = "{} - {} ({})".format(st["date_time"]["firstCreateDate"].split("T")[0], st["date_time"]["lastCreateDate"].split("T")[0], len(st["date_time"]["byValueCount"]))
    return soPeriodMU
    
"""
TODO: change -- move to reducing non RPC options 
"""
def muOptionsNKeys(userInfo):
    # rosByLabel = dict((res["label"], res) for res in rpcOptions(stationNo))
    pmoMU = ""
    if "primary_menu_option" in userInfo:
        pmoMU = userInfo["primary_menu_option"]
        # if userInfo["primary_menu_option"] not in rosByLabel:
        #    pmoMU += " [NOT RPC]"
    smosMU = ""
    if "secondary_menu_options" in userInfo:
        # smosMU = ", ".join(sorted([smo if smo in rosByLabel else "{} [NOT RPC]".format(smo) for smo in userInfo["secondary_menu_options"]]))
        smosMU = ", ".join(sorted(userInfo["secondary_menu_options"]))
    keysMU = ""
    if "keys" in userInfo:
        keysMU = ", ".join(sorted(userInfo["keys"]))
    return pmoMU, smosMU, keysMU
            
# ################################# DRIVER #######################
               
def main():

    assert(sys.version_info >= (2,7))
    
    if len(sys.argv) < 2:
        print "need to specify station # ex/ 442 - exiting"
        return
        
    stationNo = sys.argv[1]
    
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")
    
    if len(sys.argv) == 3:
        deidentify = sys.argv[2]
    else:
        deidentify = False
        
    if len(sys.argv) == 4:
        smallSOSet = True
    else:
        smallSOSet = False
    
    webReportUser(stationNo, deidentify, smallSOSet)
    
if __name__ == "__main__":
    main()
