import json
from dataclasses import dataclass
from typing import Dict, Optional

from zabier.zabbix.base import ZabbixBase


@dataclass
class Host:
    hostid: Optional[str]
    name: str


class HostMixin(ZabbixBase):
    def get_host_by_name(self, name: str) -> Optional[Host]:
        response: Dict = self.do_request(
            'host.get',
            {
                'filter': {
                    'name': [name]
                },
                'editable': True,
                'startSearch': True,
                'searchByAny': True
            }
        )
        if len(response['result']) == 0:
            return None
        host = response['result'].pop()
        return Host(hostid=host['hostid'], name=host['name'])

    def import_host_configuration(self,
                                  config: Dict,
                                  append_only: bool) -> bool:
        rules = {
            'hosts': {
                'createMissing': True,
                'updateExisting': True
            },
            'applications': {
                'createMissing': True,
                'updateExisting': True,
                'deleteMissing': True
            },
            'discoveryRules': {
                'createMissing': True,
                'updateExisting': True,
                'deleteMissing': True
            },
            'graphs': {
                'createMissing': True,
                'updateExisting': True,
                'deleteMissing': True
            },
            'items': {
                'createMissing': True,
                'updateExisting': True,
                'deleteMissing': True
            },
            'templateLinkage': {
                'createMissing': True
            },
            'templateScreens': {
                'createMissing': True,
                'updateExisting': True,
                'deleteMissing': True
            },
            'triggers': {
                'createMissing': True,
                'updateExisting': True,
                'deleteMissing': True
            },
            'valueMaps': {
                'createMissing': True,
                'updateExisting': True
            }
        }
        if append_only:
            rules = {
                'hosts': {
                    'createMissing': True
                },
                'applications': {
                    'createMissing': True
                },
                'discoveryRules': {
                    'createMissing': True
                },
                'graphs': {
                    'createMissing': True
                },
                'items': {
                    'createMissing': True
                },
                'templateLinkage': {
                    'createMissing': True
                },
                'templateScreens': {
                    'createMissing': True
                },
                'triggers': {
                    'createMissing': True
                },
                'valueMaps': {
                    'createMissing': True
                }
            }
        response: Dict = self.do_request(
            'configuration.import',
            {
                'format': 'json',
                'rules': rules,
                'source': json.dumps(config)
            }
        )
        return response['result']

    def export_host_configuration(self, host_id: str) -> bool:
        response: Dict = self.do_request(
            'configuration.export',
            {
                'format': 'json',
                'options': {
                    'hosts': [host_id]
                }
            }
        )
        return response['result']
