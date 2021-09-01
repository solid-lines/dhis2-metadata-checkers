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
    
    PARENT_RESOURCES = ["eventReports", "eventCharts"]

    for PARENT_RESOURCE in PARENT_RESOURCES:
        #retrieve all metadata_resources
        metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE)
        
        logger.info(f'Retrieved {len(metadata_resources[PARENT_RESOURCE])} {PARENT_RESOURCE}')
        for eventReportChart in metadata_resources[PARENT_RESOURCE]:
            flag = False
            issues = []
            metadata_url = server_url+PARENT_RESOURCE+"/"+eventReportChart["id"]+"?fields=*,options[*]"
    
            if (len(eventReportChart["dataElementDimensions"]) > 0):
                for dataElementDimension in eventReportChart["dataElementDimensions"]:
                    if "filter" in dataElementDimension:
                        filter_dhis2 = dataElementDimension["filter"]
                        dataElementUid = dataElementDimension["dataElement"]["id"]
                        dataElement = utils.get_resource_from_online(credentials=credentials, resource_type="dataElements", resource_uid=dataElementUid, fields='valueType,optionSetValue,optionSet')
                        if dataElement["optionSetValue"]:
                            options_raw = utils.get_resource_from_online(credentials=credentials, resource_type="optionSets", resource_uid=dataElement["optionSet"]["id"], fields="options[code]")
                            options = [x["code"] for x in options_raw["options"]]
                            
                            #Check if the options present in the filter are valid options
                            options_in_filter = filter_dhis2[3:].split(";") # Removing 'IN:' and convert to array
                            for option_in_filter in options_in_filter:
                                if option_in_filter not in options:
                                    flag = True
                                    issues.append(f"The option '{option_in_filter}' is in the filter but not in the options of the optionSet ({dataElement['optionSet']['id']}): {options}")
            if flag:
                logger.error(f"Issue/s in filter of {PARENT_RESOURCE} '{eventReportChart['name']}' ({eventReportChart['id']}). See {metadata_url}")
                for issue in issues:
                    logger.error(issue)
                logger.error("------------------")

