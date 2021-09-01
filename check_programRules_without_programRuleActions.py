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
    CHILD_RESOURCE = "programRuleActions" # Watch out singular and plural.

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,program[name]", param_filter="filter="+CHILD_RESOURCE+":empty")

    #check condition
    #check if all programStageSections are associated to a programStage
    for resource in metadata_resources[PARENT_RESOURCE]:
        if (not CHILD_RESOURCE in resource):
            metadata_url = server_url+PARENT_RESOURCE+"/"+resource["id"]
            message = f"The Program Rule '{resource['name']}' ({resource['id']}) from Program '{resource['program']['name']}' has not Program Rule Actions associated. See {metadata_url}"
            logger.error(message)
