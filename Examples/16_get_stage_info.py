from config import *
from ibm_datastage_api import DSAPI, convert_char_p_to_list

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

    print("Getting an information about the stage of the job")

    DS_JOB_STAGE_NAME = 'TR_TST'

    infoTypes_list = [
        (dsapi.DSJ_LINKLIST, 'DSJ_LINKLIST'),
        (dsapi.DSJ_STAGELASTERR, 'DSJ_STAGELASTERR'),
        (dsapi.DSJ_STAGENAME, 'DSJ_STAGENAME'),
        (dsapi.DSJ_STAGETYPE, 'DSJ_STAGETYPE'),
        (dsapi.DSJ_STAGEINROWNUM, 'DSJ_STAGEINROWNUM'),
        (dsapi.DSJ_VARLIST, 'DSJ_VARLIST'),
        (dsapi.DSJ_STAGESTARTTIMESTAMP, 'DSJ_STAGESTARTTIMESTAMP'),
        (dsapi.DSJ_STAGEENDTIMESTAMP, 'DSJ_STAGEENDTIMESTAMP'),
        (dsapi.DSJ_STAGEDESC, 'DSJ_STAGEDESC'),
        (dsapi.DSJ_STAGEINST, 'DSJ_STAGEINST'),
        (dsapi.DSJ_STAGECPU, 'DSJ_STAGECPU'),
        (dsapi.DSJ_LINKTYPES, 'DSJ_LINKTYPES'),
        (dsapi.DSJ_STAGEELAPSED, 'DSJ_STAGEELAPSED'),
        (dsapi.DSJ_STAGEPID, 'DSJ_STAGEPID'),
        (dsapi.DSJ_STAGESTATUS, 'DSJ_STAGESTATUS'),
        (dsapi.DSJ_CUSTINFOLIST, 'DSJ_CUSTINFOLIST')
    ]

    for infoType, infoName in infoTypes_list:
        res, err = dsapi.DSGetStageInfo(hjob, DS_JOB_STAGE_NAME, infoType)
        if err:
            print("{}. Can't get the stage info: {}".format(infoName, err))
        else:
            if infoName == 'DSJ_STAGELASTERR':
                print("{} = {}".format(infoName, convert_char_p_to_list(res.fullMessage)))
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
