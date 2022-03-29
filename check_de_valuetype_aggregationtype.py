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

        
    PARENT_RESOURCE = "dataElements"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,aggregationType,valueType")


    #check condition
    for resource in metadata_resources[PARENT_RESOURCE]:
        url_api = utils.get_url_api(server_url, PARENT_RESOURCE, resource["id"])
        url_ui = utils.get_url_maintenance(server_url, PARENT_RESOURCE, resource["id"])
        
        if resource["valueType"] in ["COORDINATE", "EMAIL", "FILE_RESOURCE", "GEOJSON", "LETTER", "LONG_TEXT", "PHONE_NUMBER", "TEXT", "TRACKER_ASSOCIATE", "USERNAME"] and resource["aggregationType"] != "NONE":
            message = f"The dataElement '{resource['name']}' ({resource['id']}) has an invalid 'value type - aggregation type relation'. ValueType={resource['valueType']}, AggregationType={resource['aggregationType']}. See {url_ui} or {url_api}"
            logger.error(message)
