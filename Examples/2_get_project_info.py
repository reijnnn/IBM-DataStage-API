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

hproj = None

print("Setting the parameters to connect to DataStage server")
dsapi.DSSetServerParams(DS_DOMAIN_NAME, DS_USER_NAME, DS_PASSWORD, DS_SERVER)

try:
	print("Loading the project {}".format(DS_PROJECT))
	hproj, err = dsapi.DSOpenProject(DS_PROJECT)
	if err:
		raise Exception("Can't open the project {}: {}".format(DS_PROJECT, err))

	print("Getting an information about the project")

	res, err = dsapi.DSGetProjectInfo(hproj, dsapi.DSJ_PROJECTNAME)
	if err:
		raise Exception("Can't get the project info: {}".format(err))
	print("DSJ_PROJECTNAME = {}".format(res))

	res, err = dsapi.DSGetProjectInfo(hproj, dsapi.DSJ_HOSTNAME)
	if err:
		raise Exception("Can't get the project info: {}".format(err))
	print("DSJ_HOSTNAME = {}".format(res))

	res, err = dsapi.DSGetProjectInfo(hproj, dsapi.DSJ_TCPPORT)
	if err:
		raise Exception("Can't get the project info: {}".format(err))
	print("DSJ_TCPPORT = {}".format(res))

	res, err = dsapi.DSGetProjectInfo(hproj, dsapi.DSJ_PROJECTPATH)
	if err:
		raise Exception("Can't get the project info: {}".format(err))
	print("DSJ_PROJECTPATH = {}".format(res))

	res, err = dsapi.DSGetProjectInfo(hproj, dsapi.DSJ_JOBLIST)
	if err:
		raise Exception("Can't get the project info: {}".format(err))
	print("DSJ_JOBLIST = {}".format(res))

	print("Closing the project")
	dsapi.DSCloseProject(hproj)
	hproj = None

except Exception as e:
	print("Runtime error: {}".format(str(e)))

	if hproj:
		print("Closing the project")
		dsapi.DSCloseProject(hproj)
		hproj = None

dsapi.DSUnloadLibrary()
print("Exit.")
