#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import numpy

from fmqlutils.reporter.reportUtils import MarkdownTable, reportPercent, reportAbsAndPercent

from ..webReportUtils import checkDataPresent, splitTypeDatas, filteredResultIterator, reduce200, singleValue, TOP_MD_TEMPL, SITE_DIR_TEMPL, keyStats, roundFloat

"""
Images types, references (TIU, Radiology), Acquisition Devices, Users ...

Note: may aspects of images will appear in other more specific reports and some of the
breakdowns below (TODO) may become functions to enable that reporting ex/ Image-centric documents etc.

TODO: move towards patient centric view of images and using reference typing to type images as native form not good enough (expand on this theme). Also expand on user access to images. Overall, WANT TO FOLLOW SAME PATTERNS as other data types. 
"""
    
def webReportImaging(stationNo):

    # Too many here - part of plus
    allThere, details = checkDataPresent(stationNo, [
    
        {"fileType": "702_09", "check": "ALL"}, # in 2005RF too
        {"fileType": "2005", "check": "TYPESO"}, # object_type-pdf-capture_application (off 2005RF)
        {"fileType": "2005_02", "check": "TYPE"},
        {"fileType": "2005_03", "check": "ALL"},
        {"fileType": "2006_04", "check": "ALL"},
        {"fileType": "2006_82", "check": "TYPESO"}, # workstation (used for 2005RF too)
        {"fileType": "8925", "check": "TYPESO"}, # document_type (used for 2005RF too)

        # Just for 2005 RF
        {"fileType": "74", "check": "ALL"}, # will index in a shelve
        {"fileType": "8925_1", "check": "ALL"},
        {"fileType": "8925_91", "check": "ALL"} # shelve to have doc by img and vica versa

    ])
    if not allThere:
        raise Exception("Some required data is missing - {}".format(details))

    # ###################### Preparation/ Preprocessing #########################
          
    allTypeData, subTypeDatas = splitTypeDatas(stationNo, "2005", useSO=True, expectSubTypeProperty="object_type-pdf-capture_application")
    totalAll = allTypeData["_total"]
    
    """
    The CAP and CAP-IMPORT actions in 2006_82 are already mined into an enhanced
    2005 to allow WS identification for CAPTURE and redundant definition for
    IMPORT API. Bringing this in again, allows more:
    - if only one user in byWS then can id the real user for IMPORT API as all seem 
    set to one
    - activity of READ-ONLY so can see number of workstations involved.
    """
    _2006_82AllTypeInfo, _2006_82SubTypeInfos = splitTypeDatas(stationNo, "2006_82", useSO=True, expectSubTypeProperty="workstation")
    
    """
    Enforce things about capture_application and image_save_by etc as interpretation
    and derivation rely on them
    """
    def enforce2005(typeInfo):
    
        """
        Acquisition Device (2006.04): mandatory for I:Import API and D:DICOM Gateway but 
        never C:Capture Workstation 
        """
        if "capture_application" not in typeInfo:
            if "acquisition_device" in typeInfo:
                raise Exception("Didn't expect acquisition device if no capture_application")
        else:
            totalCAID = sum(typeInfo["capture_application"]["byValueCount"][ca] for ca in typeInfo["capture_application"]["byValueCount"] if ca != "C:Capture Workstation")
            if totalCAID and ("acquisition_device" not in typeInfo or typeInfo["acquisition_device"]["count"] != totalCAID):
                raise Exception("Expected acquisition device if capture application is D:DICOM or I:Import")
                
        """
        Image Save By:
        - mandatory for I:Import API and C:Capture and even for DICOM Gateway
        if it leads to DICOM:TIU (unsure how that can happen!) ie/ not for DICOM:RADIOLOGY
          ... possible that DICOM:TIU is one user too??????
        - I:Import API leads to one and only one user across the system ie a default guy!
        """
        totalCAIC = sum(typeInfo["capture_application"]["byValueCount"][ca] for ca in typeInfo["capture_application"]["byValueCount"] if "capture_application" in typeInfo and ca != "D:DICOM Gateway")
        if ("image_save_by" in typeInfo and (typeInfo["image_save_by"]["count"] != totalCAIC)) or (totalCAIC and "image_save_by" not in typeInfo):
            raise Exception("Expected 'image_save_by' to match combo of capture I and C")
        totalCAI = sum(typeInfo["capture_application"]["byValueCount"][ca] for ca in typeInfo["capture_application"]["byValueCount"] if "capture_application" in typeInfo and ca == "I:Import API")
        # in == <=> as typeInfo is fixed to one capture_application
        if "capture_application" in typeInfo and "I:Import API" in typeInfo["capture_application"]["byValueCount"]:
            if "image_save_by" not in typeInfo:
                raise Exception("Import API but no Image Save User Set?")
            noI = typeInfo["capture_application"]["byValueCount"]["I:Import API"]
            possImportAPIUsers = set(userId for userId in typeInfo["image_save_by"]["byValueCount"] if typeInfo["image_save_by"]["byValueCount"][userId] == noI)
            if not len(possImportAPIUsers):
                raise Exception("Expect (at least) one user to a/c for Import API!")
    for subTypeData in subTypeDatas:
        enforce2005(subTypeData)
        
    # ####################### Make Report / Web Page #############################
            
    userSiteDir = SITE_DIR_TEMPL.format(stationNo)
    if not os.path.isdir(userSiteDir):
        raise Exception("Expect User Site to already exist with its basic contents")

    title = "Imaging".format(stationNo)
    mu = TOP_MD_TEMPL.format("Imaging", title)
    mu += """VistA Imaging ...
    
> support(s) the goal making a patient’s complete medical record available online

"""
    
    # ################################ Format / Reference #################

    mu += webReportFormatReference(stationNo, allTypeData, subTypeDatas)
    
    # ################################ Others Plus ##################
    
    # mu += webReportImageAcquisition(stationNo, subTypeDatas, _2006_82SubTypeInfos)
    # mu += webReportImageDocumentTypes(stationNo) 
    # mu += crudeTIULinkReport(stationNo)
            
    open(userSiteDir + "imaging.md", "w").write(mu)
        
# #################### Format/ Reference ###################

def webReportFormatReference(stationNo, allTypeData, subTypeDatas):

    """
    subtypes - splitting out (XRAY)_GROUP as not 'really' an image ie/ IMAGE GROUP
    - with fileref => individual images
    - without: expect object_group for children and grouper
    """
    def distinguishFileRefAndGroupSubTypes(subTypeDatas):
        filerefSubTypesByOT = defaultdict(list)
        groupSubTypes = []
        for i, subTypeInfo in enumerate(sorted(subTypeDatas, key=lambda x: singleValue(x, "object_type"), reverse=True), 1): 
            ot = singleValue(subTypeInfo, "object_type").split(" [")[0]
            if ot == "XRAY GROUP":
                if "object_group" not in subTypeInfo:
                    raise Exception("Expected ALL groupers to have children")
                groupSubTypes.append(subTypeInfo)
                continue
            if "object_group" in subTypeInfo:
                raise Exception("Expected NO Individual Images to have children")
            filerefSubTypesByOT[ot].append(subTypeInfo)
        return filerefSubTypesByOT, groupSubTypes 
    filerefSubTypesByOT, groupSubTypes = distinguishFileRefAndGroupSubTypes(subTypeDatas)

    mu = ""
        
    """
    Individual Images: all have fileref 
    
    Missing: [TODO]
    - patient as didn't capture byValueCount for 2 in reduction. Must redo OR redo
    uniques iff do subtyping just by type and not type_pdf
    
    Note: keeping 'capture' for now - will expand Acquisition below to report on formats
    and capture mode and take out of here later. TODO
    """
    tbl = MarkdownTable(["Type", "Count", "Form", "Capture", "Direct Referenced", "Group Referenced", "Orphan"])
    imageTotal = 0
    userCntByTypeSubType = defaultdict(lambda: defaultdict(dict))
    allTotalLessDICOM = 0
    allTotalOrphansLessDICOM = 0 
    pdfLabelsSeen = set()  
    importAPIUser = "" 
    
    """
    TO AUDIT: iffy logic - assuming that individual images get link as well as
    parent if parent has link. There is NO separate check that only a parent
    link. Doesn't seem to matter but??
    """
    # Global one to isolate out just by PDFLabel irrespective of image type (ot)
    # ... will see only TIU (and a few NOSET) apply for import api
    byCAByPDFLabel = defaultdict(lambda: defaultdict(int))
    # type ie/ DICOM IMAGE etc
    summs = []
    summPies = []
    for typeId in sorted(filerefSubTypesByOT.keys(), key=lambda x: sum(y["_total"] for y in filerefSubTypesByOT[x]), reverse=True):
        
        subTypeInfos = filerefSubTypesByOT[typeId]
        
        typeTotal = sum(subTypeInfo["_total"] for subTypeInfo in subTypeInfos)
        imageTotal += typeTotal
        if typeId != "DICOM IMAGE":
            allTotalLessDICOM += typeTotal
        
        suffixesCount = defaultdict(int)
        caCount = defaultdict(int)
        oiCount = defaultdict(int)

        linksDirectByPDF = defaultdict(int)
        linksFromParentByPDF = {}
        orphanNo = 0
            
        for subTypeInfo in subTypeInfos:
                                
            # typeLabel = subTypeValue.split("/")[0]
            typeLabel = singleValue(subTypeInfo, "object_type").split(" [")[0]
            pdfLabel = singleValue(subTypeInfo, "pdf", "NOSET")
            pdfLabelsSeen.add(pdfLabel)
                            
            for suffix in subTypeInfo["fileref_suffix"]["byValueCount"]:
                suffixesCount[suffix] += subTypeInfo["fileref_suffix"]["byValueCount"][suffix]
            for ca in subTypeInfo["capture_application"]["byValueCount"]:
                caCount[ca] += subTypeInfo["capture_application"]["byValueCount"][ca]
                byCAByPDFLabel[ca][pdfLabel] += subTypeInfo["capture_application"]["byValueCount"][ca]
                
            # User - for CA == capture_workstation only - come back to him later
            # ... note: some Capture Workstation missing em!
            if "image_save_by" in subTypeInfo:
                for userId in subTypeInfo["image_save_by"]["byValueCount"]:
                    userCntByTypeSubType[typeId][pdfLabel][userId] = subTypeInfo["image_save_by"]["byValueCount"][userId]
            if "origin_index" in subTypeInfo:
                for oi in subTypeInfo["origin_index"]["byValueCount"]:
                    oiCount[oi] += subTypeInfo["origin_index"]["byValueCount"][oi]
                            
            """
            The following leverages:
            - one NOSET vs others
            - others "parent_data_file" < "_total" => parent is responsible!
            """
            if pdfLabel != "NOSET":
                if "parent_data_file" in subTypeInfo:
                    linksDirectByPDF[pdfLabel] += subTypeInfo["parent_data_file"]["count"]
                if "group_parent" in subTypeInfo:
                    rangeCount = subTypeInfo["group_parent"]["rangeCount"] if "rangeCount" in subTypeInfo["group_parent"] else len(subTypeInfo["group_parent"]["byValueCount"])
                    # rem: B3 sub typing so must be incremental
                    if pdfLabel not in linksFromParentByPDF:
                        linksFromParentByPDF[pdfLabel] = [subTypeInfo["group_parent"]["count"], rangeCount]
                    else: 
                        linksFromParentByPDF[pdfLabel][0] += subTypeInfo["group_parent"]["count"]
                        linksFromParentByPDF[pdfLabel][1] += rangeCount
                continue
                
            # From NOSET (must exist as here!) ... can be C or I
            orphanNo += subTypeInfo["_total"]    
            if typeId != "DICOM IMAGE":
                allTotalOrphansLessDICOM += subTypeInfo["_total"]  
            
        summ = {"name": re.sub(r'\_', ' ', typeId)}
        summPie = {"Type": re.sub(r'\_', ' ', typeId)}
            
        # Note: argument to take parent and not direct DICOM which would then show orphans
        # ... seems like RAD goes to GROUP and not individual and may be missing.             
        totalLinked = sum(linksFromParentByPDF[x][0] for x in linksFromParentByPDF if typeId != "DICOM_IMAGE") + sum(linksDirectByPDF[x] for x in linksDirectByPDF)
 
        typeTotalMU = "{:,}".format(typeTotal)
        
        summPie["Count"] = typeTotal
 
        if len(suffixesCount) == 1:
            suffixesMU = suffixesCount.keys()[0]
        else:
            suffixesMU = "<br><br>".join(["{} ({:,})".format(suffix, suffixesCount[suffix]) for suffix in sorted(suffixesCount, key=lambda x: suffixesCount[x], reverse=True)])

        if len(caCount) == 1:
            captureMU = caCount.keys()[0].split(":")[1]
        else:
            captureMU = "<br><br>".join(["{} ({:,})".format(vc.split(":")[1], caCount[vc]) for vc in sorted(caCount, key=lambda x: caCount[x], reverse=True)])

        if len(oiCount) == 1:
            originMU = oiCount.keys()[0].split(":")[1]
        else:
            originMU = "<br><br>".join(["{} ({:,})".format(vc.split(":")[1], oiCount[vc]) for vc in sorted(oiCount, key=lambda x: oiCount[x], reverse=True)])  

        """
        Direct Links
        """
        directLinkMU = "<br><br>".join(["{} ({:,})".format(re.sub(r'_', ' ', pdf), linksDirectByPDF[pdf]) for pdf in linksDirectByPDF])
        
        summ["directReferenced"] = sum(linksDirectByPDF[pdf] for pdf in linksDirectByPDF)        

        """
        Parent/Group
        """
        parentLinkMU = "<br><br>".join(["{} ({:,}/{:,})".format(re.sub(r'_', ' ', gpdf), linksFromParentByPDF[gpdf][0], linksFromParentByPDF[gpdf][1]) for gpdf in linksFromParentByPDF]) 
        
        summ["groupReferenced"] = sum(linksFromParentByPDF[gpdf][0] for gpdf in linksFromParentByPDF) if typeId != "DICOM_IMAGE" else 0 # as redundant
        
        orphansMU = "" if orphanNo == 0 else "{:,}".format(orphanNo)
        
        summ["orphan"] = orphanNo

        # removed 'originMU' as better looked at below. Seems not to be accurate.        
        tbl.addRow([
            "__{}__".format(re.sub(r'\_', ' ', typeId)), 
            typeTotalMU, 
            suffixesMU, 
            captureMU, 
            directLinkMU,
            parentLinkMU, 
            orphansMU
        ])
    
        # Don't include DICOM in summary    
        if not re.match(r'DICOM', typeId):
            summs.append(summ)
        summPies.append(summPie)
                
    objectTypesInfo, sts = splitTypeDatas(stationNo, "2005_02", useSO=False, expectSubTypeProperty="")        
    
    totalXRG = sum(x["_total"] for x in groupSubTypes)
    
    overallFirstCreateDate = allTypeData["_firstCreateDate"].split("T")[0] 
    overallLastCreateDate = allTypeData["_lastCreateDate"].split("T")[0]
    
    mu += """<span class='yellowIt'>{imageTotal:,}</span> individual images were entered into this VistA from {overallFirstCreateDate} through {overallLastCreateDate}, the last full year for which data is available. <span class='yellowIt'>{filerefSubTypesByOTCount:,}</span> formats of image were entered from the <span class='yellowIt'>{objectTypesInfoTotal:,}</span> supported by the _VistA Imaging_ Subsystem. These images are for <span class='yellowIt'>{allTypeDataPatientRangeCount:,}</span> distinct patients.

<span class='yellowIt'>{totalXRG:,}</span> “XRAY” GROUP “Images” were also entered during this period. These group individual images and, despite their name, don’t just group XRAYs or even DICOM Images - they can group PDFs, TIFs and other Image formats too. Grouping allows individual TIU Notes (TIU) and Radiology Notes (RADIOLOGY) reference a group of Images.
    
An image can be entered in one of three ways - _Capture Workstation_ for manually entering images and _DICOM Gateway_ and _Import API_, both automated entry mechanisms.

""".format(
        imageTotal=imageTotal, 
        overallFirstCreateDate=overallFirstCreateDate, 
        overallLastCreateDate=overallLastCreateDate, 
        filerefSubTypesByOTCount=len(filerefSubTypesByOT.keys()), 
        objectTypesInfoTotal=objectTypesInfo["_total"], 
        allTypeDataPatientRangeCount=allTypeData["patient"]["rangeCount"],
        totalXRG=totalXRG
    )
    
    # #################### Formats and References ###################
    """
    Two things - by format, ac dev AND reference pattern. Probably too much
    as both dimensions can be looked at separately.
    
    TO CHANGE:
    ie/ BREAK THIS PROPERLY AFTER DOING AC DEV. Ex/ of what's lost.
    ie/ the dimension of format and ac and ref both there ... two different
    items ie/ format:ref and format:ac
    
    Cheyenne:
    - 67 :C for DICOM ... sub refs to that is TIU (30), TMP (37) both from non main
    institution ie/ kind of shows no gateway there to take in DICOMS so doing in CAPTURE
    (should see those WS's as being from those places!)
    
    Note: devices too - references. Question of whether ac dev and references
    should be in same subsection. Doing AC DEV below and if appropriate then will keep
    """
    
    mu += "## Image Formats and References\n\n"
    
    mu += "The following table describes these images: [1] their types and formats, [2] their quantities, [3] whether and how they are referenced from structured data such as TIU or Radiology notes, both directly and through groups, and [4] whether they go unreferenced (\"Orphan\") ...\n\n"
    
    mu += tbl.md() + "\n\n"
        
    mu += "<strong>IMAGE \"Images by Format and References\" - sb_imagesByFormatAndReferences - put in Office Excel and 2D Bar (Stacked) Chart ...\n\n"
    mu += "__VALUES__: {}\n\n".format(json.dumps(summs))
    mu += "![](/imgs/sb_imagesByFormatAndReferences.png)\n\n"
        
    """
    Orphans
    """
        
    mu += "Setting aside DICOM (.DCM), there are <span class='yellowIt'>{:,}</span> images, <span class='yellowIt'>{}</span> of which are _Orphans_.\n\n".format(allTotalLessDICOM, reportAbsAndPercent(allTotalOrphansLessDICOM, allTotalLessDICOM))
            
    mu += "Most _Orphans_ are accounted for by a property of most images called type index. In general, this property is ambiguous with most images ending up in catch-all categories such as _Medical Record_. However, many of its less used values do account for most of the Orphans.\n\n"

    # Reframe PDF under TI. Want to see TI that are all or mainly NOSET PDF.
    def groupTypeIndexes(subTypeInfos):
        tiUnsetGroupingByOT = defaultdict(lambda: defaultdict(int))
        tiGroupingByPDF = defaultdict(lambda: defaultdict(int))
        for subTypeInfo in subTypeInfos:
            if "type_index" not in subTypeInfo:
                continue
            otLabel = singleValue(subTypeInfo, "object_type").split(" [")[0]
            pdfLabel = singleValue(subTypeInfo, "pdf", "NOSET")
            for ti in subTypeInfo["type_index"]["byValueCount"]:
                tiGroupingByPDF[ti][pdfLabel] += subTypeInfo["type_index"]["byValueCount"][ti]
                if pdfLabel == "NOSET":
                    tiUnsetGroupingByOT[ti][otLabel] += subTypeInfo["type_index"]["byValueCount"][ti]
        return tiGroupingByPDF, tiUnsetGroupingByOT
    subTypeInfos = [subTypeInfo for ot in filerefSubTypesByOT for subTypeInfo in filerefSubTypesByOT[ot]] # if ot == "ADOBE"
    tiGroupingByPDF, tiUnsetGroupingByOT = groupTypeIndexes(subTypeInfos)
    majNoSetTIs = set()
    otherNoSetTIs = set()
    majNoSetOnlysTotal = 0
    otherNoSetOnlysTotals = 0
    for ti in tiGroupingByPDF:
        if "NOSET" not in tiGroupingByPDF[ti]:
            continue
        totalTI = sum(tiGroupingByPDF[ti][pdf] for pdf in tiGroupingByPDF[ti])
        noSetPercent = (float(tiGroupingByPDF[ti]["NOSET"])/float(totalTI)) * 100
        if noSetPercent >= 50.0: # > 50 percent then!
            majNoSetTIs.add(ti)
            majNoSetOnlysTotal += tiGroupingByPDF[ti]["NOSET"] # REM: don't want to cnt if any links
        else:
            otherNoSetTIs.add(ti)
            otherNoSetOnlysTotals += tiGroupingByPDF[ti]["NOSET"]
                
    mu += "Of <span class='yellowIt'>{:,}</span> active _type index_ values, <span class='yellowIt'>{:,}</span> account for <span class='yellowIt'>{:,}</span> Orphans ...\n\n".format(len(tiGroupingByPDF), len(majNoSetTIs), majNoSetOnlysTotal)
    
    tbl = MarkdownTable(["Type Index", "All/Majority Orphans", "Minority Referenced", "Orphan Type(s)"])
    for ti in sorted(list(majNoSetTIs), key=lambda x: tiGroupingByPDF[x]["NOSET"], reverse=True):
    
        setPDFMU = ", ".join(["{} ({})".format(pdfLabel, tiGroupingByPDF[ti][pdfLabel]) for pdfLabel in tiGroupingByPDF[ti] if pdfLabel != "NOSET"])
        otUSMU = ", ".join(["{} ({})".format(re.sub(r'\_', ' ', ot), tiUnsetGroupingByOT[ti][ot]) for ot in sorted(tiUnsetGroupingByOT[ti], key=lambda x: tiUnsetGroupingByOT[ti][x], reverse=True)]) if len(tiUnsetGroupingByOT[ti]) > 1 else tiUnsetGroupingByOT[ti].keys()[0]
        
        tbl.addRow([
            "__{}__".format(ti.split(" [")[0]), 
            tiGroupingByPDF[ti]["NOSET"], 
            setPDFMU, 
            otUSMU
        ])
        
    mu += tbl.md() + "\n\n"
    
    mu += "The balance of unreferenced Images, <span class='yellowIt'>{:,}</span>, belong to <span class='yellowIt'>{:,}</span> types that usually have references. For example, Progress Notes and Images are nearly always referenced. These Orphans are either mischaracterized or mistakenly left unreferenced.\n\n".format(otherNoSetOnlysTotals, len(otherNoSetTIs))
    
    tbl = MarkdownTable(["Type Index", "Minority Orphans", "Majority Referenced", "Orphan Type(s)"])
    for ti in sorted(list(otherNoSetTIs), key=lambda x: tiGroupingByPDF[x]["NOSET"], reverse=True):
    
        setPDFMU = ", ".join(["{} ({})".format(pdfLabel, tiGroupingByPDF[ti][pdfLabel]) for pdfLabel in tiGroupingByPDF[ti] if pdfLabel != "NOSET"])
        otUSMU = ", ".join(["{} ({})".format(re.sub(r'\_', ' ', ot), tiUnsetGroupingByOT[ti][ot]) for ot in sorted(tiUnsetGroupingByOT[ti], key=lambda x: tiUnsetGroupingByOT[ti][x], reverse=True)]) if len(tiUnsetGroupingByOT[ti]) > 1 else tiUnsetGroupingByOT[ti].keys()[0]
        cntAllOfTI = sum(tiGroupingByPDF[ti][pdfLabel] for pdfLabel in tiGroupingByPDF[ti])
        
        tbl.addRow([
            "__{}__".format(ti.split(" [")[0]), 
            reportAbsAndPercent(tiGroupingByPDF[ti]["NOSET"], cntAllOfTI),
            setPDFMU, 
            otUSMU
        ])
        
    mu += tbl.md() + "\n\n"
    
    """
    All possible referencing types 
    """ 
           
    tbl = MarkdownTable(["Id", "(Parent) Reference File", "Reference Subfile", "Abbrev", "Pkg", "Class"])
    noInThisSystemImages = 0
    resourceIter = filteredResultIterator(stationNo, "2005_03")
    for i, resource in enumerate(resourceIter, 1):
        # Chey 442 has corruption in its file ... 640 doesn't
        parentFileMU = "{} ({})".format(resource["file_pointer"]["label"], resource["file_pointer"]["id"].split("-")[1]) if resource["file_pointer"]["id"] != "1--1" else ""
        subFileMU = "{} ({})".format(resource["label"], resource["_id"].split("-")[1]) if resource["_id"].split("-")[1] != resource["file_pointer"]["id"].split("-")[1] else ""
        package_indexMU = "" if "package_index" not in resource else resource["package_index"].split(":")[1]
        class_indexMU = "" if "class_index" not in resource else resource["class_index"]["label"] # 2005_82
        root = resource["global_root_type"].split(":")[1]
        
        # Ignoring Root = [1] simple global (ex/ ^SRO), [2] global with fileid (ex/ ^XMB(3.9,) or [3] LAB with its multiples ie/ only ROOT 3 of interes
        # TODO: consider spec_subspec_index and proc_event_index (ie/ only other fields)
        
        inThisSystemsImages = resource["file_subfile_name"] in pdfLabelsSeen
        name = "__{}__".format(resource["file_subfile_name"]) if inThisSystemsImages else resource["file_subfile_name"]
        if inThisSystemsImages:
            noInThisSystemImages += 1
        
        tbl.addRow([
            name, 
            parentFileMU, 
            subFileMU, 
            resource["abbreviation"], 
            package_indexMU, 
            class_indexMU
        ])
                    
    mu += "VistA Imaging supports image references from <span class='yellowIt'>{:,}</span> types of record (\"parent data files\"). Many of these types - for example, Cardiac Catherization (691.1) - have been deprecated since VistA Imaging was launched and only a minority reference images today. This system employs only <span class='yellowIt'>{:,}</span> ...\n\n".format(i, noInThisSystemImages)
    
    mu += tbl.md() + "\n\n"
    
    return mu
        
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

    webReportImaging(stationNo)
                 
if __name__ == "__main__":
    main()
