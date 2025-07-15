#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os
import re
from collections import Counter

if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    

        
    RESOURCE_TYPE = "programRuleVariables"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=RESOURCE_TYPE, fields="id,name,program[name,id]", param_filter=None)

    all_prv = list()
        
    for resource in metadata_resources[RESOURCE_TYPE]:

        # Creating a tuple (program_name, program_id, prv_name)
        all_prv.append((resource['program']['name'], resource['program']['id'], resource["name"]))

        forbidden = ["and", "or", "not"] # (dhis version >= 2.34)
        #update for inicio de linea y fin de linea

        if any([" "+substring+" " in resource["name"] for substring in forbidden]) or \
           any([resource["name"].startswith(substring+" ") for substring in forbidden]) or \
           any([resource["name"].endswith(" "+substring) for substring in forbidden]):
            metadata_url = server_url+RESOURCE_TYPE+"/"+resource["id"]
            message = f"In Program '{resource['program']['name']}' ({resource['program']['id']}), the PRV {resource['name']} ({resource['id']}) contains 'and/or/not'. See {metadata_url}"
            logger.error(message)

        if not bool(re.match("^[a-zA-Z\d_\-\.\ ]+$", resource["name"])):
            metadata_url = server_url+RESOURCE_TYPE+"/"+resource["id"]
            message = f"In Program '{resource['program']['name']}' ({resource['program']['id']}), the PRV {resource['name']} ({resource['id']}) contains unexpected characters. See {metadata_url}"
            logger.error(message)


    prv_name_dup = [k for k,count in Counter(all_prv).items() if count > 1]
    for prv in prv_name_dup:
        message = f"In Program '{prv[0]}' ({prv[1]}), there are more than one PRV with the same name '{prv[2]}'."
        logger.error(message)
