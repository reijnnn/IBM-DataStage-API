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
hjob  = None

print("Setting the parameters to connect to DataStage server")
dsapi.DSSetServerParams(DS_DOMAIN_NAME, DS_USER_NAME, DS_PASSWORD, DS_SERVER)

try:
	print("Loading the project {}".format(DS_PROJECT))
	hproj, err = dsapi.DSOpenProject(DS_PROJECT)
	if err:
		raise Exception("Can't open the project {}: {}".format(DS_PROJECT, err))

	print("Loading the job {}".format(DS_JOB_NAME))
	hjob, err = dsapi.DSOpenJob(hproj, DS_JOB_NAME)
	if err:
		raise Exception("Can't open the job {}: {}".format(DS_JOB_NAME, err))

	print("Getting a list of event log IDs for a last job invocation")
	res, err = dsapi.DSGetLogEventIds(hjob)
	if err:
		raise Exception("Can't get a list of event log IDs: {}".format(err))
	print(res)
	
	print("Getting a list of event log IDs for a previous job invocation")
	res, err = dsapi.DSGetLogEventIds(hjob, -1)
	if err:
		raise Exception("Can't get a list of event log IDs: {}".format(err))
	print(res)
	
	print("Getting a list of event log IDs for a previous job invocation. Only Start/End('S') and Fatal('F') events")
	"""
	I - Informational
	W - Warning
	F - Fatal
	S - Start or End events
	B - Batch or Control events
	R - Purge or reset events
	J - Reject events 	
	"""
	res, err = dsapi.DSGetLogEventIds(hjob, -1, 'SF')
	if err:
		raise Exception("Can't get a list of event log IDs: {}".format(err))
	print(res)
	
	print("Closing the job")
	dsapi.DSCloseJob(hjob)
	hjob = None

	print("Closing the project")
	dsapi.DSCloseProject(hproj)
	hproj = None

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
