# -*- coding: utf-8 -*-

def print_job_dependencies(job_name, level = 0):

	print('    ' * level + '|----' + job_name)

	res, err = dsapi.DSGetReposUsage(hproj, dsapi.DSS_JOB_USES_JOB, job_name)
	if err:
		print(err)
		return

	# no data found
	if res is None:
		return

	jobs_list = []
	while True:
		curr_job_type = res.jobtype
		curr_job_name = dsapi.decodeBytes(res.jobname).split("\\")[-1]

		jobs_list.append(curr_job_name)

		if res.nextjob:
			res = res.nextjob.contents
		else:
			break

	for job in jobs_list:
		print_job_dependencies(job, level + 1)

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

	print("Building dependency tree for a job {}".format(DS_JOB_NAME))
	print_job_dependencies(DS_JOB_NAME)

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
