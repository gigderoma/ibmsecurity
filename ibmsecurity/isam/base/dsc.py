import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)

uri = "/isam/dsc/config"
requires_modules = None
requires_version = None


def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieve the current distributed session cache policy
    """
    return isamAppliance.invoke_get("Retrieve the current distributed session cache policy", uri,
                                    requires_modules=requires_modules, requires_version=requires_version)


def set(isamAppliance, service_port=443, replication_port=444, worker_threads=64, max_session_lifetime=3600,
        client_grace=600, servers=None, check_mode=False, force=False):
    """
    Update the current distributed session cache policy
    """
    warnings = []
    # Create a simple json with just the main client attributes
    dsc_json = {
        "worker_threads": worker_threads,
        "max_session_lifetime": max_session_lifetime,
        "client_grace": client_grace,
        "service_port": service_port,
        "replication_port": replication_port
    }
    if servers is not None:
        dsc_json["servers"] = servers

    if force is True or _check(isamAppliance, dsc_json) is False:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True, warnings=warnings)
        else:
            return isamAppliance.invoke_put("Update the current distributed session cache policy", uri, dsc_json,
                                            requires_modules=requires_modules, requires_version=requires_version,
                                            warnings=warnings)

    return isamAppliance.create_return_object(warnings=warnings)


def _check(isamAppliance, cluster_json, ignore_password_for_idempotency):
    """
    Check if provided json values match the configuration on appliance

    :param isamAppliance:
    :param cluster_json:
    :return:
    """
    ret_obj = get(isamAppliance)
    sorted_ret_obj = tools.json_sort(ret_obj['data'])
    sorted_json_data = tools.json_sort(cluster_json)
    logger.debug("Sorted Existing Data:{0}".format(sorted_ret_obj))
    logger.debug("Sorted Desired  Data:{0}".format(sorted_json_data))

    if sorted_ret_obj != sorted_json_data:
        logger.info("Existing and input data do not match - updated needed.")
        return False
    else:
        return True


def compare(isamAppliance1, isamAppliance2):
    """
    Compare DSC configuration between two appliances
    """
    ret_obj1 = get(isamAppliance1)
    ret_obj2 = get(isamAppliance2)

    return tools.json_compare(ret_obj1, ret_obj2, deleted_keys=[])
