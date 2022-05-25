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

    PARENT_RESOURCE = "programStages"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,program[name,id],name,dataEntryForm[id,htmlCode]", param_filter="filter=dataEntryForm:!null")
    
    #check condition (programStage with dataEntryForm)
    for programStage in metadata_resources[PARENT_RESOURCE]:
        url_api = utils.get_url_api(server_url, PARENT_RESOURCE, programStage["id"])
        url_ui = utils.get_url_maintenance(server_url, PARENT_RESOURCE, programStage["program"]["id"])
        
        program_id = programStage['program']['id']
        program_name = programStage['program']['name']
        if "htmlCode" in programStage["dataEntryForm"]:
            message = f"In program '{program_name}' ({program_id}), the program stage '{programStage['name']}' ({programStage['id']}) has a custom form. See {url_ui} or {url_api}"
            logger.warn(message)
        else:
            message = f"In program '{program_name}' ({program_id}), the program stage '{programStage['name']}' ({programStage['id']}) has an empty custom form. See {url_ui} or {url_api}"
            logger.error(message)

    
    ############################################################################

    PARENT_RESOURCE = "programs"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,dataEntryForm[id,htmlCode]", param_filter="filter=dataEntryForm:!null")
    
    #check condition (programStage with dataEntryForm)
    for program in metadata_resources[PARENT_RESOURCE]:
        url_api = utils.get_url_api(server_url, PARENT_RESOURCE, program["id"])
        url_ui = utils.get_url_maintenance(server_url, PARENT_RESOURCE, program["id"])
        
        program_id = program['id']
        program_name = program['name']
        if "htmlCode" in program["dataEntryForm"]:
            message = f"The program '{program_name}' ({program_id}) has a custom form. See {url_ui} or {url_api}"
            logger.warn(message)
        else:
            message = f"The program '{program_name}' ({program_id}) has an empty custom form. See {url_ui} or {url_api}"
            logger.error(message)

    ############################################################################

    PARENT_RESOURCE = "dataSets"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,dataEntryForm[id,htmlCode]", param_filter="filter=dataEntryForm:!null")
    
    #check condition (programStage with dataEntryForm)
    for dataset in metadata_resources[PARENT_RESOURCE]:
        url_api = utils.get_url_api(server_url, PARENT_RESOURCE, dataset["id"])
        url_ui = utils.get_url_maintenance(server_url, PARENT_RESOURCE+"-dataEntryForms", dataset["id"])
        
        dataset_id = dataset['id']
        dataset_name = dataset['name']
        if "htmlCode" in dataset["dataEntryForm"]:
            message = f"The dataSet '{dataset_name}' ({dataset_id}) has a custom form. See {url_ui} or {url_api}"
            logger.warn(message)
        else:
            message = f"The dataSet '{dataset_name}' ({dataset_id}) has an empty custom form. See {url_ui} or {url_api}"
            logger.error(message)