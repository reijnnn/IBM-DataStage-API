# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

from config import *
from ibm_datastage_api import DSAPI, DSPARAM

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

   print("Blocking the job {}".format(DS_JOB_NAME))
   res, err = dsapi.DSLockJob(hjob)
   if err:
      raise Exception("Can't block the job: {}".format(err))

   DS_JOB_PARAM_NAME  = 'bad_param_name'
   DS_JOB_PARAM_VALUE = 'bad_param_value'

   print("Setting launch parameters")
   job_param = DSPARAM()
   job_param.paramType = dsapi.DSJ_PARAMTYPE_STRING
   job_param.paramValue.pString = dsapi.encodeString(DS_JOB_PARAM_VALUE)
   res, err = dsapi.DSSetParam(hjob, DS_JOB_PARAM_NAME, job_param)
   if err:
      print("Can't set the parameter: {}".format(err))

   last_err_code = err['code']

   print('Preparing message with your own template')
   res, err = dsapi.DSServerMessage('Error calling DSSetParam(%1), code=%2[E]', [DS_JOB_PARAM_NAME, last_err_code])
   if err:
      print("Can't prepare the message: {}".format(err))
   else:
      print(res)

   print('Preparing message using the message id = DSTAGE_JSG_M_0002 and the InfoSphere DataStage message file')
   res, err = dsapi.DSServerMessage('', [DS_JOB_PARAM_NAME, last_err_code], 'DSTAGE_JSG_M_0002')
   if err:
      print("Can't prepare the message: {}".format(err))
   else:
      print(res)

   print("Deblocking the job")
   dsapi.DSUnlockJob(hjob)

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
