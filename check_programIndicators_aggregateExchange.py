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

    
    PARENT_RESOURCE = "programIndicators"
    ATTRIBUTE_IN_PI_TO_DATAELEMENT_FOR_AGGREGATE_EXPORT = "vudyDP7jUy5"
    PROGRAM = None # Use a Program UID (like "kFlCUSPV9mH") or None
    CC_DEFAULT = "bjDvmb4bfuf"

    # Filter by program
    param_filter = "filter=attributeValues.attribute.id:eq:"+ATTRIBUTE_IN_PI_TO_DATAELEMENT_FOR_AGGREGATE_EXPORT
    if PROGRAM:
        param_filter = param_filter+"&filter=program.id:eq:"+PROGRAM

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,program[id,name],attributeValues,aggregateExportCategoryOptionCombo,aggregateExportAttributeOptionCombo", param_filter=param_filter)

    for resource in metadata_resources[PARENT_RESOURCE]:
        metadata_url = server_url+PARENT_RESOURCE+"/"+resource["id"]
        attributeValues = {x["attribute"]["id"]: x["value"] for x in resource["attributeValues"]}
        de_code = attributeValues[ATTRIBUTE_IN_PI_TO_DATAELEMENT_FOR_AGGREGATE_EXPORT]
        de_resource = utils.get_resources_from_online(credentials=credentials, resource_type="dataElements", fields="id,name,code,categoryCombo", param_filter="filter=code:eq:"+de_code)
        de_cc = None
        
        if len(de_resource["dataElements"]) != 1:
            message = f"In Program '{resource['program']['name']}' ({resource['program']['id']}), the programIndicator '{resource['name']}' ({resource['id']}) use a DE code ('{de_code}') for aggregation export that doesn't exist. See {metadata_url}"
            logger.error(message)
        else:
            de_cc = de_resource["dataElements"][0]["categoryCombo"]["id"]

###

        if "aggregateExportCategoryOptionCombo" not in resource:
            coc_cc = CC_DEFAULT
        else:
            coc_code = resource["aggregateExportCategoryOptionCombo"]
            coc_resource = utils.get_resources_from_online(credentials=credentials, resource_type="categoryOptionCombos", fields="id,name,code,categoryCombo", param_filter="filter=code:eq:"+coc_code)
            coc_cc = None
            if len(coc_resource["categoryOptionCombos"]) != 1:
                message = f"In Program '{resource['program']['name']}' ({resource['program']['id']}), the programIndicator '{resource['name']}' ({resource['id']}) use a COC code ('{coc_code}') for aggregation export that doesn't exist. See {metadata_url}"
                logger.error(message)
            else:
                coc_cc = coc_resource["categoryOptionCombos"][0]["categoryCombo"]["id"]
        
        if de_cc and coc_cc and de_cc != coc_cc: # If DE CC has value and COC CC has value and their values are different
            message = f"In Program '{resource['program']['name']}' ({resource['program']['id']}), the programIndicator '{resource['name']}' ({resource['id']}) use a DE code ('{de_code}') and COC code ('{coc_code}') for aggregation export that don't share the same Category Combo (DE CC={de_cc}) (COC CC={coc_cc}). See {metadata_url}"
            logger.error(message)
