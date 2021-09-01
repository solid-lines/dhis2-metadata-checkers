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
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PROGRAMS, fields="name,id,programStages[programStageDataElements[dataElement[id,name]]]", param_filter=None)
    
    programs_data = {}
    for program in metadata_resources[PROGRAMS]:
        programs_data[program["id"]] = { "name": program["name"], "dataElements": []}
        for ps in program["programStages"]:
            for psde in ps["programStageDataElements"]:
                programs_data[program["id"]]["dataElements"].append(psde["dataElement"]["id"])
    
    PROGRAM_RULE_VBLES = "programRuleVariables"
    program_rule_vbles = utils.get_resources_from_online(credentials=credentials, resource_type=PROGRAM_RULE_VBLES, fields="name,id,programRuleVariableSourceType,program[id,name],dataElement[id,name]", param_filter="filter=programRuleVariableSourceType:neq:TEI_ATTRIBUTE&filter=programRuleVariableSourceType:neq:CALCULATED_VALUE")

    for prv in program_rule_vbles[PROGRAM_RULE_VBLES]:
        program_uid = prv["program"]["id"]
        if "dataElement" in prv:
            if prv["dataElement"]["id"] not in programs_data[program_uid]["dataElements"]:
                logger.error(f"Program Rule Variable '{prv['name']}' ({prv['id']}) uses a DE '{prv['dataElement']['name']}' ({prv['dataElement']['id']}) that does not belong to the associated program '{prv['program']['name']}' ")
        else:
            logger.error(f"Program Rule Variable '{prv['name']}' ({prv['id']}) of type DataElement without value assigned")

