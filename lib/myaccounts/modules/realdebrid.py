# -*- coding: utf-8 -*-

'''
	My Accounts
'''

import json
import requests

from myaccounts.modules import control
from myaccounts.modules import log_utils


FormatDateTime = "%Y-%m-%dT%H:%M:%S.%fZ"
rest_base_url = 'https://api.real-debrid.com/rest/1.0/'
oauth_base_url = 'https://api.real-debrid.com/oauth/v2/'
device_code_url = 'device/code?%s'
credentials_url = 'device/credentials?%s'

rd_icon = control.joinPath(control.artPath(), 'realdebrid.png')

class RealDebrid:

	def __init__(self):
		self.token = control.setting('realdebrid.token')
		self.client_ID = control.setting('realdebrid.client_id')
		if self.client_ID == '':
			self.client_ID = 'X245A4XAIBGVM'
		self.secret = control.setting('realdebrid.secret')
		self.device_code = ''
		self.auth_timeout = 0
		self.auth_step = 0


	def _get(self, url, fail_check=False, token_ck=False):
		try:
			original_url = url
			url = rest_base_url + url
			if self.token == '':
				log_utils.log('No Real Debrid Token Found', __name__, log_utils.LOGDEBUG)
				return None
			# if not fail_check: # with fail_check=True new token does not get added
			if '?' not in url:
				url += "?auth_token=%s" % self.token
			else:
				url += "&auth_token=%s" % self.token
			response = requests.get(url, timeout=15).json()
			if 'bad_token' in str(response) or 'Bad Request' in str(response):
				if not fail_check:
					if self.refresh_token() and token_ck:
						return
					response = self._get(original_url, fail_check=True)
			return response
		except:
			log_utils.error()
			pass
		return None


	def _post(self, url, data):
		original_url = url
		url = rest_base_url + url
		if self.token == '':
			log_utils.log('No Real Debrid Token Found', __name__, log_utils.LOGDEBUG)
			return None
		if '?' not in url:
			url += "?auth_token=%s" % self.token
		else:
			url += "&auth_token=%s" % self.token
		response = requests.post(url, data=data, timeout=15).text
		if 'bad_token' in response or 'Bad Request' in response:
			self.refresh_token()
			response = self._post(original_url, data)
		elif 'error' in response:
			response = json.loads(response)
			control.notification(title='default', message=response.get('error'), icon='default')
			return None
		try:
			return json.loads(response)
		except:
			return response


	def auth_loop(self):
		control.sleep(self.auth_step*1000)
		url = 'client_id=%s&code=%s' % (self.client_ID, self.device_code)
		url = oauth_base_url + credentials_url % url
		response = json.loads(requests.get(url).text)
		if 'error' in response:
			return #
		else:
			try:
				control.progressDialog.close()
				self.client_ID = response['client_id']
				self.secret = response['client_secret']
			except:
				log_utils.error()
				control.okDialog(title='default', message=control.lang(40019))
			return


	def auth(self):
		self.secret = ''
		self.client_ID = 'X245A4XAIBGVM'
		url = 'client_id=%s&new_credentials=yes' % self.client_ID
		url = oauth_base_url + device_code_url % url
		response = json.loads(requests.get(url).text)
		control.progressDialog.create(control.lang(40055))
		control.progressDialog.update(-1,
				control.lang(32513) % 'https://real-debrid.com/device',
				control.lang(32514) % response['user_code'])

		self.auth_timeout = int(response['expires_in'])
		self.auth_step = int(response['interval'])
		self.device_code = response['device_code']

		while self.secret == '':
			if control.progressDialog.iscanceled():
				control.progressDialog.close()
				break
			self.auth_loop()
		if self.secret:
			if self.get_token():
				control.notification(message=40079, icon=rd_icon)
			else:
				return control.okDialog(title='default', message=control.lang(40019))


	def account_info(self):
		return self._get('user')


	def account_info_to_dialog(self):
		from datetime import datetime
		import time
		try:
			userInfo = self.account_info()
			try:
				expires = datetime.strptime(userInfo['expiration'], FormatDateTime)
			except:
				expires = datetime(*(time.strptime(userInfo['expiration'], FormatDateTime)[0:6]))
			days_remaining = (expires - datetime.today()).days
			expires = expires.strftime("%A, %B %d, %Y")
			items = []
			items += [control.lang(40035) % userInfo['email']]
			items += [control.lang(40036) % userInfo['username']]
			items += [control.lang(40037) % userInfo['type'].capitalize()]
			items += [control.lang(40041) % expires]
			items += [control.lang(40042) % days_remaining]
			items += [control.lang(40038) % userInfo['points']]
			return control.selectDialog(items, 'Real-Debrid')
		except:
			log_utils.error()
			pass
		return


	def refresh_token(self):
		try:
			self.client_ID = control.setting('realdebrid.client_id')
			self.secret = control.setting('realdebrid.secret')
			self.device_code = control.setting('realdebrid.refresh')
			log_utils.log('Refreshing Expired Real Debrid Token: |%s|%s|' % (self.client_ID, self.device_code), __name__, log_utils.LOGDEBUG)
			if not self.get_token():
				self.revoke()
				log_utils.log('Unable to Refresh Real Debrid Token', __name__, log_utils.LOGDEBUG)
			else:
				log_utils.log('Real Debrid Token Successfully Refreshed', __name__, log_utils.LOGDEBUG)
				return True
		except:
			log_utils.error()
			return False

	def get_token(self):
		try:
			url = oauth_base_url + 'token'
			postData = {'client_id': self.client_ID, 'client_secret': self.secret, 'code': self.device_code, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
			response = requests.post(url, data=postData).json()
			self.token = response['access_token']
			control.sleep(1500)
			account_info = self.account_info()
			username = account_info['username']
			control.setSetting('realdebrid.username', username)
			control.setSetting('realdebrid.client_id', self.client_ID)
			control.setSetting('realdebrid.secret', self.secret,)
			control.setSetting('realdebrid.token', self.token)
			control.setSetting('realdebrid.refresh', response['refresh_token'])
			return True
		except Exception as e:
			log_utils.log('Real Debrid Authorization Failed: %s' % e, __name__, log_utils.LOGDEBUG)
			return False


	def revoke(self):
		try:
			control.setSetting('realdebrid.client_id', '')
			control.setSetting('realdebrid.secret', '')
			control.setSetting('realdebrid.token', '')
			control.setSetting('realdebrid.refresh', '')
			control.setSetting('realdebrid.username', '')
			control.dialog.ok('My Accounts', control.lang(32314))
		except:
			log_utils.error()
			pass