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

    # Program Rule expression (condition)
            
    RESOURCE_TYPE = "programRules"
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields="id,name", param_filter="filter=condition:like:program_stage_name")
    
    for resource in metadata_resources[RESOURCE_TYPE]:
        url_ui = utils.get_url_maintenance(server_url, RESOURCE_TYPE, resource['id'])
        message = f"The PR '{resource['name']}' ({resource['id']}) contains 'program_stage_name' in the filter. See {url_ui}" 
        logger.error(message)

    ############################################################################    

    # Program Rule Action expression
            
    RESOURCE_TYPE = "programRuleActions"
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields="id,data,programRule[id,name]", param_filter="filter=data:like:program_stage_name")
    
    for resource in metadata_resources[RESOURCE_TYPE]:
        url_ui = utils.get_url_maintenance(server_url, "programRules", resource['programRule']['id'])
        message = f"The PR '{resource['programRule']['name']}' ({resource['programRule']['id']}) contains 'program_stage_name' in a PRAction ({resource['id']}). See {url_ui}" 
        logger.error(message)

    ############################################################################    

    # Program Indicator: expression
            
    RESOURCE_TYPE = "programIndicators"
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields="id,name", param_filter="filter=expression:like:program_stage_name")
    
    for resource in metadata_resources[RESOURCE_TYPE]:
        url_ui = utils.get_url_maintenance(server_url, RESOURCE_TYPE, resource['id'])
        message = f"The PI '{resource['name']}' ({resource['id']}) contains 'program_stage_name' in the expression. See {url_ui}" 
        logger.error(message)

    ############################################################################    

    # Program Indicator: filter
            
    RESOURCE_TYPE = "programIndicators"
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields="id,name,program[id,name]", param_filter="filter=filter:like:program_stage_name")
    
    for resource in metadata_resources[RESOURCE_TYPE]:
        url_ui = utils.get_url_maintenance(server_url, RESOURCE_TYPE, resource['id'])
        message = f"From program '{resource['program']['name']}' ({resource['program']['id']}), the PI '{resource['name']}' ({resource['id']}) contains 'program_stage_name' in the filter. See {url_ui}" 
        logger.error(message)
