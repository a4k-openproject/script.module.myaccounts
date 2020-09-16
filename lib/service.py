# -*- coding: utf-8 -*-

'''
	My Accounts
'''

from myaccounts.modules import control
from myaccounts.modules import log_utils


class AddonCheckUpdate:
	def run(self):
		log_utils.log('My Accounts checking available updates', log_utils.LOGNOTICE)
		try:
			import re
			import requests
			repo_xml = requests.get('https://raw.githubusercontent.com/a4k-openproject/repository.myaccounts/master/zips/addons.xml')
			if repo_xml.status_code != 200:
				log_utils.log('Could not connect to My Accounts repo XML, status: %s' % repo_xml.status_code, log_utils.LOGNOTICE)
				return
			repo_version = re.findall(r'<addon id=\"script.module.myaccounts\".*version=\"(\d*.\d*.\d*.\d*)\"', repo_xml.text)[0]
			local_version = control.addonVersion()
			if control.check_version_numbers(local_version, repo_version):
				while control.condVisibility('Library.IsScanningVideo'):
					control.sleep(10000)
				log_utils.log('A newer version of My Accounts is available. Installed Version: v%s, Repo Version: v%s' % (local_version, repo_version), log_utils.LOGNOTICE)
				control.notification(title = 'default', message = 'A new verison of My Accounts is available from the repository. Please consider updating to v%s' % repo_version, icon = 'default', time=5000, sound=False)
		except:
			log_utils.error()
			pass

if control.setting('general.checkAddonUpdates') == 'true':
	AddonCheckUpdate().run()
	xbmc.log('[ script.module.myaccounts ] Addon update check complete', xbmc.LOGNOTICE)