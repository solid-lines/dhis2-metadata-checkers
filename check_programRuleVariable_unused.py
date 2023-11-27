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

    # Retrieve all program rule variables
    prv_resources = utils.get_resources_from_online(credentials=credentials, resource_type="programRuleVariables", fields="id,name,program[name,id]", param_filter=None)
    # Retrieve all program rules
    pr_resources = utils.get_resources_from_online(credentials=credentials, resource_type="programRules", fields="id,name,condition,programRuleActions[id,content,data,programRule]")
    
    # Retrieve all program rules
    
    for resource in prv_resources["programRuleVariables"]:
        
        used_in_program_rules = []
        used_in_program_rule_actions = []
        for program_rule in pr_resources["programRules"]:
            condition = program_rule.get("condition", "")
            if re.search(r"#\{" + re.escape(resource["name"]) + r"}", condition):
                used_in_program_rules.append(program_rule)

            for program_rule_action in program_rule["programRuleActions"]:
                data_field = program_rule_action.get("data", "")
                content_field = program_rule_action.get("content", "")
                if re.search(r"#\{" + re.escape(resource["name"]) + r"}", data_field) or re.search(r"#\{" + re.escape(resource["name"]) + r"}", content_field):
                    used_in_program_rule_actions.append(program_rule_action)

        # If not used, add information to the rows list and log a warning message
        if not used_in_program_rules and not used_in_program_rule_actions:
            message = f"In Program '{resource['program']['name']}' ({resource['program']['id']}), the PRV '{resource['name']}' ({resource['id']}) is not being used by any programRule or ProgramRuleAction."
            logger.error(message)

