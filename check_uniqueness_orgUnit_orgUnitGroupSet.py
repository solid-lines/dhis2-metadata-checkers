#!/usr/bin/python
# -*- coding: UTF-8 -*-

import utils
import os


# A key property of the group set concept in DHIS2 to understand is exclusivity, which implies that an organisation unit can be member of exactly one of the groups in a group set. A violation of this rule would lead to duplication of data when aggregating health facility data by the different groups, as a facility assigned to two groups in the same group set would be counted twice.
# https://docs.dhis2.org/en/implement/understanding-dhis2-implementation/organisation-units.html#organisation-unit-groups-and-group-sets

if __name__ == "__main__":

    credentials = utils.get_credentials()    
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)
    
    server_url = credentials["server"]
    
    ############################################################################

    OUG_SET = "organisationUnitGroupSets"
    OU_GROUP = "organisationUnitGroups"
    OU = "organisationUnits"

    #retrieve all metadata_resources
    metadata_resources = utils.get_resources_from_online(credentials=credentials, resource_type=OUG_SET, fields="id,name,organisationUnitGroups[*]")

    for oug_set in metadata_resources[OUG_SET]:
        
        names = {}
        ous_in_oug_set = []
        ous_by_oug = {}
        
        if not oug_set[OU_GROUP]: #if empty
            continue

        for ougroup in oug_set[OU_GROUP]:
            org_group = utils.get_resource_from_online(credentials=credentials, resource_type=OU_GROUP, resource_uid=ougroup["id"], fields="id,name,organisationUnits[id, name]")
            names[org_group["id"]] = org_group["name"]            
            org_units_in_this_ougroup = [ou["id"] for ou in org_group[OU]]
            
            for ou in org_group[OU]:
                names[ou["id"]] = ou["name"]
            
            ous_by_oug[ougroup["id"]] = org_units_in_this_ougroup
            
            ous_in_oug_set = ous_in_oug_set + org_units_in_this_ougroup 
        
        duplicates = {x for x in ous_in_oug_set if ous_in_oug_set.count(x) > 1}
        
        if duplicates:
            logger.error(f"OU Group SET {oug_set['name']} ({oug_set['id']})")
            for oug, ous in ous_by_oug.items():
                for dup in duplicates:
                    if dup in ous:
                        logger.error(f"check OU Group {names[oug]} ({oug}) and OU {names[dup]} ({dup}))")
            logger.error("-----------------------------------")
