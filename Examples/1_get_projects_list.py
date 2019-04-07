# -*- coding: utf-8 -*-

from config import *

import os, sys
sys.path.insert(0, os.path.dirname(os.getcwd()))

from ibm_datastage_api import DSAPI

dsapi = DSAPI()
res, err = dsapi.DSLoadLibrary(API_LIB_FILE)
if(err):
	print("Loading the library failed: {}".format(err))
	exit()

print("Setting the parameters to connect to DataStage server")
dsapi.DSSetServerParams(DS_DOMAIN_NAME, DS_USER_NAME, DS_PASSWORD, DS_SERVER)

try:
	print("The list of available projects is on the server:")
	res, err = dsapi.DSGetProjectList()
	if err:
		raise Exception("Can't get the list of the projects: {}".format(err))

	print(res)

except Exception as e:
	print("Runtime error: {}".format(str(e)))

dsapi.DSUnloadLibrary()
print("Exit.")
