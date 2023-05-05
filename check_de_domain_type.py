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

        
    # Retrieving all dataSets with at least one DE which domain type is different than AGGREGATE
    dataSets_resources = utils.get_resources_from_online(credentials=credentials, resource_type="dataSets", fields="id,name,dataSetElements[dataElement[id,name,domainType]", param_filter="filter=dataSetElements.dataElement.domainType:neq:AGGREGATE")
    dataSets_resources["dataSets"].sort(key=lambda x: x["name"])

    for ds in dataSets_resources["dataSets"]:
        filtered_data_elements = [de["dataElement"] for de in ds["dataSetElements"] if de["dataElement"]["domainType"] != "AGGREGATE"]
        if filtered_data_elements:
            message = f"The dataSet '{ds['name']}' ({ds['id']}) has at least one dataElement with domainType different to AGGREGATE."
            logger.warning(message)
            for de in filtered_data_elements:
                message = f"- DataElement '{de['name']}' ({de['id']}) with domainType {de['domainType']}."
                logger.info(message)


    # Retrieving all programStages with at least one DE which domain type is different than TRACKER
    program_stages_resources = utils.get_resources_from_online(credentials=credentials, resource_type="programStages",
                                                               fields="id,name,program[name,id],programStageDataElements[dataElement[id,name,domainType]]",
                                                               param_filter="filter=programStageDataElements.dataElement.domainType:neq:TRACKER")

    for ps in program_stages_resources["programStages"]:
        filtered_data_elements = [de["dataElement"] for de in ps["programStageDataElements"] if de["dataElement"]["domainType"] != "TRACKER"]
        if filtered_data_elements:
            message = f"In program '{ps['program']['name']}' ({ps['program']['id']}), the programStage '{ps['name']}' ({ps['id']}) has at least one dataElement with domainType different to TRACKER"
            logger.warning(message)
            for de in filtered_data_elements:
                message = f"- DataElement '{de['name']}' ({de['id']}) with domainType {de['domainType']}."
                logger.warning(message)
