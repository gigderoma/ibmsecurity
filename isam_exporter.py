import logging.config
import pprint
from ibmsecurity.appliance.isamappliance import ISAMAppliance
from ibmsecurity.user.applianceuser import ApplianceUser
import pkgutil
import importlib
import os
import sys
import requests
import time
import json
import prometheus_client
from prometheus_client import start_http_server, Metric, REGISTRY


def import_submodules(package, recursive=True):
    """
    Import all submodules of a module, recursively, including subpackages
    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


import ibmsecurity

# Import all packages within ibmsecurity - recursively
# Note: Advisable to replace this code with specific imports for production code
import_submodules(ibmsecurity)

# Setup logging to send to stdout, format and set log level
# logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig()
# Valid values are 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'
logLevel = 'DEBUG'
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': logLevel,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'level': logLevel,
            'handlers': ['default'],
            'propagate': True
        },
        'requests.packages.urllib3.connectionpool': {
            'level': 'ERROR',
            'handlers': ['default'],
            'propagate': True
        }
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)


# Function to pretty print JSON data
def p(jdata):
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(jdata)
	
	
	
	
	
	
class JsonCollector(object):
    def __init__(self):
        pass

    def collect(self):
        #Get the Json from ISAM api
			
			
		# Create a user credential for ISAM appliance
        u = ApplianceUser(username="admin@local", password="admin")
        # Create an ISAM appliance with above credential
        isam_server = ISAMAppliance(hostname="192.168.198.100", user=u, lmi_port=443)

        # Get the current SNMP monitoring setup details
        p(ibmsecurity.isam.base.snmp_monitoring.get(isamAppliance=isam_server))
        # Set the V2 SNMP monitoring
        p(ibmsecurity.isam.base.snmp_monitoring.set_v1v2(isamAppliance=isam_server, community="IBM"))
			
		p(ibmsecurity.isam.web.reverse_proxy.get_all(isamAppliance=isam_server,instance_id="base"))
        

        
        
        r = ibmsecurity.isam.web.reverse_proxy.get_all(isamAppliance=isam_server,instance_id="base")
        metric = Metric('jobs_running', 'Current Jobs Running', 'gauge')
        metric.add_sample('jobs_running', value=float(len(r.json())), labels={})
        yield metric

        status = 'failed'
       
        metric = Metric('jobs_failed', 'Number of failed jobs', 'gauge')
        metric.add_sample('jobs_failed', value=float(len(r.json())), labels={})
        yield metric

        status = 'succeeded'
        
        metric = Metric('jobs_succeeded', 'Number of failed jobs', 'gauge')
        metric.add_sample('jobs_succeeded', value=float(len(r.json())), labels={})
        yield metric
	
	
	

if __name__ == "__main__":
    start_http_server(8000)
    REGISTRY.register(JsonCollector())
    while True: time.sleep(1)
