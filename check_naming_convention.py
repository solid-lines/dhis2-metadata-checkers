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


    # DE-MQ-2: The name/shortName/formName SHOULD not contains "Number of" or "number of"    

    PARENT_RESOURCE = "dataElements"

    for n in ["name", "shortName", "formName"]:
        #retrieve all metadata_resources
        metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,"+n, param_filter="filter="+n+":ilike:number of")
        
        for de in metadata_resources[PARENT_RESOURCE]:
            metadata_url = server_url+PARENT_RESOURCE+"/"+de["id"]
            message = f"DataElement contains the words 'number of' ({de['id']}) {n}='{de[n]}'"    
            logger.error(message)
