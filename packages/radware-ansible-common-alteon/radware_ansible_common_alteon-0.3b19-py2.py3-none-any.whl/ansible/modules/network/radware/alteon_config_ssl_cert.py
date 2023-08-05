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
from radware.alteon.sdk.configurators.ssl_cert import SSLCertConfigurator

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'certified'}

DOCUMENTATION = r'''
module: alteon_config_ssl_cert
short_description: Manage SSL certificates in Radware Alteon
description:
  - Manage SSL certificates in Radware Alteon
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
      - Parameters for SSL certificate configuration.
    suboptions:
      index:
        description:
          - An identifier for a certificate.
        required: true
        default: null
        type: str
      certificate_type:
        description:
          - Certificate type.
        required: true
        default: null
        choices:
        - serverCertificate
        - trustedCertificate
        - intermediateCertificate
      description:
        description:
          - An optional descriptive name of the server certificate in addition to the certificate ID.
        required: false
        default: null
        type: str
      intermediate_ca_name:
        description:
          - The intermediate CA certificate.
        required: false
        default: null
        type: str
      intermediate_ca_type:
        description:
          - Specifies whether an Intermediate CA certificate or certificate chain (group) must be sent to the client together with the server certificate to construct the trust chain to the user's trusted CAs.
        required: false
        default: null
        choices:
        - group
        - cert
      content:
        description:
          - The certificate string.
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
  alteon_config_ssl_cert:
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
      certificate_type: serverCertificate
      description: test_cert_desc_2
      content: |
        -----BEGIN CERTIFICATE-----
        MIIDbzCCAlegAwIBAgIEVq+/eDANBgkqhkiG9w0BAQsFADAUMRIwEAYDVQQDDAli
        bG9vbWJlcmcwHhcNMTYwMjAxMjAyNjMyWhcNMjYwMTI5MjAyNjMyWjAUMRIwEAYD
        VQQDDAlibG9vbWJlcmcwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC1
        bsxZGddsiWCc8stZeA2kEt8HMPetgxP/ejVeUbLouuqNaw7o5MOEFwdPS49Fs4JZ
        QM+clsDBwhEpBRLcDuqHMY+2yZAJlRwPlb6Wu7ONCMiRfoZGIZYkExe0eeX4EdjW
        TU5jvQ2vaiVd0o7/ZPZ/wh1aODiEt81oWdfwZrugnL52pWrkci7Ws18BuIXIa50p
        2GaAWLUItH+BCb667ZH1oEWWsmvP1i3a5rLzZtxP/CQyeNQRHHDUev0UzTap3KV+
        wo/bileegq+5EvU1hawOyJZ/f0p0K7WTxtZ4fKuqtN4xIErJoQHUFvlJKiGoiFZT
        4t6So6TR+VSBsHbHsAwbAgMBAAGjgcgwgcUwDwYDVR0TAQH/BAUwAwEB/zARBglg
        hkgBhvhCAQEEBAMCAkQwMgYJYIZIAYb4QgENBCUWI0FsdGVvbi9Ob3J0ZWwgR2Vu
        ZXJhdGVkIENlcnRpZmljYXRlMB0GA1UdDgQWBBRpp51IPQltMXMnr/8I5s9eynB6
        SjA/BgNVHSMEODA2gBRpp51IPQltMXMnr/8I5s9eynB6SqEYpBYwFDESMBAGA1UE
        AwwJYmxvb21iZXJnggRWr794MAsGA1UdDwQEAwIC7DANBgkqhkiG9w0BAQsFAAOC
        AQEApmewYCbgyZm1heODA1LRcxtlV/Y9FOMtJhaSsx0PBw7xviVermB8JOneZ8Nl
        TeTWR8u87MhxE5wuPJqplRvU1fGrffL4C2IhTkWyHfMK/uD/TDbvxW8CCV95noq1
        fqcTvnnx1SV/KvxD5Ykobg0X3ZtQYMNeB3Ea2lrDse9/FKUkpVAh/337PD2WvLzq
        bx/2o5ow1dCzcb+r/3rFNtVdxg3u9JFw/LY9W40XjXiTeWf7DlCR24mfEBv6Xsqc
        /kz74+YOTTWkogvkNNWHHYZWppeiB6tGYtj47alSSiuhTJ66Xm5yCaeZoy7IJv4g
        KilcwHHsCGVc1YWYixA1zcCqwQ==
        -----END CERTIFICATE-----
'''

RETURN = r'''
result:
  description: Message detailing run result
  returned: success
  type: str
  sample: test_cert ,EnumSlbSslCertsType.serverCertificate deployed successfully
'''


class ModuleManager(AlteonConfigurationModule):
    def __init__(self, **kwargs):
        super(ModuleManager, self).__init__(SSLCertConfigurator, **kwargs)


def main():
    spec = ArgumentSpec(SSLCertConfigurator)
    module = AnsibleModule(argument_spec=spec.argument_spec, supports_check_mode=spec.supports_check_mode)

    try:
        mm = ModuleManager(module=module)
        result = mm.exec_module()
        module.exit_json(**result)
    except RadwareModuleError as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())


if __name__ == '__main__':
    main()