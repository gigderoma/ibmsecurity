import logging
from ibmsecurity.utilities import tools

logger = logging.getLogger(__name__)


def run(isamAppliance, application_interface, statistics_duration, check_mode=False, force=False):
    """
    Retrieving the Application Interface Statistics
    """
    return isamAppliance.invoke_get("Run pdadmin command",
                                    "/analysis/interface_statistics.json{0}".format(
                                        tools.create_query_string(prefix=application_interface,
timespan=statistics_duration)))
