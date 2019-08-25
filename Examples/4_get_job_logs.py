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

	print("Loading the job {}".format(DS_JOB_NAME))
	hjob, err = dsapi.DSOpenJob(hproj, DS_JOB_NAME)
	if err:
		raise Exception("Can't open the job {}: {}".format(DS_JOB_NAME, err))

	print("Getting the last start time of the job")
	job_start_timestamp, err = dsapi.DSGetJobInfo(hjob, dsapi.DSJ_JOBSTARTTIMESTAMP)
	if err:
		raise Exception("Can't get job info {}: {}".format(DS_JOB_NAME, err))

	log_event, err = dsapi.DSFindFirstLogEntry(hjob, dsapi.DSJ_LOGANY, job_start_timestamp)
	if err:
		raise Exception("Can't get logs of job {}: {}".format(DS_JOB_NAME, err))

	print("Reading logs")
	event_id = log_event.eventId
	while True:
		log_detail, err = dsapi.DSGetLogEntryFull(hjob, event_id)
		if err:
			raise Exception("Can't get details for eventId = {}: {}".format(event_id, err))

		print("[{}][{}][{}]: {}".format(log_detail.eventId, log_detail.type, log_detail.username, dsapi.charPointerToList(log_detail.fullMessage)))

		log_event, err = dsapi.DSFindNextLogEntry(hjob)
		if err:
			break

		event_id = log_event.eventId

	print("Closing the job")
	dsapi.DSCloseJob(hjob)
	hjob = None

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
