import json
from dataclasses import asdict, dataclass
from typing import Dict, IO

import click

from dacite import from_dict

from datadiff import diff

import yaml

from zabier.zabbix import constants
from zabier.zabbix import get_client
from zabier.zabbix.action import Action
from zabier.zabbix.hostgroup import HostGroup
from zabier.zabbix.maintenance import Maintenance


def hostgroup(name: str, dry_run: bool):
    zabbix = get_client()
    if zabbix.host_group_exists(name):
        click.echo(f'Host group "{name}" is already exists.')
    else:
        hostgroup = HostGroup(groupid=None, name=name)
        if dry_run:
            click.echo(f'The new host group will be created.')
        else:
            groupid = zabbix.create_host_group(hostgroup)
            click.echo(f'Host group created. ID: {groupid}')


def action(name: str, file: str, dry_run: bool):
    zabbix = get_client()
    action = zabbix.get_action_by_name(name)
    action_def = _load_config_file(file)
    action_config = action_def.get('config', {})
    if 'auto_registration_config' in action_def:
        action_config = action_def['auto_registration_config']
        action_config = _refine_auto_registration_config(name, action_config)
    if action is None:
        new_action = from_dict(data_class=Action, data=action_config)
        if dry_run:
            click.echo(f'The new action will be created.')
        else:
            actionid = zabbix.create_action(new_action)
            click.echo(f'Action created. ID: {actionid}')
    else:
        remote_action = action
        local_action = from_dict(data_class=Action, data=action_config)
        click.echo(_diff_actions(local_action, remote_action))
        local_action.actionid = remote_action.actionid
        if not dry_run:
            actionid = zabbix.update_action(local_action)
            click.echo(f'Action updated. ID: {actionid}')


def template(name: str, file: str, dry_run: bool, export: bool):
    zabbix = get_client()
    template = zabbix.get_template_by_name(name)
    if export:
        if template is None:
            raise click.UsageError(
                f'template "{name}" is not exists.')
        config = zabbix.export_template_configuration(template.templateid)
        open(file, 'w').write(yaml.dump(json.loads(config)))
        click.echo(f'Template exported.')
    else:
        local_config = _load_config_file(file)
        if template is not None:
            remote_config = zabbix.export_template_configuration(template.templateid)
            click.echo(_diff_configs(local_config, json.loads(remote_config)))
        if not dry_run:
            zabbix.import_template_configuration(local_config)
            click.echo(f'Template imported.')


def host(name: str, file: str, dry_run: bool, export: bool, append_only: bool):
    zabbix = get_client()
    host = zabbix.get_host_by_name(name)
    if export:
        if host is None:
            raise click.UsageError(
                f'Host "{name}" is not exists.')
        config = zabbix.export_host_configuration(host.hostid)
        open(file, 'w').write(yaml.dump(json.loads(config)))
        click.echo(f'Host exported.')
    else:
        local_config = _load_config_file(file)
        if host is not None:
            remote_config = zabbix.export_host_configuration(host.hostid)
            click.echo(_diff_configs(local_config, json.loads(remote_config)))
        if not dry_run:
            zabbix.import_host_configuration(local_config, append_only)
            click.echo(f'Host imported.')


def maintenance(name: str, file: str, dry_run: bool):
    zabbix = get_client()
    remote_maintenance = zabbix.get_maintenance_by_name(name)
    local_maintenance = _load_maintenance_file(name, file)
    if remote_maintenance is None:
        if not dry_run:
            maintenanceid = zabbix.create_maintenance(local_maintenance)
            click.echo(f'Maintenance created. ID: {maintenanceid}')
    else:
        click.echo(
            _diff_maintenances(local_maintenance, remote_maintenance))
        if not dry_run:
            local_maintenance.maintenanceid = remote_maintenance.maintenanceid
            maintenanceid = zabbix.update_maintenance(local_maintenance)
            click.echo(f'Maintenance updated. ID: {maintenanceid}')


def _diff_maintenances(local: Maintenance, remote: Maintenance):
    local = asdict(local)
    remote = asdict(remote)
    del local['maintenanceid']
    del remote['maintenanceid']
    return diff(remote, local)


def _load_maintenance_file(name: str, file: IO) -> Dict:
    config = yaml.full_load(open(file)).get('maintenance_config')
    groups = []
    hosts = []
    zabbix = get_client()
    for group_name in config.get('groups', []):
        group = zabbix.get_host_group_by_name(group_name)
        if group is None:
            raise click.UsageError(
                f'Hostgroup "{group_name}" is not exists.')
        groups.append({
            'groupid': group.groupid,
            'name': group.name
        })
    for host_name in config.get('hosts', []):
        host = zabbix.get_host_by_name(host_name)
        if host is None:
            raise click.UsageError(
                f'Host "{host_name}" is not exists.')
        hosts.append({
            'hostid': host.hostid,
            'name': host.name
        })

    maintenance = Maintenance(
        maintenanceid=None,
        name=name,
        maintenance_type=config.get('maintenance_type', '0'),
        description=config.get('description', ''),
        active_since=config.get('active_since'),
        active_till=config.get('active_till'),
        groups=groups,
        hosts=hosts,
        timeperiods=config.get('timeperiods'))
    return maintenance



def _load_config_file(file: IO) -> Dict:
    return yaml.full_load(open(file))


def _diff_configs(local: Dict, remote: Dict):
    try:
        del local['zabbix_export']['date']
        del remote['zabbix_export']['date']
    except KeyError:
        pass
    return diff(remote, local)


def _diff_actions(local: dataclass, remote: dataclass):
    local = asdict(local)
    remote = asdict(remote)
    try:
        del local['actionid']
        del remote['actionid']
        del remote['filter']['eval_formula']
        for op in remote['operations']:
            del op['actionid']
            del op['operationid']
            for key in ['optemplate', 'opgroup']:
                if key in op:
                    for op2 in op[key]:
                        del op2['operationid']
    except (KeyError, TypeError):
        pass
    return diff(remote, local)


def _refine_auto_registration_config(name: str, config: Dict) -> Dict:
    zabbix = get_client()
    try:
        hostgroup_name = config['hostgroup']
        hostgroup = zabbix.get_host_group_by_name(hostgroup_name)
        if hostgroup is None:
            raise click.UsageError(f'HostGroup "{hostgroup_name}" is not exists.')

        t_names = config['templates']
        templates = []
        for t_name in t_names:
            template = zabbix.get_template_by_name(t_name)
            if template is None:
                raise click.UsageError(f'Template "{t_name}" is not exists.')
            templates.append({'templateid': str(template.templateid)})

        host_status_operationtype = constants.OPERATION_TYPE_ENABLE_HOST
        if config['disable_host']:
            host_status_operationtype = constants.OPERATION_TYPE_DISABLE_HOST

        refined_config = {
            'esc_period': '0',
            'eventsource': constants.EVENTSOURCE_AUTO_REGISTERED_HOST,
            'name': name,
            'status': config['status'],
            'operations': [
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': constants.OPERATION_TYPE_ADD_HOST
                },
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': constants.OPERATION_TYPE_ADD_TO_HOSTGROUP,
                    'opgroup': [
                        {'groupid': str(hostgroup.groupid)}
                    ]
                },
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': constants.OPERATION_TYPE_LINK_TO_TEMPLATE,
                    'optemplate': templates
                },
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': host_status_operationtype
                }
            ],
            'filter': {
                'conditions': [
                    {
                        'conditiontype': constants.CONDITION_TYPE_HOST_METADATA,
                        'value': config['hostmetadata'],
                        'operator': constants.CONDITION_OPERATOR_LIKE,
                        'formulaid': 'A'
                    }
                ],
                'evaltype': '0',
                'formula': ''
            }
        }

        return refined_config
    except KeyError as e:
        key_name = e.args[0]
        raise click.UsageError(
            f'"{key_name}" is required in "auto_registration_config".')
