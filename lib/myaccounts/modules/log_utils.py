# -*- coding: utf-8 -*-

'''
	My Accounts
'''

from datetime import datetime
import inspect
import xbmc
from xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING  # @UnusedImport

from myaccounts.modules import control

DEBUGPREFIX = '[COLOR red][ My Accounts DEBUG ][/COLOR]'
LOGPATH = xbmc.translatePath('special://logpath/')
addonName = "My Accounts"


def log(msg, caller=None, level=LOGNOTICE):
	debug_enabled = control.setting('debug.enabled') == 'true'
	debug_log = control.setting('debug.location')

	if not debug_enabled:
		return
	try:
		if caller is not None and level == LOGDEBUG:
			func = inspect.currentframe().f_back.f_code
			line_number = inspect.currentframe().f_back.f_lineno
			caller = "%s.%s()" % (caller, func.co_name)
			msg = 'From func name: %s Line # :%s\n                       msg : %s' % (caller, line_number, msg)

		if caller is not None and level == LOGERROR:
			msg = 'From func name: %s.%s() Line # :%s\n                       msg : %s' % (caller[0], caller[1], caller[2], msg)

		if isinstance(msg, unicode):
			msg = '%s (ENCODED)' % (msg.encode('utf-8'))

		if debug_log == '1':
			log_file = control.joinPath(LOGPATH, 'myaccounts.log')
			if not control.existsPath(log_file):
				f = open(log_file, 'w')
				f.close()
			with open(log_file, 'a') as f:
				line = '[%s %s] %s: %s' % (datetime.now().date(), str(datetime.now().time())[:8], DEBUGPREFIX, msg)
				f.write(line.rstrip('\r\n')+'\n')
		else:
			print('%s: %s' % (DEBUGPREFIX, msg))
	except Exception as e:
		import traceback
		traceback.print_exc()

		try:
			xbmc.log('Logging Failure: %s' % (e), level)
		except:
			pass


def log2(msg, level='info'):
	msg = safeStr(msg)
	msg = addonName.upper() + ': ' + msg
	if level == 'error':
		xbmc.log(msg, level=xbmc.LOGERROR)
	elif level == 'info':
		xbmc.log(msg, level=xbmc.LOGINFO)
	elif level == 'notice':
		xbmc.log(msg, level=xbmc.LOGNOTICE)
	elif level == 'warning':
		xbmc.log(msg, level=xbmc.LOGWARNING)
	else:
		xbmc.log(msg)


def error(message=None, exception=True):
	try:
		import sys
		if exception:
			type, value, traceback = sys.exc_info()
			addon = 'script.module.myaccounts'
			filename = (traceback.tb_frame.f_code.co_filename)
			filename = filename.split(addon)[1]
			name = traceback.tb_frame.f_code.co_name
			linenumber = traceback.tb_lineno
			errortype = type.__name__
			errormessage = value.message or value # sometime value.message is null while value is not
			if str(errormessage) == '':
				return
			if message:
				message += ' -> '
			else:
				message = ''
			message += str(errortype) + ' -> ' + str(errormessage)
			caller = [filename, name, linenumber]
		else:
			caller = None
		log(msg=message, caller=caller, level=LOGERROR)
		del(type, value, traceback) # So we don't leave our local labels/objects dangling
	except:
		import traceback
		traceback.print_exc()
		pass


def safeStr(obj):
	try:
		return str(obj)
	except UnicodeEncodeError:
		return obj.encode('utf-8', 'ignore').decode('ascii', 'ignore')
	except:
		return ""

