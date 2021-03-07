from config import *
from ibm_datastage_api import DSAPI

dsapi = DSAPI()
hproj = None
hjob = None

try:
    _, err = dsapi.DSLoadLibrary(API_LIB_FILE)
    if err:
        raise Exception("Loading the library failed: {}".format(err))

    print("Setting the parameters to connect to DataStage server")
    dsapi.DSSetServerParams(DS_DOMAIN_NAME, DS_USER_NAME, DS_PASSWORD, DS_SERVER)

    print("Loading the project {}".format(DS_PROJECT))
    hproj, err = dsapi.DSOpenProject(DS_PROJECT)
    if err:
        raise Exception("Can't open the project {}: {}".format(DS_PROJECT, err))

    print("Getting an information about the project")

    infoTypes_list = [
        (dsapi.DSJ_JOBLIST, 'DSJ_JOBLIST'),
        (dsapi.DSJ_PROJECTNAME, 'DSJ_PROJECTNAME'),
        (dsapi.DSJ_HOSTNAME, 'DSJ_HOSTNAME'),
        (dsapi.DSJ_INSTALLTAG, 'DSJ_INSTALLTAG'),
        (dsapi.DSJ_TCPPORT, 'DSJ_TCPPORT'),
        (dsapi.DSJ_PROJECTPATH, 'DSJ_PROJECTPATH')
    ]

    for infoType, infoName in infoTypes_list:
        res, err = dsapi.DSGetProjectInfo(hproj, infoType)
        if err:
            print("{}. Can't get the project info: {}".format(infoName, err))
        else:
            print("{} = {}".format(infoName, res))

    print("Closing the project")
    dsapi.DSCloseProject(hproj)
    hproj = None

    dsapi.DSUnloadLibrary()

except Exception as e:
    print("Runtime error: {}".format(str(e)))

    if hjob:
        print("Unblocking the job")
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
