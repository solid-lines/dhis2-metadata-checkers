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
    
    PROGRAM_RULE_VBLES = "programRuleVariables"
    program_rule_vbles = utils.get_resources_from_online(credentials=credentials, resource_type=PROGRAM_RULE_VBLES, fields="name,id,programRuleVariableSourceType,program[id,name],trackedEntityAttribute[id,name]", param_filter="filter=programRuleVariableSourceType:eq:TEI_ATTRIBUTE")
    
    for prv in program_rule_vbles[PROGRAM_RULE_VBLES]:
        program_uid = prv["program"]["id"]
        if "trackedEntityAttribute" in prv:
            if prv["trackedEntityAttribute"]["id"] not in programs_data[program_uid]["teas"]:
                logger.error(f"Program Rule Variable '{prv['name']}' ({prv['id']}) uses a trackedEntityAttribute '{prv['trackedEntityAttribute']['name']}' ({prv['trackedEntityAttribute']['id']}) that does not belong to the associated program '{prv['program']['name']}' ")
        else:
            logger.error(f"Program Rule Variable '{prv['name']}' ({prv['id']}) of type trackedEntityAttribute without value assigned")


