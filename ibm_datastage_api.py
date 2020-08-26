import ctypes
import os

# TYPES
from sys import platform as _platform_name

if _platform_name.startswith('win'):
   time_t = ctypes.c_uint32
else:
   time_t = ctypes.c_uint64

# API STRUCTURES
class DSPROJECT(ctypes.Structure):
   _fields_ = [("dsapiVersionNo", ctypes.c_int),
               ("sessionId",      ctypes.c_int),
               ("valueMark",      ctypes.c_ubyte),
               ("fieldMark",      ctypes.c_ubyte)]

class DSJOB(ctypes.Structure):
   _fields_ = [("hProject",        ctypes.POINTER(DSPROJECT)),
               ("serverJobHandle", ctypes.c_char_p),
               ("logData",         ctypes.c_char_p),
               ("logDataLen",      ctypes.c_int),
               ("logDataPsn",      ctypes.c_int)]

class DSJOBINFO_info(ctypes.Union):
   _fields_ = [("jobStatus",         ctypes.c_int),
               ("jobController",     ctypes.c_char_p),
               ("jobStartTime",      time_t),
               ("jobWaveNumber",     ctypes.c_int),
               ("userStatus",        ctypes.c_char_p),
               ("stageList",         ctypes.POINTER(ctypes.c_char)),
               ("paramList",         ctypes.POINTER(ctypes.c_char)),
               ("jobName",           ctypes.c_char_p),
               ("jobControl",        ctypes.c_int),
               ("jobPid",            ctypes.c_int),
               ("jobLastTime",       time_t),
               ("jobInvocations",    ctypes.POINTER(ctypes.c_char)),
               ("jobInterimStatus",  ctypes.c_int),
               ("jobInvocationId",   ctypes.c_char_p),
               ("jobDesc",           ctypes.c_char_p),
               ("stageList2",        ctypes.POINTER(ctypes.c_char)),
               ("jobElapsed",        ctypes.c_int),
               ("jobDMIService",     ctypes.c_int),
               ("jobMultiInvokable", ctypes.c_int),
               ("jobFullDesc",       ctypes.c_char_p),
               ("jobRestartable",    ctypes.c_int)]

class DSJOBINFO(ctypes.Structure):
   _fields_ = [("infoType", ctypes.c_int),
               ("info",     DSJOBINFO_info)]

class DSPROJECTINFO_info(ctypes.Union):
   _fields_ = [("jobList",      ctypes.POINTER(ctypes.c_char)),
               ("projectName",  ctypes.c_char_p),
               ("projectPath",  ctypes.c_char_p),
               ("hostName",     ctypes.c_char_p),
               ("installTag",   ctypes.c_char_p),
               ("tcpPort",      ctypes.c_char_p)]

class DSPROJECTINFO(ctypes.Structure):
   _fields_ = [("infoType", ctypes.c_int),
               ("info",     DSPROJECTINFO_info)]

class DSLOGEVENT(ctypes.Structure):
   _fields_ = [("eventId",   ctypes.c_int),
               ("timestamp", time_t),
               ("type",      ctypes.c_int),
               ("message",   ctypes.c_char_p)]

class DSLOGDETAILFULL(ctypes.Structure):
   _fields_ = [("eventId",      ctypes.c_int),
               ("timestamp",    time_t),
               ("type",         ctypes.c_int),
               ("username",     ctypes.c_char_p),
               ("fullMessage",  ctypes.POINTER(ctypes.c_char)),
               ("messageId",    ctypes.c_char_p),
               ("invocationId", ctypes.c_char_p)]

class DSLOGDETAIL(ctypes.Structure):
   _fields_ = [("eventId",      ctypes.c_int),
               ("timestamp",    time_t),
               ("type",         ctypes.c_int),
               ("username",     ctypes.c_char_p),
               ("fullMessage",  ctypes.POINTER(ctypes.c_char))]

class DSPARAM_value(ctypes.Union):
   _fields_ = [("pString",    ctypes.c_char_p),
               ("pEncrypt",   ctypes.c_char_p),
               ("pInt",       ctypes.c_int),
               ("pFloat",     ctypes.c_float),
               ("pPath",      ctypes.c_char_p),
               ("pListValue", ctypes.c_char_p),
               ("pDate",      ctypes.c_char_p),
               ("pTime",      ctypes.c_char_p)]

class DSPARAM(ctypes.Structure):
   _fields_ = [("paramType",  ctypes.c_int),
               ("paramValue", DSPARAM_value)]

class DSPARAMINFO(ctypes.Structure):
   _fields_ = [("defaultValue",    DSPARAM),
               ("helpText",        ctypes.c_char_p),
               ("paramPrompt",     ctypes.c_char_p),
               ("paramType",       ctypes.c_int),
               ("desDefaultValue", DSPARAM),
               ("listValues",      ctypes.c_char_p),
               ("desListValues",   ctypes.c_char_p),
               ("promptAtRun",     ctypes.c_int)]

class DSREPORTINFO_info(ctypes.Union):
   _fields_ = [("reportText", ctypes.c_char_p)]

class DSREPORTINFO(ctypes.Structure):
   _fields_ = [("reportType",  ctypes.c_int),
               ("info",        DSREPORTINFO_info)]

class DSREPOSUSAGEJOB(ctypes.Structure):
   pass
DSREPOSUSAGEJOB._fields_ = [("jobname",  ctypes.c_char_p),
                            ("jobtype",  ctypes.c_int),
                            ("nextjob",  ctypes.POINTER(DSREPOSUSAGEJOB)),
                            ("childjob", ctypes.POINTER(DSREPOSUSAGEJOB))]

class DSREPOSUSAGE_info(ctypes.Union):
   _fields_ = [("jobs", ctypes.POINTER(DSREPOSUSAGEJOB))]

class DSREPOSUSAGE(ctypes.Structure):
   _fields_ = [("infoType", ctypes.c_int),
               ("info",     DSREPOSUSAGE_info)]

class DSREPOSJOBINFO(ctypes.Structure):
   pass
DSREPOSJOBINFO._fields_ = [("jobname", ctypes.c_char_p),
                           ("jobtype", ctypes.c_int),
                           ("nextjob", ctypes.POINTER(DSREPOSJOBINFO))]

class DSREPOSINFO_info(ctypes.Union):
   _fields_ = [("jobs", ctypes.POINTER(DSREPOSJOBINFO))]

class DSREPOSINFO(ctypes.Structure):
   _fields_ = [("infoType", ctypes.c_int),
               ("info",     DSREPOSINFO_info)]

class DSSTAGEINFO_info(ctypes.Union):
   _fields_ = [("lastError",      DSLOGDETAIL),
               ("typeName",       ctypes.c_char_p),
               ("inRowNum",       ctypes.c_int),
               ("linkList",       ctypes.POINTER(ctypes.c_char)),
               ("stageName",      ctypes.c_char_p),
               ("varList",        ctypes.POINTER(ctypes.c_char)),
               ("stageStartTime", time_t),
               ("stageEndTime",   time_t),
               ("linkTypes",      ctypes.POINTER(ctypes.c_char)),
               ("stageDesc",      ctypes.c_char_p),
               ("instList",       ctypes.POINTER(ctypes.c_char)),
               ("cpuList",        ctypes.POINTER(ctypes.c_char)),
               ("stageElapsed",   ctypes.c_char_p),
               ("pidList",        ctypes.POINTER(ctypes.c_char)),
               ("stageStatus",    ctypes.c_int),
               ("custInfoList",   ctypes.POINTER(ctypes.c_char))]

class DSSTAGEINFO(ctypes.Structure):
   _fields_ = [("infoType", ctypes.c_int),
               ("info",     DSSTAGEINFO_info)]

class DSLINKINFO_info(ctypes.Union):
   _fields_ = [("lastError",    DSLOGDETAIL),
               ("rowCount",     ctypes.c_int),
               ("linkName",     ctypes.c_char_p),
               ("linkSQLState", ctypes.c_char_p),
               ("linkDBMSCode", ctypes.c_char_p),
               ("linkDesc",     ctypes.c_char_p),
               ("linkedStage",  ctypes.c_char_p),
               ("rowCountList", ctypes.POINTER(ctypes.c_char))]

class DSLINKINFO(ctypes.Structure):
   _fields_ = [("infoType", ctypes.c_int),
               ("info",     DSLINKINFO_info)]

# API INTERFACE
class DSAPI:
   # API Version
   DSAPI_VERSION = 1

   # DSJOBINFO 'jobStatus' values
   DSJS_RUNNING     = 0  # Job running
   DSJS_RUNOK       = 1  # Job finished a normal run with no warnings
   DSJS_RUNWARN     = 2  # Job finished a normal run with warnings
   DSJS_RUNFAILED   = 3  # Job finished a normal run with a fatal error
   DSJS_QUEUED      = 4  # Job queued waiting for resource allocation
   DSJS_VALOK       = 11 # Job finished a validation run with no warnings
   DSJS_VALWARN     = 12 # Job finished a validation run with warnings
   DSJS_VALFAILED   = 13 # Job failed a validation run
   DSJS_RESET       = 21 # Job finished a reset run
   DSJS_CRASHED     = 96 # Job was stopped by some indeterminate action
   DSJS_STOPPED     = 97 # Job was stopped by operator intervention (can't tell run type)
   DSJS_NOTRUNNABLE = 98 # Job has not been compiled
   DSJS_NOTRUNNING  = 99 # Any other status

   # DSJOBINFO 'infoType' values
   DSJ_JOBSTATUS         = 1  # Current status of the job.
   DSJ_JOBNAME           = 2  # Name of the job referenced by JobHandle.
   DSJ_JOBCONTROLLER     = 3  # Name of job controlling the job referenced by JobHandle.
   DSJ_JOBSTARTTIMESTAMP = 4  # Date and time when the job started.
   DSJ_JOBWAVENO         = 5  # Wave number of last or current run.
   DSJ_PARAMLIST         = 6  # List of job parameter names
   DSJ_STAGELIST         = 7  # List of names of stages in job
   DSJ_USERSTATUS        = 8  # Value, if any,  set as the user status by the job.
   DSJ_JOBCONTROL        = 9  # Job control STOP/SUSPEND/RESUME
   DSJ_JOBPID            = 10 # Process id of DSD.RUN process
   DSJ_JOBLASTTIMESTAMP  = 11 # Server date/time of job last finished: "YYYY-MM-DD HH:MM:SS"
   DSJ_JOBINVOCATIONS    = 12 # Comma-separated list of job invocation ids
   DSJ_JOBINTERIMSTATUS  = 13 # Current interim status of job
   DSJ_JOBINVOCATIONID   = 14 # Invocation name of the job referenced
   DSJ_JOBDESC           = 15 # Job description
   DSJ_STAGELIST2        = 16 # list of stages not in DSJ.STAGELIST
   DSJ_JOBELAPSED        = 17 # Job Elapsed time in seconds
   DSJ_JOBEOTCOUNT       = 18 # Count of EndOfTransmission blocks processed by this job so far
   DSJ_JOBEOTTIMESTAMP   = 19 # Date/time of the last EndOfTransmission block processed by this job
   DSJ_JOBDMISERVICE     = 20 # Job is a DMI (aka WEB) service
   DSJ_JOBMULTIINVOKABLE = 21 # Job can be multiply invoked
   DSJ_JOBFULLDESC       = 22 # Full job description
   DSJ_JOBRESTARTABLE    = 24 # Job can be restarted

   # DSPROJECTINFO 'infoType' values
   DSJ_JOBLIST     = 1 # List of jobs in project
   DSJ_PROJECTNAME = 2 # Name of current project
   DSJ_HOSTNAME    = 3 # Host name of the server
   DSJ_INSTALLTAG  = 4 # Install tag of the server DSEngine
   DSJ_TCPPORT     = 5 # TCP port    of the server DSEngine
   DSJ_PROJECTPATH = 6 # Directory path of current project

   # DSSTAGEINFO 'infoType' values
   DSJ_LINKLIST            = 1  # List of stage link names
   DSJ_STAGELASTERR        = 2  # Last error message reported from any link of the stage.
   DSJ_STAGENAME           = 3  # Actual name of stage
   DSJ_STAGETYPE           = 4  # Stage type name.
   DSJ_STAGEINROWNUM       = 5  # Primary links input row number.
   DSJ_VARLIST             = 6  # List of stage variable names
   DSJ_STAGESTARTTIMESTAMP = 7  # Date and time when stage started
   DSJ_STAGEENDTIMESTAMP   = 8  # Date and time when stage finished
   DSJ_STAGEDESC           = 9  # Stage Description
   DSJ_STAGEINST           = 10 # Comma-seperated list of stage instance ids
   DSJ_STAGECPU            = 11 # Comma-seperated list of stage instance CPU in seconds
   DSJ_LINKTYPES           = 12 # Comma-seperated list of link types
   DSJ_STAGEELAPSED        = 13 # Stage elapsed time in seconds
   DSJ_STAGEPID            = 14 # Comma-seperated list of stage instance PIDs
   DSJ_STAGESTATUS         = 15 # Stage status
   DSJ_STAGEEOTCOUNT       = 16 # Count of EndOfTransmission blocks processed by this stage so far.
   DSJ_STAGEEOTTIMESTAMP   = 17 # Data/time of last EndOfTransmission block received by this stage.
   DSJ_CUSTINFOLIST        = 18 # List of custom info names

   # DSLINKINFO 'infoType' values
   DSJ_LINKLASTERR     = 1  # Last error message reported by link.
   DSJ_LINKNAME        = 2  # Actual name of link
   DSJ_LINKROWCOUNT    = 3  # Number of rows that have passed down the link.
   DSJ_LINKSQLSTATE    = 4  # SQLSTATE value from Last error message
   DSJ_LINKDBMSCODE    = 5  # DBMSCODE value from Last error message
   DSJ_LINKDESC        = 6  # Link description
   DSJ_LINKSTAGE       = 7  # Stage at other end of link
   DSJ_INSTROWCOUNT    = 8  # Comma seperated list of rowcounts for each stage instance
   DSJ_LINKEOTROWCOUNT = 9  # Row count since last EndOfTransmission block.
   DSJ_LINKEXTROWCOUNT = 10 # Extended rowcount, using strings

   # DSLOGDETAILFULL 'eventType' values
   DSJ_LOGINFO     = 1  # Information message.
   DSJ_LOGWARNING  = 2  # Warning message.
   DSJ_LOGFATAL    = 3  # Fatal error message.
   DSJ_LOGREJECT   = 4  # Rejected row message.
   DSJ_LOGSTARTED  = 5  # Job started message.
   DSJ_LOGRESET    = 6  # Job reset message.
   DSJ_LOGBATCH    = 7  # Batch control
   DSJ_LOGOTHER    = 98 # Category other than above
   DSJ_LOGANY      = 99 # Any type of event

   # DSRUNJOB 'runMode' values
   DSJ_RUNNORMAL   = 1 # Standard job run.
   DSJ_RUNRESET    = 2 # Job is to be reset.
   DSJ_RUNVALIDATE = 3 # Job is to be validated only.
   DSJ_RUNRESTART  = 4 # Restart job with previous parameters, job must be in Restartable state.

   # DSPARAM 'paramType' values
   DSJ_PARAMTYPE_STRING    = 0
   DSJ_PARAMTYPE_ENCRYPTED = 1
   DSJ_PARAMTYPE_INTEGER   = 2
   DSJ_PARAMTYPE_FLOAT     = 3
   DSJ_PARAMTYPE_PATHNAME  = 4
   DSJ_PARAMTYPE_LIST      = 5
   DSJ_PARAMTYPE_DATE      = 6
   DSJ_PARAMTYPE_TIME      = 7

   # DSREPORTINFO 'reportType' values
   DSJ_REPORT0 = 0 # Basic
   DSJ_REPORT1 = 1 # Stage/link detail
   DSJ_REPORT2 = 2 # Text string containing full XML report

   # DSREPOSUSAGEJOB 'relationshipType' values
   DSS_JOB_USES_JOB                   = 1
   DSS_JOB_USEDBY_JOB                 = 2
   DSS_JOB_HASSOURCE_TABLEDEF         = 3
   DSS_JOB_HASTARGET_TABLEDEF         = 4
   DSS_JOB_HASSOURCEORTARGET_TABLEDEF = 5

   # DSREPOSINFO 'infoType' values
   DSS_JOBS          = 1  # The Object Type to return
   DSS_JOB_ALL       = 15 # list all jobs
   DSS_JOB_SERVER    = 1  # list all server jobs
   DSS_JOB_PARALLEL  = 2  # list all parallel jobs
   DSS_JOB_MAINFRAME = 4  # list all mainframe jobs
   DSS_JOB_SEQUENCE  = 8  # list all sequence jobs

   # DSAddEnvVar 'varType' values
   DSA_ENVVAR_TYPE_STRING    = 'String'
   DSA_ENVVAR_TYPE_ENCRYPTED = 'Encrypted'

   # DSSetJobLimit 'limitType' values
   DSJ_LIMITWARN = 1 # Job to be stopped after LimitValue warning events
   DSJ_LIMITROWS = 2 # Stages to be limited to LimitValue rows

   # DSSetProjectProperty 'property' values
   DSA_OSHVISIBLEFLAG                = 'OSHVisibleFlag'
   DSA_PRJ_JOBADMIN_ENABLED          = 'JobAdminEnabled'
   DSA_PRJ_RTCP_ENABLED              = 'RTCPEnabled'
   DSA_PRJ_PROTECTION_ENABLED        = 'ProtectionEnabled'
   DSA_PRJ_PX_ADVANCED_RUNTIME_OPTS  = 'PXAdvRTOptions'
   DSA_PRJ_PX_DEPLOY_CUSTOM_ACTION   = 'PXDeployCustomAction'
   DSA_PRJ_PX_DEPLOY_JOBDIR_TEMPLATE = 'PXDeployJobDirectoryTemplate'
   DSA_PRJ_PX_BASEDIR                = 'PXRemoteBaseDirectory'
   DSA_PRJ_PX_DEPLOY_GENERATE_XML    = 'PXDeployGenerateXML'

   def __init__(self):
      self.__api        = None
      self.__handleProj = None

   # API FUNCTIONS
   def DSSetServerParams(self, domainName, userName, password, serverName):
      self.__api.DSSetServerParams.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
      self.__api.DSSetServerParams.restype  = ctypes.c_void_p

      self.__api.DSSetServerParams(self.encodeString(domainName), self.encodeString(userName), self.encodeString(password), self.encodeString(serverName))

      return True, None

   def DSGetProjectList(self):
      self.__api.DSGetProjectList.argtypes = []
      self.__api.DSGetProjectList.restype  = ctypes.POINTER(ctypes.c_char)

      projectList = self.__api.DSGetProjectList()

      if not projectList:
         return None, self.createError("DSGetProjectList", self.DSGetLastError())
      else:
         return self.charPointerToList(projectList), None

   def DSOpenProject(self, projectName):
      self.__api.DSOpenProjectEx.argtypes = [ctypes.c_int, ctypes.c_char_p]
      self.__api.DSOpenProjectEx.restype  = ctypes.POINTER(DSPROJECT)

      handleProj = self.__api.DSOpenProjectEx(self.DSAPI_VERSION, self.encodeString(projectName))

      if not handleProj:
         return None, self.createError("DSOpenProject", self.DSGetLastError())
      else:
         self.__handleProj = handleProj
         return handleProj, None

   def DSGetProjectInfo(self, handleProj, infoType):
      self.__api.DSGetProjectInfo.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int, ctypes.POINTER(DSPROJECTINFO)]
      self.__api.DSGetProjectInfo.restype  = ctypes.c_int

      projInfo = DSPROJECTINFO()
      res = self.__api.DSGetProjectInfo(handleProj, infoType, ctypes.pointer(projInfo))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetProjectInfo", self.DSGetLastError())

      if infoType == self.DSJ_JOBLIST:
         return self.charPointerToList(projInfo.info.jobList), None
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
      self.__api.DSGetLastErrorMsg.restype  =  ctypes.c_char_p

      error_code = self.__api.DSGetLastError()
      error_msg  = None

      if self.__handleProj is not None:
         error_msg = self.decodeBytes(self.__api.DSGetLastErrorMsg(self.__handleProj))

      if not error_msg:
         error_msg = DSAPI_ERRORS.get_error_msg(error_code)

      return {'code': error_code, 'msg': error_msg}

   def DSOpenJob(self, handleProj, jobName):
      self.__api.DSOpenJob.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
      self.__api.DSOpenJob.restype  = ctypes.POINTER(DSJOB)

      handleJob = self.__api.DSOpenJob(handleProj, ctypes.c_char_p(self.encodeString(jobName)))

      if not handleJob:
         return None, self.createError("DSOpenJob", self.DSGetLastError())
      else:
         self.handleJob = handleJob
         return handleJob, None

   def DSGetJobInfo(self, handleJob, infoType):
      self.__api.DSGetJobInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSJOBINFO)]
      self.__api.DSGetJobInfo.restype  = ctypes.c_int

      jobInfo = DSJOBINFO()
      res = self.__api.DSGetJobInfo(handleJob, infoType, ctypes.pointer(jobInfo))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetJobInfo", self.DSGetLastError())
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
            return self.charPointerToList(jobInfo.info.paramList), None
         if infoType == self.DSJ_STAGELIST:
            return self.charPointerToList(jobInfo.info.stageList), None
         if infoType == self.DSJ_USERSTATUS:
            return jobInfo.info.userStatus, None
         if infoType == self.DSJ_JOBCONTROL:
            return jobInfo.info.jobControl, None
         if infoType == self.DSJ_JOBPID:
            return jobInfo.info.jobPid, None
         if infoType == self.DSJ_JOBLASTTIMESTAMP:
            return jobInfo.info.jobLastTime, None
         if infoType == self.DSJ_JOBINVOCATIONS:
            return self.charPointerToList(jobInfo.info.jobInvocations), None
         if infoType == self.DSJ_JOBINTERIMSTATUS:
            return jobInfo.info.jobInterimStatus, None
         if infoType == self.DSJ_JOBINVOCATIONID:
            return jobInfo.info.jobInvocationId, None
         if infoType == self.DSJ_JOBDESC:
            return jobInfo.info.jobDesc, None
         if infoType == self.DSJ_STAGELIST2:
            return self.charPointerToList(jobInfo.info.stageList2), None
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
      self.__api.DSGetStageInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(DSSTAGEINFO)]
      self.__api.DSGetStageInfo.restype  = ctypes.c_int

      stageInfo = DSSTAGEINFO()
      res = self.__api.DSGetStageInfo(handleJob, self.encodeString(stageName), infoType, ctypes.pointer(stageInfo))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetStageInfo", self.DSGetLastError())
      else:
         if infoType == self.DSJ_LINKLIST:
            return self.charPointerToList(stageInfo.info.linkList), None
         if infoType == self.DSJ_STAGELASTERR:
            return stageInfo.info.lastError, None
         if infoType == self.DSJ_STAGENAME:
            return stageInfo.info.stageName, None
         if infoType == self.DSJ_STAGETYPE:
            return stageInfo.info.typeName, None
         if infoType == self.DSJ_STAGEINROWNUM:
            return stageInfo.info.inRowNum, None
         if infoType == self.DSJ_VARLIST:
            return self.charPointerToList(stageInfo.info.varList), None
         if infoType == self.DSJ_STAGESTARTTIMESTAMP:
            return stageInfo.info.stageStartTime, None
         if infoType == self.DSJ_STAGEENDTIMESTAMP:
            return stageInfo.info.stageEndTime, None
         if infoType == self.DSJ_STAGEDESC:
            return stageInfo.info.stageDesc, None
         if infoType == self.DSJ_STAGEINST:
            return self.charPointerToList(stageInfo.info.instList), None
         if infoType == self.DSJ_STAGECPU:
            return self.charPointerToList(stageInfo.info.cpuList), None
         if infoType == self.DSJ_LINKTYPES:
            return self.charPointerToList(stageInfo.info.linkTypes), None
         if infoType == self.DSJ_STAGEELAPSED:
            return stageInfo.info.stageElapsed, None
         if infoType == self.DSJ_STAGEPID:
            return self.charPointerToList(stageInfo.info.pidList), None
         if infoType == self.DSJ_STAGESTATUS:
            return stageInfo.info.stageStatus, None
         if infoType == self.DSJ_CUSTINFOLIST:
            return self.charPointerToList(stageInfo.info.custInfoList), None
         else:
            return '', None

   def DSGetLinkInfo(self, handleJob, stageName, linkName, infoType):
      self.__api.DSGetLinkInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(DSLINKINFO)]
      self.__api.DSGetLinkInfo.restype  = ctypes.c_int

      linkInfo = DSLINKINFO()
      res = self.__api.DSGetLinkInfo(handleJob, self.encodeString(stageName), self.encodeString(linkName), infoType, ctypes.pointer(linkInfo))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetLinkInfo", self.DSGetLastError())
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
            return self.charPointerToList(linkInfo.info.rowCountList), None
         if infoType == self.DSJ_LINKEXTROWCOUNT:
            return self.charPointerToList(linkInfo.info.rowCountList), None
         else:
            return '', None

   def DSFindFirstLogEntry(self, handleJob, eventType=DSJ_LOGANY, startTime=0, endTime=0, maxNumber=500):
      self.__api.DSFindFirstLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, time_t, time_t, ctypes.c_int, ctypes.POINTER(DSLOGEVENT)]
      self.__api.DSFindFirstLogEntry.restype  = ctypes.c_int

      logInfo = DSLOGEVENT()
      res = self.__api.DSFindFirstLogEntry(handleJob, eventType, startTime, endTime, maxNumber, ctypes.pointer(logInfo))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSFindFirstLogEntry", self.DSGetLastError())
      else:
         return logInfo, None

   def DSFindNextLogEntry(self, handleJob):
      self.__api.DSFindNextLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.POINTER(DSLOGEVENT)]
      self.__api.DSFindNextLogEntry.restype  = ctypes.c_int

      logEvent = DSLOGEVENT()
      res = self.__api.DSFindNextLogEntry(handleJob, ctypes.pointer(logEvent))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSFindNextLogEntry", self.DSGetLastError())
      else:
         return logEvent, None

   def DSGetLogEntryFull(self, handleJob, eventId):
      self.__api.DSGetLogEntryFull.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSLOGDETAILFULL)]
      self.__api.DSGetLogEntryFull.restype  = ctypes.c_int

      logDetail = DSLOGDETAILFULL()
      res = self.__api.DSGetLogEntryFull(handleJob, eventId, ctypes.pointer(logDetail))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetLogEntryFull", self.DSGetLastError())
      else:
         return logDetail, None

   def DSGetLogEntry(self, handleJob, eventId):
      self.__api.DSGetLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSLOGDETAIL)]
      self.__api.DSGetLogEntry.restype  = ctypes.c_int

      logDetail = DSLOGDETAIL()
      res = self.__api.DSGetLogEntry(handleJob, eventId, ctypes.pointer(logDetail))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetLogEntry", self.DSGetLastError())
      else:
         return logDetail, None

   def DSGetNewestLogId(self, handleJob, eventType):
      self.__api.DSGetNewestLogId.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
      self.__api.DSGetNewestLogId.restype  = ctypes.c_int

      lastLogId = self.__api.DSGetNewestLogId(handleJob, eventType)

      if lastLogId == -1:
         return None, self.createError("DSGetNewestLogId", self.DSGetLastError())
      else:
         return lastLogId, None

   def DSGetLogEventIds(self, handleJob, runNumber=0, filter=''):
      self.__api.DSGetLogEventIds.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
      self.__api.DSGetLogEventIds.restype  = ctypes.c_int

      eventsPointer = ctypes.POINTER(ctypes.c_char)()
      res = self.__api.DSGetLogEventIds(handleJob, runNumber, self.encodeString(filter), ctypes.pointer(eventsPointer))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetLogEventIds", self.DSGetLastError())
      else:
         return self.charPointerToList(eventsPointer), None

   def DSGetQueueList(self):
      self.__api.DSGetQueueList.restype = ctypes.POINTER(ctypes.c_char)
      qList = self.__api.DSGetQueueList()

      return self.charPointerToList(qList), None

   def DSSetJobQueue(self, handleJob, queueName):
      self.__api.DSSetJobQueue.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p]
      self.__api.DSSetJobQueue.restype  = ctypes.c_int

      res = self.__api.DSSetJobQueue(handleJob, queueName)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetJobQueue", self.DSGetLastError())
      else:
         return 0, None

   def DSCloseJob(self, handleJob):
      self.__api.DSCloseJob.argtypes = [ctypes.POINTER(DSJOB)]
      self.__api.DSCloseJob.restype  = ctypes.c_int

      res = self.__api.DSCloseJob(handleJob)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSCloseJob", self.DSGetLastError())
      else:
         return 0, None

   def DSCloseProject(self, handleProj):
      self.__api.DSCloseProject.argtypes = [ctypes.POINTER(DSPROJECT)]
      self.__api.DSCloseProject.restype  = ctypes.c_int

      res = self.__api.DSCloseProject(handleProj)
      self.__handleProj = None

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSCloseProject", self.DSGetLastError())
      else:
         return 0, None

   def DSSetJobLimit(self, handleJob, limitType, limitValue):
      self.__api.DSSetJobLimit.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_int]
      self.__api.DSSetJobLimit.restype  = ctypes.c_int

      res = self.__api.DSSetJobLimit(handleJob, limitType, limitValue)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetJobLimit", self.DSGetLastError())
      else:
         return 0, None

   def DSPurgeJob(self, handleJob, purgeSpec):
      self.__api.DSPurgeJob.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
      self.__api.DSPurgeJob.restype  = ctypes.c_int

      res = self.__api.DSPurgeJob(handleJob, purgeSpec)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSPurgeJob", self.DSGetLastError())
      else:
         return 0, None

   def DSRunJob(self, handleJob, runMode):
      self.__api.DSRunJob.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
      self.__api.DSRunJob.restype  = ctypes.c_int

      res = self.__api.DSRunJob(handleJob, runMode)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSRunJob", self.DSGetLastError())
      else:
         return 0, None

   def DSStopJob(self, handleJob):
      self.__api.DSStopJob.argtypes = [ctypes.POINTER(DSJOB)]
      self.__api.DSStopJob.restype  = ctypes.c_int

      res = self.__api.DSStopJob(handleJob)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSStopJob", self.DSGetLastError())
      else:
         return 0, None

   def DSLockJob(self, handleJob):
      self.__api.DSLockJob.argtypes = [ctypes.POINTER(DSJOB)]
      self.__api.DSLockJob.restype  = ctypes.c_int

      res = self.__api.DSLockJob(handleJob)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSLockJob", self.DSGetLastError())
      else:
         return 0, None

   def DSUnlockJob(self, handleJob):
      self.__api.DSUnlockJob.argtypes = [ctypes.POINTER(DSJOB)]
      self.__api.DSUnlockJob.restype  = ctypes.c_int

      res = self.__api.DSUnlockJob(handleJob)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSUnlockJob", self.DSGetLastError())
      else:
         return 0, None

   def DSWaitForJob(self, handleJob):
      self.__api.DSWaitForJob.argtypes = [ctypes.POINTER(DSJOB)]
      self.__api.DSWaitForJob.restype  = ctypes.c_int

      res = self.__api.DSWaitForJob(handleJob)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSWaitForJob", self.DSGetLastError())
      else:
         return 0, None

   def DSSetParam(self, handleJob, paramName, param):
      self.__api.DSSetParam.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.POINTER(DSPARAM)]
      self.__api.DSSetParam.restype  = ctypes.c_int

      res = self.__api.DSSetParam(handleJob, self.encodeString(paramName), ctypes.pointer(param))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetParam", self.DSGetLastError())
      else:
         return 0, None

   def DSGetParamInfo(self, handleJob, paramName):
      self.__api.DSGetParamInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.POINTER(DSPARAMINFO)]
      self.__api.DSGetParamInfo.restype  = ctypes.c_int

      paramInfo = DSPARAMINFO()
      res = self.__api.DSGetParamInfo(handleJob, self.encodeString(paramName), ctypes.pointer(paramInfo))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSGetParamInfo", self.DSGetLastError())
      else:
         return paramInfo, None

   def DSMakeJobReport(self, handleJob, reportType, lineSeparator='CRLF'):
      self.__api.DSMakeJobReport.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(DSREPORTINFO)]
      self.__api.DSMakeJobReport.restype  = ctypes.c_int

      reportInfo = DSREPORTINFO()
      res = self.__api.DSMakeJobReport(handleJob, reportType, self.encodeString(lineSeparator), ctypes.pointer(reportInfo))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSMakeJobReport", self.DSGetLastError())
      else:
         return reportInfo.info.reportText, None

   def DSGetReposUsage(self, handleProj, relationshipType, objectName, recursive=0):
      self.__api.DSGetReposUsage.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(DSREPOSUSAGE)]
      self.__api.DSGetReposUsage.restype  = ctypes.c_int

      reposUsage = DSREPOSUSAGE()
      res = self.__api.DSGetReposUsage(handleProj, relationshipType, self.encodeString(objectName), recursive, ctypes.pointer(reposUsage))

      if res > 0:
         return reposUsage.info.jobs.contents, None
      if res == 0:
         return None, None

      return None, self.createError("DSGetReposUsage", self.DSGetLastError())

   def DSGetReposInfo(self, handleProj, objectType, infoType, searchCriteria, startingCategory, subcategories=1):
      self.__api.DSGetReposInfo.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(DSREPOSINFO)]
      self.__api.DSGetReposInfo.restype  = ctypes.c_int

      reposInfo = DSREPOSINFO()
      res = self.__api.DSGetReposInfo(handleProj, objectType, infoType, self.encodeString(searchCriteria), self.encodeString(startingCategory), subcategories, ctypes.pointer(reposInfo))

      if res > 0:
         return reposInfo.info.jobs.contents, None
      if res == 0:
         return None, None

      return None, self.createError("DSGetReposInfo", self.DSGetLastError())

   def DSLogEvent(self, handleJob, eventType, message):
      self.__api.DSLogEvent.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
      self.__api.DSLogEvent.restype  = ctypes.c_int

      res = self.__api.DSLogEvent(handleJob, eventType, self.encodeString(''), self.encodeString(message))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSLogEvent", self.DSGetLastError())
      else:
         return 0, None

   def DSAddEnvVar(self, handleProj, envVarName, varType, promptText, value):
      self.__api.DSAddEnvVar.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
      self.__api.DSAddEnvVar.restype  = ctypes.c_int

      res = self.__api.DSAddEnvVar(handleProj, self.encodeString(envVarName), self.encodeString(varType), self.encodeString(promptText), self.encodeString(value))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSAddEnvVar", self.DSGetLastError())
      else:
         return 0, None

   def DSDeleteEnvVar(self, handleProj, envVarName):
      self.__api.DSDeleteEnvVar.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
      self.__api.DSDeleteEnvVar.restype  = ctypes.c_int

      res = self.__api.DSDeleteEnvVar(handleProj, self.encodeString(envVarName))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSDeleteEnvVar", self.DSGetLastError())
      else:
         return 0, None

   def DSSetEnvVar(self, handleProj, envVarName, value):
      self.__api.DSSetEnvVar.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p]
      self.__api.DSSetEnvVar.restype  = ctypes.c_int

      res = self.__api.DSSetEnvVar(handleProj, self.encodeString(envVarName), self.encodeString(value))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetEnvVar", self.DSGetLastError())
      else:
         return 0, None

   def DSListEnvVars(self, handleProj):
      self.__api.DSListEnvVars.argtypes = [ctypes.POINTER(DSPROJECT)]
      self.__api.DSListEnvVars.restype  = ctypes.POINTER(ctypes.c_char)

      varList = self.__api.DSListEnvVars(handleProj)

      if not varList:
         return None, self.createError("DSListEnvVars", self.DSGetLastError())
      else:
         return self.charPointerToList(varList), None

   def DSAddProject(self, projectName, projectLocation=''):
      self.__api.DSAddProject.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
      self.__api.DSAddProject.restype  = ctypes.c_int

      res = self.__api.DSAddProject(self.encodeString(projectName), self.encodeString(projectLocation))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSAddProject", self.DSGetLastError())
      else:
         return 0, None

   def DSDeleteProject(self, projectName):
      self.__api.DSDeleteProject.argtypes = [ctypes.c_char_p]
      self.__api.DSDeleteProject.restype  = ctypes.c_int

      res = self.__api.DSDeleteProject(self.encodeString(projectName))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSDeleteProject", self.DSGetLastError())
      else:
         return 0, None

   def DSGetIdForJob(self, handleProj, jobName):
      self.__api.DSGetIdForJob.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
      self.__api.DSGetIdForJob.restype  = ctypes.c_char_p

      jobId = self.__api.DSGetIdForJob(handleProj, self.encodeString(jobName))

      if not jobId:
         return None, self.createError("DSGetIdForJob", self.DSGetLastError())
      else:
         return jobId, None

   def DSSetIdForJob(self, handleProj, jobName, jobId):
      self.__api.DSSetIdForJob.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p]
      self.__api.DSSetIdForJob.restype  = ctypes.c_int

      res = self.__api.DSSetIdForJob(handleProj, self.encodeString(jobName), self.encodeString(jobId))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetIdForJob", self.DSGetLastError())
      else:
         return 0, None

   def DSJobNameFromJobId(self, handleProj, jobId):
      self.__api.DSJobNameFromJobId.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
      self.__api.DSJobNameFromJobId.restype  = ctypes.c_char_p

      jobName = self.__api.DSJobNameFromJobId(handleProj, self.encodeString(jobId))

      if not jobName:
         return None, self.createError("DSJobNameFromJobId", self.DSGetLastError())
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
         return None, self.createError("DSServerMessage", "Variable prms must be a list")

      maxPrms = len(prms)

      self.__api.DSServerMessage.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p * maxPrms, ctypes.c_char_p, ctypes.c_int]
      self.__api.DSServerMessage.restype  = ctypes.c_int

      encodedPrms = [self.encodeString(str(prm)) for prm in prms]
      resMessage  = ctypes.c_char_p(self.encodeString(''))

      msgSize = self.__api.DSServerMessage(self.encodeString(msgIdStr), self.encodeString(defMsg), (ctypes.c_char_p * maxPrms)(*encodedPrms), resMessage, sizeMessage)

      if not resMessage:
         return None, self.createError("DSServerMessage", self.DSGetLastError())
      else:
         return resMessage.value, None

   def DSSetProjectProperty(self, handleProj, property, value):
      self.__api.DSSetProjectProperty.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p, ctypes.c_char_p]
      self.__api.DSSetProjectProperty.restype  = ctypes.c_int

      res = self.__api.DSSetProjectProperty(handleProj, self.encodeString(property), self.encodeString(value))

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetProjectProperty", self.DSGetLastError())
      else:
         return 0, None

   def DSListProjectProperties(self, handleProj):
      self.__api.DSListProjectProperties.argtypes = [ctypes.POINTER(DSPROJECT)]
      self.__api.DSListProjectProperties.restype  = ctypes.POINTER(ctypes.c_char)

      propList = self.__api.DSListProjectProperties(handleProj)

      if not propList:
         return None, self.createError("DSListProjectProperties", self.DSGetLastError())
      else:
         return self.charPointerToList(propList), None

   def DSGetWLMEnabled(self):
      self.__api.DSGetWLMEnabled.argtypes = []
      self.__api.DSGetWLMEnabled.restype  = ctypes.c_int

      wlmEnabled = self.__api.DSGetWLMEnabled()

      if not wlmEnabled:
         return None, self.createError("DSGetWLMEnabled", self.DSGetLastError())
      else:
         return 0, None

   def DSSetGenerateOpMetaData(self, handleJob, value):
      self.__api.DSSetGenerateOpMetaData.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
      self.__api.DSSetGenerateOpMetaData.restype  = ctypes.c_int

      res = self.__api.DSSetGenerateOpMetaData(handleJob, value)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetGenerateOpMetaData", self.DSGetLastError())
      else:
         return 0, None

   def DSSetDisableProjectHandler(self, handleProj, value):
      # Does function work incorrectly due to bad definition in dsapi.h?
      self.__api.DSSetDisableProjectHandler.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int]
      self.__api.DSSetDisableProjectHandler.restype  = ctypes.c_int

      res = self.__api.DSSetDisableProjectHandler(handleProj, value)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetDisableProjectHandler", self.DSGetLastError())
      else:
         return 0, None

   def DSSetDisableJobHandler(self, handleJob, value):
      self.__api.DSSetDisableJobHandler.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
      self.__api.DSSetDisableJobHandler.restype  = ctypes.c_int

      res = self.__api.DSSetDisableJobHandler(handleJob, value)

      if res != DSAPI_ERRORS.DSJE_NOERROR:
         return None, self.createError("DSSetDisableJobHandler", self.DSGetLastError())
      else:
         return 0, None

   # CUSTOM FUNCTIONS
   def DSLoadLibrary(self, api_lib_file):
      """
      api_lib_file - full path to DataStage API library
         vmdsapi.dll on windows
         or
         libvmdsapi.so on *nix

      PATH on windows should include path where file 'vmdsapi.dll' is located
         in most cases, in the '../IBM/InformationServer/Clients/Classic/'

      LD_LIBRARY_PATH on *nix should include path where file 'libvmdsapi.so' and its dependencies are located
         in most cases, in the '../IBM/InformationServer/Server/DSEngine/lib/'
      """

      if not os.path.exists(api_lib_file) or not os.path.isfile(api_lib_file):
         return None, self.createError("DSLoadLibrary", "Path to {} doesn't exist".format(api_lib_file))

      try:
         self.__api = ctypes.CDLL(api_lib_file)
      except OSError as e:
         return None, self.createError("DSLoadLibrary", "Can't load the library: {}".format(str(e)))

      return True, None

   def DSUnloadLibrary(self):
      self.__api        = None
      self.__handleProj = None

   def charPointerToList(self, char_p):
      words_list = []

      if not char_p:
         return words_list

      start_word_pos = 0
      it = 0
      while True:
         if char_p[it] == b'\x00':
            if it - 1 >= 0 and char_p[it - 1] == b'\x00':
               break
            words_list.append(char_p[start_word_pos:it])
            start_word_pos = it + 1
         it = it + 1

      return words_list

   def createError(self, func_name, api_error):
      err_obj = {
         'type': 'error',
         'func': func_name,
         'code': None,
         'msg' : ''
      }

      if isinstance(api_error, dict):
         for key, val in api_error.items():
            err_obj[key] = val
      else:
         err_obj['msg'] = str(api_error)

      return err_obj

   def decodeBytes(self, str):
      return str.decode("cp1251", errors="ignore")

   def encodeString(self, str):
      return str.encode("utf-8")

# API ERRORS
class DSAPI_ERRORS:
   DSJE_NOERROR                = 0
   DSJE_BADHANDLE              = -1
   DSJE_BADSTATE               = -2
   DSJE_BADPARAM               = -3
   DSJE_BADVALUE               = -4
   DSJE_BADTYPE                = -5
   DSJE_WRONGJOB               = -6
   DSJE_BADSTAGE               = -7
   DSJE_NOTINSTAGE             = -8
   DSJE_BADLINK                = -9
   DSJE_JOBLOCKED              = -10
   DSJE_JOBDELETED             = -11
   DSJE_BADNAME                = -12
   DSJE_BADTIME                = -13
   DSJE_TIMEOUT                = -14
   DSJE_DECRYPTERR             = -15
   DSJE_NOACCESS               = -16
   DSJE_NOTEMPLATE             = -17
   DSJE_BADTEMPLATE            = -18
   DSJE_NOPARAM                = -19
   DSJE_NOFILEPATH             = -20
   DSJE_CMDERROR               = -21
   DSJE_BADVAR                 = -22
   DSJE_NONUNIQUEID            = -23
   DSJE_INVALIDID              = -24
   DSJE_INVALIDQUEUE           = -25
   DSJE_WLMDISABLED            = -26
   DSJE_WLMNOTRUNNING          = -27
   DSJE_NOROLEPERMISSIONS      = -28
   DSJE_REPERROR               = -99
   DSJE_NOTADMINUSER           = -100
   DSJE_ISADMINFAILED          = -101
   DSJE_READPROJPROPERTY       = -102
   DSJE_WRITEPROJPROPERTY      = -103
   DSJE_BADPROPERTY            = -104
   DSJE_PROPNOTSUPPORTED       = -105
   DSJE_BADPROPVALUE           = -106
   DSJE_OSHVISIBLEFLAG         = -107
   DSJE_BADENVVARNAME          = -108
   DSJE_BADENVVARTYPE          = -109
   DSJE_BADENVVARPROMPT        = -110
   DSJE_READENVVARDEFNS        = -111
   DSJE_READENVVARVALUES       = -112
   DSJE_WRITEENVVARDEFNS       = -113
   DSJE_WRITEENVVARVALUES      = -114
   DSJE_DUPENVVARNAME          = -115
   DSJE_BADENVVAR              = -116
   DSJE_NOTUSERDEFINED         = -117
   DSJE_BADBOOLEANVALUE        = -118
   DSJE_BADNUMERICVALUE        = -119
   DSJE_BADLISTVALUE           = -120
   DSJE_PXNOTINSTALLED         = -121
   DSJE_ISPARALLELLICENCED     = -122
   DSJE_ENCODEFAILED           = -123
   DSJE_DELPROJFAILED          = -124
   DSJE_DELPROJFILESFAILED     = -125
   DSJE_LISTSCHEDULEFAILED     = -126
   DSJE_CLEARSCHEDULEFAILED    = -127
   DSJE_BADPROJNAME            = -128
   DSJE_GETDEFAULTPATHFAILED   = -129
   DSJE_BADPROJLOCATION        = -130
   DSJE_INVALIDPROJECTLOCATION = -131
   DSJE_OPENFAILED             = -132
   DSJE_READUFAILED            = -133
   DSJE_ADDPROJECTBLOCKED      = -134
   DSJE_ADDPROJECTFAILED       = -135
   DSJE_LICENSEPROJECTFAILED   = -136
   DSJE_RELEASEFAILED          = -137
   DSJE_DELETEPROJECTBLOCKED   = -138
   DSJE_NOTAPROJECT            = -139
   DSJE_ACCOUNTPATHFAILED      = -140
   DSJE_LOGTOFAILED            = -141
   DSJE_PROTECTFAILED          = -142
   DSJE_UNKNOWN_JOBNAME        = -201
   DSJE_NOMORE                 = -1001
   DSJE_BADPROJECT             = -1002
   DSJE_NO_DATASTAGE           = -1003
   DSJE_OPENFAIL               = -1004
   DSJE_NO_MEMORY              = -1005
   DSJE_SERVER_ERROR           = -1006
   DSJE_NOT_AVAILABLE          = -1007
   DSJE_BAD_VERSION            = -1008
   DSJE_INCOMPATIBLE_SERVER    = -1009
   DSJE_DOMAINLOGTOFAILED      = -1010
   DSJE_NOPRIVILEGE            = -1011
   DSJE_LICENSE_EXPIRED        = 39121
   DSJE_LIMIT_REACHED          = 39134
   DSJE_BAD_CREDENTIAL         = 80011
   DSJE_PASSWORD_EXPIRED       = 80019
   DSJE_BAD_HOST               = 81011

   __mapping = [
      {'token': 'DSJE_NOERROR', 'code': 0, 'msg': 'No error'},
      {'token': 'DSJE_BADHANDLE', 'code': -1, 'msg': 'Invalid JobHandle'},
      {'token': 'DSJE_BADSTATE', 'code': -2, 'msg': 'Job is not in the right state (must be compiled & not running)'},
      {'token': 'DSJE_BADPARAM', 'code': -3, 'msg': 'ParamName is not a parameter name in the job'},
      {'token': 'DSJE_BADVALUE', 'code': -4, 'msg': 'LimitValue is not appropriate for the limiting condition type'},
      {'token': 'DSJE_BADTYPE', 'code': -5, 'msg': 'Invalid EventType value'},
      {'token': 'DSJE_WRONGJOB', 'code': -6, 'msg': 'Job for this JobHandle was not started from a call to DSRunJob by the current process'},
      {'token': 'DSJE_BADSTAGE', 'code': -7, 'msg': 'StageName does not refer to a known stage in the job'},
      {'token': 'DSJE_NOTINSTAGE', 'code': -8, 'msg': 'INTERNAL TO SERVER'},
      {'token': 'DSJE_BADLINK', 'code': -9, 'msg': 'LinkName does not refer to a known link for the stage in question'},
      {'token': 'DSJE_JOBLOCKED', 'code': -10, 'msg': 'Job is locked by another user'},
      {'token': 'DSJE_JOBDELETED', 'code': -11, 'msg': 'Job has been deleted !'},
      {'token': 'DSJE_BADNAME', 'code': -12, 'msg': 'Job name badly formed'},
      {'token': 'DSJE_BADTIME', 'code': -13, 'msg': 'Timestamp parameter was badly formed'},
      {'token': 'DSJE_TIMEOUT', 'code': -14, 'msg': 'Given up waiting for something to happen'},
      {'token': 'DSJE_DECRYPTERR', 'code': -15, 'msg': 'Decryption of encrypted value failed'},
      {'token': 'DSJE_NOACCESS', 'code': -16, 'msg': 'Cannot get values, Default values or Design Default values for any job except the current job (Job Handle == DSJ.ME)'},
      {'token': 'DSJE_NOTEMPLATE', 'code': -17, 'msg': 'Cannot find template file'},
      {'token': 'DSJE_BADTEMPLATE', 'code': -18, 'msg': 'Error encountered when processing template file'},
      {'token': 'DSJE_NOPARAM', 'code': -19, 'msg': 'Parameter name missing - field does not look like \'name:value\''},
      {'token': 'DSJE_NOFILEPATH', 'code': -20, 'msg': 'File path name not given'},
      {'token': 'DSJE_CMDERROR', 'code': -21, 'msg': 'Error when executing external command'},
      {'token': 'DSJE_BADVAR', 'code': -22, 'msg': 'Stage Variable name not recognised'},
      {'token': 'DSJE_NONUNIQUEID', 'code': -23, 'msg': 'Id already exists for a job in this project'},
      {'token': 'DSJE_INVALIDID', 'code': -24, 'msg': 'Invalid Job Id'},
      {'token': 'DSJE_INVALIDQUEUE', 'code': -25, 'msg': 'Invalid Queue'},
      {'token': 'DSJE_WLMDISABLED', 'code': -26, 'msg': 'WLM is not enabled'},
      {'token': 'DSJE_WLMNOTRUNNING', 'code': -27, 'msg': 'WLM is not running'},
      {'token': 'DSJE_NOROLEPERMISSIONS', 'code': -28, 'msg': 'User does not have required role permissions to perform this operation'},
      {'token': 'DSJE_REPERROR', 'code': -99, 'msg': 'General server \'other error\''},
      {'token': 'DSJE_NOTADMINUSER', 'code': -100, 'msg': 'User is not an administrative user'},
      {'token': 'DSJE_ISADMINFAILED', 'code': -101, 'msg': 'Unable to determine if user is an administrative user'},
      {'token': 'DSJE_READPROJPROPERTY', 'code': -102, 'msg': 'Reading project properties failed'},
      {'token': 'DSJE_WRITEPROJPROPERTY', 'code': -103, 'msg': 'Writing project properties failed'},
      {'token': 'DSJE_BADPROPERTY', 'code': -104, 'msg': 'Property name is invalid'},
      {'token': 'DSJE_PROPNOTSUPPORTED', 'code': -105, 'msg': 'Unsupported property'},
      {'token': 'DSJE_BADPROPVALUE', 'code': -106, 'msg': 'Value given is not valid for this property'},
      {'token': 'DSJE_OSHVISIBLEFLAG', 'code': -107, 'msg': 'Failed to set OSHVisible value'},
      {'token': 'DSJE_BADENVVARNAME', 'code': -108, 'msg': 'Invalid environment variable name'},
      {'token': 'DSJE_BADENVVARTYPE', 'code': -109, 'msg': 'Invalid environment variable type'},
      {'token': 'DSJE_BADENVVARPROMPT', 'code': -110, 'msg': 'Missing environment variable prompt'},
      {'token': 'DSJE_READENVVARDEFNS', 'code': -111, 'msg': 'Reading environment variable definitions failed'},
      {'token': 'DSJE_READENVVARVALUES', 'code': -112, 'msg': 'Reading environment variable values failed'},
      {'token': 'DSJE_WRITEENVVARDEFNS', 'code': -113, 'msg': 'Writing environment variable definitions failed'},
      {'token': 'DSJE_WRITEENVVARVALUES', 'code': -114, 'msg': 'Writing environment variable values failed'},
      {'token': 'DSJE_DUPENVVARNAME', 'code': -115, 'msg': 'Environment variable name already exists'},
      {'token': 'DSJE_BADENVVAR', 'code': -116, 'msg': 'Environment variable name not recognised'},
      {'token': 'DSJE_NOTUSERDEFINED', 'code': -117, 'msg': 'Environment variable is not user defined'},
      {'token': 'DSJE_BADBOOLEANVALUE', 'code': -118, 'msg': 'Invalid value given for a boolean environment variable'},
      {'token': 'DSJE_BADNUMERICVALUE', 'code': -119, 'msg': 'Invalid value given for a numeric environment variable'},
      {'token': 'DSJE_BADLISTVALUE', 'code': -120, 'msg': 'Invalid value given for a list environment variable'},
      {'token': 'DSJE_PXNOTINSTALLED', 'code': -121, 'msg': 'PX not installed'},
      {'token': 'DSJE_ISPARALLELLICENCED', 'code': -122, 'msg': 'Failed to find out if PX licensed'},
      {'token': 'DSJE_ENCODEFAILED', 'code': -123, 'msg': 'Encoding of an encrypted value failed'},
      {'token': 'DSJE_DELPROJFAILED', 'code': -124, 'msg': 'Deletion of project definition & SCHEMA failed'},
      {'token': 'DSJE_DELPROJFILESFAILED', 'code': -125, 'msg': 'Deletion of project files & subdirectories failed'},
      {'token': 'DSJE_LISTSCHEDULEFAILED', 'code': -126, 'msg': 'Failed to get list of scheduled jobs for project'},
      {'token': 'DSJE_CLEARSCHEDULEFAILED', 'code': -127, 'msg': 'Failed to clear scheduled jobs for project'},
      {'token': 'DSJE_BADPROJNAME', 'code': -128, 'msg': 'Project name contains invalid characters'},
      {'token': 'DSJE_GETDEFAULTPATHFAILED', 'code': -129, 'msg': 'Failed to get default path for project'},
      {'token': 'DSJE_BADPROJLOCATION', 'code': -130 , 'msg': 'Project location path contains invalid characters'},
      {'token': 'DSJE_INVALIDPROJECTLOCATION', 'code': -131, 'msg': 'Project location is invalid'},
      {'token': 'DSJE_OPENFAILED', 'code': -132, 'msg': 'Failed to open file'},
      {'token': 'DSJE_READUFAILED', 'code': -133, 'msg': 'Failed to lock administration record'},
      {'token': 'DSJE_ADDPROJECTBLOCKED', 'code': -134, 'msg': 'Administration record locked by another user'},
      {'token': 'DSJE_ADDPROJECTFAILED', 'code': -135, 'msg': 'Adding project failed'},
      {'token': 'DSJE_LICENSEPROJECTFAILED', 'code': -136, 'msg': 'Licensing project failed'},
      {'token': 'DSJE_RELEASEFAILED', 'code': -137, 'msg': 'Failed to release administration record'},
      {'token': 'DSJE_DELETEPROJECTBLOCKED', 'code': -138, 'msg': 'Project locked by another user'},
      {'token': 'DSJE_NOTAPROJECT', 'code': -139 , 'msg': 'Failed to log to project'},
      {'token': 'DSJE_ACCOUNTPATHFAILED', 'code': -140 , 'msg': 'Failed to get account path'},
      {'token': 'DSJE_LOGTOFAILED', 'code': -141 , 'msg': 'Failed to log to UV account'},
      {'token': 'DSJE_PROTECTFAILED', 'code': -142, 'msg': 'Protect or unprotect project failed'},
      {'token': 'DSJE_UNKNOWN_JOBNAME', 'code': -201, 'msg': 'Could not find the supplied job name'},
      {'token': 'DSJE_NOMORE', 'code': -1001, 'msg': 'All events matching the filter criteria have been returned'},
      {'token': 'DSJE_BADPROJECT', 'code': -1002, 'msg': 'Unknown project name'},
      {'token': 'DSJE_NO_DATASTAGE', 'code': -1003, 'msg': 'DataStage not installed on server'},
      {'token': 'DSJE_OPENFAIL', 'code': -1004, 'msg': 'Attempt to open job failed'},
      {'token': 'DSJE_NO_MEMORY', 'code': -1005, 'msg': 'Malloc failure'},
      {'token': 'DSJE_SERVER_ERROR', 'code': -1006, 'msg': 'Server generated error - error msg text desribes it'},
      {'token': 'DSJE_NOT_AVAILABLE', 'code': -1007, 'msg': 'Not data available from server'},
      {'token': 'DSJE_BAD_VERSION', 'code': -1008, 'msg': 'Version is DSOpenProjectEx is invalid'},
      {'token': 'DSJE_INCOMPATIBLE_SERVER', 'code': -1009, 'msg': 'Server version incompatible with this version of the DSAPI'},
      {'token': 'DSJE_DOMAINLOGTOFAILED', 'code': -1010, 'msg': 'Failed to authenticate to Domain'},
      {'token': 'DSJE_NOPRIVILEGE', 'code': -1011, 'msg': 'The isf user does not have sufficient DataStage privileges'},
      {'token': 'DSJE_LICENSE_EXPIRED', 'code': 39121, 'msg': 'The InfoSphere DataStage license has expired'},
      {'token': 'DSJE_LIMIT_REACHED', 'code': 39134, 'msg': 'The InfoSphere DataStage user limit has been reached'},
      {'token': 'DSJE_BAD_CREDENTIAL', 'code': 80011, 'msg': 'Incorrect system name or invalid user name or password provided'},
      {'token': 'DSJE_PASSWORD_EXPIRED', 'code': 80019, 'msg': 'Password has expired'},
      {'token': 'DSJE_BAD_HOST', 'code': 81011, 'msg': 'The host name specified is not valid, or the host is not responding'}
   ]

   @staticmethod
   def get_error(error_code):
      for err in DSAPI_ERRORS.__mapping:
         if err['code'] == int(error_code):
            return err
      return {'token': 'DSJE_UNKNOWN_ERRORCODE', 'code': error_code, 'msg': 'Unknown error code'}

   @staticmethod
   def get_error_msg(error_code):
      return DSAPI_ERRORS.get_error(error_code)['msg']
