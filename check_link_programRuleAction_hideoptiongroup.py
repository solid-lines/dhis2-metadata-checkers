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
    metadata_resources = utils.get_resources_from_online(credentials=credentials,resource_type=RESOURCE, fields="id,programRule[name,id,program[name,id]],optionGroup[name,optionSet],trackedEntityAttribute[id,name,optionSet[id,name,options]],dataElement[id,name,optionSet[id]],option", param_filter="filter=programRuleActionType:eq:HIDEOPTIONGROUP")
    
    for pra in metadata_resources[RESOURCE]:
        if "dataElement" in pra:
            if pra["dataElement"]["optionSet"]["id"] != pra["optionGroup"]["optionSet"]["id"]:
                logger.error(f"In program '{pra['programRule']['program']['name']}' ({pra['programRule']['program']['id']}), the program Rule '{pra['programRule']['name']}' ({pra['programRule']['id']}) in the PR Action ({pra['id']}) hides an optiongroup '{pra['optionGroup']['name']}' linked to an optionSet ({pra['optionGroup']['optionSet']['id']}) that is not the same than the optionSet ({pra['dataElement']['optionSet']['id']}) linked to the selected DE '{pra['dataElement']['name']}' ({pra['dataElement']['id']})")
        if "trackedEntityAttribute" in pra:
            if pra["trackedEntityAttribute"]["optionSet"]["id"] != pra["optionGroup"]["optionSet"]["id"]:
                logger.error(f"In program '{pra['programRule']['program']['name']}' ({pra['programRule']['program']['id']}), the program Rule '{pra['programRule']['name']}' ({pra['programRule']['id']}) in the PR Action ({pra['id']}) hides an optiongroup '{pra['optionGroup']['name']}' linked to an optionSet ({pra['optionGroup']['optionSet']['id']}) that is not the same than the optionSet ({pra['trackedEntityAttribute']['optionSet']['id']}) linked to the selected TEA '{pra['trackedEntityAttribute']['name']}' ({pra['trackedEntityAttribute']['id']})")
                
        if "option" in pra:
            logger.warn(f"In program '{pra['programRule']['program']['name']}' ({pra['programRule']['program']['id']}), the program Rule '{pra['programRule']['name']}' ({pra['programRule']['id']}) in the PR Action ({pra['id']}) contains an unexpected 'option' field ")
