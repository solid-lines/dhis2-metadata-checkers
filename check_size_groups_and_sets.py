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

    groups = {
        "programIndicatorGroups": "programIndicators",
        "dataElementGroups" : "dataElements",
        "indicatorGroups" : "indicators",
        "validationRuleGroups" : "validationRules",
        "predictorGroups": "predictors",
        "categoryOptionGroups": "categoryOptions",
        "organisationUnitGroups": "organisationUnits",
        "userGroups": "users",
        "optionGroups": "options",
    
        "categories": "categoryOptions",
        
        "indicatorGroupSets": "indicatorGroups",
        "organisationUnitGroupSets": "organisationUnitGroups",
        "optionSets": "options",
        "legendSets": "legends",
        "dataElementGroupSets": "dataElementGroups",
        "categoryOptionGroupSets": "categoryOptionGroups",
        "dataSets": "dataSetElements",
       # "colorSets": "colors",
        "optionGroupSets": "optionGroups"
    }

    # programTrackedEntityAttributeGroups removed since 2.40
    dhis2_version = utils.get_dhis2_version(credentials)
    dhis2_version_detail = int(dhis2_version.split(".")[1])
    if dhis2_version_detail < 40:
        groups["programTrackedEntityAttributeGroups"] = "programTrackedEntityAttributes"
    
    for k,v in groups.items():
        #retrieve all metadata_resources
        response = utils.get_resources_from_online(credentials=credentials, resource_type=k, fields="id,name,"+v+"::size", param_filter=None)

        for group in response[k]:
            #check condition
            if (group[v] <= 1):
                metadata_url = server_url+k+"/"+group["id"]
                message = "The "+ k +" '"+ str(group["name"]) + "' (" + str(group["id"]) + ") has not the expected number of "+v + " (size obtained="+str(group[v])+"). See "+metadata_url
                logger.error(message)
     
    
    expected_one = {
        "dataElements" : "dataSetElements",
    }
    
    for k,v in expected_one.items():
        #retrieve all metadata_resources
        response = utils.get_resources_from_online(credentials=credentials, resource_type=k, fields="id,name,"+v+"::size", param_filter=None)
        for group in response[k]:
            #check condition
            if (group[v] > 1):
                metadata_url = server_url+k+"/"+group["id"]
                message = "The "+ k +" "+ str(group["name"]) + "' (" + str(group["id"]) + ") has not the expected number of "+v + " (size obtained="+str(group[v])+"). See "+metadata_url
                logger.error(message)
