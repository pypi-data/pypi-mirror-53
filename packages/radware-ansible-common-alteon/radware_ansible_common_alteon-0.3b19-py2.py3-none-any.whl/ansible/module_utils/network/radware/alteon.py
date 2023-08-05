#!/usr/bin/python
#
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from future.utils import raise_with_traceback
__metaclass__ = type

from abc import abstractmethod
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.radware.configuration import ConfigurationArgumentSpec, ConfigurationModule
from ansible.module_utils.network.radware.common import RadwareBaseModule, RadwareModuleError, \
    radware_adc_argument_spec
try:
    from radware.alteon.api.mgmt import AlteonManagement
    from radware.alteon.api import AlteonDeviceConnection
    from radware.sdk.exceptions import RadwareError
    from radware.alteon import __minimum_supported_version__
except ModuleNotFoundError:
    AnsibleModule(argument_spec={}, check_invalid_arguments=False).fail_json(
        msg="The alteon-sdk package is required")


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
module: Alteon Management and Configuration module
author:
  - Leon Meguira (@leonmeguira)
'''


class AlteonManagementArgumentSpec(object):
    def __init__(self, mng_class):
        self.supports_check_mode = False
        argument_spec = dict(
            command=dict(
                required=True,
                choices=mng_class.api_function_names()
            )
        )
        self.argument_spec = {}
        self.argument_spec.update(radware_adc_argument_spec)
        self.argument_spec.update(argument_spec)


class AlteonConfigurationArgumentSpec(ConfigurationArgumentSpec):

    def __init__(self, config_class):
        super(AlteonConfigurationArgumentSpec, self).__init__(config_class)
        additional_argument_spec = dict(
            revert_on_error=dict(
                required=False,
                type='bool',
                default=False
            )
        )
        self.argument_spec.update(additional_argument_spec)


class AlteonAnsibleModule(RadwareBaseModule):
    def __init__(self, **kwargs):
        super(AlteonAnsibleModule, self).__init__(**kwargs)
        self._connection = AlteonDeviceConnection(**self.provider)
        self._mng = AlteonManagement(self._connection)


class AlteonManagementModule(AlteonAnsibleModule):
    def __init__(self, parameters_class, **kwargs):
        super(AlteonManagementModule, self).__init__(**kwargs)
        self.arguments = parameters_class(params=self.params)

    def exec_module(self):
        result = None
        try:
            self._mng.verify_device_accessible(retries=2)
            result = {}
            result.update(command=self.arguments.command, result=self.execute())
        except RadwareError as e:
            raise_with_traceback(RadwareModuleError(e))
        return result

    @abstractmethod
    def execute(self):
        pass


class AlteonConfigurationModule(AlteonAnsibleModule, ConfigurationModule):
    def __init__(self, configurator_class, **kwargs):
        AlteonAnsibleModule.__init__(self, **kwargs)
        ConfigurationModule.__init__(self, configurator_class, **kwargs)
        self._revert_on_error = self.params['revert_on_error']

    @property
    def _base(self):
        return self

    @property
    def _device_mng(self):
        return self._mng

    @property
    def _device_connection(self):
        return self._connection

    @property
    def revert_on_error(self):
        return self._revert_on_error

    def _on_error(self):
        self.module.warn('please verify your alteon is running a version >= {0}'.format(__minimum_supported_version__))
        if self._revert_on_error:
            self._mng.config.revert()

