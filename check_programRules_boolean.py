#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os
import re

if __name__ == "__main__":

    credentials = utils.get_credentials()
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)

    server_url = credentials["server"]

    ############################################################################


    #retrieve all metadata_resources
    program_rules = utils.get_resources_from_online(credentials=credentials, resource_type="programRules", fields="id,name,program[id,name],condition")

    prv_not_boolean = utils.get_resources_from_online(credentials=credentials, resource_type="programRuleVariables", fields="name,id,programRuleVariableSourceType,program,dataElement[valueType],trackedEntityAttribute[valueType]", param_filter="filter=dataElement.valueType:!in:[TRUE_ONLY,BOOLEAN]&filter=programRuleVariableSourceType:neq:CALCULATED_VALUE")
    prv_not_boolean = prv_not_boolean["programRuleVariables"]

    #print(f"Number of program rules {len(program_rules['programRules'])}")
    for pr in program_rules["programRules"]:
        if "condition" not in pr:
            logger.error(f"Program Rule without condition {pr}")
            continue
        #print(pr["condition"])
        # PR-ST-1. !#{varible_name} will only work with boolean type variables (BOOLEAN and TRUE_ONLY).
        prv_uids_not = [x.replace("!","").strip().replace("#","").replace("{","").replace("}","") for x in re.findall(r'\![ ]*#\{[a-zA-Z0-9 -\._ ]*\}', pr["condition"])]

        for prv_name in prv_uids_not:
            not_bool = [x for x in prv_not_boolean if x["name"]==prv_name and x["program"]["id"]==pr["program"]["id"]]

            if not_bool:
                if not_bool[0]['programRuleVariableSourceType'] == "CALCULATED_VALUE":
                    logger.warning(f"Program '{pr['program']['name']}' ({pr['program']['id']}). The PRV '{prv_name}' ({not_bool[0]['programRuleVariableSourceType']}) is NOT boolean and it is used using !#{{prv_name}} in PR '{pr['name']}' ({pr['id']}): condition '{pr['condition']}'")
                elif not_bool[0]['programRuleVariableSourceType'] == "TEI_ATTRIBUTE":
                    logger.error(f"Program '{pr['program']['name']}' ({pr['program']['id']}). The PRV '{prv_name}' ({not_bool[0]['programRuleVariableSourceType']}) is NOT boolean ({not_bool[0]['trackedEntityAttribute']['valueType']}) and it is used using !#{{prv_name}} in PR '{pr['name']}' ({pr['id']}): condition '{pr['condition']}'")
                else: # Data Element
                    logger.error(f"Program '{pr['program']['name']}' ({pr['program']['id']}). The PRV '{prv_name}' ({not_bool[0]['programRuleVariableSourceType']}) is NOT boolean ({not_bool[0]['dataElement']['valueType']}) and it is used using !#{{prv_name}} in PR '{pr['name']}' ({pr['id']}): condition '{pr['condition']}'")


