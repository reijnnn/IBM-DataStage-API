import ctypes
import os

#####################################################
###                    TYPES                      ###
#####################################################
from sys import platform as _platform_name

if _platform_name.startswith('win'):
	time_t = ctypes.c_uint32
else:
	time_t = ctypes.c_uint64

#####################################################
###                  API STRUCT                   ###
#####################################################

class DSPROJECT(ctypes.Structure):
	_fields_ = [("dsapiVersionNo", ctypes.c_int),
				("sessionId", 	   ctypes.c_int),
				("valueMark", 	   ctypes.c_ubyte),
				("fieldMark", 	   ctypes.c_ubyte)]

class DSJOB(ctypes.Structure):
	_fields_ = [("hProject",        ctypes.POINTER(DSPROJECT)),
				("serverJobHandle", ctypes.c_char_p),
				("logData", 		ctypes.c_char_p),
				("logDataLen", 		ctypes.c_int),
				("logDataPsn", 		ctypes.c_int)]

class DSJOBINFO_info(ctypes.Union):
	_fields_ = [("jobStatus", 		  ctypes.c_int),
				("jobController",     ctypes.c_char_p),
				("jobStartTime", 	  time_t),
				("jobWaveNumber", 	  ctypes.c_int),
				("userStatus", 		  ctypes.c_char_p),
				("stageList", 		  ctypes.c_char_p),
				("paramList", 		  ctypes.POINTER(ctypes.c_char)),
				("jobName", 		  ctypes.c_char_p),
				("jobControl", 		  ctypes.c_int),
				("jobPid", 			  ctypes.c_int),
				("jobLastTime", 	  time_t),
				("jobInvocations", 	  ctypes.POINTER(ctypes.c_char)),
				("jobInterimStatus",  ctypes.c_int),
				("jobInvocationId",   ctypes.c_char_p),
				("jobDesc", 		  ctypes.c_char_p),
				("stageList2", 		  ctypes.c_char_p),
				("jobElapsed", 		  ctypes.c_char_p),
				("jobDMIService", 	  ctypes.c_int),
				("jobMultiInvokable", ctypes.c_int),
				("jobFullDesc",		  ctypes.c_char_p),
				("jobRestartable", 	  ctypes.c_int)]

class DSJOBINFO(ctypes.Structure):
	_fields_ = [("infoType", ctypes.c_int),
				("info",     DSJOBINFO_info)]

class DSPROJECTINFO_info(ctypes.Union):
	_fields_ = [("jobList", 		ctypes.POINTER(ctypes.c_char)),
				("projectName",     ctypes.c_char_p),
				("projectPath", 	ctypes.c_char_p),
				("hostName", 	    ctypes.c_char_p),
				("installTag", 		ctypes.c_char_p),
				("tcpPort", 		ctypes.c_char_p)]

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
	_fields_ = [("pString", 		ctypes.c_char_p),
				("pEncrypt",     	ctypes.c_char_p),
				("pInt", 			ctypes.c_int),
				("pFloat", 	    	ctypes.c_float),
				("pPath", 			ctypes.c_char_p),
				("pListValue", 		ctypes.c_char_p),
				("pDate", 			ctypes.c_char_p),
				("pTime", 			ctypes.c_char_p)]

class DSPARAM(ctypes.Structure):
	_fields_ = [("paramType",  ctypes.c_int),
				("paramValue", DSPARAM_value)]

class DSREPORTINFO_info(ctypes.Union):
	_fields_ = [("reportText", ctypes.c_char_p)]

class DSREPORTINFO(ctypes.Structure):
	_fields_ = [("reportType",  ctypes.c_int),
				("info", DSREPORTINFO_info)]


#####################################################
###                 API INTERFACE                 ###
#####################################################
class DSAPI:

	# API Version
	DSAPI_VERSION = 1

	# API Error Codes
	DSJE_NOERROR = 0;

	# DSJOBINFO 'infoType' values
	DSJ_JOBSTATUS = 1       # Current status of the job.
	DSJ_JOBNAME   = 2       # Name of the job referenced by JobHandle.
	DSJ_JOBCONTROLLER = 3	# Name of job controlling the job referenced by JobHandle.
	DSJ_JOBSTARTTIMESTAMP = 4 # Date and time when the job started.
	DSJ_JOBWAVENO = 5		  # Wave number of last or current run.
	DSJ_PARAMLIST = 6	      # List of job parameter names
	DSJ_STAGELIST = 7		  # List of names of stages in job
	DSJ_USERSTATUS = 8		  # Value, if any,  set as the user status by the job.
	DSJ_JOBCONTROL = 9  	  # Job control STOP/SUSPEND/RESUME
	DSJ_JOBPID = 10     	  # Process id of DSD.RUN process
	DSJ_JOBLASTTIMESTAMP = 11   # Server date/time of job last finished: "YYYY-MM-DD HH:MM:SS"
	DSJ_JOBINVOCATIONS = 12     # Comma-separated list of job invocation ids
	DSJ_JOBINTERIMSTATUS = 13   # Current interim status of job
	DSJ_JOBINVOCATIONID = 14    # Invocation name of the job referenced
	DSJ_JOBDESC = 15		 	# Job description
	DSJ_STAGELIST2 = 16			# list of stages not in DSJ.STAGELIST
	DSJ_JOBELAPSED = 17			# Job Elapsed time in seconds
	DSJ_JOBEOTCOUNT = 18
	DSJ_JOBEOTTIMESTAMP = 19
	DSJ_JOBDMISERVICE  = 20		# Job is a DMI (aka WEB) service
	DSJ_JOBMULTIINVOKABLE = 21	# Job can be multiply invoked
	DSJ_JOBFULLDESC = 22		# Full job description
	DSJ_JOBRESTARTABLE = 24		# Job can be restarted

	# DSPROJECTINFO 'infoType' values
	DSJ_JOBLIST	= 1	    # List of jobs in project
	DSJ_PROJECTNAME	= 2	# Name of current project
	DSJ_HOSTNAME = 3	# Host name of the server
	DSJ_INSTALLTAG = 4	# Install tag of the server DSEngine
	DSJ_TCPPORT	= 5		# TCP port    of the server DSEngine
	DSJ_PROJECTPATH	= 6	# Directory path of current project

	# DSLOGDETAILFULL 'eventType' values
	DSJ_LOGINFO		= 1	 # Information message.
	DSJ_LOGWARNING	= 2	 # Warning message.
	DSJ_LOGFATAL	= 3	 # Fatal error message.
	DSJ_LOGREJECT	= 4	 # Rejected row message.
	DSJ_LOGSTARTED	= 5	 # Job started message.
	DSJ_LOGRESET	= 6	 # Job reset message.
	DSJ_LOGBATCH	= 7	 # Batch control
	DSJ_LOGOTHER	= 98 # Category other than above
	DSJ_LOGANY		= 99 # Any type of event

	# DSRUNJOB 'runMode' values
	DSJ_RUNNORMAL	= 1	# Standard job run.
	DSJ_RUNRESET	= 2	# Job is to be reset.
	DSJ_RUNVALIDATE	= 3	# Job is to be validated only.
	DSJ_RUNRESTART	= 4 # Restart job with previous parameters, job must be in Restartable state.

	# DSPARAM 'paramType' values
	DSJ_PARAMTYPE_STRING	= 0
	DSJ_PARAMTYPE_ENCRYPTED	= 1
	DSJ_PARAMTYPE_INTEGER	= 2
	DSJ_PARAMTYPE_FLOAT		= 3
	DSJ_PARAMTYPE_PATHNAME	= 4
	DSJ_PARAMTYPE_LIST		= 5
	DSJ_PARAMTYPE_DATE		= 6
	DSJ_PARAMTYPE_TIME		= 7

	def __init__(self):
		self.libapi 	= None
		self.handleProj = None

	#####################################################
	###                API FUNCTIONS                  ###
	#####################################################
	def DSSetServerParams(self, DomainName, UserName, Password, ServerName):
		self.libapi.DSSetServerParams.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
		self.libapi.DSSetServerParams.restype  = ctypes.c_void_p
		self.libapi.DSSetServerParams(self.encodeString(DomainName), self.encodeString(UserName), self.encodeString(Password), self.encodeString(ServerName))

		return True, None

	def DSGetProjectList(self):
		self.libapi.DSGetProjectList.argtypes = []
		self.libapi.DSGetProjectList.restype  = ctypes.POINTER(ctypes.c_char)
		projectList = self.libapi.DSGetProjectList()

		if not projectList:
			return None, self.createError("[DSGetProjectList]: {}".format(self.DSGetLastError()))
		else:
			return self.charPointerToList(projectList), None

	def DSOpenProject(self, projectName):
		self.libapi.DSOpenProjectEx.argtypes = [ctypes.c_int, ctypes.c_char_p]
		self.libapi.DSOpenProjectEx.restype  = ctypes.POINTER(DSPROJECT)
		handleProj = self.libapi.DSOpenProjectEx(self.DSAPI_VERSION, self.encodeString(projectName))

		if not handleProj:
			return None, self.createError("[DSOpenProject]: {}".format(self.DSGetLastError()))
		else:
			self.handleProj = handleProj
			return handleProj, None

	def DSGetProjectInfo(self, handleProj, infoType):

		if infoType < self.DSJ_JOBLIST or infoType > self.DSJ_PROJECTPATH:
			return None, self.createError("[DSGetProjectInfo]: infotype = {} doesn't exsist".format(infoType))

		self.libapi.DSGetProjectInfo.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_int, ctypes.POINTER(DSPROJECTINFO)]
		self.libapi.DSGetProjectInfo.restype  = ctypes.c_int

		projInfo = DSPROJECTINFO()
		res = self.libapi.DSGetProjectInfo(handleProj, infoType, ctypes.pointer(projInfo))

		if res != self.DSJE_NOERROR:
			return None, res

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
		self.libapi.DSGetLastError.restype = ctypes.c_int

		self.libapi.DSGetLastErrorMsg.argtypes = [ctypes.POINTER(DSPROJECT)]
		self.libapi.DSGetLastErrorMsg.restype  =  ctypes.c_char_p

		if self.handleProj is not None:
			return str(self.libapi.DSGetLastError()) + ", " + self.decodeBytes(self.libapi.DSGetLastErrorMsg(self.handleProj))
		else:
			return str(self.libapi.DSGetLastError())

	def DSOpenJob(self, handleProj, jobName):

		if handleProj is None:
			return None, self.createError("[DSOpenJob]: the project doesn't select")

		self.libapi.DSOpenJob.argtypes = [ctypes.POINTER(DSPROJECT), ctypes.c_char_p]
		self.libapi.DSOpenJob.restype  = ctypes.POINTER(DSJOB)
		handleJob = self.libapi.DSOpenJob(handleProj, ctypes.c_char_p(self.encodeString(jobName)))

		if not handleJob:
			return None, self.createError("[DSOpenJob]: {}".format(self.DSGetLastError()))
		else:
			self.handleJob = handleJob
			return handleJob, None

	def DSGetJobInfo(self, handleJob, infoType):

		if handleJob is None:
			return None, self.createError("[DSGetJobInfo]: the job doesn't open")

		if infoType < self.DSJ_JOBSTATUS or infoType > self.DSJ_JOBRESTARTABLE:
			return None, self.createError("[DSGetJobInfo]: infotype = {} doesn't exsist".format(infoType))

		self.libapi.DSGetJobInfo.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSJOBINFO)]
		self.libapi.DSGetJobInfo.restype  = ctypes.c_int

		jobInfo = DSJOBINFO()
		res = self.libapi.DSGetJobInfo(handleJob, infoType, ctypes.pointer(jobInfo))

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSGetJobInfo]: {}".format(self.DSGetLastError()))
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
				return jobInfo.info.stageList, None
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
				return jobInfo.info.stageList2, None
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

	def DSFindFirstLogEntry(self, handleJob, eventType = DSJ_LOGANY, startTime = 0, endTime = 0, maxNumber = 250):
		if handleJob is None:
			return None, self.createError("[DSFindFirstLogEntry]: the job doesn't open")

		if eventType < self.DSJ_LOGINFO or eventType > self.DSJ_LOGANY:
			return None, self.createError("[DSFindFirstLogEntry]: eventtype = {} doesn't exsist".format(eventType))

		self.libapi.DSFindFirstLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, time_t, time_t, ctypes.c_int, ctypes.POINTER(DSLOGEVENT)]
		self.libapi.DSFindFirstLogEntry.restype  = ctypes.c_int

		logInfo = DSLOGEVENT()
		res = self.libapi.DSFindFirstLogEntry(handleJob, eventType, startTime, endTime, maxNumber, ctypes.pointer(logInfo))

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSFindFirstLogEntry]: {}".format(self.DSGetLastError()))
		else:
			return logInfo, None

	def DSFindNextLogEntry(self, handleJob):
		if handleJob is None:
			return None, self.createError("[DSFindNextLogEntry]: the job doesn't open")

		self.libapi.DSFindNextLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.POINTER(DSLOGEVENT)]
		self.libapi.DSFindNextLogEntry.restype = ctypes.c_int

		logEvent = DSLOGEVENT()
		res = self.libapi.DSFindNextLogEntry(handleJob, ctypes.pointer(logEvent))

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSFindNextLogEntry]: {}".format(self.DSGetLastError()))
		else:
			return logEvent, None

	def DSGetLogEntryFull(self, handleJob, eventId):
		if handleJob is None:
			return None, self.createError("[DSGetLogEntryFull]: the job doesn't open")

		self.libapi.DSGetLogEntryFull.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSLOGDETAILFULL)]
		self.libapi.DSGetLogEntryFull.restype  = ctypes.c_int

		logDetail = DSLOGDETAILFULL()
		res = self.libapi.DSGetLogEntryFull(handleJob, eventId, ctypes.pointer(logDetail))

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSGetLogEntryFull]: {}".format(self.DSGetLastError()))
		else:
			return logDetail, None

	def DSGetLogEntry(self, handleJob, eventId):
		if handleJob is None:
			return None, self.createError("[DSGetLogEntry]: the job doesn't open")

		self.libapi.DSGetLogEntry.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.POINTER(DSLOGDETAIL)]
		self.libapi.DSGetLogEntry.restype  = ctypes.c_int

		logDetail = DSLOGDETAIL()
		res = self.libapi.DSGetLogEntry(handleJob, eventId, ctypes.pointer(logDetail))

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSGetLogEntry]: {}".format(self.DSGetLastError()))
		else:
			return logDetail, None

	def DSGetNewestLogId(self, handleJob, eventType):
		if handleJob is None:
			return None, self.createError("[DSGetNewestLogId]: the job doesn't open")

		self.libapi.DSGetNewestLogId.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
		self.libapi.DSGetNewestLogId.restype = ctypes.c_int

		lastLogId = self.libapi.DSGetNewestLogId(handleJob, eventType)

		if lastLogId == -1:
			return None, self.createError("[DSGetNewestLogId]: {}".format(self.DSGetLastError()))
		else:
			return lastLogId, None

	def DSGetQueueList(self):
		self.libapi.DSGetQueueList.restype = ctypes.POINTER(ctypes.c_char)
		qList = self.libapi.DSGetQueueList()

		return self.charPointerToList(qList), None

	def DSSetJobQueue(self, handleJob, queueName):
		if handleJob is None:
			return None, self.createError("[DSSetJobQueue]: the job doesn't open")

		self.libapi.DSSetJobQueue.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p]
		self.libapi.DSSetJobQueue.restype  = ctypes.c_int

		res = self.libapi.DSSetJobQueue(handleJob, queueName)

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSSetJobQueue]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSCloseJob(self, handleJob):

		self.libapi.DSCloseJob.argtypes = [ctypes.POINTER(DSJOB)]
		self.libapi.DSCloseJob.restype  = ctypes.c_int

		res = self.libapi.DSCloseJob(handleJob)

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSCloseJob]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSCloseProject(self, handleProj):

		self.libapi.DSCloseProject.argtypes = [ctypes.POINTER(DSPROJECT)]
		self.libapi.DSCloseProject.restype  = ctypes.c_int

		res = self.libapi.DSCloseProject(self.handleProj)
		self.handleProj = None

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSCloseProject]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSRunJob(self, handleJob, runMode):
		if handleJob is None:
			return None, self.createError("[DSRunJob]: the job doesn't open")

		self.libapi.DSRunJob.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int]
		self.libapi.DSRunJob.restype  = ctypes.c_int

		res = self.libapi.DSRunJob(handleJob, runMode)

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSRunJob]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSLockJob(self, handleJob):
		if handleJob is None:
			return None, self.createError("[DSLockJob]: the job doesn't open")

		self.libapi.DSLockJob.argtypes = [ctypes.POINTER(DSJOB)]
		self.libapi.DSLockJob.restype  = ctypes.c_int

		res = self.libapi.DSLockJob(handleJob)

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSLockJob]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSUnlockJob(self, handleJob):
		if handleJob is None:
			return None, self.createError("[DSUnlockJob]: the job doesn't open")

		self.libapi.DSUnlockJob.argtypes = [ctypes.POINTER(DSJOB)]
		self.libapi.DSUnlockJob.restype  = ctypes.c_int

		res = self.libapi.DSUnlockJob(handleJob)

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSUnlockJob]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSWaitForJob(self, handleJob):
		if handleJob is None:
			return None, self.createError("[DSWaitForJob]: the job doesn't open")

		self.libapi.DSWaitForJob.argtypes = [ctypes.POINTER(DSJOB)]
		self.libapi.DSWaitForJob.restype  = ctypes.c_int

		res = self.libapi.DSWaitForJob(handleJob)

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSWaitForJob]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSSetParam(self, handleJob, ParamName, Param):
		if handleJob is None:
			return None, self.createError("[DSSetParam]: the job doesn't open")

		self.libapi.DSSetParam.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_char_p, ctypes.POINTER(DSPARAM)]
		self.libapi.DSSetParam.restype  = ctypes.c_int

		res = self.libapi.DSSetParam(handleJob, ParamName, ctypes.pointer(Param))

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSSetParam]: {}".format(self.DSGetLastError()))
		else:
			return 0, None

	def DSMakeJobReport(self, handleJob, reportType, lineSeparator='CRLF'):
		if handleJob is None:
			return None, self.createError("[DSMakeJobReport]: the job doesn't open")

		self.libapi.DSMakeJobReport.argtypes = [ctypes.POINTER(DSJOB), ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(DSREPORTINFO)]
		self.libapi.DSMakeJobReport.restype  = ctypes.c_int

		reportInfo = DSREPORTINFO()
		res = self.libapi.DSMakeJobReport(handleJob, reportType, self.encodeString(lineSeparator), ctypes.pointer(reportInfo))

		if res != self.DSJE_NOERROR:
			return None, self.createError("[DSMakeJobReport]: {}".format(self.DSGetLastError()))
		else:
			return reportInfo.info.reportText, None

	#####################################################
	###              CUSTOM FUNCTIONS                 ###
	#####################################################

	def DSLoadLibrary(self, api_lib_file):
		"""
		api_lib_file - full path to C api library
			vmdsapi.dll on WIN
			or
			libvmdsapi.so on HP-UX

		PATH on WIN should include paths
			where located files: ['vmdsapi.dll', 'dsrpc32.dll', 'DSCLNT32.DLL']

		LD_LIBRARY_PATH on HP-UX should include paths
			where located files: ['libvmdsapi.so', 'libinvocation_cpp.so'] and its dependences 
		"""

		if not os.path.exists(api_lib_file) or not os.path.isfile(api_lib_file):
			return None, self.createError("[DSLoadLibrary]: path to {} doesn't exsist".format(api_lib_file))

		try:
			self.libapi = ctypes.CDLL(api_lib_file)
		except OSError as e:
			return None, self.createError("[DSLoadLibrary]: can't load the library. Error: {}; Edit your PATH(win) or LD_LIBRARY_PATH(hp-ux)".format(str(e)))

		return True, None

	def DSUnloadLibrary(self):
		self.libapi 	= None
		self.handleProj = None

	def charPointerToList(self, char_pointer):

		if not char_pointer:
			return []

		char_list 	  = []
		word      	  = ''
		pred_char 	  = '*'
		stop_char	  = b'\x00'
		it 		  	  = 0

		while True:
			if char_pointer[it] == stop_char:
				if pred_char == stop_char:
					break

				char_list.append(word)
				word = ''
			else:
				word = word + self.decodeBytes(char_pointer[it])

			pred_char = char_pointer[it]
			it = it + 1

		return char_list

	def createError(self, error_msg):
		return "[ERROR.DSAPI]: {}" .format(error_msg)

	def decodeBytes(self, str):
		return str.decode("cp1251", errors="ignore")

	def encodeString(self, str):
		return str.encode("utf-8")
