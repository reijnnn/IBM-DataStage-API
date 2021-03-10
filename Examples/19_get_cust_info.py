from config import *
from ibm_datastage_api import DSAPI, decode_bytes

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

    print("Loading the job {}".format(DS_JOB_NAME))
    hjob, err = dsapi.DSOpenJob(hproj, DS_JOB_NAME)
    if err:
        raise Exception("Can't open the job {}: {}".format(DS_JOB_NAME, err))

    print("Getting an information about custom variable of the stage")

    DS_JOB_STAGE_NAME = 'TR_TST'
    DS_JOB_STAGE_CUSTINFO_VAR_NAME = 'SUMVALUEINSTANCE'

    infoTypes_list = [
        (dsapi.DSJ_CUSTINFOVALUE, 'DSJ_CUSTINFOVALUE'),
        (dsapi.DSJ_CUSTINFODESC, 'DSJ_CUSTINFODESC')
    ]

    for infoType, infoName in infoTypes_list:
        res, err = dsapi.DSGetCustInfo(hjob, DS_JOB_STAGE_NAME, DS_JOB_STAGE_CUSTINFO_VAR_NAME, infoType)
        if err:
            print("{}. Can't get the custom variable info: {}".format(infoName, err))
        else:
            print("{} = {}".format(infoName, res))

    print("Forming the report")
    res, err = dsapi.DSMakeJobReport(hjob, dsapi.DSJ_REPORT2)
    if err:
        raise Exception("Can't form the report: {}".format(err))

    res = decode_bytes(res).split("\r\n")
    for info in res:
        print(info)

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
