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
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PROGRAMS, fields="name,id,programTrackedEntityAttributes[trackedEntityAttribute[id,name]],trackedEntityType[id,name,trackedEntityTypeAttributes[trackedEntityAttribute[id,name]]]", param_filter=None)
    
    programs_data = {}
    for program in metadata_resources[PROGRAMS]:
        program_uid = program["id"]
        programs_data[program_uid] = { "name": program["name"], "teas": []}
        teas = program["programTrackedEntityAttributes"]
        if "trackedEntityType" in program:
            teas = teas + program["trackedEntityType"]["trackedEntityTypeAttributes"]
        for tea in teas:
            programs_data[program_uid]["teas"].append(tea["trackedEntityAttribute"]["id"])
    
    
    PROGRAM_RULES = "programRules"
    program_rules = utils.get_resources_from_online(credentials=credentials, resource_type=PROGRAM_RULES, fields="name,id,program[id,name],programRuleActions[trackedEntityAttribute[id,name]]", param_filter=None)
    
    for program_rule in program_rules[PROGRAM_RULES]:
        program_uid = program_rule["program"]["id"]
        for pra in program_rule["programRuleActions"]:
            if "trackedEntityAttribute" in pra and pra["trackedEntityAttribute"]["id"] not in programs_data[program_uid]["teas"]:
                logger.error(f"Program Rule '{program_rule['name']}' ({program_rule['id']}) in the PR Action uses a TEA '{pra['trackedEntityAttribute']['name']}' ({pra['trackedEntityAttribute']['id']}) that does not belong to the associated program '{program_rule['program']['name']}' or the TET")
