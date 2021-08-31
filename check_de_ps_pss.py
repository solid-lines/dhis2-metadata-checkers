#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os

    
if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    ############################################################################
    
    PROGRAM_STAGES = "programStages"
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PROGRAM_STAGES, fields="name,id,program[id,name],programStageDataElements[dataElement],programStageSections[dataElements]", param_filter="filter=formType:eq:SECTION&filter=program:!null")
    
    programs_data = {}
    for programStage in metadata_resources[PROGRAM_STAGES]:
        program_uid = programStage["program"]["id"]
        program_name = programStage["program"]["name"]
        programStage_uid = programStage["id"]
        programStage_name = programStage["name"]
        programStageDataElements = [x["dataElement"]["id"] for x in programStage["programStageDataElements"]]
        programStageSectionsDE = list()
        for pss in programStage["programStageSections"]:
            programStageSectionsDE = programStageSectionsDE + [x["id"] for x in pss["dataElements"]]

        a = set(programStageDataElements)
        b = set(programStageSectionsDE)
 
        if a != b:
            logger.warning(f"The DE assigned to this Program Stage are not included in the program Stage Section. Check the programStage '{programStage_name}' ({programStage_uid}) of the program '{program_name}' ({program_uid})")
