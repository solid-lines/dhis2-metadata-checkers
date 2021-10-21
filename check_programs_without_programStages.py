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

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name", param_filter="filter=programStages:empty")
    
    for program in metadata_resources[PARENT_RESOURCE]:
        url_api = utils.get_url_api(server_url, PARENT_RESOURCE, program["id"])
        url_ui = utils.get_url_maintenance(server_url, PARENT_RESOURCE, program["id"])

        message = f"The program '{program['name']}' ({program['id']}) has NOT stages. See {url_ui} or {url_api}"
        logger.error(message)
