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
    program_rules_without_condition = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,program[name],condition", param_filter="filter=condition:null")

    #check condition
    #check if all programStageSections are associated to a programStage
    for resource in program_rules_without_condition[PARENT_RESOURCE]:
        metadata_url = server_url+PARENT_RESOURCE+"/"+resource["id"]
        message = f"The Program Rule '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}' has not condition. See {metadata_url}"
        logger.error(message)
