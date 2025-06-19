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

    resource_types = ["dataElements", "trackedEntityAttributes", "programs", "dataSets"]

    for resource_type in resource_types:
        # retrieve all metadata_resources
        resources = utils.get_resources_from_online(credentials=credentials, resource_type=resource_type, fields="id,name,created,lastUpdated", param_filter="filter=sharing.userGroups:empty&filter=sharing.public:eq:--------")

        for r in resources[resource_type]:
            message = f"The {resource_type} '{r['name']}' ({r['id']}) is not public shared and it does not have any userGroup associated."
            logger.warning(message)
