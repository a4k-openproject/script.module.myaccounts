# -*- coding: utf-8 -*-

'''
	My Accounts
'''

import sys
try:
	from urlparse import parse_qsl
except:
	from urllib.parse import parse_qsl
from myaccounts.modules import control


params = {}
for param in sys.argv[1:]:
	param = param.split('=')
	param_dict = dict([param])
	params = dict(params, **param_dict)

action = params.get('action')
query = params.get('query')


if action is None:
	control.openSettings(query, "script.module.myaccounts")

elif action == 'traktAcct':
	from myaccounts.modules import trakt
	trakt.Trakt().account_info_to_dialog()

elif action == 'traktAuth':
	from myaccounts.modules import trakt
	trakt.Trakt().auth()

elif action == 'traktRevoke':
	from myaccounts.modules import trakt
	trakt.Trakt().revoke()

elif action == 'alldebridAcct':
	from myaccounts.modules import alldebrid
	alldebrid.AllDebrid().account_info_to_dialog()

elif action == 'alldebridAuth':
	from myaccounts.modules import alldebrid
	alldebrid.AllDebrid().auth()

elif action == 'alldebridRevoke':
	from myaccounts.modules import alldebrid
	alldebrid.AllDebrid().revoke()

elif action == 'premiumizeAcct':
	from myaccounts.modules import premiumize
	premiumize.Premiumize().account_info_to_dialog()

elif action == 'premiumizeAuth':
	from myaccounts.modules import premiumize
	premiumize.Premiumize().auth()

elif action == 'premiumizeRevoke':
	from myaccounts.modules import premiumize
	premiumize.Premiumize().revoke()

elif action == 'realdebridAcct':
	from myaccounts.modules import realdebrid
	realdebrid.RealDebrid().account_info_to_dialog()

elif action == 'realdebridAuth':
	from myaccounts.modules import realdebrid
	realdebrid.RealDebrid().auth()

elif action == 'realdebridRevoke':
	from myaccounts.modules import realdebrid
	realdebrid.RealDebrid().revoke()

elif action == 'tmdbAuth':
	from myaccounts.modules import tmdb
	tmdb.Auth().create_session_id()

elif action == 'tmdbRevoke':
	from myaccounts.modules import tmdb
	tmdb.Auth().revoke_session_id()

elif action == 'ShowChangelog':
	from myaccounts.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from myaccounts.help import help
	help.get(params.get('name'))
