#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os
import re


PATTERN_CODE = re.compile("^([a-zA-Z0-9\_\|\-\.])+$") # upper and lower case letters, digits, '_', '|', '-', '.'
#PATTERN_CODE = re.compile("^([0-9A-Z_\|\-\.])+$") # upper case, _ , -, |

def is_valid_code(code):
    return PATTERN_CODE.search(code)


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    ############################################################################
    
    server_url = credentials["server"]

    RESOURCE_TYPE = "options"
    
    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields="id,name,code")
    for resource in metadata_resources[RESOURCE_TYPE]:
        
        if not is_valid_code(resource["code"]):
            metadata_url = server_url+RESOURCE_TYPE+"/"+resource["id"]
            message = f"The option code='{resource['code']}' (name='{resource['name']}' uid={resource['id']}) has an invalid code. See {metadata_url}"
            logger.error(message)
        else:
            pass#logging.debug(resource["code"])