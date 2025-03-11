#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os

def log_error(optionSet, metadata_url, logger):
    """Logs an error message for invalid sort order."""
    message = f"The optionSet '{optionSet['name']}' ({optionSet['id']}) has errors in the sortOrder. See {metadata_url}"
    logger.error(message)

if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    
    
    PARENT_RESOURCE = "optionSets"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,options[sortOrder]")


    for optionSet in metadata_resources[PARENT_RESOURCE]:
        size = len(optionSet["options"]);
        sortOrders = [x["sortOrder"] for x in optionSet["options"]]
        sortOrders = sorted(sortOrders)
        metadata_url = server_url+PARENT_RESOURCE+"/"+optionSet["id"]+"?fields=*,options[*]"

        #check condition
        #check if each optionSet has at least 2 options
        if (size <= 1):
            message = "The optionSet '"+ str(optionSet["name"]) + "' (" + str(optionSet["id"]) + ") has one or less options. See "+metadata_url
            logger.error(message)
        elif len(sortOrders) != size:
            log_error(optionSet, metadata_url, logger)
        else:
            first_sortOrder = sortOrders[0]

            # Check if the sortOrder of the options is valid (it could starts at 0 or 1. They could coexist in the same instance)
            # Check if the sortOrder of the options is valid: latest has the value of the size of the optionList).
            if first_sortOrder == 0:
                if (sortOrders[size - 1] != size - 1):
                    log_error(optionSet, metadata_url, logger)
            elif first_sortOrder == 1:
                if (sortOrders[size - 1] != size):
                    log_error(optionSet, metadata_url, logger)
            else:
                log_error(optionSet, metadata_url, logger)