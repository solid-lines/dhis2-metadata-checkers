#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os

def code_compatible(value, valueType):

    if valueType=="TEXT" or valueType=="LONG_TEXT":
        return True

    # TODO: add float support
    if valueType=="NUMBER" or valueType=="INTEGER" or valueType=="INTEGER_ZERO_OR_POSITIVE":
        if value.isdigit():
            return True

    return False
    

if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    
    
    PARENT_RESOURCE = "dataElements"

    #retrieve all metadata_resources
    fields="id,name,optionSetValue,valueType,optionSet[id,name,valueType,options[code]]"
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields=fields, param_filter="filter=optionSetValue:eq:true")

    for dataElement in metadata_resources[PARENT_RESOURCE]:
        metadata_url = server_url+PARENT_RESOURCE+"/"+dataElement["id"]+"?fields="+fields
        
        de_valuetype = dataElement["valueType"]
        optionSet = dataElement["optionSet"]

        if de_valuetype != dataElement["optionSet"]["valueType"]:
            message = f"The dataElement '{dataElement['name']}' ({dataElement['id']}) value type ({dataElement['valueType']}) is different than the value type ({optionSet['valueType']}) of the optionSet '{optionSet['name']}' ({optionSet['id']}). See {metadata_url}"
            logger.warn(message)

        
        
        for option in dataElement["optionSet"]["options"]:
            if not code_compatible(option["code"], de_valuetype):
                message = f"The dataElement '{dataElement['name']}' ({dataElement['id']}) value type ({dataElement['valueType']}) doesn't match the option code value ({option['code']}) of the optionSet '{optionSet['name']}' ({optionSet['id']}). See {metadata_url}"
                logger.warn(message)
