# -*- coding: utf-8 -*-

'''
	My Accounts
'''

from myaccounts.modules import control


def getAll():
	dict1 = dict(getTrakt(), **getAllDebrid())
	dict2 = dict(dict1, **getAllMeta())
	dict3 = dict(dict2, **getAllScraper())
	return dict3


def getTrakt():
	trakt = {'trakt': {}}
	trakt['trakt']['token'] = control.setting('trakt.token')
	trakt['trakt']['username'] = control.setting('trakt.username')
	trakt['trakt']['refresh'] = control.setting('trakt.refresh')
	trakt['trakt']['expires'] = control.setting('trakt.expires')
	return trakt


def getAllDebrid():
	dict1 = dict(getAD(), **getPM())
	dict2 = dict(dict1, **getRD())
	return dict2


def getAD():
	ad = {'alldebrid': {}}
	ad['alldebrid']['token'] = control.setting('alldebrid.token')
	ad['alldebrid']['username'] = control.setting('alldebrid.username')
	return ad


def getPM():
	pm = {'premiumize': {}}
	pm['premiumize']['token'] = control.setting('premiumize.token')
	pm['premiumize']['username'] = control.setting('premiumize.username')
	return pm


def getRD():
	rd = {'realdebrid': {}}
	rd['realdebrid']['token'] = control.setting('realdebrid.token')
	rd['realdebrid']['username'] = control.setting('realdebrid.username')
	rd['realdebrid']['client_id'] = control.setting('realdebrid.client_id')
	rd['realdebrid']['refresh'] = control.setting('realdebrid.refresh')
	rd['realdebrid']['secret'] = control.setting('realdebrid.secret')
	return rd


def getAllMeta():
	dict1 = dict(getFanart_tv(), **getTMDb())
	dict2 = dict(dict1, **getTVDb())
	dict3 = dict(dict2, **getIMDb())
	return dict3


def getFanart_tv():
	fanart = {'fanart_tv': {}}
	fanart['fanart_tv']['api_key'] = control.setting('fanart.tv.api.key')
	return fanart


def getTMDb():
	tmdb = {'tmdb': {}}
	tmdb['tmdb']['api_key'] = control.setting('tmdb.api.key')
	tmdb['tmdb']['username'] = control.setting('tmdb.username')
	tmdb['tmdb']['password'] = control.setting('tmdb.password')
	tmdb['tmdb']['session_id'] = control.setting('tmdb.session_id')
	return tmdb


def getTVDb():
	tvdb = {'tvdb': {}}
	# keys must be .decode('base64') by addon to use
	tvdb_key_list = [
		'MDZjZmYzMDY5MGY5Yjk2MjI5NTcwNDRmMjE1OWZmYWU=',
		'MUQ2MkYyRjkwMDMwQzQ0NA==',
		'N1I4U1paWDkwVUE5WU1CVQ==']
	api_key = tvdb_key_list[int(control.setting('tvdb.api.key'))]
	tvdb['tvdb']['api_key'] = api_key
	return tvdb


def getIMDb():
	imdb = {'imdb': {}}
	imdb['imdb']['user'] = control.setting('imdb.user')
	return imdb


def getAllScraper():
	dict1 = dict(getFilepursuit(), **getFurk())
	dict2 = dict(dict1, **getEasyNews())
	dict3 = dict(dict2, **getOrro())
	return dict3


def getFilepursuit():
	filePursuit = {'filepursuit': {}}
	filePursuit['filepursuit']['api_key'] = control.setting('filepursuit.api.key')
	return filePursuit


def getFurk():
	furk = {'furk': {}}
	furk['furk']['username'] = control.setting('furk.username')
	furk['furk']['password'] = control.setting('furk.password')
	furk['furk']['api_key'] = control.setting('furk.api.key')
	return furk


def getEasyNews():
	easyNews = {'easyNews': {}}
	easyNews['easyNews']['username'] = control.setting('easynews.username')
	easyNews['easyNews']['password'] = control.setting('easynews.password')
	return easyNews


def getOrro():
	ororo = {'ororo': {}}
	ororo['ororo']['email'] = control.setting('ororo.email')
	ororo['ororo']['password'] = control.setting('ororo.password')
	return ororo

def traktRefreshToken():
	from modules.trakt import Trakt
	Trakt().refresh_token()

def realdebridRefreshToken():
	from modules.realdebrid import RealDebrid
	RealDebrid().refresh_token()