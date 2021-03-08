# IBM-DataStage-API
[![PyPi Version](https://img.shields.io/pypi/v/IBM-DataStage-API.svg)](https://pypi.python.org/pypi/IBM-DataStage-API)
![Python versions](https://img.shields.io/pypi/pyversions/IBM-DataStage-API.svg)

IBM-DataStage-API on Python.
Please read [InfoSphere DataStage Development Kit](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.ds.cliapi.ref.doc/topics/r_dsvjbref_WebSphere_DataStage_Development_Kit.html) to find details.

## Requirements

For the correct work `ctypes` with DataStage API library (32-bit or 64-bit) you need Python of the same version (32-bit or 64-bit)

`PATH` on Windows should include a directory where file `vmdsapi.dll` is located.  
In most cases, in the `../IBM/InformationServer/Clients/Classic/`

`LD_LIBRARY_PATH` on \*nix should include a directory where file `libvmdsapi.so` and its dependencies are located.  
In most cases, in the `../IBM/InformationServer/Server/DSEngine/lib/`

Also activation of [dsenv](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.productization.iisinfsv.install.doc/topics/wsisinst_dsenv_file.html) can help you  
`cd ../IBM/InformationServer/Server/DSEngine/`  
`. ./dsenv`

## Installation
```
pip install IBM-DataStage-API
```

## Getting Started

Create your own `config.py` with path to DataStage API library (`vmdsapi.dll` on a client or `libvmdsapi.so` on a server) and configure connection's parameters.

There are two types of setting login parameters

1. Using operating system user credentials of [Engine tier](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.productization.iisinfsv.overview.arch.doc/topics/wsisinst_arch_engine_layer.html), by default, `dsadm`
```
+: fast work
-: doesn't support admin functions (DSAddProject, DSSetProjectProperty...)

DS_DOMAIN_NAME = ''
DS_USER_NAME   = 'dsadm'
DS_PASSWORD    = 'dsadm_password'
DS_SERVER      = 'HOST_NAME:ENGINE_TIER_PORT'
```

2. Using user credentials of [Services tier](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.productization.iisinfsv.overview.arch.doc/topics/wsisinst_arch_domain_layer.html)
```
+: support admin functions
-: slow work

DS_DOMAIN_NAME = 'HOST_NAME:SERVICES_TIER_PORT'
DS_USER_NAME   = 'user_login'
DS_PASSWORD    = 'user_password'
DS_SERVER      = 'HOST_NAME:ENGINE_TIER_PORT'
```

See Examples/config_example.py

## Running the program

Import classes for work in your code

```
from ibm_datastage_api import *
```

See Examples/
