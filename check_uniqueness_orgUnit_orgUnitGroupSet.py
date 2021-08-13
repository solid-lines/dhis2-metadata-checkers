#!/usr/bin/python
# -*- coding: UTF-8 -*-

from configparser import ConfigParser
import requests
from requests.auth import HTTPBasicAuth
from datetime import date
import logging
import os

##### Obtain credentials ####
credentials = {}
parser = ConfigParser()
parser.read("credentials.ini")
params = parser.items("credentials_clone") # CHANGE select here your credentials

for param in params:
    credentials[param[0]] = param[1]

SERVER_URL = credentials["server"]
SERVER_NAME = credentials["server_name"]
USERNAME = credentials["user"]
PASSWORD = credentials["password"]
PAGESIZE = credentials["page_size"]


##### Logging setup ####
today = date.today().strftime("%Y-%m-%d")
check_name = os.path.basename(__file__).replace(".py","")
FILENAME_LOG = today + "-"+SERVER_NAME+"-"+check_name+".log"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs error messages
fh = logging.FileHandler(FILENAME_LOG, encoding='utf-8')
fh.setLevel(logging.ERROR)
# create console handler which logs even debug messages
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


################################################################################


def get_resources_from_online(parent_resource, fields):
    page = 0
    resources = { parent_resource : [] }
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = SERVER_URL + parent_resource + ".json?fields="+(','.join(fields))+"&pageSize=" + str(PAGESIZE) + "&format=json&order=created:ASC&skipMeta=true&page=" + str(page)
        logging.debug(url_resource)
        response = requests.get(url_resource, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.ok:
            resources[parent_resource].extend(response.json()[parent_resource])
            if ("nextPage" not in response.json()["pager"]):
                data_to_query = False
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()

    return resources

def get_resource_fields(resource, resourceUID, fields):
    urlSource = SERVER_URL+resource+"/"+resourceUID+".json?fields="+(",".join(fields))
    logging.debug(urlSource)
    response = requests.get(urlSource, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return response.json()


################################################################################

# A key property of the group set concept in DHIS2 to understand is exclusivity, which implies that an organisation unit can be member of exactly one of the groups in a group set. A violation of this rule would lead to duplication of data when aggregating health facility data by the different groups, as a facility assigned to two groups in the same group set would be counted twice.
# https://docs.dhis2.org/en/implement/understanding-dhis2-implementation/organisation-units.html#organisation-unit-groups-and-group-sets

if __name__ == "__main__":

    OUG_SET = "organisationUnitGroupSets"
    OU_GROUP = "organisationUnitGroups"
    OU = "organisationUnits"

    #retrieve all metadata_resources
    metadata_resources = get_resources_from_online(parent_resource=OUG_SET, fields=["id", "name", "organisationUnitGroups[*]"])

    for oug_set in metadata_resources[OUG_SET]:
        
        names = {}
        ous_in_oug_set = []
        ous_by_oug = {}
        
        if not oug_set[OU_GROUP]: #if empty
            continue

        for ougroup in oug_set[OU_GROUP]:
            org_group = get_resource_fields(resource=OU_GROUP, resourceUID=ougroup["id"], fields=["id", "name", "organisationUnits[id, name]"])
            names[org_group["id"]] = org_group["name"]            
            org_units_in_this_ougroup = [ou["id"] for ou in org_group[OU]]
            
            for ou in org_group[OU]:
                names[ou["id"]] = ou["name"]
            
            ous_by_oug[ougroup["id"]] = org_units_in_this_ougroup
            
            ous_in_oug_set = ous_in_oug_set + org_units_in_this_ougroup 
        
        duplicates = {x for x in ous_in_oug_set if ous_in_oug_set.count(x) > 1}
        
        if duplicates:
            logging.error(f"OU Group SET {oug_set['name']} ({oug_set['id']})")
            for oug, ous in ous_by_oug.items():
                for dup in duplicates:
                    if dup in ous:
                        logger.error(f"check OU Group {names[oug]} ({oug}) and OU {names[dup]} ({dup}))")
            logging.error("-----------------------------------")
