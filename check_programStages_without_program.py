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

    
    PARENT_RESOURCE = "programStages"
    CHILD_RESOURCE = "program" # Watch out singular and plural.

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name", param_filter="filter="+CHILD_RESOURCE+":null")
    
    #check condition
    #check if each program has at least one programStage    
    for programStage in metadata_resources[PARENT_RESOURCE]:
        metadata_url = server_url+PARENT_RESOURCE+"/"+programStage["id"]
        message = f"The program stage '{programStage['name']}' ({programStage['id']}) + has NOT program associated. See {metadata_url}"
        logger.error(message)
