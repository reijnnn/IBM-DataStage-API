import ctypes
from sys import platform as _platform_name

if _platform_name.startswith('win'):
    time_t = ctypes.c_uint32
else:
    time_t = ctypes.c_uint64


class DSPROJECT(ctypes.Structure):
    _fields_ = [("dsapiVersionNo", ctypes.c_int),
                ("sessionId", ctypes.c_int),
                ("valueMark", ctypes.c_ubyte),
                ("fieldMark", ctypes.c_ubyte)]


class DSJOB(ctypes.Structure):
    _fields_ = [("hProject", ctypes.POINTER(DSPROJECT)),
                ("serverJobHandle", ctypes.c_char_p),
                ("logData", ctypes.c_char_p),
                ("logDataLen", ctypes.c_int),
                ("logDataPsn", ctypes.c_int)]


class _DSJOBINFO(ctypes.Union):
    _fields_ = [("jobStatus", ctypes.c_int),
                ("jobController", ctypes.c_char_p),
                ("jobStartTime", time_t),
                ("jobWaveNumber", ctypes.c_int),
                ("userStatus", ctypes.c_char_p),
                ("stageList", ctypes.POINTER(ctypes.c_char)),
                ("paramList", ctypes.POINTER(ctypes.c_char)),
                ("jobName", ctypes.c_char_p),
                ("jobControl", ctypes.c_int),
                ("jobPid", ctypes.c_int),
                ("jobLastTime", time_t),
                ("jobInvocations", ctypes.POINTER(ctypes.c_char)),
                ("jobInterimStatus", ctypes.c_int),
                ("jobInvocationId", ctypes.c_char_p),
                ("jobDesc", ctypes.c_char_p),
                ("stageList2", ctypes.POINTER(ctypes.c_char)),
                ("jobElapsed", ctypes.c_int),
                ("jobDMIService", ctypes.c_int),
                ("jobMultiInvokable", ctypes.c_int),
                ("jobFullDesc", ctypes.c_char_p),
                ("jobRestartable", ctypes.c_int)]


class DSJOBINFO(ctypes.Structure):
    _fields_ = [("infoType", ctypes.c_int),
                ("info", _DSJOBINFO)]


class _DSPROJECTINFO(ctypes.Union):
    _fields_ = [("jobList", ctypes.POINTER(ctypes.c_char)),
                ("projectName", ctypes.c_char_p),
                ("projectPath", ctypes.c_char_p),
                ("hostName", ctypes.c_char_p),
                ("installTag", ctypes.c_char_p),
                ("tcpPort", ctypes.c_char_p)]


class DSPROJECTINFO(ctypes.Structure):
    _fields_ = [("infoType", ctypes.c_int),
                ("info", _DSPROJECTINFO)]


class DSLOGEVENT(ctypes.Structure):
    _fields_ = [("eventId", ctypes.c_int),
                ("timestamp", time_t),
                ("type", ctypes.c_int),
                ("message", ctypes.c_char_p)]


class DSLOGDETAILFULL(ctypes.Structure):
    _fields_ = [("eventId", ctypes.c_int),
                ("timestamp", time_t),
                ("type", ctypes.c_int),
                ("username", ctypes.c_char_p),
                ("fullMessage", ctypes.POINTER(ctypes.c_char)),
                ("messageId", ctypes.c_char_p),
                ("invocationId", ctypes.c_char_p)]


class DSLOGDETAIL(ctypes.Structure):
    _fields_ = [("eventId", ctypes.c_int),
                ("timestamp", time_t),
                ("type", ctypes.c_int),
                ("username", ctypes.c_char_p),
                ("fullMessage", ctypes.POINTER(ctypes.c_char))]


class _DSPARAM(ctypes.Union):
    _fields_ = [("pString", ctypes.c_char_p),
                ("pEncrypt", ctypes.c_char_p),
                ("pInt", ctypes.c_int),
                ("pFloat", ctypes.c_float),
                ("pPath", ctypes.c_char_p),
                ("pListValue", ctypes.c_char_p),
                ("pDate", ctypes.c_char_p),
                ("pTime", ctypes.c_char_p)]


class DSPARAM(ctypes.Structure):
    _fields_ = [("paramType", ctypes.c_int),
                ("paramValue", _DSPARAM)]


class DSPARAMINFO(ctypes.Structure):
    _fields_ = [("defaultValue", DSPARAM),
                ("helpText", ctypes.c_char_p),
                ("paramPrompt", ctypes.c_char_p),
                ("paramType", ctypes.c_int),
                ("desDefaultValue", DSPARAM),
                ("listValues", ctypes.c_char_p),
                ("desListValues", ctypes.c_char_p),
                ("promptAtRun", ctypes.c_int)]


class _DSREPORTINFO(ctypes.Union):
    _fields_ = [("reportText", ctypes.c_char_p)]


class DSREPORTINFO(ctypes.Structure):
    _fields_ = [("reportType", ctypes.c_int),
                ("info", _DSREPORTINFO)]


class DSREPOSUSAGEJOB(ctypes.Structure):
    pass


DSREPOSUSAGEJOB._fields_ = [("jobname", ctypes.c_char_p),
                            ("jobtype", ctypes.c_int),
                            ("nextjob", ctypes.POINTER(DSREPOSUSAGEJOB)),
                            ("childjob", ctypes.POINTER(DSREPOSUSAGEJOB))]


class _DSREPOSUSAGE(ctypes.Union):
    _fields_ = [("jobs", ctypes.POINTER(DSREPOSUSAGEJOB))]


class DSREPOSUSAGE(ctypes.Structure):
    _fields_ = [("infoType", ctypes.c_int),
                ("info", _DSREPOSUSAGE)]


class DSREPOSJOBINFO(ctypes.Structure):
    pass


DSREPOSJOBINFO._fields_ = [("jobname", ctypes.c_char_p),
                           ("jobtype", ctypes.c_int),
                           ("nextjob", ctypes.POINTER(DSREPOSJOBINFO))]


class _DSREPOSINFO(ctypes.Union):
    _fields_ = [("jobs", ctypes.POINTER(DSREPOSJOBINFO))]


class DSREPOSINFO(ctypes.Structure):
    _fields_ = [("infoType", ctypes.c_int),
                ("info", _DSREPOSINFO)]


class _DSSTAGEINFO(ctypes.Union):
    _fields_ = [("lastError", DSLOGDETAIL),
                ("typeName", ctypes.c_char_p),
                ("inRowNum", ctypes.c_int),
                ("linkList", ctypes.POINTER(ctypes.c_char)),
                ("stageName", ctypes.c_char_p),
                ("varList", ctypes.POINTER(ctypes.c_char)),
                ("stageStartTime", time_t),
                ("stageEndTime", time_t),
                ("linkTypes", ctypes.POINTER(ctypes.c_char)),
                ("stageDesc", ctypes.c_char_p),
                ("instList", ctypes.POINTER(ctypes.c_char)),
                ("cpuList", ctypes.POINTER(ctypes.c_char)),
                ("stageElapsed", ctypes.c_char_p),
                ("pidList", ctypes.POINTER(ctypes.c_char)),
                ("stageStatus", ctypes.c_int),
                ("custInfoList", ctypes.POINTER(ctypes.c_char))]


class DSSTAGEINFO(ctypes.Structure):
    _fields_ = [("infoType", ctypes.c_int),
                ("info", _DSSTAGEINFO)]


class _DSLINKINFO(ctypes.Union):
    _fields_ = [("lastError", DSLOGDETAIL),
                ("rowCount", ctypes.c_int),
                ("linkName", ctypes.c_char_p),
                ("linkSQLState", ctypes.c_char_p),
                ("linkDBMSCode", ctypes.c_char_p),
                ("linkDesc", ctypes.c_char_p),
                ("linkedStage", ctypes.c_char_p),
                ("rowCountList", ctypes.POINTER(ctypes.c_char))]


class DSLINKINFO(ctypes.Structure):
    _fields_ = [("infoType", ctypes.c_int),
                ("info", _DSLINKINFO)]


class _DSVARINFO(ctypes.Union):
    _fields_ = [("varValue", ctypes.c_char_p),
                ("varDesc", ctypes.c_char_p)]


class DSVARINFO(ctypes.Structure):
    _fields_ = [("infoType", ctypes.c_int),
                ("info", _DSVARINFO)]
