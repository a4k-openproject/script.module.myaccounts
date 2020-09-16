# -*- coding: utf-8 -*-

'''
	My Accounts
'''

import os.path
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

addon = xbmcaddon.Addon
addonObject = addon('script.module.myaccounts')
addonInfo = addonObject.getAddonInfo
setting = addonObject.getSetting
setSetting = addonObject.setSetting

getLangString = xbmcaddon.Addon().getLocalizedString

condVisibility = xbmc.getCondVisibility
execute = xbmc.executebuiltin
jsonrpc = xbmc.executeJSONRPC
monitor = xbmc.Monitor()

dialog = xbmcgui.Dialog()
progressDialog = xbmcgui.DialogProgress()

joinPath = os.path.join

existsPath = xbmcvfs.exists
makeFile = xbmcvfs.mkdir
openFile = xbmcvfs.File



def lang(language_id):
	text = getLangString(language_id)
	if getKodiVersion() < 19:
		text = text.encode('utf-8', 'replace')
	return text


def sleep(time):  # Modified `sleep` command that honors a user exit request
	while time > 0 and not monitor.abortRequested():
		xbmc.sleep(min(100, time))
		time = time - 100


def getKodiVersion():
	return int(xbmc.getInfoLabel("System.BuildVersion")[:2])


def check_version_numbers(current, new):
	# Compares version numbers and return True if new version is newer
	current = current.split('.')
	new = new.split('.')
	step = 0
	for i in current:
		if int(new[step]) > int(i):
			return True
		if int(i) == int(new[step]):
			step += 1
			continue
	return False


def addonId():
	return addonInfo('id')


def addonName():
	return addonInfo('name')


def addonVersion():
	return addonInfo('version')


def addonIcon():
	return addonInfo('icon')


def artPath():
	return os.path.join(xbmcaddon.Addon('script.module.myaccounts').getAddonInfo('path'), 'resources', 'icons')


def openSettings(query=None, id=addonInfo('id')):
	try:
		idle()
		execute('Addon.OpenSettings(%s)' % id)
		if query is None:
			raise Exception()
		c, f = query.split('.')
		if getKodiVersion() >= 18:
			execute('SetFocus(%i)' % (int(c) - 100))
			execute('SetFocus(%i)' % (int(f) - 80))
		else:
			execute('SetFocus(%i)' % (int(c) + 100))
			execute('SetFocus(%i)' % (int(f) + 200))
	except:
		return


def idle():
	if getKodiVersion() >= 18 and condVisibility('Window.IsActive(busydialognocancel)'):
		return execute('Dialog.Close(busydialognocancel)')
	else:
		return execute('Dialog.Close(busydialog)')


def notification(title=None, message=None, icon=None, time=3000, sound=False):
	if title == 'default' or title is None:
		title = addonName()
	if isinstance(title, (int, long)):
		heading = lang(title)
	else:
		heading = str(title)
	if isinstance(message, (int, long)):
		body = lang(message)
	else:
		body = str(message)
	if icon is None or icon == '' or icon == 'default':
		icon = addonIcon()
	elif icon == 'INFO':
		icon = xbmcgui.NOTIFICATION_INFO
	elif icon == 'WARNING':
		icon = xbmcgui.NOTIFICATION_WARNING
	elif icon == 'ERROR':
		icon = xbmcgui.NOTIFICATION_ERROR
	dialog.notification(heading, body, icon, time, sound=sound)


def yesnoDialog(line1, line2, line3, heading=addonInfo('name'), nolabel='', yeslabel=''):
	return dialog.yesno(heading, line1, line2, line3, nolabel, yeslabel)


def selectDialog(list, heading=addonInfo('name')):
	return dialog.select(heading, list)


def okDialog(title=None, message=None):
	if title == 'default' or title is None:
		title = addonName()
	if isinstance(title, (int, long)):
		heading = lang(title)
	else:
		heading = str(title)
	if isinstance(message, (int, long)):
		body = lang(message)
	else:
		body = str(message)
	return dialog.ok(heading, body)


def closeAll():
	return execute('Dialog.Close(all, true)')


def jsondate_to_datetime(jsondate_object, resformat, remove_time=False):
	import _strptime  # fix bug in python import
	from datetime import datetime
	import time
	if remove_time:
		try: datetime_object = datetime.strptime(jsondate_object, resformat).date()
		except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6])).date()
	else:
		try: datetime_object = datetime.strptime(jsondate_object, resformat)
		except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6]))
	return datetime_object