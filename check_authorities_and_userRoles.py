import utils
import os


def flatten(l):
    return [item for sublist in l for item in sublist]

def main():
    credentials = utils.get_credentials()
    check_name = os.path.basename(__file__).replace(".py", "")
    logger = utils.get_logger(credentials, check_name)


    # Only since version 2.37
 
    dhis2_version = utils.get_dhis2_version(credentials)
    dhis2_version_detail = int(dhis2_version.split(".")[1])
 
    if dhis2_version_detail < 37:
        logger.info(f"Skip authorities & userRoles validation because the dhis2 version instance is lower than 2.37 ({dhis2_version})")
        return

    ############################################################################

    # UserRoles without any authority associated
    userRoles_without_authorities = utils.get_resources_from_online(credentials=credentials, resource_type="userRoles", fields="id,name", param_filter="filter=authorities:eq:0")
    if userRoles_without_authorities["userRoles"]:
        message = f'{len(userRoles_without_authorities["userRoles"])} User Roles do not have assigned any authority: {userRoles_without_authorities["userRoles"]}'
        logger.warning(message)

    
    authorities = utils.get_resource_from_online(credentials=credentials, resource_type="authorities", resource_uid="", fields="id,name")  # Hacked this call. Sending empty resource id because the response is not matching the resource type name (authorities vs systemAuthorities)
    userRoles = utils.get_resources_from_online(credentials=credentials, resource_type="userRoles", fields="id,name,authorities", param_filter="filter=authorities:gt:0")

    authorities_uid = [i["id"] for i in authorities["systemAuthorities"]]
    authorities_in_roles_uid = flatten([ra["authorities"] for ra in userRoles["userRoles"]])


    # Determining which authorities are declared but they are not used by any User Role
    authorities_not_used = [au for au in authorities_uid if au not in authorities_in_roles_uid].sort()  # sorted alphabetically
    if authorities_not_used:
        message = f"{len(authorities_not_used)} authorities are declared but they are not used by any UserRole: {authorities_not_used}"
        logger.info(message)

    # Determining which authorities are present in the userRoles but not declared as authorities
    authorities_not_declared = sorted(set([au for au in authorities_in_roles_uid if au not in authorities_uid])) # sorted alphabetically


    if authorities_not_declared:
        message = f"{len(authorities_not_declared)} authorities are present in the userRoles but they not declared in systemAuthorities"
        logger.warning(message)

        for rar in userRoles["userRoles"]:
            for a in rar["authorities"]:
                if a not in authorities_uid:
                    message = f"In userRole '{rar['name']}', the Authority '{a}' is present but it is not declared in systemAuthorities"
                    logger.warning(message)


if __name__ == "__main__":
    main()

