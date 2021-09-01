#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os
from collections import Counter


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    

    PARENT_RESOURCE = "optionSets"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,options[name,code]", param_filter=None)


    for optionSet in metadata_resources[PARENT_RESOURCE]:
        metadata_url = server_url+PARENT_RESOURCE+"/"+optionSet["id"]+"?fields=*,options[*]"

        #check condition
        # all option's names that belong to a optionSet MUST be unique
        names = [o["name"]for o in optionSet["options"]]
        if len(names) != len(set(names)):
            d =  Counter(names)
            res = ["'"+k+"'" for k, v in d.items() if v > 1]
            message = "There are options in the optionSet "+ str(optionSet["name"]) + "' (" + str(optionSet["id"]) + ") with the same name. The duplicated names are ("+', '.join(res)+"). See "+metadata_url
            logger.error(message)
            
        # all option's codes that belong to a optionSet MUST be unique
        codes = [o["code"]for o in optionSet["options"]]
        if len(codes) != len(set(codes)):
            d =  Counter(codes)
            res = ["'"+k+"'" for k, v in d.items() if v > 1]
            message = "There are options in the optionSet "+ str(optionSet["name"]) + "' (" + str(optionSet["id"]) + ") with the same code. The duplicated codes are: ("+', '.join(res)+"). See "+metadata_url
            logger.error(message)