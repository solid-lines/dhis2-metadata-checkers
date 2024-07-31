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

    resource_types = ["eventReports", "eventCharts", "dashboards", "maps"]

    dhis2_version = utils.get_dhis2_version(credentials)
    dhis2_version_detail = int(dhis2_version.split(".")[1])

    if dhis2_version_detail >= 35:
        resource_types.append("visualizations")

    if dhis2_version_detail < 38:
        resource_types.append("reportTables")

    for resource_type in resource_types:
        #retrieve all metadata_resources
        response = utils.get_resources_from_online(credentials=credentials, resource_type=resource_type, fields='id,name', param_filter=None)
        for resource in response[resource_type]:
            metadata_url = server_url + resource_type + "/" + resource["id"]

            r = utils.check_OK(credentials, metadata_url)
            if not r["valid"]:
                message = f"The {resource_type} '{resource['name']}' ({resource['id']}) returns {r['response'].json()}. See {metadata_url}"
                logger.error(message)
