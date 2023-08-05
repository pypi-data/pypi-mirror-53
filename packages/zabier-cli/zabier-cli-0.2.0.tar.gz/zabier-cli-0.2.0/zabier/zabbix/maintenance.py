from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

from dacite import from_dict

from zabier.zabbix.base import ZabbixBase


@dataclass
class Maintenance:
    maintenanceid: Optional[str]
    name: str
    maintenance_type: str
    description: str
    active_since: str
    active_till: str
    groups: List[Dict]
    hosts: List[Dict]
    timeperiods: List[Dict]


class MaintenanceMixin(ZabbixBase):
    def get_maintenance_by_name(self, name: str) -> Optional[Maintenance]:
        response: Dict = self.do_request(
            'maintenance.get',
            {
                'filter': {
                    'name': [name]
                },
                'editable': True,
                'startSearch': True,
                'searchByAny': True,
                'selectGroups': 'extend',
                'selectHosts': 'extend',
                'selectTimeperiods': 'extend'
            }
        )
        if len(response['result']) == 0:
            return None
        maintenance = response['result'].pop()
        groups = []
        hosts = []
        for group in maintenance['groups']:
            groups.append({
                'groupid': group['groupid'],
                'name': group['name']})
        for host in maintenance['hosts']:
            hosts.append({
                'hostid': host['hostid'],
                'name': host['name']})
        maintenance['groups'] = groups
        maintenance['hosts'] = hosts
        return from_dict(data_class=Maintenance, data=maintenance)

    def create_maintenance(self, maintenance: Maintenance) -> int:
        maintenance_dict = self._maintenance_to_api_dict(maintenance)
        del maintenance_dict['maintenanceid']
        response: Dict = self.do_request(
            'maintenance.create',
            maintenance_dict)
        return response['result']['maintenanceids'].pop()

    def update_maintenance(self, maintenance: Maintenance) -> int:
        maintenance_dict = self._maintenance_to_api_dict(maintenance)
        response: Dict = self.do_request(
            'maintenance.update',
            maintenance_dict)
        return response['result']['maintenanceids'].pop()

    def _maintenance_to_api_dict(self, maintenance: Maintenance) -> Dict:
        maintenance_dict = asdict(maintenance)
        groupids = []
        hostids = []
        for group in maintenance_dict.get('groups', []):
            groupids.append(group['groupid'])
        for host in maintenance_dict.get('hosts', []):
            hostids.append(host['hostid'])
        del maintenance_dict['groups']
        del maintenance_dict['hosts']
        maintenance_dict['groupids'] = groupids
        maintenance_dict['hostids'] = hostids
        return maintenance_dict
