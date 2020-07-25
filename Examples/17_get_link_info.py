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

   print("Getting an information about the link of the stage")

   DS_JOB_STAGE_NAME      = 'Transformer_0'
   DS_JOB_STAGE_LINK_NAME = 'DSLink2'

   infoTypes_list = [
      (dsapi.DSJ_LINKLASTERR,     'DSJ_LINKLASTERR'),
      (dsapi.DSJ_LINKNAME,        'DSJ_LINKNAME'),
      (dsapi.DSJ_LINKROWCOUNT,    'DSJ_LINKROWCOUNT'),
      (dsapi.DSJ_LINKSQLSTATE,    'DSJ_LINKSQLSTATE'),
      (dsapi.DSJ_LINKDBMSCODE,    'DSJ_LINKDBMSCODE'),
      (dsapi.DSJ_LINKDESC,        'DSJ_LINKDESC'),
      (dsapi.DSJ_LINKSTAGE,       'DSJ_LINKSTAGE'),
      (dsapi.DSJ_INSTROWCOUNT,    'DSJ_INSTROWCOUNT'),
      (dsapi.DSJ_LINKEXTROWCOUNT, 'DSJ_LINKEXTROWCOUNT')
   ]

   for infoType, infoName in infoTypes_list:
      res, err = dsapi.DSGetLinkInfo(hjob, DS_JOB_STAGE_NAME, DS_JOB_STAGE_LINK_NAME, infoType)
      if err:
         print("{}. Can't get the link infoo: {}".format(infoName, err))
      else:
         if infoName == 'DSJ_LINKLASTERR':
            print("{} = {}".format(infoName, dsapi.charPointerToList(res.fullMessage)))
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
