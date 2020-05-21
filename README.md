# IBM-DataStage-API

IBM-DataStage-API on Python.
Please read [InfoSphere DataStage Development Kit](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.ds.cliapi.ref.doc/topics/r_dsvjbref_WebSphere_DataStage_Development_Kit.html) to find details.

## Requirements

For the correct work `ctypes` with DataStage API library (32-bit or 64-bit) you need Python of the same version (32-bit or 64-bit)

`PATH` on windows should include path where file `vmdsapi.dll` is located.  
In most cases, in the `../IBM/InformationServer/Clients/Classic/`

`LD_LIBRARY_PATH` on \*nix should include path where file `libvmdsapi.so` and its dependences are located.  
In most cases, in the `../IBM/InformationServer/Server/DSEngine/lib/`

Also activation of [dsenv](https://www.ibm.com/support/knowledgecenter/en/SSZJPZ_11.7.0/com.ibm.swg.im.iis.productization.iisinfsv.install.doc/topics/wsisinst_dsenv_file.html) can help you  
`cd ../IBM/InformationServer/Server/DSEngine/`  
`. ./dsenv`

## Getting Started

Create your own `config.py` with path to DataStage API library (`vmdsapi.dll` on client or `libvmdsapi.so` on server) and configure connection's parameters.

See Examples/config_example.py

## Running the program

Import classes for work in your code

```
from ibm_datastage_api import *
```

See Examples/
