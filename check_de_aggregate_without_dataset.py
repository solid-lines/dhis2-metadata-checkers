#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    flag_at_least_one_issue = False
    
    ############################################################################    

    try:    
        PARENT_RESOURCE = "dataElements"

        #retrieve all metadata_resources
        metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name", param_filter="filter=domainType:eq:AGGREGATE&filter=dataSetElements:empty")

        #check condition
        for resource in metadata_resources[PARENT_RESOURCE]:
            url_api = utils.get_url_api(server_url, PARENT_RESOURCE, resource["id"])
            url_ui = utils.get_url_maintenance(server_url, PARENT_RESOURCE, resource["id"])
        
            message = f"The dataElement (aggregate) '{resource['name']}' ({resource['id']}) is NOT associated to any dataset. See {url_ui} or {url_api}"
            logger.error(message)
            flag_at_least_one_issue = True
    
    except Exception as e:
        logger.error(f"Error while processing dataElements validation")
        logger.error(e)
        flag_at_least_one_issue = True
    
    if flag_at_least_one_issue:
        exit(1)  # exit unsuccessfully
