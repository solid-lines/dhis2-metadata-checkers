#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    
    
    PARENT_RESOURCE = "programRules"

    #retrieve all metadata_resources
    program_rules_without_condition = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,program[name],programRuleActions[id,programRuleActionType,content,data,dataElement[valueType],trackedEntityAttribute[valueType]]", param_filter="filter=programRuleActions.programRuleActionType:in:[ASSIGN,DISPLAYTEXT,DISPLAYKEYVALUEPAIR,SHOWWARNING,SHOWERROR,WARNINGONCOMPLETE,ERRORONCOMPLETE]&filter=programRuleActions.data:!null")

    for resource in program_rules_without_condition[PARENT_RESOURCE]:
        metadata_url = server_url+PARENT_RESOURCE+"/"+resource["id"]
        
        for pra in resource["programRuleActions"]:
            if ("data" in pra) and ("true" not in pra["data"] and "false" not in pra["data"] and "{" not in pra["data"] and "d2" not in pra["data"]) and (pra["data"][0] != "'" or pra["data"][-1] != "'" or pra["data"].count("'") != 2):
                if (pra["programRuleActionType"] in ["DISPLAYTEXT", "DISPLAYKEYVALUEPAIR", "SHOWWARNING", "SHOWERROR", "WARNINGONCOMPLETE", "ERRORONCOMPLETE"]) :
                    message = f"PRA-MQ-2 - Missing '' in assignment text of a Program Rule Action. The Program Rule '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}'. PRA uid='{pra['id']}' actionType={pra['programRuleActionType']} data={pra['data']}"
                    logger.error(message)
                elif pra["programRuleActionType"] in ["ASSIGN"]:
                    if "dataElement" in pra:
                        if pra['dataElement']['valueType'] in ["TEXT", "LONG_TEXT"]:
                            message = f"PRA-MQ-2 - Missing '' in assignment text of a Program Rule Action. The Program Rule '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}'. PRA uid='{pra['id']}' actionType={pra['programRuleActionType']} dataElement.valueType={pra['dataElement']['valueType']} data={pra['data']}"
                            logger.error(message)                        
                    elif "trackedEntityAttribute" in pra:
                        if pra['trackedEntityAttribute']['valueType'] in ["TEXT", "LONG_TEXT"]:
                            message = f"PRA-MQ-2 - Missing '' in assignment text of a Program Rule Action. The Program Rule '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}'. PRA uid='{pra['id']}' actionType={pra['programRuleActionType']} trackedEntityAttribute.valueType={pra['trackedEntityAttribute']['valueType']} data={pra['data']}"
                            logger.error(message)                        
                    else:
                        logger.debug(f"CALCULATED_VALUE {pra}")

                      
