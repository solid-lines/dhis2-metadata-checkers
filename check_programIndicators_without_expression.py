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

    
    PARENT_RESOURCE = "programIndicators"
    CHILD_RESOURCE = "expression" # Watch out singular and plural.

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name", param_filter="filter="+CHILD_RESOURCE+":null")

    #check condition
    #check if all programIndicators has a expression
    for resource in metadata_resources[PARENT_RESOURCE]:
        if CHILD_RESOURCE not in resource:
            metadata_url = server_url+PARENT_RESOURCE+"/"+resource["id"]
            message = "The programIndicator '"+ str(resource["name"]) + "' (" + str(resource["id"]) + ") has not a expression. See "+metadata_url
            logger.error(message)
