#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os


def find_duplicate_dictionaries(list_of_dicts):
    """
    Finds and returns a list of duplicate dictionaries within a list.

    Args:
        list_of_dicts: A list of dictionaries.

    Returns:
        A list of duplicate dictionaries.
    """
    seen = []
    duplicates = []
    for d in list_of_dicts:
        # Convert dictionary to a hashable type (like a tuple of sorted items)
        # to compare dictionaries by content.
        sorted_items = tuple(sorted(d.items()))
        if sorted_items in seen:
            duplicates.append(d)
        else:
            seen.append(sorted_items)
    return duplicates


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    

    # Retrieve all program rules
    pr_resources = utils.get_resources_from_online(credentials=credentials, resource_type="programRules", fields="id,name,programRuleActions[programRuleActionType,content,data,dataElement,trackedEntityDataValue,programStageSection,trackedEntityAttribute,messageTemplate,programStage]", param_filter=None)
    
    for resource in pr_resources["programRules"]:
        pras = resource["programRuleActions"]        
        duplicates = find_duplicate_dictionaries(pras)

        if duplicates:
            message = f"In Program Rule '{resource['name']}' ({resource['id']}), there are duplicated Program Rule Actions: {duplicates}"
            logger.error(message)            
