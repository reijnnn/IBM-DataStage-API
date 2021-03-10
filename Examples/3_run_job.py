from config import *
from ibm_datastage_api import DSAPI, DSPARAM, encode_string, decode_bytes

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

    print("Getting an information about the job")

    res, err = dsapi.DSGetJobInfo(hjob, dsapi.DSJ_JOBSTATUS)
    if err:
        raise Exception("DSJ_JOBSTATUS. Can't get the job info: {}".format(err))
    print("DSJ_JOBSTATUS = {}".format(res))

    res, err = dsapi.DSGetJobInfo(hjob, dsapi.DSJ_PARAMLIST)
    if err:
        raise Exception("DSJ_PARAMLIST. Can't get the job info: {}".format(err))
    print("DSJ_PARAMLIST = {}".format(res))

    print("Blocking the job {}".format(DS_JOB_NAME))
    _, err = dsapi.DSLockJob(hjob)
    if err:
        raise Exception("Can't block the job: {}".format(err))

    DS_JOB_STR_PARAM_NAME = 'p_str'
    DS_JOB_STR_PARAM_VALUE = 'string param value'

    print("Setting launch parameters")
    job_param = DSPARAM()
    job_param.paramType = dsapi.DSJ_PARAMTYPE_STRING
    job_param.paramValue.pString = encode_string(DS_JOB_STR_PARAM_VALUE)
    res, err = dsapi.DSSetParam(hjob, DS_JOB_STR_PARAM_NAME, job_param)
    if err:
        print("Can't set the parameter: {}".format(err))

    DS_JOB_STR_ENCRYPTED_PARAM_NAME = 'p_str_encrypted'
    DS_JOB_STR_ENCRYPTED_PARAM_VALUE = 'string encrypted param value'

    job_param = DSPARAM()
    job_param.paramType = dsapi.DSJ_PARAMTYPE_ENCRYPTED
    job_param.paramValue.pEncrypt = encode_string(DS_JOB_STR_ENCRYPTED_PARAM_VALUE)
    res, err = dsapi.DSSetParam(hjob, DS_JOB_STR_ENCRYPTED_PARAM_NAME, job_param)
    if err:
        print("Can't set the parameter: {}".format(err))

    DS_JOB_STR_FAKE_PARAM_NAME = 'p_str_fake'
    DS_JOB_STR_FAKE_PARAM_VALUE = 'string fake param value'

    job_param = DSPARAM()
    job_param.paramType = dsapi.DSJ_PARAMTYPE_ENCRYPTED
    job_param.paramValue.pEncrypt = encode_string(DS_JOB_STR_FAKE_PARAM_VALUE)
    res, err = dsapi.DSSetParam(hjob, DS_JOB_STR_FAKE_PARAM_NAME, job_param)
    if err:
        print("Can't set the parameter: {}".format(err))

    print("Launching the job {}".format(DS_JOB_NAME))
    _, err = dsapi.DSRunJob(hjob, dsapi.DSJ_RUNNORMAL)
    if err:
        raise Exception("Can't launch the job: {}".format(err))

    print("Unblocking the job")
    dsapi.DSUnlockJob(hjob)

    print("Waiting the end of the work process...")
    dsapi.DSWaitForJob(hjob)

    print("Forming the report")
    res, err = dsapi.DSMakeJobReport(hjob, dsapi.DSJ_REPORT0)
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
