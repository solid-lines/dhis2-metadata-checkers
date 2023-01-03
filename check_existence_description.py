#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import utils


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    server_url = credentials["server"]
    
    ############################################################################
        
    for resource_type in ["programs", "dataSets", "dataElements", "trackedEntityAttributes", "trackedEntityTypes", "indicators", "programIndicators", "validationRules", "predictors", "programRules", "visualizations", "dashboards"]:
        # Retrieve resources
        logger.info(f"Processing resource type: {resource_type}")
        try:
            response = utils.get_resources_from_online(credentials=credentials, resource_type=resource_type, fields='id,name,description', param_filter="filter=description:null")
            for resource in response[resource_type]:
                if not "description" in resource:
                    logger.warning(f"ALL-MQ-8 - Not description in resource '{resource_type}' ({resource['id']}).")
            
        except Exception as e: 
            logger.error(f"Error while processing resource type: {resource_type}")
            logger.error(e)
            response[resource_type] = {}
            