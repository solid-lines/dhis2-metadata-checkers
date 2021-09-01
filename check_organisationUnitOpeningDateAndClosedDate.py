#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os
from datetime import datetime


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    
    
    PARENT_RESOURCE = "organisationUnits"
    OPENING_DATE = "openingDate"
    CLOSED_DATE = "closedDate"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=PARENT_RESOURCE, fields="id,name,openingDate,closedDate", param_filter="filter=closedDate:!null")
    
    #check condition
    #check if each organization unit has coherent dates    
    for orgUnit in metadata_resources[PARENT_RESOURCE]:
        closedDate = datetime.strptime(orgUnit[CLOSED_DATE],"%Y-%m-%dT%H:%M:%S.%f")
        openingDate = datetime.strptime(orgUnit[OPENING_DATE],"%Y-%m-%dT%H:%M:%S.%f")

        metadata_url = server_url+PARENT_RESOURCE+"/"+orgUnit["id"]
        if closedDate > datetime.now():
            logger.error("The organisationUnit '"+ str(orgUnit["name"]) + "' (" + str(orgUnit["id"]) + ") has a closedDate in the future (later than today): "+str(closedDate)+". See "+metadata_url)

        if openingDate > closedDate:
            logger.error("The organisationUnit '"+ str(orgUnit["name"]) + "' (" + str(orgUnit["id"]) + ") has the opening date ("+str(openingDate)+") later than the closed date: ("+str(closedDate)+"). See "+metadata_url)
