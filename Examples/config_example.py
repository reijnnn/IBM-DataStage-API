# There are two types of setting login parameters

'''
1. Using operating system user credentials of Engine tier, by default, `dsadm`
+: fast work
-: doesn't support admin functions (DSAddProject, DSSetProjectProperty...)
'''
DS_DOMAIN_NAME = ''
DS_USER_NAME   = 'dsadm'
DS_PASSWORD    = 'dsadm_password'
DS_SERVER      = 'HOST_NAME:ENGINE_TIER_PORT'

'''
2. Using user credentials of Services tier
+: support admin functions
-: slow work
'''
DS_DOMAIN_NAME = 'HOST_NAME:SERVICES_TIER_PORT'
DS_USER_NAME   = 'user_login'
DS_PASSWORD    = 'user_password'
DS_SERVER      = 'HOST_NAME:ENGINE_TIER_PORT'

# Project/Job
DS_PROJECT  = 'dsdev_project'
DS_JOB_NAME = 'dsjob_name'

# Full path to API library (vmdsapi.dll or libvmdsapi.so)
API_LIB_FILE = '../IBM/InformationServer/Clients/Classic/vmdsapi.dll'
