#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict
from datetime import datetime

from fmqlutils.schema.reduceTypeUtils import singleValue

"""
TOADD (beyond SO, 200)
- ImagingUsers(stationNo, _2006_82WSAllTypeInfo, _2006_82WSSubTypeDatas)
- 38.1 access too
"""

"""
Classify Active (with SO) Users

Uses User (200), 3.081 (last year or some period up to now) reduction
"""
class UserClassifier:

    def __init__(self, stationNo, userInfoByUserRef, all3_081, st3_081sByUserRef, smallSO=False):
    
        if not (len(userInfoByUserRef) and len(st3_081sByUserRef)):
            raise Exception("Can't classify without both user infos AND SO types per user")
        
        firstSODay = all3_081["_firstCreateDate"].split("T")[0]
        lastSODay = all3_081["_lastCreateDate"].split("T")[0]
        
        self.__result = { 
        
            "firstSODay": firstSODay,
            "lastSODay": lastSODay,
            
            "inactiveUserCount": 0,
            "remoteExcludeReasonCount": defaultdict(int),
                    
            "activeUserRefs": set(st3_081sByUserRef.keys()),
            
            "dodUserRef": "", # special machine 'proxy' (CAPRI, not av)
            "postmasterUserRef": "",
            
            "activeProxyUserRefs": set(), # machine proxy with av
            "activeNonProxyMachineUserRefs": set(), # machine
            "activeRemoteUserRefs": set(), # real people
            "activeLocalUserRefs": set(), # real people
            
            "activeNotCategorizedUserRefs": set(),
            
            "warningsByUserRef": defaultdict(list)
                                                    
        }
                        
        # Make a reduced form of signed_on_froms for SO period if SO period long enough
        def makeSignedOnFromsSO(overallFirstSODay, userInfoByUserRef):
            overallFirstSODayDT = datetime.strptime(overallFirstSODay, "%Y-%m-%d")
            deletedAsNone = 0
            for userRef in userInfoByUserRef:
                userInfo = userInfoByUserRef[userRef]
                if "signed_on_froms" not in userInfo:
                    continue
                signed_on_froms_so = {}
                for siteId in userInfo["signed_on_froms"]:
                    detail = userInfo["signed_on_froms"][siteId]
                    if detail == None or "last" not in detail:
                        continue
                    lastSODayDT = datetime.strptime(detail["last"].split("T")[0], "%Y-%m-%d")
                    if lastSODayDT < overallFirstSODayDT: 
                        continue
                    signed_on_froms_so[siteId] = detail
                if len(signed_on_froms_so):
                    userInfo["signed_on_froms"] = signed_on_froms_so
                else:
                    del userInfo["signed_on_froms"]
        if smallSO == False:
            makeSignedOnFromsSO(firstSODay, userInfoByUserRef)
        
        self.__stationNo = stationNo
        self.__userInfoByUserRef = userInfoByUserRef
        self.__st3_081sByUserRef = st3_081sByUserRef
                
    def classify(self):
    
        print("Classifying {:,} active (with SO) users of out {:,} total".format(
            len(self.__result["activeUserRefs"]), 
            len(self.__userInfoByUserRef)
        ))
        
        self.__result["postmasterUserRef"] = self.__findPostmaster() # really an enforce 
        self.__result["dodUserRef"] = self.__findDoDUser() # one off
                
        for userRef in self.__userInfoByUserRef:
        
            if userRef not in self.__result["activeUserRefs"]:
                self.__result["inactiveUserCount"] += 1
                continue
                
            if userRef in [self.__result["dodUserRef"], self.__result["postmasterUserRef"]]:
                continue
                
            userInfo = self.__userInfoByUserRef[userRef]
            signOnType = self.__st3_081sByUserRef[userRef]
            
            if self.__testProxyUser(userRef, userInfo, signOnType):
                self.__result["activeProxyUserRefs"].add(userRef)
                continue
            if self.__testNonProxyMachineUser(userRef, userInfo, signOnType):
                self.__result["activeNonProxyMachineUserRefs"].add(userRef)
                continue
            if self.__testRemoteUser(userRef, userInfo, signOnType):
                self.__result["activeRemoteUserRefs"].add(userRef)
                continue
            if self.__testLocalUser(userRef, userInfo, signOnType):
                self.__result["activeLocalUserRefs"].add(userRef)
                continue
                
            self.__result["activeLocalUserRefs"].add(userRef)
            
        print("Finished Classification")
                
        return self.__result
        
    """
    Postmaster
    - .5 IEN
    - pmo, smos, keys
    - signins
    
    Expect:
    - NO ssn
    """
    def __findPostmaster(self):
        postmasters = [userRef for userRef in self.__userInfoByUserRef if re.match(r'POSTMASTER \[', userRef)]
        if len(postmasters) > 1:
            raise Exception("> 1 user has name POSTMASTER")
        userRef = postmasters[0]
        if not re.search(r'\[200-\.5\]$', userRef):
            raise Exception("Expected POSTMASTER to be IEN .5")
        if userRef not in self.__st3_081sByUserRef:
            raise Exception("Expect POSTMASTER to have sign ins")
        userInfo = self.__userInfoByUserRef[userRef]
        if not ("primary_menu_option" in userInfo and "secondary_menu_options" in userInfo and "keys" in userInfo):
            warning = "Expected POSTMASTER to have all of primary_menu_option, secondary_menu_options and keys"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
        if "ssn" in userInfo:
            warning = "Unexpected to have SSN"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
        return userRef
        
    """
    Special Non Proxy Machine User for DoD and other remote accesses via CAPRI
    
        Most visited_froms in System AND
        No User Class AND 
        has SSN AND 
        has at least CAPRI, CPRS, VPR SMOs
        has sign ins
        
    Expect (warn otherwise):
        visited from 524:14358 (Braintree) and 506:10000029117 AND
        SSN is machine form AND
        signs are all LOA == 1 AND no remote_app setting (CAPRI)
        
    Not enforcing X:1 for station:IEN for most and then JLV IP/DoD user (may do
    later)

    Note: 663 shows alias 'VISITOR'
    """
    def __findDoDUser(self):
        candidatesByVisitedFromCount = defaultdict(list)
        for userRef in self.__userInfoByUserRef:
        
            userInfo = self.__userInfoByUserRef[userRef]
            
            if "user_class" in userInfo:
                continue
            if "ssn" not in userInfo:
                continue
            if "signed_on_froms" not in userInfo:
                continue
            if "secondary_menu_options" not in userInfo or len(set(["DVBA CAPRI GUI", "OR CPRS GUI CHART", "VPR APPLICATION PROXY"]) - set(userInfo["secondary_menu_options"])):
                continue
                
            candidatesByVisitedFromCount[len(userInfo["signed_on_froms"])].append(userRef)
            
        if len(candidatesByVisitedFromCount) == 0:
            raise Exception("Can't reduce DOD User - none!")            
        maxCount = sorted(candidatesByVisitedFromCount.keys(), reverse=True)[0]
        if len(candidatesByVisitedFromCount[maxCount]) > 1:
            raise Exception("Can't reduce DOD User - ambiguous!")
            
        userRef = candidatesByVisitedFromCount[maxCount][0]
        
        if userRef not in self.__st3_081sByUserRef:
            raise Exception("Expect DoD User to have sign ins")
        
        userInfo = self.__userInfoByUserRef[userRef]
        if sum(1 for sof in userInfo["signed_on_froms"] if re.match(r'523:14358', sof)) == 0:
            warning = "Expected to have 523:14358 but it doesn't"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
        if sum(1 for sof in userInfo["signed_on_froms"] if re.match(r'506:10000029117', sof)) == 0:
            warning = "Expected to have 506:10000029117 but it doesn't"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
        if not couldBeMachineSSN(userInfo["ssn"]):
            warning = "Expected to have machine SSN but {}".format(userInfo["ssn"])
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
            
        signOnType = self.__st3_081sByUserRef[userRef]
        if not enforceLOA(signOnType, "1") or "remote_app" in signOnType:
            warning = "Expected to have SO LOA 1 and no remote_app ie/ CAPRI login"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
                        
        return userRef
                
    """
    Proxy User
        user_class CONNECTOR PROXY and 
        NO visited_from and
        access, verify and
        SO's all LOA 2 and
        NO remote_*'s set in SO <---- triple AV/LOA2/no remote_... == CPRS like
        
    Expect:
        if SSN then Machine SSN
        
    TODO:
    - workstation_name == TCP Connect patterns
    """
    def __testProxyUser(self, userRef, userInfo, signOnType):
    
        if "user_class" not in userInfo:
            return False
            
        if not re.search(r'PROXY', userInfo["user_class"]):
            return False
            
        if "signed_on_froms" in userInfo:
            raise Exception("Didn't expect proxy user {} to have visited_from".format(userRef))
            
        if len(set(["access_code", "verify_code"]) - set(userInfo["hasProps"])):
            raise Exception("Expected proxy user {} to have access verify".format(userRef))
                        
        if sum(1 for prop in signOnType if re.match(r'remote', prop)):
            raise Exception("Unexpected \"remote_...\" property in SO of Proxy User {}".format(userRef))
            
        # HMP SPOK only => need to show
        if userInfo["user_class"].split(" ")[0] != "CONNECTOR":
            warning = "Expected CONNECTOR Proxies but {}".format(userInfo["user_class"].split(" ")[0])
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
            
        if not enforceLOA(signOnType, "2"):
            warning = "Expected Only SO LOA 2"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
            
        if not ("ssn" in userInfo and couldBeMachineSSN(userInfo["ssn"])):
            warning = "Expected Machine SSN for Proxy Users"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
            
        return True
        

    """
    Not Proxy and Going off Keywords - does NOT include DoD User irrespective of name
    and POSTMASTER isn't here either.
    
    Expect:
    - machine SSN 
    
    Note:
    - not enforcing LOA 2 as see 200, 2001 combos where first is 1 and then move to 2
    
    TODO:
    - CVIX remote_user_ien seems to have a fixed IEN
        CVIX_MHVUSER_SSNIEN = "200:412864" # expect 2001 too and 2006_95's >> sign ons
        CVIX_USER_SSNIEN = "200:217122" # expect 2001 too; 2006_95 << sign ons 
        ...
        and fixed IP and LOA 1 usually
    """
    def __testNonProxyMachineUser(self, userRef, userInfo, signOnType):
        
        if "user_class" in userInfo:
            return False
            
        if not re.search(r'(\,USER$|^USER\,|CVIX|CHCS|WEB ITS|RADIOLOGY|PHARMACY)', userRef):
            return False
           
        if not ("ssn" in userInfo and couldBeMachineSSN(userInfo["ssn"])):
            warning = "Expected Machine SSN for Non Proxy Machine Users"
            self.__result["warningsByUserRef"][userRef].append(warning)
            print("** Warning: {} for {}".format(warning, userRef))
        
        return True
        

    PUREZEROSOCREATEDUSER_200_MAND_PROPS = set([
        "name", "alias", "name_components", "signature_block_printed_name", "date_entered", "creator", "last_signon_date_time", "xus_logon_attempt_count", "xus_active_user", "secondary_menu_options", "timestamp", "visited_from"
    ])    
    
    PUREZEROSOCREATEDUSER_200_OPT_PROPS = set([    

        # not in 668
        "initial",

        # nearly always EXCEPT never for Manilla
        "ssn",

        # Optional id's
        "network_username", "email_address",   

        # Never 442, Always 640, 668 - "SCREEN EDITOR - VA FILEMAN"
        "preferred_editor",     

        # Doesn't seem to effect CAPRI at all (in MM in some systems)
        "disuser", "entry_last_edit_date", "termination_reason",

        # Termination Date: This is the date after which the computer will no longer recognize this user's ACCESS CODE. Once this date has passed, when the USER TERMINATE job runs it will clean out this users data based on flags in the NEW PERSON file.
        # 640 has for them all ie/ sets when WILL term and then 
        # actual term kicks in
        "termination_date" # 640 and JLV user
    ]) 
    
    """
    Remote means comes from other station AND created by such sign ons (ie/ no clerk
    creates)
    
        Not Machine User (Proxy or Otherwise) AND
        0 Created AND
        Has only ALLOWED PROPERTIES AND
        Has All Mandatory Properties* AND
        if no SSN then Manilla
        signed on from AND
        signed on from at least one remote station
        
    MORE TODO: sub again
    - VISTAWEBPROD_IP = '10.224.74.88'
    - no SMO?
    - force ALL remotes and put others into "mixed"?
    - WARN if REMOTEs have LOA != 2 ie/ BSE? and if remote_app == 100% sign ons
        
    """
    def __testRemoteUser(self, userRef, userInfo, signOnType):
    
        if "is_created_by_0" not in userInfo:
            self.__result["remoteExcludeReasonCount"]["0_CREATED"] += 1
            return False
            
        ALLOWED_PROPS = UserClassifier.PUREZEROSOCREATEDUSER_200_MAND_PROPS.union(UserClassifier.PUREZEROSOCREATEDUSER_200_OPT_PROPS)
        userInfo["hasProps"] = list(set(userInfo["hasProps"]) - set(["_id", "label", "type"]))
        if len(set(userInfo["hasProps"]) - ALLOWED_PROPS) > 0:
            self.__result["remoteExcludeReasonCount"]["ALLOWED_PROPS"] += 1
            return False
            
        # May be too strict: SMO + TimeStamp missing from some (subgroup?)
        # ... all seem to have LOA 1
        if len(UserClassifier.PUREZEROSOCREATEDUSER_200_MAND_PROPS - set(userInfo["hasProps"])):
            self.__result["remoteExcludeReasonCount"]["MAND_PROPS"] += 1
            missingMands = (UserClassifier.PUREZEROSOCREATEDUSER_200_MAND_PROPS - set(userInfo["hasProps"])) - set(["secondary_menu_options", "timestamp"])
            if len(missingMands) != 0:
                raise Exception("At this point in Remote Check, only expected mandatory SMO and TimeStamp could be missing but {}".format(
                                    "/".join(list(missingMands))
                                ))
            return False
            
        if "ssn" not in userInfo and sum(1 for vf in userInfo["signed_on_froms"] if re.match(r'358\:', vf)) == 0:
            self.__result["remoteExcludeReasonCount"]["MANILLA_NO_SSN"] += 1
            return False
            
        if "signed_on_froms" not in userInfo or sum(1 for sof in userInfo["signed_on_froms"] if re.match(self.__stationNo, sof)) == len(userInfo["signed_on_froms"]):
            self.__result["remoteExcludeReasonCount"]["ONLY_LOCAL_STATION_NO"] += 1
            return False
          
        # NOT doing as too many  
        #   if couldBeMachineSSN(userInfo["ssn"]):
            
        return True
        
    """
    Parallel a strict remote with a pure Local and put others in Mixed as before
    """
    def __testLocalUser(self, userRef, userInfo, signOnType):
        return False
   
"""
Heuristic - use for warnings etc
"""     
def couldBeMachineSSN(ssn):
    if ssn in ["123456789"]:
        return True
    # >= 4 identical digits in a row
    # 000006777, 111116777, 099999999, 000998888, 123456789, 000005678 ...
    if re.search(r'(\d)\1{3,}', ssn):
        return True
    # Pairs RE
    if len(re.findall(r'(\d)\1{1,}', ssn)) >= 2:
        return True
    return False
    
def enforceLOA(signOnType, loaValue):
    loa = None
    try:
        loa = singleValue(signOnType, "level_of_assurance")
    except:
        return False
    if loa != loaValue:
        return False
    return True
    