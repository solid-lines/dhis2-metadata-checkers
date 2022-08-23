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

    # Filling the arrays with the IDs from OptionSets, dataElements and trackedEntityAttributes
    optionsets_uid = [os["id"] for os in optionSet_resources["optionSets"]]
    optionsets_dict = {os["id"] : os["name"] for os in optionSet_resources["optionSets"]}

    teas_uid = [attribute["optionSet"]["id"] for attribute in tea_resources["trackedEntityAttributes"]]
    des_uid = [element["optionSet"]["id"] for element in dataElement_resources["dataElements"]]
           
    optionset_not_used = [os for os in optionsets_uid if os not in teas_uid+des_uid]
    if optionset_not_used:
        message = f"{len(optionset_not_used)} optionSets {optionset_not_used} are not used by any TEA/DE."
        logger.warn(message)

        for os in optionset_not_used:
            message = f"The optionSets '{optionsets_dict[os]}' ({os}) is not used by any TEA/DE."
            logger.warn(message)
