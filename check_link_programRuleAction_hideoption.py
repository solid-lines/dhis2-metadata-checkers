#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os

    
if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    ############################################################################

    RESOURCE = "programRuleActions"
    metadata_resources = utils.get_resources_from_online(credentials=credentials,resource_type=RESOURCE, fields="id,programRule[name,id,program[name,id]],option,trackedEntityAttribute[id,name,optionSet[id,name,options]],dataElement[id,name,optionSet[id,name,options]],optionGroup", param_filter="filter=programRuleActionType:eq:HIDEOPTION")
    
    for pra in metadata_resources[RESOURCE]:
        option = pra["option"]["id"]
        if "dataElement" in pra:
            valid_options = [x["id"] for x in pra["dataElement"]["optionSet"]["options"]]
            if option not in valid_options:
                logger.error(f"In program '{pra['programRule']['program']['name']}' ({pra['programRule']['program']['id']}), the program Rule '{pra['programRule']['name']}' ({pra['programRule']['id']}) has a PR Action ({pra['id']}) that hides an option ({pra['option']['id']}) that does not belong to the optionSet '{pra['dataElement']['optionSet']['name']}' ({pra['dataElement']['optionSet']['id']}) linked to the selected DE '{pra['dataElement']['name']}' ({pra['dataElement']['id']}). Valid options are {valid_options}")
        if "trackedEntityAttribute" in pra:
            valid_options = [x["id"] for x in pra["trackedEntityAttribute"]["optionSet"]["options"]]
            if option not in valid_options:
                logger.error(f"In program '{pra['programRule']['program']['name']}' ({pra['programRule']['program']['id']}), the program Rule '{pra['programRule']['name']}' ({pra['programRule']['id']}) has a PR Action ({pra['id']}) that hides an option ({pra['option']['id']}) that does not belong to the optionSet '{pra['trackedEntityAttribute']['optionSet']['name']}' ({pra['trackedEntityAttribute']['optionSet']['id']}) linked to the selected TEA '{pra['trackedEntityAttribute']['name']}' ({pra['trackedEntityAttribute']['id']}). Valid options are {valid_options}")
        if "optionGroup" in pra:
            logger.warn(f"In program '{pra['programRule']['program']['name']}' ({pra['programRule']['program']['id']}), the program Rule '{pra['programRule']['name']}' ({pra['programRule']['id']}) in the PR Action ({pra['id']}) contains an unexpected 'optionGroup' field ")
