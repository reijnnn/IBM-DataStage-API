import os
import ctypes

from ibm_datastage_api.ibm_datastage_api_utils import (
    convert_char_p_to_list,
    encode_string,
    decode_bytes
)

from ibm_datastage_api.ibm_datastage_api_structures import (
    time_t,
    DSPROJECT,
    DSJOB,
    DSJOBINFO,
    DSPROJECTINFO,
    DSLOGEVENT,
    DSLOGDETAILFULL,
    DSLOGDETAIL,
    DSPARAM,
    DSPARAMINFO,
    DSREPORTINFO,
    DSREPOSUSAGE,
    DSREPOSINFO,
    DSSTAGEINFO,
    DSLINKINFO,
    DSVARINFO
)

from ibm_datastage_api.ibm_datastage_api_errors import (
    DSAPIERROR
)


class DSAPI:
    # API Version
    DSAPI_VERSION = 1

    # DSJOBINFO 'jobStatus' values
    DSJS_RUNNING = 0  # Job running
    DSJS_RUNOK = 1  # Job finished a normal run with no warnings
    DSJS_RUNWARN = 2  # Job finished a normal run with warnings
    DSJS_RUNFAILED = 3  # Job finished a normal run with a fatal error
    DSJS_QUEUED = 4  # Job queued waiting for resource allocation
    DSJS_VALOK = 11  # Job finished a validation run with no warnings
    DSJS_VALWARN = 12  # Job finished a validation run with warnings
    DSJS_VALFAILED = 13  # Job failed a validation run
    DSJS_RESET = 21  # Job finished a reset run
    DSJS_CRASHED = 96  # Job was stopped by some indeterminate action
    DSJS_STOPPED = 97  # Job was stopped by operator intervention (can't tell run type)
    DSJS_NOTRUNNABLE = 98  # Job has not been compiled
    DSJS_NOTRUNNING = 99  # Any other status

    # DSJOBINFO 'infoType' values
    DSJ_JOBSTATUS = 1  # Current status of the job.
    DSJ_JOBNAME = 2  # Name of the job referenced by JobHandle.
    DSJ_JOBCONTROLLER = 3  # Name of job controlling the job referenced by JobHandle.
    DSJ_JOBSTARTTIMESTAMP = 4  # Date and time when the job started.
    DSJ_JOBWAVENO = 5  # Wave number of last or current run.
    DSJ_PARAMLIST = 6  # List of job parameter names
    DSJ_STAGELIST = 7  # List of names of stages in job
    DSJ_USERSTATUS = 8  # Value, if any,  set as the user status by the job.
    DSJ_JOBCONTROL = 9  # Job control STOP/SUSPEND/RESUME
    DSJ_JOBPID = 10  # Process id of DSD.RUN process
    DSJ_JOBLASTTIMESTAMP = 11  # Server date/time of job last finished: "YYYY-MM-DD HH:MM:SS"
    DSJ_JOBINVOCATIONS = 12  # Comma-separated list of job invocation ids
    DSJ_JOBINTERIMSTATUS = 13  # Current interim status of job
    DSJ_JOBINVOCATIONID = 14  # Invocation name of the job referenced
    DSJ_JOBDESC = 15  # Job description
    DSJ_STAGELIST2 = 16  # list of stages not in DSJ.STAGELIST
    DSJ_JOBELAPSED = 17  # Job Elapsed time in seconds
    DSJ_JOBEOTCOUNT = 18  # Count of EndOfTransmission blocks processed by this job so far
    DSJ_JOBEOTTIMESTAMP = 19  # Date/time of the last EndOfTransmission block processed by this job
    DSJ_JOBDMISERVICE = 20  # Job is a DMI (aka WEB) service
    DSJ_JOBMULTIINVOKABLE = 21  # Job can be multiply invoked
    DSJ_JOBFULLDESC = 22  # Full job description
    DSJ_JOBRESTARTABLE = 24  # Job can be restarted

    # DSPROJECTINFO 'infoType' values
    DSJ_JOBLIST = 1  # List of jobs in project
    DSJ_PROJECTNAME = 2  # Name of current project
    DSJ_HOSTNAME = 3  # Host name of the server
    DSJ_INSTALLTAG = 4  # Install tag of the server DSEngine
    DSJ_TCPPORT = 5  # TCP port    of the server DSEngine
    DSJ_PROJECTPATH = 6  # Directory path of current project

    # DSSTAGEINFO 'infoType' values
    DSJ_LINKLIST = 1  # List of stage link names
    DSJ_STAGELASTERR = 2  # Last error message reported from any link of the stage.
    DSJ_STAGENAME = 3  # Actual name of stage
    DSJ_STAGETYPE = 4  # Stage type name.
    DSJ_STAGEINROWNUM = 5  # Primary links input row number.
    DSJ_VARLIST = 6  # List of stage variable names
    DSJ_STAGESTARTTIMESTAMP = 7  # Date and time when stage started
    DSJ_STAGEENDTIMESTAMP = 8  # Date and time when stage finished
    DSJ_STAGEDESC = 9  # Stage Description
    DSJ_STAGEINST = 10  # Comma-seperated list of stage instance ids
    DSJ_STAGECPU = 11  # Comma-seperated list of stage instance CPU in seconds
    DSJ_LINKTYPES = 12  # Comma-seperated list of link types
    DSJ_STAGEELAPSED = 13  # Stage elapsed time in seconds
    DSJ_STAGEPID = 14  # Comma-seperated list of stage instance PIDs
    DSJ_STAGESTATUS = 15  # Stage status
    DSJ_STAGEEOTCOUNT = 16  # Count of EndOfTransmission blocks processed by this stage so far.
    DSJ_STAGEEOTTIMESTAMP = 17  # Data/time of last EndOfTransmission block received by this stage.
    DSJ_CUSTINFOLIST = 18  # List of custom info names

    # DSLINKINFO 'infoType' values
    DSJ_LINKLASTERR = 1  # Last error message reported by link.
    DSJ_LINKNAME = 2  # Actual name of link
    DSJ_LINKROWCOUNT = 3  # Number of rows that have passed down the link.
    DSJ_LINKSQLSTATE = 4  # SQLSTATE value from Last error message
    DSJ_LINKDBMSCODE = 5  # DBMSCODE value from Last error message
    DSJ_LINKDESC = 6  # Link description
    DSJ_LINKSTAGE = 7  # Stage at other end of link
    DSJ_INSTROWCOUNT = 8  # Comma seperated list of rowcounts for each stage instance
    DSJ_LINKEOTROWCOUNT = 9  # Row count since last EndOfTransmission block.
    DSJ_LINKEXTROWCOUNT = 10  # Extended rowcount, using strings

    # DSVARINFO 'infoType' values
    DSJ_VARVALUE = 1  # Stage variable value
    DSJ_VARDESC = 2  # Stage variable description

    # DSLOGDETAILFULL 'eventType' values
    DSJ_LOGINFO = 1  # Information message.
    DSJ_LOGWARNING = 2  # Warning message.
    DSJ_LOGFATAL = 3  # Fatal error message.
    DSJ_LOGREJECT = 4  # Rejected row message.
    DSJ_LOGSTARTED = 5  # Job started message.
    DSJ_LOGRESET = 6  # Job reset message.
    DSJ_LOGBATCH = 7  # Batch control
    DSJ_LOGOTHER = 98  # Category other than above
    DSJ_LOGANY = 99  # Any type of event

    # DSRUNJOB 'runMode' values
    DSJ_RUNNORMAL = 1  # Standard job run.
    DSJ_RUNRESET = 2  # Job is to be reset.
    DSJ_RUNVALIDATE = 3  # Job is to be validated only.
    DSJ_RUNRESTART = 4  # Restart job with previous parameters, job must be in Restartable state.

    # DSPARAM 'paramType' values
    DSJ_PARAMTYPE_STRING = 0
    DSJ_PARAMTYPE_ENCRYPTED = 1
    DSJ_PARAMTYPE_INTEGER = 2
    DSJ_PARAMTYPE_FLOAT = 3
    DSJ_PARAMTYPE_PATHNAME = 4
    DSJ_PARAMTYPE_LIST = 5
    DSJ_PARAMTYPE_DATE = 6
    DSJ_PARAMTYPE_TIME = 7

    # DSREPORTINFO 'reportType' values
    DSJ_REPORT0 = 0  # Basic
    DSJ_REPORT1 = 1  # Stage/link detail
    DSJ_REPORT2 = 2  # Text string containing full XML report

    # DSREPOSUSAGEJOB 'relationshipType' values
    DSS_JOB_USES_JOB = 1
    DSS_JOB_USEDBY_JOB = 2
    DSS_JOB_HASSOURCE_TABLEDEF = 3
    DSS_JOB_HASTARGET_TABLEDEF = 4
    DSS_JOB_HASSOURCEORTARGET_TABLEDEF = 5

    # DSREPOSINFO 'infoType' values
    DSS_JOBS = 1  # The Object Type to return
    DSS_JOB_ALL = 15  # list all jobs
    DSS_JOB_SERVER = 1  # list all server jobs
    DSS_JOB_PARALLEL = 2  # list all parallel jobs
    DSS_JOB_MAINFRAME = 4  # list all mainframe jobs
    DSS_JOB_SEQUENCE = 8  # list all sequence jobs

    # DSAddEnvVar 'varType' values
    DSA_ENVVAR_TYPE_STRING = 'String'
    DSA_ENVVAR_TYPE_ENCRYPTED = 'Encrypted'

    # DSSetJobLimit 'limitType' values
    DSJ_LIMITWARN = 1  # Job to be stopped after LimitValue warning events
    DSJ_LIMITROWS = 2  # Stages to be limited to LimitValue rows

    # DSSetProjectProperty 'property' values
    DSA_OSHVISIBLEFLAG = 'OSHVisibleFlag'
    DSA_PRJ_JOBADMIN_ENABLED = 'JobAdminEnabled'
    DSA_PRJ_RTCP_ENABLED = 'RTCPEnabled'
    DSA_PRJ_PROTECTION_ENABLED = 'ProtectionEnabled'
    DSA_PRJ_PX_ADVANCED_RUNTIME_OPTS = 'PXAdvRTOptions'
    DSA_PRJ_PX_DEPLOY_CUSTOM_ACTION = 'PXDeployCustomAction'
    DSA_PRJ_PX_DEPLOY_JOBDIR_TEMPLATE = 'PXDeployJobDirectoryTemplate'
    DSA_PRJ_PX_BASEDIR = 'PXRemoteBaseDirectory'
    DSA_PRJ_PX_DEPLOY_GENERATE_XML = 'PXDeployGenerateXML'

    def __init__(self):
        self.__api = None
        self.__handleProj = None
        self.__handleJob = None

    def DSSetServerParams(self, domainName, userName, password, serverName):
        self.__api.DSSetServerParams.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.__api.DSSetServerParams.restype = ctypes.c_void_p

        self.__api.DSSetServerParams(encode_string(domainName), encode_string(userName),
                                     encode_string(password), encode_string(serverName))

        return True, None

    def DSGetProjectList(self):
        self.__api.DSGetProjectList.argtypes = []
        self.__api.DSGetProjectList.restype = ctypes.POINTER(ctypes.c_char)

        projectList = self.__api.DSGetProjectList()

        if not projectList:
            return None, DSAPIERROR.create_error("DSGetProjectList", self.DSGetLastError())
        else:
            return convert_char_p_to_list(projectList), None

    def DSOpenProject(self, projectName):
        self.__api.DSOpenProjectEx.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.__api.DSOpenProjectEx.restype = ctypes.POINTER(DSPROJECT)

        handleProj = self.__api.DSOpenProjectEx(self.DSAPI_VERSION, encode_string(projectName))

        if not handleProj:
            return None, DSAPIERROR.create_error("DSOpenProject", self.DSGetLastError())
        else:
            self.__handleProj = handleProj
            return handleProj, None

    def DSGetProjectInfo(self, handleProj, infoType):
        self.__api.DSGetProjectInfo.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int, ctypes.POINTER(DSPROJECTINFO)]
        self.__api.DSGetProjectInfo.restype = ctypes.c_int

        projInfo = DSPROJECTINFO()
        res = self.__api.DSGetProjectInfo(handleProj, infoType, ctypes.pointer(projInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetProjectInfo", self.DSGetLastError())

        if infoType == self.DSJ_JOBLIST:
            return convert_char_p_to_list(projInfo.info.jobList), None
        if infoType == self.DSJ_PROJECTNAME:
            return projInfo.info.projectName, None
        if infoType == self.DSJ_HOSTNAME:
            return projInfo.info.projectPath, None
        if infoType == self.DSJ_INSTALLTAG:
            return projInfo.info.hostName, None
        if infoType == self.DSJ_TCPPORT:
            return projInfo.info.installTag, None
        if infoType == self.DSJ_PROJECTPATH:
            return projInfo.info.tcpPort, None
        else:
            return '', None

    def DSGetLastError(self):
        self.__api.DSGetLastError.restype = ctypes.c_int

        self.__api.DSGetLastErrorMsg.argtypes = [ctypes.POINTER(DSPROJECT)]
        self.__api.DSGetLastErrorMsg.restype = ctypes.c_char_p

        error_code = self.__api.DSGetLastError()
        error_msg = None

        if self.__handleProj is not None:
            error_msg = decode_bytes(self.__api.DSGetLastErrorMsg(self.__handleProj))

        if not error_msg:
            error_msg = DSAPIERROR.get_error_msg(error_code)

        return {'code': error_code, 'msg': error_msg}

    def DSOpenJob(self, handleProj, jobName):
        self.__api.DSOpenJob.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
        self.__api.DSOpenJob.restype = ctypes.POINTER(DSJOB)

        handleJob = self.__api.DSOpenJob(handleProj, ctypes.c_char_p(encode_string(jobName)))

        if not handleJob:
            return None, DSAPIERROR.create_error("DSOpenJob", self.DSGetLastError())
        else:
            self.__handleJob = handleJob
            return handleJob, None

    def DSGetJobInfo(self, handleJob, infoType):
        self.__api.DSGetJobInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSJOBINFO)]
        self.__api.DSGetJobInfo.restype = ctypes.c_int

        jobInfo = DSJOBINFO()
        res = self.__api.DSGetJobInfo(handleJob, infoType, ctypes.pointer(jobInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetJobInfo", self.DSGetLastError())
        else:
            if infoType == self.DSJ_JOBSTATUS:
                return jobInfo.info.jobStatus, None
            if infoType == self.DSJ_JOBNAME:
                return jobInfo.info.jobName, None
            if infoType == self.DSJ_JOBCONTROLLER:
                return jobInfo.info.jobController, None
            if infoType == self.DSJ_JOBSTARTTIMESTAMP:
                return jobInfo.info.jobStartTime, None
            if infoType == self.DSJ_JOBWAVENO:
                return jobInfo.info.jobWaveNumber, None
            if infoType == self.DSJ_PARAMLIST:
                return convert_char_p_to_list(jobInfo.info.paramList), None
            if infoType == self.DSJ_STAGELIST:
                return convert_char_p_to_list(jobInfo.info.stageList), None
            if infoType == self.DSJ_USERSTATUS:
                return jobInfo.info.userStatus, None
            if infoType == self.DSJ_JOBCONTROL:
                return jobInfo.info.jobControl, None
            if infoType == self.DSJ_JOBPID:
                return jobInfo.info.jobPid, None
            if infoType == self.DSJ_JOBLASTTIMESTAMP:
                return jobInfo.info.jobLastTime, None
            if infoType == self.DSJ_JOBINVOCATIONS:
                return convert_char_p_to_list(jobInfo.info.jobInvocations), None
            if infoType == self.DSJ_JOBINTERIMSTATUS:
                return jobInfo.info.jobInterimStatus, None
            if infoType == self.DSJ_JOBINVOCATIONID:
                return jobInfo.info.jobInvocationId, None
            if infoType == self.DSJ_JOBDESC:
                return jobInfo.info.jobDesc, None
            if infoType == self.DSJ_STAGELIST2:
                return convert_char_p_to_list(jobInfo.info.stageList2), None
            if infoType == self.DSJ_JOBELAPSED:
                return jobInfo.info.jobElapsed, None
            if infoType == self.DSJ_JOBDMISERVICE:
                return jobInfo.info.jobDMIService, None
            if infoType == self.DSJ_JOBMULTIINVOKABLE:
                return jobInfo.info.jobMultiInvokable, None
            if infoType == self.DSJ_JOBFULLDESC:
                return jobInfo.info.jobFullDesc, None
            if infoType == self.DSJ_JOBRESTARTABLE:
                return jobInfo.info.jobRestartable, None
            else:
                return '', None

    def DSGetStageInfo(self, handleJob, stageName, infoType):
        self.__api.DSGetStageInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.c_int,
                                              ctypes.POINTER(DSSTAGEINFO)]
        self.__api.DSGetStageInfo.restype = ctypes.c_int

        stageInfo = DSSTAGEINFO()
        res = self.__api.DSGetStageInfo(handleJob, encode_string(stageName), infoType, ctypes.pointer(stageInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetStageInfo", self.DSGetLastError())
        else:
            if infoType == self.DSJ_LINKLIST:
                return convert_char_p_to_list(stageInfo.info.linkList), None
            if infoType == self.DSJ_STAGELASTERR:
                return stageInfo.info.lastError, None
            if infoType == self.DSJ_STAGENAME:
                return stageInfo.info.stageName, None
            if infoType == self.DSJ_STAGETYPE:
                return stageInfo.info.typeName, None
            if infoType == self.DSJ_STAGEINROWNUM:
                return stageInfo.info.inRowNum, None
            if infoType == self.DSJ_VARLIST:
                return convert_char_p_to_list(stageInfo.info.varList), None
            if infoType == self.DSJ_STAGESTARTTIMESTAMP:
                return stageInfo.info.stageStartTime, None
            if infoType == self.DSJ_STAGEENDTIMESTAMP:
                return stageInfo.info.stageEndTime, None
            if infoType == self.DSJ_STAGEDESC:
                return stageInfo.info.stageDesc, None
            if infoType == self.DSJ_STAGEINST:
                return convert_char_p_to_list(stageInfo.info.instList), None
            if infoType == self.DSJ_STAGECPU:
                return convert_char_p_to_list(stageInfo.info.cpuList), None
            if infoType == self.DSJ_LINKTYPES:
                return convert_char_p_to_list(stageInfo.info.linkTypes), None
            if infoType == self.DSJ_STAGEELAPSED:
                return stageInfo.info.stageElapsed, None
            if infoType == self.DSJ_STAGEPID:
                return convert_char_p_to_list(stageInfo.info.pidList), None
            if infoType == self.DSJ_STAGESTATUS:
                return stageInfo.info.stageStatus, None
            if infoType == self.DSJ_CUSTINFOLIST:
                return convert_char_p_to_list(stageInfo.info.custInfoList), None
            else:
                return '', None

    def DSGetLinkInfo(self, handleJob, stageName, linkName, infoType):
        self.__api.DSGetLinkInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
                                             ctypes.POINTER(DSLINKINFO)]
        self.__api.DSGetLinkInfo.restype = ctypes.c_int

        linkInfo = DSLINKINFO()
        res = self.__api.DSGetLinkInfo(handleJob, encode_string(stageName), encode_string(linkName), infoType,
                                       ctypes.pointer(linkInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetLinkInfo", self.DSGetLastError())
        else:
            if infoType == self.DSJ_LINKLASTERR:
                return linkInfo.info.lastError, None
            if infoType == self.DSJ_LINKNAME:
                return linkInfo.info.linkName, None
            if infoType == self.DSJ_LINKROWCOUNT:
                return linkInfo.info.rowCount, None
            if infoType == self.DSJ_LINKSQLSTATE:
                return linkInfo.info.linkSQLState, None
            if infoType == self.DSJ_LINKDBMSCODE:
                return linkInfo.info.linkDBMSCode, None
            if infoType == self.DSJ_LINKDESC:
                return linkInfo.info.linkDesc, None
            if infoType == self.DSJ_LINKSTAGE:
                return linkInfo.info.linkedStage, None
            if infoType == self.DSJ_INSTROWCOUNT:
                return convert_char_p_to_list(linkInfo.info.rowCountList), None
            if infoType == self.DSJ_LINKEXTROWCOUNT:
                return convert_char_p_to_list(linkInfo.info.rowCountList), None
            else:
                return '', None

    def DSGetVarInfo(self, handleJob, stageName, varName, infoType):
        self.__api.DSGetVarInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
                                            ctypes.POINTER(DSVARINFO)]
        self.__api.DSGetVarInfo.restype = ctypes.c_int

        varInfo = DSVARINFO()
        res = self.__api.DSGetVarInfo(handleJob, encode_string(stageName), encode_string(varName), infoType,
                                      ctypes.pointer(varInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetVarInfo", self.DSGetLastError())
        else:
            if infoType == self.DSJ_VARVALUE:
                return varInfo.info.varValue, None
            if infoType == self.DSJ_VARDESC:
                return varInfo.info.varDesc, None
            else:
                return '', None

    def DSFindFirstLogEntry(self, handleJob, eventType=DSJ_LOGANY, startTime=0, endTime=0, maxNumber=500):
        self.__api.DSFindFirstLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, time_t, time_t, ctypes.c_int,
                                                   ctypes.POINTER(DSLOGEVENT)]
        self.__api.DSFindFirstLogEntry.restype = ctypes.c_int

        logInfo = DSLOGEVENT()
        res = self.__api.DSFindFirstLogEntry(handleJob, eventType, startTime, endTime, maxNumber,
                                             ctypes.pointer(logInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSFindFirstLogEntry", self.DSGetLastError())
        else:
            return logInfo, None

    def DSFindNextLogEntry(self, handleJob):
        self.__api.DSFindNextLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.POINTER(DSLOGEVENT)]
        self.__api.DSFindNextLogEntry.restype = ctypes.c_int

        logEvent = DSLOGEVENT()
        res = self.__api.DSFindNextLogEntry(handleJob, ctypes.pointer(logEvent))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSFindNextLogEntry", self.DSGetLastError())
        else:
            return logEvent, None

    def DSGetLogEntryFull(self, handleJob, eventId):
        self.__api.DSGetLogEntryFull.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSLOGDETAILFULL)]
        self.__api.DSGetLogEntryFull.restype = ctypes.c_int

        logDetail = DSLOGDETAILFULL()
        res = self.__api.DSGetLogEntryFull(handleJob, eventId, ctypes.pointer(logDetail))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetLogEntryFull", self.DSGetLastError())
        else:
            return logDetail, None

    def DSGetLogEntry(self, handleJob, eventId):
        self.__api.DSGetLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSLOGDETAIL)]
        self.__api.DSGetLogEntry.restype = ctypes.c_int

        logDetail = DSLOGDETAIL()
        res = self.__api.DSGetLogEntry(handleJob, eventId, ctypes.pointer(logDetail))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetLogEntry", self.DSGetLastError())
        else:
            return logDetail, None

    def DSGetNewestLogId(self, handleJob, eventType):
        self.__api.DSGetNewestLogId.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
        self.__api.DSGetNewestLogId.restype = ctypes.c_int

        lastLogId = self.__api.DSGetNewestLogId(handleJob, eventType)

        if lastLogId == -1:
            return None, DSAPIERROR.create_error("DSGetNewestLogId", self.DSGetLastError())
        else:
            return lastLogId, None

    def DSGetLogEventIds(self, handleJob, runNumber=0, filter=''):
        self.__api.DSGetLogEventIds.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_char_p,
                                                ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
        self.__api.DSGetLogEventIds.restype = ctypes.c_int

        eventsPointer = ctypes.POINTER(ctypes.c_char)()
        res = self.__api.DSGetLogEventIds(handleJob, runNumber, encode_string(filter), ctypes.pointer(eventsPointer))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetLogEventIds", self.DSGetLastError())
        else:
            return convert_char_p_to_list(eventsPointer), None

    def DSGetQueueList(self):
        self.__api.DSGetQueueList.restype = ctypes.POINTER(ctypes.c_char)
        qList = self.__api.DSGetQueueList()

        return convert_char_p_to_list(qList), None

    def DSSetJobQueue(self, handleJob, queueName):
        self.__api.DSSetJobQueue.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p]
        self.__api.DSSetJobQueue.restype = ctypes.c_int

        res = self.__api.DSSetJobQueue(handleJob, queueName)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetJobQueue", self.DSGetLastError())
        else:
            return 0, None

    def DSCloseJob(self, handleJob):
        self.__api.DSCloseJob.argtypes = [ctypes.POINTER(DSJOB)]
        self.__api.DSCloseJob.restype = ctypes.c_int

        res = self.__api.DSCloseJob(handleJob)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSCloseJob", self.DSGetLastError())
        else:
            return 0, None

    def DSCloseProject(self, handleProj):
        self.__api.DSCloseProject.argtypes = [ctypes.POINTER(DSPROJECT)]
        self.__api.DSCloseProject.restype = ctypes.c_int

        res = self.__api.DSCloseProject(handleProj)
        self.__handleProj = None

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSCloseProject", self.DSGetLastError())
        else:
            return 0, None

    def DSSetJobLimit(self, handleJob, limitType, limitValue):
        self.__api.DSSetJobLimit.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_int]
        self.__api.DSSetJobLimit.restype = ctypes.c_int

        res = self.__api.DSSetJobLimit(handleJob, limitType, limitValue)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetJobLimit", self.DSGetLastError())
        else:
            return 0, None

    def DSPurgeJob(self, handleJob, purgeSpec):
        self.__api.DSPurgeJob.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
        self.__api.DSPurgeJob.restype = ctypes.c_int

        res = self.__api.DSPurgeJob(handleJob, purgeSpec)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSPurgeJob", self.DSGetLastError())
        else:
            return 0, None

    def DSRunJob(self, handleJob, runMode):
        self.__api.DSRunJob.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
        self.__api.DSRunJob.restype = ctypes.c_int

        res = self.__api.DSRunJob(handleJob, runMode)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSRunJob", self.DSGetLastError())
        else:
            return 0, None

    def DSStopJob(self, handleJob):
        self.__api.DSStopJob.argtypes = [ctypes.POINTER(DSJOB)]
        self.__api.DSStopJob.restype = ctypes.c_int

        res = self.__api.DSStopJob(handleJob)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSStopJob", self.DSGetLastError())
        else:
            return 0, None

    def DSLockJob(self, handleJob):
        self.__api.DSLockJob.argtypes = [ctypes.POINTER(DSJOB)]
        self.__api.DSLockJob.restype = ctypes.c_int

        res = self.__api.DSLockJob(handleJob)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSLockJob", self.DSGetLastError())
        else:
            return 0, None

    def DSUnlockJob(self, handleJob):
        self.__api.DSUnlockJob.argtypes = [ctypes.POINTER(DSJOB)]
        self.__api.DSUnlockJob.restype = ctypes.c_int

        res = self.__api.DSUnlockJob(handleJob)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSUnlockJob", self.DSGetLastError())
        else:
            return 0, None

    def DSWaitForJob(self, handleJob):
        self.__api.DSWaitForJob.argtypes = [ctypes.POINTER(DSJOB)]
        self.__api.DSWaitForJob.restype = ctypes.c_int

        res = self.__api.DSWaitForJob(handleJob)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSWaitForJob", self.DSGetLastError())
        else:
            return 0, None

    def DSSetParam(self, handleJob, paramName, param):
        self.__api.DSSetParam.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.POINTER(DSPARAM)]
        self.__api.DSSetParam.restype = ctypes.c_int

        res = self.__api.DSSetParam(handleJob, encode_string(paramName), ctypes.pointer(param))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetParam", self.DSGetLastError())
        else:
            return 0, None

    def DSGetParamInfo(self, handleJob, paramName):
        self.__api.DSGetParamInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.POINTER(DSPARAMINFO)]
        self.__api.DSGetParamInfo.restype = ctypes.c_int

        paramInfo = DSPARAMINFO()
        res = self.__api.DSGetParamInfo(handleJob, encode_string(paramName), ctypes.pointer(paramInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSGetParamInfo", self.DSGetLastError())
        else:
            return paramInfo, None

    def DSMakeJobReport(self, handleJob, reportType, lineSeparator='CRLF'):
        self.__api.DSMakeJobReport.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_char_p,
                                               ctypes.POINTER(DSREPORTINFO)]
        self.__api.DSMakeJobReport.restype = ctypes.c_int

        reportInfo = DSREPORTINFO()
        res = self.__api.DSMakeJobReport(handleJob, reportType, encode_string(lineSeparator),
                                         ctypes.pointer(reportInfo))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSMakeJobReport", self.DSGetLastError())
        else:
            return reportInfo.info.reportText, None

    def DSGetReposUsage(self, handleProj, relationshipType, objectName, recursive=0):
        self.__api.DSGetReposUsage.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                                               ctypes.POINTER(DSREPOSUSAGE)]
        self.__api.DSGetReposUsage.restype = ctypes.c_int

        reposUsage = DSREPOSUSAGE()
        res = self.__api.DSGetReposUsage(handleProj, relationshipType, encode_string(objectName), recursive,
                                         ctypes.pointer(reposUsage))

        if res > 0:
            return reposUsage.info.jobs.contents, None
        if res == 0:
            return None, None

        return None, DSAPIERROR.create_error("DSGetReposUsage", self.DSGetLastError())

    def DSGetReposInfo(self, handleProj, objectType, infoType, searchCriteria, startingCategory, subcategories=1):
        self.__api.DSGetReposInfo.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int, ctypes.c_int, ctypes.c_char_p,
                                              ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(DSREPOSINFO)]
        self.__api.DSGetReposInfo.restype = ctypes.c_int

        reposInfo = DSREPOSINFO()
        res = self.__api.DSGetReposInfo(handleProj, objectType, infoType, encode_string(searchCriteria),
                                        encode_string(startingCategory), subcategories, ctypes.pointer(reposInfo))

        if res > 0:
            return reposInfo.info.jobs.contents, None
        if res == 0:
            return None, None

        return None, DSAPIERROR.create_error("DSGetReposInfo", self.DSGetLastError())

    def DSLogEvent(self, handleJob, eventType, message):
        self.__api.DSLogEvent.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
        self.__api.DSLogEvent.restype = ctypes.c_int

        res = self.__api.DSLogEvent(handleJob, eventType, encode_string(''), encode_string(message))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSLogEvent", self.DSGetLastError())
        else:
            return 0, None

    def DSAddEnvVar(self, handleProj, envVarName, varType, promptText, value):
        self.__api.DSAddEnvVar.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                                           ctypes.c_char_p]
        self.__api.DSAddEnvVar.restype = ctypes.c_int

        res = self.__api.DSAddEnvVar(handleProj, encode_string(envVarName), encode_string(varType),
                                     encode_string(promptText), encode_string(value))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSAddEnvVar", self.DSGetLastError())
        else:
            return 0, None

    def DSDeleteEnvVar(self, handleProj, envVarName):
        self.__api.DSDeleteEnvVar.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
        self.__api.DSDeleteEnvVar.restype = ctypes.c_int

        res = self.__api.DSDeleteEnvVar(handleProj, encode_string(envVarName))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSDeleteEnvVar", self.DSGetLastError())
        else:
            return 0, None

    def DSSetEnvVar(self, handleProj, envVarName, value):
        self.__api.DSSetEnvVar.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p]
        self.__api.DSSetEnvVar.restype = ctypes.c_int

        res = self.__api.DSSetEnvVar(handleProj, encode_string(envVarName), encode_string(value))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetEnvVar", self.DSGetLastError())
        else:
            return 0, None

    def DSListEnvVars(self, handleProj):
        self.__api.DSListEnvVars.argtypes = [ctypes.POINTER(DSPROJECT)]
        self.__api.DSListEnvVars.restype = ctypes.POINTER(ctypes.c_char)

        varList = self.__api.DSListEnvVars(handleProj)

        if not varList:
            return None, DSAPIERROR.create_error("DSListEnvVars", self.DSGetLastError())
        else:
            return convert_char_p_to_list(varList), None

    def DSAddProject(self, projectName, projectLocation=''):
        self.__api.DSAddProject.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.__api.DSAddProject.restype = ctypes.c_int

        res = self.__api.DSAddProject(encode_string(projectName), encode_string(projectLocation))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSAddProject", self.DSGetLastError())
        else:
            return 0, None

    def DSDeleteProject(self, projectName):
        self.__api.DSDeleteProject.argtypes = [ctypes.c_char_p]
        self.__api.DSDeleteProject.restype = ctypes.c_int

        res = self.__api.DSDeleteProject(encode_string(projectName))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSDeleteProject", self.DSGetLastError())
        else:
            return 0, None

    def DSGetIdForJob(self, handleProj, jobName):
        self.__api.DSGetIdForJob.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
        self.__api.DSGetIdForJob.restype = ctypes.c_char_p

        jobId = self.__api.DSGetIdForJob(handleProj, encode_string(jobName))

        if not jobId:
            return None, DSAPIERROR.create_error("DSGetIdForJob", self.DSGetLastError())
        else:
            return jobId, None

    def DSSetIdForJob(self, handleProj, jobName, jobId):
        self.__api.DSSetIdForJob.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p]
        self.__api.DSSetIdForJob.restype = ctypes.c_int

        res = self.__api.DSSetIdForJob(handleProj, encode_string(jobName), encode_string(jobId))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetIdForJob", self.DSGetLastError())
        else:
            return 0, None

    def DSJobNameFromJobId(self, handleProj, jobId):
        self.__api.DSJobNameFromJobId.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
        self.__api.DSJobNameFromJobId.restype = ctypes.c_char_p

        jobName = self.__api.DSJobNameFromJobId(handleProj, encode_string(jobId))

        if not jobName:
            return None, DSAPIERROR.create_error("DSJobNameFromJobId", self.DSGetLastError())
        else:
            return jobName, None

    def DSServerMessage(self, defMsg, prms=None, msgIdStr='', sizeMessage=1000):
        # How to use messages from the msg.text file?
        # Where to find another message ids? For example DSTAGE_JSG_M_0001-DSTAGE_JSG_M_0075
        # Why [L] and [E] are not replaced?
        # What errors are possible?
        if prms is None:
            prms = []

        if not isinstance(prms, list):
            return None, DSAPIERROR.create_error("DSServerMessage", "Variable prms must be a list")

        maxPrms = len(prms)

        self.__api.DSServerMessage.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p * maxPrms,
                                               ctypes.c_char_p, ctypes.c_int]
        self.__api.DSServerMessage.restype = ctypes.c_int

        encodedPrms = [encode_string(str(prm)) for prm in prms]
        resMessage = ctypes.c_char_p(encode_string(''))

        msgSize = self.__api.DSServerMessage(encode_string(msgIdStr), encode_string(defMsg),
                                             (ctypes.c_char_p * maxPrms)(*encodedPrms), resMessage, sizeMessage)

        if not resMessage:
            return None, DSAPIERROR.create_error("DSServerMessage", self.DSGetLastError())
        else:
            return resMessage.value, None

    def DSSetProjectProperty(self, handleProj, property, value):
        self.__api.DSSetProjectProperty.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p]
        self.__api.DSSetProjectProperty.restype = ctypes.c_int

        res = self.__api.DSSetProjectProperty(handleProj, encode_string(property), encode_string(value))

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetProjectProperty", self.DSGetLastError())
        else:
            return 0, None

    def DSListProjectProperties(self, handleProj):
        self.__api.DSListProjectProperties.argtypes = [ctypes.POINTER(DSPROJECT)]
        self.__api.DSListProjectProperties.restype = ctypes.POINTER(ctypes.c_char)

        propList = self.__api.DSListProjectProperties(handleProj)

        if not propList:
            return None, DSAPIERROR.create_error("DSListProjectProperties", self.DSGetLastError())
        else:
            return convert_char_p_to_list(propList), None

    def DSGetWLMEnabled(self):
        self.__api.DSGetWLMEnabled.argtypes = []
        self.__api.DSGetWLMEnabled.restype = ctypes.c_int

        wlmEnabled = self.__api.DSGetWLMEnabled()

        if not wlmEnabled:
            return None, DSAPIERROR.create_error("DSGetWLMEnabled", self.DSGetLastError())
        else:
            return 0, None

    def DSSetGenerateOpMetaData(self, handleJob, value):
        self.__api.DSSetGenerateOpMetaData.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
        self.__api.DSSetGenerateOpMetaData.restype = ctypes.c_int

        res = self.__api.DSSetGenerateOpMetaData(handleJob, value)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetGenerateOpMetaData", self.DSGetLastError())
        else:
            return 0, None

    def DSSetDisableProjectHandler(self, handleProj, value):
        # Does function work incorrectly due to bad definition in dsapi.h?
        self.__api.DSSetDisableProjectHandler.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int]
        self.__api.DSSetDisableProjectHandler.restype = ctypes.c_int

        res = self.__api.DSSetDisableProjectHandler(handleProj, value)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetDisableProjectHandler", self.DSGetLastError())
        else:
            return 0, None

    def DSSetDisableJobHandler(self, handleJob, value):
        self.__api.DSSetDisableJobHandler.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
        self.__api.DSSetDisableJobHandler.restype = ctypes.c_int

        res = self.__api.DSSetDisableJobHandler(handleJob, value)

        if res != DSAPIERROR.DSJE_NOERROR:
            return None, DSAPIERROR.create_error("DSSetDisableJobHandler", self.DSGetLastError())
        else:
            return 0, None

    def DSLoadLibrary(self, api_lib_file):
        """
        api_lib_file - full path to DataStage API library
            vmdsapi.dll on windows
            or
            libvmdsapi.so on *nix

        PATH on windows should include directory where file 'vmdsapi.dll' is located
        in most cases, in the '../IBM/InformationServer/Clients/Classic/'

        LD_LIBRARY_PATH on *nix should include directory where file 'libvmdsapi.so' and its dependencies are located
        in most cases, in the '../IBM/InformationServer/Server/DSEngine/lib/'
        """

        if not os.path.exists(api_lib_file) or not os.path.isfile(api_lib_file):
            return None, DSAPIERROR.create_error("DSLoadLibrary", "Path to {} doesn't exist".format(api_lib_file))

        try:
            self.__api = ctypes.CDLL(api_lib_file)
        except OSError as e:
            return None, DSAPIERROR.create_error("DSLoadLibrary", "Can't load the library: {}".format(str(e)))

        return True, None

    def DSUnloadLibrary(self):
        self.__api = None
        self.__handleProj = None
        self.__handleJob = None
