#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os

    
if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    ############################################################################
       
    program_rule_actions = utils.get_resources_from_online(credentials=credentials, resource_type="programRuleActions", fields="id,programRule[id,name,program[id,name]],data,dataElement[id,name,optionSet[id,name,options[code]]],trackedEntityAttribute[id,name,optionSet[id,name,options[code]]],content", param_filter="filter=programRuleActionType:eq:ASSIGN")

    for pra in program_rule_actions["programRuleActions"]:
        # Not support content (PRV)
        if "content" in pra:
            continue
        if "dataElement" in pra and not "optionSet" in pra["dataElement"]:
            continue
        if "trackedEntityAttribute" in pra and not "optionSet" in pra["trackedEntityAttribute"]:
            continue

        value_to_assign = pra["data"]
        value_to_assign = value_to_assign.replace("'","")

        # Heuristic (keep only straight values). Can be improved
        if "#" in value_to_assign or value_to_assign == "":
            continue
        
        target = None
        if "dataElement" in pra:
            int_type = "DE"
            target = pra["dataElement"]
            optionSet = target["optionSet"]
        elif "trackedEntityAttribute" in pra:
            int_type = "TEA"
            target = pra["trackedEntityAttribute"]
            optionSet = target["optionSet"]
        else:
            continue

        valid_option_codes = [x["code"] for x in optionSet["options"]]
        
        if value_to_assign not in valid_option_codes:
            program_rule = pra["programRule"]
            program = program_rule["program"]
            logger.error(f"In program '{program['name']}' ({program['id']}), in Program Rule '{program_rule['name']}' ({program_rule['id']}), the PR Action ({pra['id']}) tries to assign the value {pra['data']} to a {int_type} '{target['name']}' ({target['id']}), and this value is an invalid code (the {int_type} is linked to the optionSet '{optionSet['name']}' ({optionSet['id']}) and valid option codes are {valid_option_codes}) ")
