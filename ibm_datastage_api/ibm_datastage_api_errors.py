class DSAPIERROR:
    DSJE_NOERROR = 0
    DSJE_BADHANDLE = -1
    DSJE_BADSTATE = -2
    DSJE_BADPARAM = -3
    DSJE_BADVALUE = -4
    DSJE_BADTYPE = -5
    DSJE_WRONGJOB = -6
    DSJE_BADSTAGE = -7
    DSJE_NOTINSTAGE = -8
    DSJE_BADLINK = -9
    DSJE_JOBLOCKED = -10
    DSJE_JOBDELETED = -11
    DSJE_BADNAME = -12
    DSJE_BADTIME = -13
    DSJE_TIMEOUT = -14
    DSJE_DECRYPTERR = -15
    DSJE_NOACCESS = -16
    DSJE_NOTEMPLATE = -17
    DSJE_BADTEMPLATE = -18
    DSJE_NOPARAM = -19
    DSJE_NOFILEPATH = -20
    DSJE_CMDERROR = -21
    DSJE_BADVAR = -22
    DSJE_NONUNIQUEID = -23
    DSJE_INVALIDID = -24
    DSJE_INVALIDQUEUE = -25
    DSJE_WLMDISABLED = -26
    DSJE_WLMNOTRUNNING = -27
    DSJE_NOROLEPERMISSIONS = -28
    DSJE_REPERROR = -99
    DSJE_NOTADMINUSER = -100
    DSJE_ISADMINFAILED = -101
    DSJE_READPROJPROPERTY = -102
    DSJE_WRITEPROJPROPERTY = -103
    DSJE_BADPROPERTY = -104
    DSJE_PROPNOTSUPPORTED = -105
    DSJE_BADPROPVALUE = -106
    DSJE_OSHVISIBLEFLAG = -107
    DSJE_BADENVVARNAME = -108
    DSJE_BADENVVARTYPE = -109
    DSJE_BADENVVARPROMPT = -110
    DSJE_READENVVARDEFNS = -111
    DSJE_READENVVARVALUES = -112
    DSJE_WRITEENVVARDEFNS = -113
    DSJE_WRITEENVVARVALUES = -114
    DSJE_DUPENVVARNAME = -115
    DSJE_BADENVVAR = -116
    DSJE_NOTUSERDEFINED = -117
    DSJE_BADBOOLEANVALUE = -118
    DSJE_BADNUMERICVALUE = -119
    DSJE_BADLISTVALUE = -120
    DSJE_PXNOTINSTALLED = -121
    DSJE_ISPARALLELLICENCED = -122
    DSJE_ENCODEFAILED = -123
    DSJE_DELPROJFAILED = -124
    DSJE_DELPROJFILESFAILED = -125
    DSJE_LISTSCHEDULEFAILED = -126
    DSJE_CLEARSCHEDULEFAILED = -127
    DSJE_BADPROJNAME = -128
    DSJE_GETDEFAULTPATHFAILED = -129
    DSJE_BADPROJLOCATION = -130
    DSJE_INVALIDPROJECTLOCATION = -131
    DSJE_OPENFAILED = -132
    DSJE_READUFAILED = -133
    DSJE_ADDPROJECTBLOCKED = -134
    DSJE_ADDPROJECTFAILED = -135
    DSJE_LICENSEPROJECTFAILED = -136
    DSJE_RELEASEFAILED = -137
    DSJE_DELETEPROJECTBLOCKED = -138
    DSJE_NOTAPROJECT = -139
    DSJE_ACCOUNTPATHFAILED = -140
    DSJE_LOGTOFAILED = -141
    DSJE_PROTECTFAILED = -142
    DSJE_UNKNOWN_JOBNAME = -201
    DSJE_NOMORE = -1001
    DSJE_BADPROJECT = -1002
    DSJE_NO_DATASTAGE = -1003
    DSJE_OPENFAIL = -1004
    DSJE_NO_MEMORY = -1005
    DSJE_SERVER_ERROR = -1006
    DSJE_NOT_AVAILABLE = -1007
    DSJE_BAD_VERSION = -1008
    DSJE_INCOMPATIBLE_SERVER = -1009
    DSJE_DOMAINLOGTOFAILED = -1010
    DSJE_NOPRIVILEGE = -1011
    DSJE_LICENSE_EXPIRED = 39121
    DSJE_LIMIT_REACHED = 39134
    DSJE_BAD_CREDENTIAL = 80011
    DSJE_PASSWORD_EXPIRED = 80019
    DSJE_BAD_HOST = 81011

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
        {'token': 'DSJE_BADPROJLOCATION', 'code': -130, 'msg': 'Project location path contains invalid characters'},
        {'token': 'DSJE_INVALIDPROJECTLOCATION', 'code': -131, 'msg': 'Project location is invalid'},
        {'token': 'DSJE_OPENFAILED', 'code': -132, 'msg': 'Failed to open file'},
        {'token': 'DSJE_READUFAILED', 'code': -133, 'msg': 'Failed to lock administration record'},
        {'token': 'DSJE_ADDPROJECTBLOCKED', 'code': -134, 'msg': 'Administration record locked by another user'},
        {'token': 'DSJE_ADDPROJECTFAILED', 'code': -135, 'msg': 'Adding project failed'},
        {'token': 'DSJE_LICENSEPROJECTFAILED', 'code': -136, 'msg': 'Licensing project failed'},
        {'token': 'DSJE_RELEASEFAILED', 'code': -137, 'msg': 'Failed to release administration record'},
        {'token': 'DSJE_DELETEPROJECTBLOCKED', 'code': -138, 'msg': 'Project locked by another user'},
        {'token': 'DSJE_NOTAPROJECT', 'code': -139, 'msg': 'Failed to log to project'},
        {'token': 'DSJE_ACCOUNTPATHFAILED', 'code': -140, 'msg': 'Failed to get account path'},
        {'token': 'DSJE_LOGTOFAILED', 'code': -141, 'msg': 'Failed to log to UV account'},
        {'token': 'DSJE_PROTECTFAILED', 'code': -142, 'msg': 'Protect or unprotect project failed'},
        {'token': 'DSJE_UNKNOWN_JOBNAME', 'code': -201, 'msg': 'Could not find the supplied job name'},
        {'token': 'DSJE_NOMORE', 'code': -1001, 'msg': 'All events matching the filter criteria have been returned'},
        {'token': 'DSJE_BADPROJECT', 'code': -1002, 'msg': 'Unknown project name'},
        {'token': 'DSJE_NO_DATASTAGE', 'code': -1003, 'msg': 'DataStage not installed on server'},
        {'token': 'DSJE_OPENFAIL', 'code': -1004, 'msg': 'Attempt to open job failed'},
        {'token': 'DSJE_NO_MEMORY', 'code': -1005, 'msg': 'Malloc failure'},
        {'token': 'DSJE_SERVER_ERROR', 'code': -1006, 'msg': 'Server generated error - error msg text describes it'},
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
        for err in DSAPIERROR.__mapping:
            if err['code'] == int(error_code):
                return err
        return {'token': 'DSJE_UNKNOWN_ERRORCODE', 'code': error_code, 'msg': 'Unknown error code'}

    @staticmethod
    def get_error_msg(error_code):
        return DSAPIERROR.get_error(error_code)['msg']

    @staticmethod
    def create_error(func_name, api_error):
        err_obj = {
            'type': 'error',
            'func': func_name,
            'code': None,
            'msg': ''
        }

        if isinstance(api_error, dict):
            for key, val in api_error.items():
                err_obj[key] = val
        else:
            err_obj['msg'] = str(api_error)

        return err_obj
