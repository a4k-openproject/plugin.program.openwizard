################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from resources.libs import wizard as wiz

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = wiz.addonId(ADDON_ID)
DIALOG         = xbmcgui.Dialog()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADDOND         = os.path.join(USERDATA,  'addon_data')
LOGINFOLD      = os.path.join(ADDONDATA, 'login')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPLOGIN      = wiz.getS('keeplogin')
LOGINSAVE      = wiz.getS('loginlastsave')
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
ORDER          = ['fanart-exodusredux', 'fanart-gaia', 'fanart-numbers', 'fanart-overeasy', 'fanart-metadatautils', 'fanart-placenta', 'fanart-premiumizer', 'fanart-realizer', 'fanart-scrubs', 'fanart-thecrew', 'fanart-venom', 'fanart-yoda', 'imdb-exodusredux', 'imdb-gaia', 'imdb-numbers', 'imdb-overeasy', 'imdb-placenta', 'imdb-premiumizer', 'imdb-realizer', 'imdb-scrubs', 'imdb-thecrew', 'imdb-venom', 'imdb-yoda', 'kitsu-wonderfulsubs', 'login-iagl', 'login-netflix', 'mal-wonderfulsubs', 'omdb-metadatautils', 'omdb-metahandler', 'login-opensubtitles', 'login-opensubsbyopensubs', 'login-orion', 'tmdb-exodusredux', 'login-eis', 'tmdb-gaia', 'tmdb-metadatautils', 'tmdb-numbers', 'tmdb-eis', 'tmdb-openmeta', 'tmdb-overeasy', 'tmdb-placenta', 'tmdb-premiumizer', 'tmdb-realizer', 'tmdb-scrubs', 'tmdb-seren', 'tmdb-thecrew', 'tmdb-venom', 'tmdb-yoda', 'trakt-openmeta', 'trakt-seren', 'tvdb-metahandler', 'tvdb-openmeta', 'tvdb-premiumizer', 'tvdb-realizer', 'tvdb-seren', 'location-yahoo', 'ws-wonderfulsubs']

LOGINID = {
	'login-opensubtitles': {
		'name'     : 'OpenSubtitles.org',
		'plugin'   : 'service.subtitles.opensubtitles',
		'saved'    : 'login-opensubtitles',
		'path'     : os.path.join(ADDONS, 'service.subtitles.opensubtitles'),
		'icon'     : os.path.join(ADDONS, 'service.subtitles.opensubtitles', 'resources/media/os_logo_512x512.png'),
		'fanart'   : os.path.join(ADDONS, 'service.subtitles.opensubtitles', 'resources/media/os_fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'opensub_login'),
		'settings' : os.path.join(ADDOND, 'service.subtitles.opensubtitles', 'settings.xml'),
		'default'  : 'OSuser',
		'data'     : ['OSuser', 'OSpass'],
		'activate' : ''},
	'login-opensubsbyopensubs': {
		'name'     : 'OpenSubtitles.org by OpenSubtitles',
		'plugin'   : 'service.subtitles.opensubtitles_by_opensubtitles',
		'saved'    : 'login-opensubtitles',
		'path'     : os.path.join(ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles'),
		'icon'     : os.path.join(ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles', 'resources/media/os_logo_512x512.png'),
		'fanart'   : os.path.join(ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles', 'resources/media/os_fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'opensubsbyopensubs_login'),
		'settings' : os.path.join(ADDOND, 'service.subtitles.opensubtitles_by_opensubtitles', 'settings.xml'),
		'default'  : 'OSuser',
		'data'     : ['OSuser', 'OSpass'],
		'activate' : ''},
	'login-orion': {
		'name'     : 'Orion',
		'plugin'   : 'script.module.orion',
		'saved'    : 'login-orion',
		'path'     : os.path.join(ADDONS, 'script.module.orion'),
		'icon'     : os.path.join(ADDONS, 'script.module.orion', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.module.orion', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'orion_login'),
		'settings' : os.path.join(ADDOND, 'script.module.orion', 'settings.xml'),
		'default'  : 'account.key',
		'data'     : ['account.key', 'account.valid'],
		'activate' : 'RunPlugin(plugin://script.module.orion/?action=settingsAccountLogin)'},
	'tmdb-seren': {
		'name'     : 'TMDb - Seren',
		'plugin'   : 'plugin.video.seren',
		'saved'    : 'tmdb-seren',
		'path'     : os.path.join(ADDONS, 'plugin.video.seren'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.seren', 'temp-icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
		'file'     : os.path.join(LOGINFOLD, 'seren_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.seren', 'settings.xml'),
		'default'  : 'tmdb.apikey',
		'data'     : ['tmdb.apikey'],
		'activate' : ''},
	'trakt-seren': {
		'name'     : 'Trakt - Seren',
		'plugin'   : 'plugin.video.seren',
		'saved'    : 'trakt-seren',
		'path'     : os.path.join(ADDONS, 'plugin.video.seren'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.seren', 'temp-icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
		'file'     : os.path.join(LOGINFOLD, 'seren_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.seren', 'settings.xml'),
		'default'  : 'trakt.clientid',
		'data'     : ['trakt.clientid', 'trakt.secret'],
		'activate' : ''},
	'tvdb-seren': {
		'name'     : 'TVDB - Seren',
		'plugin'   : 'plugin.video.seren',
		'saved'    : 'tvdb-seren',
		'path'     : os.path.join(ADDONS, 'plugin.video.seren'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.seren', 'temp-icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
		'file'     : os.path.join(LOGINFOLD, 'seren_tvdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.seren', 'settings.xml'),
		'default'  : 'tvdb.apikey',
		'data'     : ['tvdb.apikey', 'tvdb.jw', 'tvdb.expiry'],
		'activate' : ''},
	'fanart-placenta': {
		'name'     : 'Fanart.tv - Placenta',
		'plugin'   : 'plugin.video.placenta',
		'saved'    : 'fanart-placenta',
		'path'     : os.path.join(ADDONS, 'plugin.video.placenta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.placenta', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.placenta', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'placenta_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.placenta', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-placenta': {
		'name'     : 'TMDb - Placenta',
		'plugin'   : 'plugin.video.placenta',
		'saved'    : 'tmdb-placenta',
		'path'     : os.path.join(ADDONS, 'plugin.video.placenta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.placenta', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.placenta', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'placenta_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.placenta', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-placenta': {
		'name'     : 'IMDb - Placenta',
		'plugin'   : 'plugin.video.placenta',
		'saved'    : 'imdb-placenta',
		'path'     : os.path.join(ADDONS, 'plugin.video.placenta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.placenta', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.placenta', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'placenta_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.placenta', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'fanart-thecrew': {
		'name'     : 'Fanart.tv - THE CREW',
		'plugin'   : 'plugin.video.thecrew',
		'saved'    : 'fanart-thecrew',
		'path'     : os.path.join(ADDONS, 'plugin.video.thecrew'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.thecrew', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'thecrew_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.thecrew', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-thecrew': {
		'name'     : 'TMDb - THE CREW',
		'plugin'   : 'plugin.video.thecrew',
		'saved'    : 'tmdb-thecrew',
		'path'     : os.path.join(ADDONS, 'plugin.video.thecrew'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.thecrew', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'thecrew_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.thecrew', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-thecrew': {
		'name'     : 'IMDb - THE CREW',
		'plugin'   : 'plugin.video.thecrew',
		'saved'    : 'imdb-thecrew',
		'path'     : os.path.join(ADDONS, 'plugin.video.thecrew'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.thecrew', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'thecrew_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.thecrew', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'fanart-gaia': {
		'name'     : 'Fanart.tv - Gaia',
		'plugin'   : 'plugin.video.gaia',
		'saved'    : 'fanart-gaia',
		'path'     : os.path.join(ADDONS, 'plugin.video.gaia'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.gaia', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'gaia_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.gaia', 'settings.xml'),
		'default'  : 'accounts.artwork.fanart.api',
		'data'     : ['accounts.artwork.fanart.enabled', 'accounts.artwork.fanart.api'],
		'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=accountSettings)'},
	'imdb-gaia': {
		'name'     : 'IMDb - Gaia',
		'plugin'   : 'plugin.video.gaia',
		'saved'    : 'imdb-gaia',
		'path'     : os.path.join(ADDONS, 'plugin.video.gaia'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.gaia', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'gaia_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.gaia', 'settings.xml'),
		'default'  : 'accounts.informants.imdb.user',
		'data'     : ['accounts.informants.imdb.enabled', 'accounts.informants.imdb.user'],
		'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=accountSettings)'},
	'tmdb-gaia': {
		'name'     : 'TMDb - Gaia',
		'plugin'   : 'plugin.video.gaia',
		'saved'    : 'tmdb-gaia',
		'path'     : os.path.join(ADDONS, 'plugin.video.gaia'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.gaia', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'gaia_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.gaia', 'settings.xml'),
		'default'  : 'accounts.informants.tmdb.api',
		'data'     : ['accounts.informants.tmdb.enabled', 'accounts.informants.tmdb.api'],
		'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=accountSettings)'},
	'login-eis': {
		'name'     : 'TMDb Login - ExtendedInfo Script',
		'plugin'   : 'script.extendedinfo',
		'saved'    : 'login-eis',
		'path'     : os.path.join(ADDONS, 'script.extendedinfo'),
		'icon'     : os.path.join(ADDONS, 'script.extendedinfo', 'resources/icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.extendedinfo', 'resources/fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'eis_login'),
		'settings' : os.path.join(ADDOND, 'script.extendedinfo', 'settings.xml'),
		'default'  : 'tmdb_username',
		'data'     : ['tmdb_username', 'tmdb_password'],
		'activate' : ''},
	'tmdb-eis': {
		'name'     : 'TMDb - OpenInfo',
		'plugin'   : 'script.extendedinfo',
		'saved'    : 'tmdb-eis',
		'path'     : os.path.join(ADDONS, 'script.extendedinfo'),
		'icon'     : os.path.join(ADDONS, 'script.extendedinfo', 'resources/icon.png'),
		'fanart'   : os.path.join(ADDONS, 'script.extendedinfo', 'resources/fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'eis_tmdb'),
		'settings' : os.path.join(ADDOND, 'script.extendedinfo', 'settings.xml'),
		'default'  : 'tmdb_api',
		'data'     : ['tmdb_api'],
		'activate' : ''},
	'tmdb-metahandler': {
		'name'     : 'TMDb - metahandler',
		'plugin'   : 'script.module.metahandler',
		'saved'    : 'tmdb-metahandler',
		'path'     : os.path.join(ADDONS, 'script.module.metahandler'),
		'icon'     : os.path.join(ADDONS, 'script.module.metahandler', 'icon.png'),
		'fanart'   : '',
		'file'     : os.path.join(LOGINFOLD, 'metahandler_tmdb'),
		'settings' : os.path.join(ADDOND, 'script.module.metahandler', 'settings.xml'),
		'default'  : 'tmdb_api_key',
		'data'     : ['tmdb_api_key', 'omdb_api_key', 'tvdb_api_key'],
		'activate' : ''},
	'omdb-metahandler': {
		'name'     : 'OMDb - metahandler',
		'plugin'   : 'script.module.metahandler',
		'saved'    : 'omdb-metahandler',
		'path'     : os.path.join(ADDONS, 'script.module.metahandler'),
		'icon'     : os.path.join(ADDONS, 'script.module.metahandler', 'icon.png'),
		'fanart'   : '',
		'file'     : os.path.join(LOGINFOLD, 'metahandler_omdb'),
		'settings' : os.path.join(ADDOND, 'script.module.metahandler', 'settings.xml'),
		'default'  : 'omdb_api_key',
		'data'     : ['omdb_api_key'],
		'activate' : ''},
	'tvdb-metahandler': {
		'name'     : 'TVDB - metahandler',
		'plugin'   : 'script.module.metahandler',
		'saved'    : 'tvdb-metahandler',
		'path'     : os.path.join(ADDONS, 'script.module.metahandler'),
		'icon'     : os.path.join(ADDONS, 'script.module.metahandler', 'icon.png'),
		'fanart'   : '',
		'file'     : os.path.join(LOGINFOLD, 'metahandler_tvdb'),
		'settings' : os.path.join(ADDOND, 'script.module.metahandler', 'settings.xml'),
		'default'  : 'tvdb_api_key',
		'data'     : ['tvdb_api_key'],
		'activate' : ''},
	'fanart-metadatautils': {
		'name'     : 'Fanart.tv - script.module.metadatautils',
		'plugin'   : 'script.module.metadatautils',
		'saved'    : 'fanart-metadatautils',
		'path'     : os.path.join(ADDONS, 'script.module.metadatautils'),
		'icon'     : os.path.join(ADDONS, 'script.module.metadatautils', 'icon.png'),
		'fanart'   : '',
		'file'     : os.path.join(LOGINFOLD, 'metadatautils_fanart'),
		'settings' : os.path.join(ADDOND, 'script.module.metadatautils', 'settings.xml'),
		'default'  : 'fanarttv_apikey',
		'data'     : ['fanarttv_apikey', 'omdbapi_apikey', 'tmdb_apikey'],
		'activate' : ''},
	'omdb-metadatautils': {
		'name'     : 'OMDb - script.module.metadatautils',
		'plugin'   : 'script.module.metadatautils',
		'saved'    : 'omdb-metadatautils',
		'path'     : os.path.join(ADDONS, 'script.module.metadatautils'),
		'icon'     : os.path.join(ADDONS, 'script.module.metadatautils', 'icon.png'),
		'fanart'   : '',
		'file'     : os.path.join(LOGINFOLD, 'metadatautils_omdb'),
		'settings' : os.path.join(ADDOND, 'script.module.metadatautils', 'settings.xml'),
		'default'  : 'omdbapi_apikey',
		'data'     : ['omdbapi_apikey'],
		'activate' : ''},
	'tmdb-metadatautils': {
		'name'     : 'TMDb - script.module.metadatautils',
		'plugin'   : 'script.module.metadatautils',
		'saved'    : 'tmdb-metadatautils',
		'path'     : os.path.join(ADDONS, 'script.module.metadatautils'),
		'icon'     : os.path.join(ADDONS, 'script.module.metadatautils', 'icon.png'),
		'fanart'   : '',
		'file'     : os.path.join(LOGINFOLD, 'metadatautils_tmdb'),
		'settings' : os.path.join(ADDOND, 'script.module.metadatautils', 'settings.xml'),
		'default'  : 'tmdb_apikey',
		'data'     : ['tmdb_apikey'],
		'activate' : ''},
	'fanart-exodusredux': {
		'name'     : 'Fanart.tv - Exodus Redux',
		'plugin'   : 'plugin.video.exodusredux',
		'saved'    : 'fanart-exodusredux',
		'path'     : os.path.join(ADDONS, 'plugin.video.exodusredux'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.exodusredux', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'exodusredux_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodusredux', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-exodusredux': {
		'name'     : 'TMDb - Exodus Redux',
		'plugin'   : 'plugin.video.exodusredux',
		'saved'    : 'tmdb-exodusredux',
		'path'     : os.path.join(ADDONS, 'plugin.video.exodusredux'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.exodusredux', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'exodusredux_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodusredux', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-exodusredux': {
		'name'     : 'IMDb - Exodus Redux',
		'plugin'   : 'plugin.video.exodusredux',
		'saved'    : 'imdb-exodusredux',
		'path'     : os.path.join(ADDONS, 'plugin.video.exodusredux'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.exodusredux', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'exodusredux_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.exodusredux', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'fanart-venom': {
		'name'     : 'Fanart.tv - Venom',
		'plugin'   : 'plugin.video.venom',
		'saved'    : 'fanart-venom',
		'path'     : os.path.join(ADDONS, 'plugin.video.venom'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.venom', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.venom', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'venom_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.venom', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-venom': {
		'name'     : 'TMDb - Venom',
		'plugin'   : 'plugin.video.venom',
		'saved'    : 'tmdb-venom',
		'path'     : os.path.join(ADDONS, 'plugin.video.venom'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.venom', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.venom', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'venom_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.venom', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-venom': {
		'name'     : 'IMDb - Venom',
		'plugin'   : 'plugin.video.venom',
		'saved'    : 'imdb-venom',
		'path'     : os.path.join(ADDONS, 'plugin.video.venom'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.venom', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.venom', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'venom_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.venom', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'fanart-numbers': {
		'name'     : 'Fanart.tv - NuMb3r5',
		'plugin'   : 'plugin.video.numbersbynumbers',
		'saved'    : 'fanart-numbers',
		'path'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'numbers_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.numbersbynumbers', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-numbers': {
		'name'     : 'TMDb - NuMb3r5',
		'plugin'   : 'plugin.video.numbersbynumbers',
		'saved'    : 'tmdb-numbers',
		'path'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'numbers_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.numbersbynumbers', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-numbers': {
		'name'     : 'IMDb - NuMb3r5',
		'plugin'   : 'plugin.video.numbersbynumbers',
		'saved'    : 'imdb-numbers',
		'path'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'numbers_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.numbersbynumbers', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'trakt-openmeta': {
		'name'     : 'Trakt - OpenMeta',
		'plugin'   : 'plugin.video.openmeta',
		'saved'    : 'trakt-openmeta',
		'path'     : os.path.join(ADDONS, 'plugin.video.openmeta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'openmeta_trakt'),
		'settings' : os.path.join(ADDOND, 'plugin.video.openmeta', 'settings.xml'),
		'default'  : 'trakt_api_client_id',
		'data'     : ['trakt_api_client_id', 'trakt_api_client_secret'],
		'activate' : ''},
	'tmdb-openmeta': {
		'name'     : 'TMDb - OpenMeta',
		'plugin'   : 'plugin.video.openmeta',
		'saved'    : 'tmdb-openmeta',
		'path'     : os.path.join(ADDONS, 'plugin.video.openmeta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'openmeta_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.openmeta', 'settings.xml'),
		'default'  : 'tmdb_api',
		'data'     : ['tmdb_api'],
		'activate' : ''},
	'tvdb-openmeta': {
		'name'     : 'TVDB - OpenMeta',
		'plugin'   : 'plugin.video.openmeta',
		'saved'    : 'tvdb-openmeta',
		'path'     : os.path.join(ADDONS, 'plugin.video.openmeta'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'openmeta_tvdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.openmeta', 'settings.xml'),
		'default'  : 'tvdb_api',
		'data'     : ['tvdb_api'],
		'activate' : ''},
	'login-netflix': {
		'name'     : 'Netflix',
		'plugin'   : 'plugin.video.netflix',
		'saved'    : 'login-netflix',
		'path'     : os.path.join(ADDONS, 'plugin.video.netflix'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.netflix', 'resources/icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.netflix', 'resources/fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'netflix_login'),
		'settings' : os.path.join(ADDOND, 'plugin.video.netflix', 'settings.xml'),
		'default'  : 'email',
		'data'     : ['email', 'password'],
		'activate' : ''},
	'location-yahoo': {
		'name'     : 'Yahoo! Weather',
		'plugin'   : 'weather.yahoo',
		'saved'    : 'location-yahoo',
		'path'     : os.path.join(ADDONS, 'weather.yahoo'),
		'icon'     : os.path.join(ADDONS, 'weather.yahoo', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'weather.yahoo', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'yahoo_location'),
		'settings' : os.path.join(ADDOND, 'weather.yahoo', 'settings.xml'),
		'default'  : 'Location1',
		'data'     : ['Location1', 'Location1id', 'Location2', 'Location2id', 'Location3', 'Location3id', 'Location4', 'Location4id', 'Location5', 'Location5id'],
		'activate' : ''},
	'login-iagl': {
		'name'     : 'Internet Archive - IAGL',
		'plugin'   : 'plugin.program.iagl',
		'saved'    : 'login-iagl',
		'path'     : os.path.join(ADDONS, 'plugin.program.iagl'),
		'icon'     : os.path.join(ADDONS, 'plugin.program.iagl', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.program.iagl', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'iagl_login'),
		'settings' : os.path.join(ADDOND, 'plugin.program.iagl', 'settings.xml'),
		'default'  : 'iagl_setting_ia_username',
		'data'     : ['iagl_setting_ia_username', 'iagl_setting_ia_password', 'iagl_setting_enable_login'],
		'activate' : ''},
	'kitsu-wonderfulsubs': {
		'name'     : 'Kitsu - WonderfulSubs',
		'plugin'   : 'plugin.video.wonderfulsubs',
		'saved'    : 'kitsu-wonderfulsubs',
		'path'     : os.path.join(ADDONS, 'plugin.video.wonderfulsubs'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.wonderfulsubs', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.wonderfulsubs', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'wonderfulsubs-kitsu'),
		'settings' : os.path.join(ADDOND, 'plugin.video.wonderfulsubs', 'settings.xml'),
		'default'  : 'kitsu.name',
		'data'     : ['kitsu.name', 'kitsu.password'],
		'activate' : 'RunPlugin(plugin://plugin.video.wonderfulsubs/watchlist_login/kitsu)'},
	'mal-wonderfulsubs': {
		'name'     : 'MyAnimeList - WonderfulSubs',
		'plugin'   : 'plugin.video.wonderfulsubs',
		'saved'    : 'mal-wonderfulsubs',
		'path'     : os.path.join(ADDONS, 'plugin.video.wonderfulsubs'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.wonderfulsubs', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.wonderfulsubs', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'wonderfulsubs-mal'),
		'settings' : os.path.join(ADDOND, 'plugin.video.wonderfulsubs', 'settings.xml'),
		'default'  : 'mal.name',
		'data'     : ['mal.name', 'mal.password'],
		'activate' : 'RunPlugin(plugin://plugin.video.wonderfulsubs/watchlist_login/mal)'},
	'ws-wonderfulsubs': {
		'name'     : 'WonderfulSubs - WonderfulSubs',
		'plugin'   : 'plugin.video.wonderfulsubs',
		'saved'    : 'ws-wonderfulsubs',
		'path'     : os.path.join(ADDONS, 'plugin.video.wonderfulsubs'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.wonderfulsubs', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.wonderfulsubs', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'wonderfulsubs-ws'),
		'settings' : os.path.join(ADDOND, 'plugin.video.wonderfulsubs', 'settings.xml'),
		'default'  : 'wonderfulsubs.name',
		'data'     : ['wonderfulsubs.name', 'wonderfulsubs.password'],
		'activate' : ''},
	'fanart-yoda': {
		'name'     : 'Fanart.tv - Yoda',
		'plugin'   : 'plugin.video.yoda',
		'saved'    : 'fanart-yoda',
		'path'     : os.path.join(ADDONS, 'plugin.video.yoda'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.yoda', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.yoda', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'yoda_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.yoda', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-yoda': {
		'name'     : 'TMDb - Yoda',
		'plugin'   : 'plugin.video.yoda',
		'saved'    : 'tmdb-yoda',
		'path'     : os.path.join(ADDONS, 'plugin.video.yoda'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.yoda', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.yoda', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'yoda_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.yoda', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-yoda': {
		'name'     : 'IMDb - Yoda',
		'plugin'   : 'plugin.video.yoda',
		'saved'    : 'imdb-yoda',
		'path'     : os.path.join(ADDONS, 'plugin.video.yoda'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.yoda', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.yoda', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'yoda_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.yoda', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'fanart-overeasy': {
		'name'     : 'Fanart.tv - Overeasy',
		'plugin'   : 'plugin.video.overeasy',
		'saved'    : 'fanart-overeasy',
		'path'     : os.path.join(ADDONS, 'plugin.video.overeasy'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.overeasy', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.overeasy', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'overeasy_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.overeasy', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-overeasy': {
		'name'     : 'TMDb - Overeasy',
		'plugin'   : 'plugin.video.overeasy',
		'saved'    : 'tmdb-overeasy',
		'path'     : os.path.join(ADDONS, 'plugin.video.overeasy'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.overeasy', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.overeasy', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'overeasy_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.overeasy', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-overeasy': {
		'name'     : 'IMDb - Overeasy',
		'plugin'   : 'plugin.video.overeasy',
		'saved'    : 'imdb-overeasy',
		'path'     : os.path.join(ADDONS, 'plugin.video.overeasy'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.overeasy', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.overeasy', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'overeasy_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.overeasy', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'fanart-scrubs': {
		'name'     : 'Fanart.tv - Scrubs v2',
		'plugin'   : 'plugin.video.scrubsv2',
		'saved'    : 'fanart-scrubs',
		'path'     : os.path.join(ADDONS, 'plugin.video.scrubsv2'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'fanart.png'),
		'file'     : os.path.join(LOGINFOLD, 'scrubs_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.scrubsv2', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user'],
		'activate' : ''},
	'tmdb-scrubs': {
		'name'     : 'TMDb - Scrubs v2',
		'plugin'   : 'plugin.video.scrubsv2',
		'saved'    : 'tmdb-scrubs',
		'path'     : os.path.join(ADDONS, 'plugin.video.scrubsv2'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'fanart.png'),
		'file'     : os.path.join(LOGINFOLD, 'scrubs_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.scrubsv2', 'settings.xml'),
		'default'  : 'tm.user',
		'data'     : ['tm.user'],
		'activate' : ''},
	'imdb-scrubs': {
		'name'     : 'IMDb - Scrubs v2',
		'plugin'   : 'plugin.video.scrubsv2',
		'saved'    : 'imdb-scrubs',
		'path'     : os.path.join(ADDONS, 'plugin.video.scrubsv2'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'icon.jpg'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'fanart.png'),
		'file'     : os.path.join(LOGINFOLD, 'scrubs_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.scrubsv2', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'fanart-premiumizer': {
		'name'     : 'Fanart.tv - Premiumizer',
		'plugin'   : 'plugin.video.premiumizer',
		'saved'    : 'fanart-premiumizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.premiumizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.premiumizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'premiumizer_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.premiumizer', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user', 'fanart.tv.project'],
		'activate' : ''},
	'tmdb-premiumizer': {
		'name'     : 'TMDb - Premiumizer',
		'plugin'   : 'plugin.video.premiumizer',
		'saved'    : 'tmdb-premiumizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.premiumizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.premiumizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'premiumizer_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.premiumizer', 'settings.xml'),
		'default'  : 'tmdb.api',
		'data'     : ['tmdb.api'],
		'activate' : ''},
	'imdb-premiumizer': {
		'name'     : 'IMDb - Premiumizer',
		'plugin'   : 'plugin.video.premiumizer',
		'saved'    : 'imdb-premiumizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.premiumizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.premiumizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'premiumizer_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.premiumizer', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'tvdb-premiumizer': {
		'name'     : 'TVDB - Premiumizer',
		'plugin'   : 'plugin.video.premiumizer',
		'saved'    : 'tvdb-premiumizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.premiumizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.premiumizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'premiumizer_tvdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.premiumizer', 'settings.xml'),
		'default'  : 'tvdb.api',
		'data'     : ['tvdb.api', 'tvdb.token', 'tvdb.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.premiumizer/?action=AuthorizeTvdb)'},
	'fanart-realizer': {
		'name'     : 'Fanart.tv - Realizer',
		'plugin'   : 'plugin.video.realizer',
		'saved'    : 'fanart-realizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.realizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.realizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'realizer_fanart'),
		'settings' : os.path.join(ADDOND, 'plugin.video.realizer', 'settings.xml'),
		'default'  : 'fanart.tv.user',
		'data'     : ['fanart.tv.user', 'fanart.tv.project'],
		'activate' : ''},
	'tmdb-realizer': {
		'name'     : 'TMDb - Realizer',
		'plugin'   : 'plugin.video.realizer',
		'saved'    : 'tmdb-realizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.realizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.realizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'realizer_tmdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.realizer', 'settings.xml'),
		'default'  : 'tmdb.api',
		'data'     : ['tmdb.api'],
		'activate' : ''},
	'imdb-realizer': {
		'name'     : 'IMDb - Realizer',
		'plugin'   : 'plugin.video.realizer',
		'saved'    : 'imdb-realizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.realizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.realizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'realizer_imdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.realizer', 'settings.xml'),
		'default'  : 'imdb.user',
		'data'     : ['imdb.user'],
		'activate' : ''},
	'tvdb-realizer': {
		'name'     : 'TVDB - Realizer',
		'plugin'   : 'plugin.video.realizer',
		'saved'    : 'tvdb-realizer',
		'path'     : os.path.join(ADDONS, 'plugin.video.realizer'),
		'icon'     : os.path.join(ADDONS, 'plugin.video.realizer', 'icon.png'),
		'fanart'   : os.path.join(ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
		'file'     : os.path.join(LOGINFOLD, 'realizer_tvdb'),
		'settings' : os.path.join(ADDOND, 'plugin.video.realizer', 'settings.xml'),
		'default'  : 'tvdb.api',
		'data'     : ['tvdb.api', 'tvdb.token', 'tvdb.refresh'],
		'activate' : 'RunPlugin(plugin://plugin.video.realizer/?action=AuthorizeTvdb)'}
}

def loginUser(who):
	user=None
	if LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			try:
				add = wiz.addonId(LOGINID[who]['plugin'])
				user = add.getSetting(LOGINID[who]['default'])
			except:
				pass
	return user

def loginIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(LOGINFOLD):  os.makedirs(LOGINFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(LOGINID[log]['path']):
				try:
					addonid   = wiz.addonId(LOGINID[log]['plugin'])
					default   = LOGINID[log]['default']
					user      = addonid.getSetting(default)
					if user == '' and do == 'update': continue
					updateLogin(do, log)
				except: pass
			else: wiz.log('[Login Info] %s(%s) is not installed' % (LOGINID[log]['name'],LOGINID[log]['plugin']), xbmc.LOGERROR)
		wiz.setS('loginlastsave', str(THREEDAYS))
	else:
		if LOGINID[who]:
			if os.path.exists(LOGINID[who]['path']):
				updateLogin(do, who)
		else: wiz.log('[Login Info] Invalid Entry: %s' % who, xbmc.LOGERROR)

def clearSaved(who, over=False):
	if who == 'all':
		for login in LOGINID:
			clearSaved(login,  True)
	elif LOGINID[who]:
		file = LOGINID[who]['file']
		if os.path.exists(file):
			os.remove(file)
			wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, LOGINID[who]['name']), '[COLOR %s]Login Info: Removed![/COLOR]' % COLOR2, 2000, LOGINID[who]['icon'])
		wiz.setS(LOGINID[who]['saved'], '')
	if over == False: wiz.refresh()

def updateLogin(do, who):
	file      = LOGINID[who]['file']
	settings  = LOGINID[who]['settings']
	data      = LOGINID[who]['data']
	addonid   = wiz.addonId(LOGINID[who]['plugin'])
	saved     = LOGINID[who]['saved']
	default   = LOGINID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = LOGINID[who]['name']
	icon      = LOGINID[who]['icon']

	if do == 'update':
		if not user == '':
			try:
				with open(file, 'w') as f:
					for login in data:
						f.write('<login>\n\t<id>%s</id>\n\t<value>%s</value>\n</login>\n' % (login, addonid.getSetting(login)))
					f.close()
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Login Data: Saved![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Login Data] Unable to Update %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Login Data: Not Registered![/COLOR]' % COLOR2, 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<login><id>(.+?)</id><value>(.+?)</value></login>').findall(g)
			try:
				if len(match) > 0:
					for login, value in match:
						addonid.setSetting(login, value)
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Login: Restored![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Login Info] Unable to Restore %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		#else: wiz.LogNotify(name,'login Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
	elif do == 'clearaddon':
		wiz.log('%s SETTINGS: %s' % (name, settings), xbmc.LOGDEBUG)
		if os.path.exists(settings):
			try:
				f = open(settings, "r"); lines = f.readlines(); f.close()
				f = open(settings, "w")
				for line in lines:
					match = wiz.parseDOM(line, 'setting', ret='id')
					if len(match) == 0: f.write(line)
					else:
						if match[0] not in data: f.write(line)
						else: wiz.log('Removing Line: %s' % line, xbmc.LOGNOTICE)
				f.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name),'[COLOR %s]Addon Data: Cleared![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Data] Unable to Clear Addon %s (%s)" % (who, str(e)), xbmc.LOGERROR)
	wiz.refresh()

def autoUpdate(who):
	if who == 'all':
		for log in LOGINID:
			if os.path.exists(LOGINID[log]['path']):
				autoUpdate(log)
	elif LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			u  = loginUser(who)
			su = wiz.getS(LOGINID[who]['saved'])
			n = LOGINID[who]['name']
			if u == None or u == '': return
			elif su == '': loginIt('update', who)
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to save the [COLOR %s]Login Info[/COLOR] for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "Addon: [COLOR springgreen][B]%s[/B][/COLOR]" % u, "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
					loginIt('update', who)
			else: loginIt('update', who)

def importlist(who):
	if who == 'all':
		for log in LOGINID:
			if os.path.exists(LOGINID[log]['file']):
				importlist(log)
	elif LOGINID[who]:
		if os.path.exists(LOGINID[who]['file']):
			d  = LOGINID[who]['default']
			sa = LOGINID[who]['saved']
			su = wiz.getS(sa)
			n  = LOGINID[who]['name']
			f  = open(LOGINID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<login><id>%s</id><value>(.+?)</value></login>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to import the [COLOR %s]Login Info[/COLOR] for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "File: [COLOR springgreen][B]%s[/B][/COLOR]" % m[0], "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)), xbmc.LOGNOTICE)
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)

def activateLogin(who):
	if LOGINID[who]:
		if os.path.exists(LOGINID[who]['path']):
			act     = LOGINID[who]['activate']
			addonid = wiz.addonId(LOGINID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(LOGINID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % LOGINID[who]['name'])
	else:
		wiz.refresh()
		return
	check = 0
	while loginUser(who) == None or loginUser(who) == "":
		if check == 30: break
		check += 1
		time.sleep(10)
	wiz.refresh()
