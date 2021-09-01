#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os


def find_duplicates(resource_type, translation_property):
    
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=resource_type, fields="id,name,translations", param_filter=None)
    
    DEFAULT_LOCALE = "en"
    
    locales_to_check = [DEFAULT_LOCALE, "es", "fr", "pt", "ru"]
    
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
            if len(dhis2_resources[locale][name]) > 1 and locale in locales_to_check:
                message = f"{resource_type} - {translation_property} '{name}' is not unique for locale '{locale}'. Duplicates uids:{dhis2_resources[locale][name]}"
                logger.error(message)
    

################################################################################


if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    

    RESOURCES = ["attributes", "categories", "categoryCombos", "categoryOptionCombos", "categoryOptions", "dataElements", "indicatorTypes", "optionSets", "trackedEntityAttributes"]
    TRANSLATION_PROPERTIES = ["NAME", "SHORT_NAME"]
    for resource in RESOURCES:
        for translation_property in TRANSLATION_PROPERTIES: 
            find_duplicates(resource, translation_property)    
