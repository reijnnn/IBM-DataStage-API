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

    print("Searching jobs by the specified type, name and folder")
    res, err = dsapi.DSGetReposInfo(hproj, dsapi.DSS_JOBS, dsapi.DSS_JOB_ALL, '*tst*', 'Jobs')
    if err:
        raise Exception("Can't search jobs: {}".format(err))

    if res is None:
        print("No data found")
    else:
        while True:
            print(res.jobname)
            if res.nextjob:
                res = res.nextjob.contents
            else:
                break

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
