#!/usr/bin/python
#
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import traceback

from ansible.module_utils.network.radware.common import RadwareModuleError
from ansible.module_utils.network.radware.common import AnsibleRadwareParameters
from ansible.module_utils.network.radware.alteon import AlteonManagementArgumentSpec, AlteonManagementModule
from radware.alteon.sdk.alteon_managment import AlteonMngOper


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
module: alteon_mng_oper
short_description: Perform opertional commands in Radware Alteon
description:
  - Perform opertional commands in Radware Alteon.
version_added: null
author: 
  - Leon Meguira (@leonmeguira)
  - Nati Fridman (@natifridman)
options:
  provider:
    description:
      - Radware Alteon connection details.
    required: true
    suboptions:
      server:
        description:
          - Radware Alteon IP.
        required: true
        default: null
      user:
        description:
          - Radware Alteon username.
        required: true
        default: null
      password:
        description:
          - Radware Alteon password.
        required: true
        default: null
      validate_certs:
        description:
          - If C(no), SSL certificates will not be validated.
          - This should only set to C(no) used on personally controlled sites using self-signed certificates.
        required: true
        default: null
        type: bool
      https_port:
        description:
          - Radware Alteon https port.
        required: true
        default: null
      ssh_port:
        description:
          - Radware Alteon ssh port.
        required: true
        default: null
      timeout:
        description:
          - Timeout for connection.
        required: true
        default: null
  command:
    description:
      - Action to run.
    required: true
    default: null
    choices:
    - reboot
    - reboot_stateful
notes:
  - Requires Radware alteon Python SDK.
requirements:
  - Radware alteon Python SDK.
'''

EXAMPLES = r'''
- name: alteon configuration command
  alteon_mng_oper:
    provider: 
      server: 192.168.1.1
      user: admin
      password: admin
      validate_certs: no
      https_port: 443
      ssh_port: 22
      timeout: 5
    command: reboot
'''

RETURN = r'''
result:
  description: Message detailing run result
  returned: success
  type: str
  sample: Device Reset
'''


class ArgumentSpec(AlteonManagementArgumentSpec):
    def __init__(self, mng_class):
        super(ArgumentSpec, self).__init__(mng_class)
        argument_spec = dict(
            timeout=dict(
                required=False,
                type='int'
            ),
            fail_on_pending_cfg=dict(
                required=False,
                type='bool',
                default=False
            )
        )
        self.argument_spec.update(argument_spec)


class Parameters(AnsibleRadwareParameters):
    def __init__(self, params):
        super(Parameters, self).__init__(**params)

    @property
    def command(self):
        return self._params['command']

    @property
    def timeout(self):
        if 'timeout' in self._params:
            return self._params['timeout']

    @property
    def fail_on_pending_cfg(self):
        return self._params['fail_on_pending_cfg']


class ModuleManager(AlteonManagementModule):
    def __init__(self, **kwargs):
        super(ModuleManager, self).__init__(Parameters, **kwargs)

    def execute(self):

        if self.arguments.fail_on_pending_cfg:
            self._mng.config.pending_configuration_validation()

        if self.arguments.command == AlteonMngOper.REBOOT:
            return self._mng.reboot()
        elif self.arguments.command == AlteonMngOper.REBOOT_STATEFUL:
            if self.arguments.timeout:
                return self._mng.reboot_stateful(self.arguments.timeout)
            else:
                return self._mng.oper.reboot_stateful()

        func = getattr(self._mng.oper, self.arguments.command)
        if callable(func):
            return func()
        else:
            return func


def main():
    spec = ArgumentSpec(AlteonMngOper)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
