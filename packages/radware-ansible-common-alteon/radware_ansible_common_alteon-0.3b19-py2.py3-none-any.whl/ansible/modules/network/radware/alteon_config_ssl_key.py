#!/usr/bin/python
#
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
import traceback

from ansible.module_utils.network.radware.common import RadwareModuleError
from ansible.module_utils.network.radware.alteon import AlteonConfigurationModule, \
    AlteonConfigurationArgumentSpec as ArgumentSpec
from radware.alteon.sdk.configurators.ssl_key import SSLKeyConfigurator

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
module: alteon_config_ssl_key
short_description: Manage SSL key in Radware Alteon
description:
  - Manage SSL key in Radware Alteon
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
    - deploy
    - update
    - read
    - delete
  revert_on_error:
    description:
      - If an error occurs, perform revert on alteon.
    required: false
    default: false
    type: bool
  write_on_change:
    description:
      - Executes Alteon write calls only when an actual change has been evaluated.
    required: false
    default: false
    type: bool
  differential_update:
    description:
      - Executes appended changes only, ignore attributes equal to existing.
      - Useful to prevent errors due to conflicts with existing configuration entries.  
      - Applicable only when command=update.
    required: false
    default: false
    type: bool
  parameters:
    description:
      - Parameters for SSL key configuration.
    suboptions:
      index:
        description:
          - An identifier for a key.
        required: true
        default: null
        type: str
      description:
        description:
          - An optional descriptive name of the server certificate in addition to the certificate ID.
        required: false
        default: null
        type: str
      passphrase:
        description:
          - The passphrase that decrypts the private key.
        required: false
        default: null
        type: str
      content:
        description:
          - The key string.
        required: false
        default: null
        type: str
notes:
  - Requires Radware alteon Python SDK.
requirements:
  - Radware alteon Python SDK.
'''

EXAMPLES = r'''
- name: alteon configuration command
  alteon_config_ssl_key:
    provider: 
      server: 192.168.1.1
      user: admin
      password: admin
      validate_certs: no
      https_port: 443
      ssh_port: 22
      timeout: 5
    command: deploy
    parameters:
      index: test_cert
      passphrase: password
      description: test_cert_desc_2
      content: |
        -----BEGIN RSA PRIVATE KEY-----
        MIIEpAIBAAKCAQEAtW7MWRnXbIlgnPLLWXgNpBLfBzD3rYMT/3o1XlGy6LrqjWsO
        6OTDhBcHT0uPRbOCWUDPnJbAwcIRKQUS3A7qhzGPtsmQCZUcD5W+lruzjQjIkX6G
        RiGWJBMXtHnl+BHY1k1OY70Nr2olXdKO/2T2f8IdWjg4hLfNaFnX8Ga7oJy+dqVq
        5HIu1rNfAbiFyGudKdhmgFi1CLR/gQm+uu2R9aBFlrJrz9Yt2uay82bcT/wkMnjU
        ERxw1Hr9FM02qdylfsKP24pXnoKvuRL1NYWsDsiWf39KdCu1k8bWeHyrqrTeMSBK
        yaEB1Bb5SSohqIhWU+LekqOk0flUgbB2x7AMGwIDAQABAoIBAQCnbW3KM5ymnke3
        zh51m+IKrRd/jWKijjmgIuio93/AYO0eP9Nse98pQA8Qz8uRKMx7DOIJwNx0cWBg
        mDwFMwaeZ9AVgAAZt65De457jw9scNSV30qN4WSqOaxAcdUUjXOqn4BdbhL48100
        LaCkckk/MKThoswVPYCicXZidItk9HJqLGxSSM/PXoBnIq+QrZG4Kg3oAXalxzhE
        j20b8Q7sQGWH939i+rvZav9K4RUMJGc6cq8367qKDoQdJTMkTYaFxa96mbHNJ1cR
        2CnFLPgfybBi9XRZpqgjdqSrdvsoYMMu4xj7KOJpZqe6BqUnxG0rGPbg/tv3/epT
        02FuQWwBAoGBAOGK9d3bXYnyLoOXZSFCH0Ho16t5AxGZDY+8h/WUKlSfYG8zsE+U
        WXMj5+mWThXxMS7+vZ+uv3zPtnByEiQtVtX3Hcqf1jxH66NioV2M9ifTN1IEXl6I
        8ZRSq3UoMNgQOEBrlIlHHxG2v7Xh1pwEsq4phv6Av6/aW45Pz8/PvVkBAoGBAM3u
        8zVM6+W7bJpw8QQeJWc5zsxoq2UluFVzy2O7lXPRXPpbVXODf2Ar59Uhu31Ucyb8
        gjazidq03ucnhWfd9CsiPQQD2V820jlLhHs/7XT9qmkThhMt0MOsAJ5v2ZxS7MqK
        b5cnY8jFvWQYkzKLqGTwmqIMiFxBhiUBYtxY9qkbAoGASLGkKzyf+m0vZsRuGPkZ
        4AFvOdpIDez5vQE0BQgbWKkByPWs9wlGh2DkR5plUpcplg8PCR+molDEaZuqkzR1
        z4LVfFBmGYnIviF1BxT+5bkjFHFKBUg4LOk0UA+DJrCboM/L0S82KVxwj+vZYvH0
        sUO7Od4/aiuD5Ot+fGlliwECgYEAgUGdF/RrEGwek6WWMb52PZ90JKsCAV+2nrQq
        kjPYb7SWhnGzZejAl22XexhMJTNPf8X4OTthqIvkaPROcM5IhpZb89wyoOe49ctn
        oTCT692YC5H8kqcsJNUeIlQUI2GNTOeteRN5NzieUmh2Y8By9sBqXpI9OKLL/wgq
        tCGG2McCgYAL3wc+nLqx65asW8W2GRClhTHb8PApT5R8Z4J/cD2ys+MbVitulTe0
        IZj20NisAhAxSamSDEId247LTUVtvcefFEg739Euy+mhAZKrFe48A8Wpn1n/3Izx
        oHbu2FdTsZGGWFG+x29DGGeLyXeKpSucAmA6mdYhPKpD9XRdGKCVfg==
        -----END RSA PRIVATE KEY-----
'''

RETURN = r'''
result:
  description: Message detailing run result
  returned: success
  type: str
  sample: test_cert deployed successfully
'''


class ModuleManager(AlteonConfigurationModule):
    def __init__(self, **kwargs):
        super(ModuleManager, self).__init__(SSLKeyConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(SSLKeyConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()
