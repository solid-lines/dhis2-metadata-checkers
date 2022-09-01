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
    
    optionSet_resources = utils.get_resources_from_online(credentials=credentials, resource_type="optionSets", fields="id,name")
    tea_resources = utils.get_resources_from_online(credentials=credentials, resource_type="trackedEntityAttributes", fields="id,name,optionSet[id,name],optionSetValue", param_filter="filter=optionSetValue:eq:true")
    dataElement_resources = utils.get_resources_from_online(credentials=credentials, resource_type="dataElements", fields="id,name,optionSet[id,name],optionSetValue", param_filter="filter=optionSetValue:eq:true")
    attributes_resources = utils.get_resources_from_online(credentials=credentials, resource_type="attributes", fields="id,name,optionSet[id,name]",param_filter="filter=optionSet:!null")

    # Filling the arrays with the IDs from OptionSets, dataElements and trackedEntityAttributes
    optionsets_uid = [os["id"] for os in optionSet_resources["optionSets"]]
    optionsets_dict = {os["id"] : os["name"] for os in optionSet_resources["optionSets"]}

    teas_uid = [tea["optionSet"]["id"] for tea in tea_resources["trackedEntityAttributes"]]
    des_uid = [de["optionSet"]["id"] for de in dataElement_resources["dataElements"]]
    atts_uid = [att["optionSet"]["id"] for att in attributes_resources["attributes"]]
           
    optionset_not_used = [os for os in optionsets_uid if os not in teas_uid+des_uid+atts_uid]
    if optionset_not_used:
        message = f"{len(optionset_not_used)} optionSets are not used by any TEA/DE/attribute: ({optionset_not_used})"
        logger.warn(message)

        for os in optionset_not_used:
            message = f"The optionSet '{optionsets_dict[os]}' ({os}) is not used by any TEA/DE/attribute."
            logger.warn(message)
