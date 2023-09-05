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

    PARENT_RESOURCE = "visualizations"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,dataDimensionItems")
    
    for v in metadata_resources[PARENT_RESOURCE]:
        flag_empty_dataDimensionItem = False
        for element in v['dataDimensionItems']:
            if element == {}:
                flag_empty_dataDimensionItem = True
        if flag_empty_dataDimensionItem:
            url_api = server_url+PARENT_RESOURCE+"/"+v["id"]
            message = f"Visualization '{v['name']}' ({v['id']}) has empty data dimensions (one or more). See {url_api}"
            logger.warn(message)                
