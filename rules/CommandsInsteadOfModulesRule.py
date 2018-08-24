# Copyright (c) 2018 Ansible, Inc.
# All Rights Reserved.

import os

from ansiblelint import AnsibleLintRule
try:
    from ansible.module_utils.parsing.convert_bool import boolean
except ImportError:
    try:
        from ansible.utils.boolean import boolean
    except ImportError:
        try:
            from ansible.utils import boolean
        except ImportError:
            from ansible import constants
            boolean = constants.mk_boolean


class CommandsInsteadOfModulesRule(AnsibleLintRule):
    id = 'GALAXYTEST301'
    shortdesc = 'Using command rather than module'
    description = 'Executing a command when there is an Ansible module ' + \
                  'is generally a bad idea'
    # tags = ['resources']
    tags = ['command-shell']

    _commands = ['command', 'shell']
    _modules = {'git': 'git', 'hg': 'hg',
                'curl': 'get_url or uri', 'wget': 'get_url or uri',
                'svn': 'subversion', 'service': 'service', 'mount': 'mount',
                'rpm': 'yum or rpm_key', 'yum': 'yum', 'apt-get': 'apt-get',
                'unzip': 'unarchive', 'tar': 'unarchive',
                'chkconfig': 'service', 'rsync': 'synchronize',
                'supervisorctl': 'supervisorctl', 'systemctl': 'systemd',
                'sed': 'template or lineinfile'}

    def matchtask(self, file, task):
        if task["action"]["__ansible_module__"] in self._commands:
            if 'cmd' in task['action']:
                first_cmd_arg = task['action']['cmd'].split()[0]
            else:
                first_cmd_arg = task["action"]["__ansible_arguments__"][0]
            if not first_cmd_arg:
                return
            executable = os.path.basename(first_cmd_arg)
            if executable in self._modules and \
                    boolean(task['action'].get('warn', True)):
                message = "{0} used in place of {1} module"
                return message.format(executable, self._modules[executable])