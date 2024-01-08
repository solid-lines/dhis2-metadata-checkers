#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os
import collections

def find_duplicated_translations(metadata, metadata_resource, properties):
    for element in metadata[metadata_resource]:
        for _property in properties:        
            locales = [tr["locale"] for tr in element["translations"] if tr["property"] == _property]
            repeated_locales = [locale for locale, count in collections.Counter(locales).items() if count > 1]
            if repeated_locales:
                message = f"The '{metadata_resource}' '{element['name']}' ({element['id']}) has more than one translation for the property '{_property}' and locale/s: {repeated_locales}:"
                logger.warning(message)
                for rep in repeated_locales:
                    for tr in element["translations"]:
                        if tr["locale"] == rep and tr["property"] == _property:
                            message = f"'{tr['property']}' : '{tr['locale']}': '{tr['value']}'"
                            logger.warning(message)

if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################    

    # get schemas.json
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type="schemas", fields="name,metadata,translatable,collectionName,properties[name,translatable]")

    # get properties that are translatable
    for resource in metadata_resources["schemas"]:
        p_translatable = [p for p in resource["properties"] if p["translatable"]]
        resource["properties"] = p_translatable
    
    for resource in metadata_resources["schemas"]:
        if not resource["metadata"]:  # Skip if it is not metadata (filter in /schemas endpoint is not working) 
            continue
        resource_type = resource["collectionName"]
        
        if (resource["properties"]):  # if there is at least one property translatable
            p_translatable = [r["name"].upper() for r in resource["properties"]]
            rs = utils.get_resources_from_online(credentials=credentials, resource_type=resource_type, fields="id,name,translations", param_filter="filter=translations.locale:!null")
            if rs[resource_type]:
                find_duplicated_translations(rs, resource_type, p_translatable)
