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

   print("Getting an information about the job")

   infoTypes_list = [
      (dsapi.DSJ_JOBSTATUS,         'DSJ_JOBSTATUS'),
      (dsapi.DSJ_JOBNAME,           'DSJ_JOBNAME'),
      (dsapi.DSJ_JOBCONTROLLER,     'DSJ_JOBCONTROLLER'),
      (dsapi.DSJ_JOBSTARTTIMESTAMP, 'DSJ_JOBSTARTTIMESTAMP'),
      (dsapi.DSJ_JOBLASTTIMESTAMP,  'DSJ_JOBLASTTIMESTAMP'),
      (dsapi.DSJ_JOBWAVENO,         'DSJ_JOBWAVENO'),
      (dsapi.DSJ_PARAMLIST,         'DSJ_PARAMLIST'),
      (dsapi.DSJ_STAGELIST,         'DSJ_STAGELIST'),
      (dsapi.DSJ_USERSTATUS,        'DSJ_USERSTATUS'),
      (dsapi.DSJ_JOBCONTROL,        'DSJ_JOBCONTROL'),
      (dsapi.DSJ_JOBPID,            'DSJ_JOBPID'),
      (dsapi.DSJ_JOBINVOCATIONS,    'DSJ_JOBINVOCATIONS'),
      (dsapi.DSJ_JOBINTERIMSTATUS,  'DSJ_JOBINTERIMSTATUS'),
      (dsapi.DSJ_JOBINVOCATIONID,   'DSJ_JOBINVOCATIONID'),
      (dsapi.DSJ_JOBDESC,           'DSJ_JOBDESC'),
      (dsapi.DSJ_STAGELIST2,        'DSJ_STAGELIST2'),
      (dsapi.DSJ_JOBELAPSED,        'DSJ_JOBELAPSED'),
      (dsapi.DSJ_JOBDMISERVICE,     'DSJ_JOBDMISERVICE'),
      (dsapi.DSJ_JOBMULTIINVOKABLE, 'DSJ_JOBMULTIINVOKABLE'),
      (dsapi.DSJ_JOBFULLDESC,       'DSJ_JOBFULLDESC'),
      (dsapi.DSJ_JOBRESTARTABLE,    'DSJ_JOBRESTARTABLE')
   ]

   for infoType, infoName in infoTypes_list:
      res, err = dsapi.DSGetJobInfo(hjob, infoType)
      if err:
         print("{}. Can't get the job info: {}".format(infoName, err))
      else:
         print("{} = {}".format(infoName, res))

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
