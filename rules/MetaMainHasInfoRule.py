from ansiblelint import AnsibleLintRule


class MetaMainHasInfoRule(AnsibleLintRule):
    id = '701'
    shortdesc = 'meta/main.yml should contain relevant info'
    info = ['author', 'description', 'company',
            'license', 'min_ansible_version', 'platforms']
    description = 'meta/main.yml should contain: ' + ', '.join(info)
    tags = ['metadata']

    def matchplay(self, file, data):
        if file['type'] != 'meta':
            return False

        galaxy_info = data.get('galaxy_info', None)
        if not galaxy_info:
            return [({'meta/main.yml': data},
                    "No 'galaxy_info' found")]

        results = []
        for info in self.info:
            if not galaxy_info.get(info, None):
                results.append(({'meta/main.yml': data},
                                'Role info should contain %s' % info))

        platforms = galaxy_info.get('platforms', None)
        if platforms:
            for platform in platforms:
                if not platform.get('name', None):
                    results.append(({'meta/main.yml': data},
                                    'Platform should contain name'))

        return results
