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


def get_resources_from_online(parent_resource, fields='*', param_filter=None):
    page = 0
    resources = { parent_resource : [] }
    data_to_query = True
    while data_to_query:
        page += 1
        url_resource = SERVER_URL + parent_resource + ".json?fields="+(','.join(fields))+"&pageSize=" + str(PAGESIZE) + "&format=json&order=created:ASC&skipMeta=true&page=" + str(page)
        if param_filter:
            url_resource = url_resource + "&filter="+param_filter
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


def find_duplicates(resource_type, translation_property):
    
    metadata_resources = get_resources_from_online(parent_resource=resource_type, fields=["id","name","translations"], param_filter=None)
    
    DEFAULT_LOCALE = "en"
    
    dhis2_resources = {}
    dhis2_resources[DEFAULT_LOCALE] = {}

    # Create the locales
    for de in metadata_resources[resource_type]:
        if "translations" in de:
            for translation in de["translations"]:
                if translation["property"] == translation_property:
                    t_locale = translation["locale"]
                    if t_locale not in dhis2_resources:
                        dhis2_resources[t_locale] = {}

    for de in metadata_resources[resource_type]:
        de_uid = de["id"]
        de_name = de["name"]
        
        dhis2_resources[DEFAULT_LOCALE][de_name] = set()
        dhis2_resources[DEFAULT_LOCALE][de_name].add(de_uid)
        
        if "translations" in de:
            for translation in de["translations"]:
                if translation["property"] == translation_property:
                    t_locale = translation["locale"]
                    t_name = translation["value"]
                    if t_name not in dhis2_resources[t_locale]:
                        dhis2_resources[t_locale][t_name] = set()
                    dhis2_resources[t_locale][t_name].add(de_uid)


    for locale in dhis2_resources:
        for name in dhis2_resources[locale]:
            if len(dhis2_resources[locale][name]) > 1:
                message = f"{resource_type} - {translation_property} '{name}' is not unique for locale '{locale}'. Duplicates uids:{dhis2_resources[locale][name]}"
                logging.error(message)
    

################################################################################


if __name__ == "__main__":
    RESOURCES = ["attributes", "categories", "categoryCombos", "categoryOptionCombos", "categoryOptions", "dataElements", "indicatorTypes", "optionSets", "trackedEntityAttributes"]
    TRANSLATION_PROPERTIES = ["NAME", "SHORT_NAME"]
    for resource in RESOURCES:
        for translation_property in TRANSLATION_PROPERTIES: 
            find_duplicates(resource, translation_property)    
