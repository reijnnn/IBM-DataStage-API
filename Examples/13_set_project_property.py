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

   print("The list of available project properties:")
   res, err = dsapi.DSListProjectProperties(hproj)
   if err:
      raise Exception("Can't get the list of the project properties".format(err))
   print(res)

   print("Setting the project property DSA_OSHVISIBLEFLAG = 1")
   res, err = dsapi.DSSetProjectProperty(hproj, dsapi.DSA_OSHVISIBLEFLAG, '1')
   if err:
      raise Exception("Can't set the project property: {}".format(err))

   print("The list of available project properties:")
   res, err = dsapi.DSListProjectProperties(hproj)
   if err:
      raise Exception("Can't get the list of the project properties".format(err))
   print(res)

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
