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

    PARENT_RESOURCE = "programs"
    CHILD_RESOURCE = "trackedEntityType" # Watch out singular and plural.

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,trackedEntityType", param_filter="filter=programType:eq:WITHOUT_REGISTRATION")
    
    #check condition
    #check if a program without registration (Event program) is associated (unexpectedly) to a Tracked Entity Type    
    for program in metadata_resources[PARENT_RESOURCE]:
        if CHILD_RESOURCE in program:
            metadata_url = server_url+PARENT_RESOURCE+"/"+program["id"]
            message = f"The event (without registration) program '{program['name']}' ({program['id']}) is associated to a Tracked Entity Type. See {metadata_url}"
            logger.error(message)
