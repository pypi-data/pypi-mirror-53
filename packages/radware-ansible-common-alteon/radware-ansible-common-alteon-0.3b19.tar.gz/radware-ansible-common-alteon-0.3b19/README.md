[![PyPI version](https://img.shields.io/pypi/v/ansible.svg)](https://pypi.python.org/pypi/ansible)


Introduction
=====================

Ansible Alteon modules and Radware common module_utils.
these modules and module infrastructure consume services from the SDK, thus it must be installed prior running them
Argument specification is a construct generate during runtime from the relevant SDK Configurator metadata,
multi-choice values are directly dynamically accesses from SDK beans, therefor any update in SDK become available to the
ansible module right after updating the SDK.
this is useful for when a new attribute is introduced or a new value to current attribute
 
all modules support Check Mode + diff display and Idempotency.
furthermore they utilize two usable features from the SDK:

- write on change: 
    - Executes Alteon write calls only when an actual change has been evaluated.
- differential update: 
    - Executes appended changes only, ignore attributes equal to existing.
    - Useful to prevent errors due to conflicts with existing configuration entries.  
    - Applicable only when command=update.

both features handles partial match, normalization and prevent unnecessary update 
    
Installation
=================

```pycon
pip install radware-ansible-common-alteon
```

Design Principles
=================

-	44 modules: some indexed & others are a summary  
-	3 management modules: info, operation, config
-	3 common modules: interfacing with SDK mng & config & common
-	The module execute configurator functions from the SDK
-	Check mode (dry_run) + diff display is supported on all modules
-	Idempotency: Change/ no change report + write on changes only (differential and write_on_change)
-	Revert_on_error
-	Exception handling: SDK stacktrace copy, warn user about supported version (from SDK)
-	Argument specification construct in runtime from SDK configurator:
        -	a construct of SDK metadata: not restricted to Ansible
        -	single point of change 
        -	choices (Enum) derive from SDK bean sub-package
        -	directly become available to users after updating the SDK 

Authors
=======

Ansible Common & Alteon was created by [Leon Meguira](https://https://github.com/leonmeguira)

Copyright
=======

Copyright 2019 Radware LTD

License
=======
GNU General Public License v3.0

See [COPYING](COPYING) to see the full text.

