#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os

    
if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    ############################################################################

    PROGRAMS = "programs"
    metadata_resources = utils.get_resources_from_online(credentials=credentials,resource_type=PROGRAMS, fields="name,id,programStages[programStageDataElements[dataElement[id,name]]]", param_filter=None)
    
    programs_data = {}
    for program in metadata_resources[PROGRAMS]:
        programs_data[program["id"]] = { "name": program["name"], "dataElements": []}
        for ps in program["programStages"]:
            for psde in ps["programStageDataElements"]:
                programs_data[program["id"]]["dataElements"].append(psde["dataElement"]["id"])
                
    
    PROGRAM_RULES = "programRules"
    program_rules = utils.get_resources_from_online(credentials=credentials, resource_type=PROGRAM_RULES, fields="name,id,program[id,name],programRuleActions[dataElement[id,name]]", param_filter=None)
    
    for program_rule in program_rules[PROGRAM_RULES]:
        program_uid = program_rule["program"]["id"]
        for pra in program_rule["programRuleActions"]:
            if "dataElement" in pra and pra["dataElement"]["id"] not in programs_data[program_uid]["dataElements"]:
                logger.error(f"Program Rule '{program_rule['name']}' ({program_rule['id']}) in the PR Action uses a DE '{pra['dataElement']['name']}' ({pra['dataElement']['id']}) that does not belong to the associated program '{program_rule['program']['name']}' ")
