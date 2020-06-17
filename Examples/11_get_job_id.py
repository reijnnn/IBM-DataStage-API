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

   DS_JOB_ID = 'job_id_1'

   print("Setting the id {} for the job {}".format(DS_JOB_ID, DS_JOB_NAME))
   res, err = dsapi.DSSetIdForJob(hproj, DS_JOB_NAME, DS_JOB_ID)
   if err:
      raise Exception("Can't set the id {} for the job {}: {}".format(DS_JOB_ID, DS_JOB_NAME, err))

   print("Getting a job id by the job name {}".format(DS_JOB_NAME))
   job_id, err = dsapi.DSGetIdForJob(hproj, DS_JOB_NAME)
   if err:
      raise Exception("Can't get a job id by the job name {}: {}".format(DS_JOB_NAME, err))
   print(job_id)

   print("Getting a job name by the job id {}".format(DS_JOB_ID))
   job_name, err = dsapi.DSJobNameFromJobId(hproj, DS_JOB_ID)
   if err:
      raise Exception("Can't get a job name by the job id {}: {}".format(DS_JOB_ID, err))
   print(job_name)

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
