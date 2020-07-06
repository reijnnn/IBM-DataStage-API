# -*- coding: utf-8 -*-

def print_job_dependencies(job_name, level=0):
   print('    ' * level + '|----' + job_name)

   res, err = dsapi.DSGetReposUsage(hproj, dsapi.DSS_JOB_USES_JOB, job_name)
   if err:
      raise Exception("Can't get the job {} info: {}".format(job_name, err))

   if res is None:
      return

   jobs_list = []
   while True:
      short_job_name = dsapi.decodeBytes(res.jobname).split("\\")[-1]
      jobs_list.append(short_job_name)

      if res.nextjob:
         res = res.nextjob.contents
      else:
         break

   for job in jobs_list:
      print_job_dependencies(job, level + 1)

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

   print("Building dependency tree for a job {}".format(DS_JOB_NAME))
   print_job_dependencies(DS_JOB_NAME)

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
