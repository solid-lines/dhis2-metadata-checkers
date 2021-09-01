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

    PARENT_RESOURCE = "programStageSections"
    CHILD_RESOURCE = "programStage" # Watch out singular and plural.

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name", param_filter="filter="+CHILD_RESOURCE+":null")

    #check condition
    #check if all programStageSections are associated to a programStage
    for resource in metadata_resources[PARENT_RESOURCE]:
        if (not CHILD_RESOURCE in resource):
            metadata_url = server_url+PARENT_RESOURCE+"/"+resource["id"]
            message = "The programStageSection '"+ str(resource["name"]) + "' (" + str(resource["id"]) + ") is NOT associated to a programStage. See "+metadata_url
            logger.error(message)
