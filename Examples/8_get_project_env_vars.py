# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from config import *
from ibm_datastage_api import DSAPI

hproj = None
hjob  = None

dsapi = DSAPI()

try:
	res, err = dsapi.DSLoadLibrary(API_LIB_FILE)
	if err:
		raise Exception("Loading the library failed: {}".format(err))

	print("Setting the parameters to connect to DataStage server")
	dsapi.DSSetServerParams(DS_DOMAIN_NAME, DS_USER_NAME, DS_PASSWORD, DS_SERVER)

	print("Loading the project {}".format(DS_PROJECT))
	hproj, err = dsapi.DSOpenProject(DS_PROJECT)
	if err:
		raise Exception("Can't open the project {}: {}".format(DS_PROJECT, err))

	ENV_VAR_NAME = 'tst_env_var'

	print("Adding the environment variable in the project")
	res, err = dsapi.DSAddEnvVar(hproj, ENV_VAR_NAME, dsapi.DSA_ENVVAR_TYPE_STRING, 'Environment variable created with the API', 'value_123')
	if err:
		raise Exception("Can't add the environment variable in the project: {}".format(err))

	print("Editing the environment variable in the project")
	res, err = dsapi.DSSetEnvVar(hproj, ENV_VAR_NAME, 'value_new_321')
	if err:
		raise Exception("Can't edit the environment variable in the project: {}".format(err))

	print("Getting a list of environment variables and their values in the project")
	res, err = dsapi.DSListEnvVars(hproj)
	if err:
		raise Exception("Can't get a list of environment variables in the project: {}".format(err))
	print("Environment variables: {}".format(res))

	print("Deleting the environment variable in the project")
	res, err = dsapi.DSDeleteEnvVar(hproj, ENV_VAR_NAME)
	if err:
		raise Exception("Can't delete the environment variable in the project: {}".format(err))

	print("Closing the project")
	dsapi.DSCloseProject(hproj)
	hproj = None

	dsapi.DSUnloadLibrary()

except Exception as e:
	print("Runtime error: {}".format(str(e)))

	if hjob:
		print("Deblocking the job")
		dsapi.DSUnlockJob(hjob)

		print("Closing the job")
		dsapi.DSCloseJob(hjob)
		hjob = None

	if hproj:
		print("Closing the project")
		dsapi.DSCloseProject(hproj)
		hproj = None

	dsapi.DSUnloadLibrary()

print("Exit.")
