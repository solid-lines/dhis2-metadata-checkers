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
    CHILD_RESOURCE = "programStages" # Watch out singular and plural.

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name", param_filter="filter="+CHILD_RESOURCE+":null")
    
    #check condition
    #check if each program has at least one programStage    
    for program in metadata_resources[PARENT_RESOURCE]:
        if not (len(program[CHILD_RESOURCE])):
            metadata_url = server_url+PARENT_RESOURCE+"/"+program["id"]
            message = "The program "+ str(program["name"]) + "' (" + str(program["id"]) + ") has NOT stages. See "+metadata_url
            logger.error(message)
