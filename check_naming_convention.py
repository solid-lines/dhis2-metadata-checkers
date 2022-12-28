#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os
import re

if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################


    # DE-MQ-2: The name/shortName/formName SHOULD not contains "Number of" or "number of"    
    for dhis2_resource in ["dataElements"]:
        for n in ["name", "shortName"]:
            #retrieve all metadata_resources
            metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=dhis2_resource, fields="id,"+n, param_filter="filter="+n+":ilike:number of")
            for de in metadata_resources[dhis2_resource]:
                metadata_url = server_url+dhis2_resource+"/"+de["id"]
                message = f"DE-MQ-2 - {dhis2_resource} contains the words 'number of' ({de['id']}) {n}='{de[n]}'"
                logger.error(message)

    # Check Numbers as part of names
    # categoryCombos has NOT a shortName
    for dhis2_resource in ["dataElements", "indicators", "programIndicators", "categories", "categoryOptions", "categoryCombos", "maps", "visualizations"]:
        for n in ["name", "shortName"]:
            if (dhis2_resource == "categoryCombos") and (n == "shortName"):
                continue
            for ch in ['>', '<', '≤', '≥']:
                metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=dhis2_resource, fields="id,"+n, param_filter="filter="+n+":ilike:"+ch)
                for res in metadata_resources[dhis2_resource]:
                    metadata_url = server_url+dhis2_resource+"/"+res["id"]
                    message = f"ALL-MQ-9 - {dhis2_resource} contains the character '{ch}' ({res['id']}) {n}='{res[n]}'"
                    logger.warning(message)

            # Checking intervals (1-4, ok. 1 - 4, wrong)
            metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=dhis2_resource, fields="id,"+n, param_filter="filter="+n+":like:-")
            for res in metadata_resources[dhis2_resource]:
                metadata_url = server_url+dhis2_resource+"/"+res["id"]
                pattern = r"\d - \d"
                result = sum(1 for _ in re.finditer(pattern, res[n]))
                if result:
                    message = f"ALL-MQ-10 - {dhis2_resource} contains the expression 'digit(0-9) - digit(0-9)' ({res['id']}) {n}='{res[n]}'"
                    logger.warning(message)