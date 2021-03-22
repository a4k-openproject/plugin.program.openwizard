################################################################################
#      Copyright (C) 2019 drinfernoo                                           #
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

import xbmc
import xbmcgui

import os
import time

from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['easynews-fen',
         'fanart-exodusredux', 'fanart-gaia', 'fanart-numbers',
         'fanart-metadatautils', 'fanart-premiumizer', 'fanart-realizer',
         'fanart-scrubs', 'fanart-seren', 'fanart-thecrew', 'fanart-tmdbhelper',
         'fanart-venom',
         'furk-fen',
         'imdb-exodusredux', 'imdb-gaia', 'imdb-numbers', 'imdb-premiumizer',
         'imdb-realizer', 'imdb-scrubs', 'imdb-thecrew', 'imdb-venom',
         'kitsu-wonderfulsubs',
         'login-iagl', 'login-netflix',
         'mal-wonderfulsubs',
         'omdb-metadatautils', 'omdb-metahandler', 'omdb-tmdbhelper',
         'login-opensubtitles', 'login-opensubsbyopensubs', 'login-orion',
         'login-eis', 'tmdb-gaia',
         'tmdb-exodusredux', 'tmdb-fen', 'tmdb-metadatautils', 'tmdb-numbers',
         'tmdb-openinfo', 'tmdb-openmeta', 'tmdb-premiumizer', 'tmdb-realizer',
         'tmdb-scrubs', 'tmdb-seren', 'tmdb-thecrew', 'tmdb-tmdbhelper',
         'tmdb-venom',
         'trakt-openmeta', 'trakt-seren',
         'tvdb-metahandler', 'tvdb-openmeta', 'tvdb-premiumizer',
         'tvdb-realizer', 'tvdb-seren',
         'location-yahoo', 'login-youtube',
         'ws-wonderfulsubs']

LOGINID = {
    'login-opensubtitles': {
        'name'     : 'OpenSubtitles.org',
        'plugin'   : 'service.subtitles.opensubtitles',
        'saved'    : 'login-opensubtitles',
        'path'     : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles', 'resources/media/os_logo_512x512.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles', 'resources/media/os_fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'opensub_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'service.subtitles.opensubtitles', 'settings.xml'),
        'default'  : 'OSuser',
        'data'     : ['OSuser', 'OSpass'],
        'activate' : ''},
    'login-opensubsbyopensubs': {
        'name'     : 'OpenSubtitles.org by OpenSubtitles',
        'plugin'   : 'service.subtitles.opensubtitles_by_opensubtitles',
        'saved'    : 'login-opensubtitles',
        'path'     : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles', 'resources/media/os_logo_512x512.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'service.subtitles.opensubtitles_by_opensubtitles', 'resources/media/os_fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'opensubsbyopensubs_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'service.subtitles.opensubtitles_by_opensubtitles', 'settings.xml'),
        'default'  : 'OSuser',
        'data'     : ['OSuser', 'OSpass'],
        'activate' : ''},
    'login-orion': {
        'name'     : 'Orion',
        'plugin'   : 'script.module.orion',
        'saved'    : 'login-orion',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.orion'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.orion', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.orion', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'orion_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.orion', 'settings.xml'),
        'default'  : 'account.key',
        'data'     : ['account.key', 'account.valid'],
        'activate' : 'RunPlugin(plugin://script.module.orion/?action=settingsAccountLogin)'},
    'tmdb-seren': {
        'name'     : 'TMDb - Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'tmdb-seren',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'ico-fox-gold-final.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'fanart-fox-gold-final.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'seren_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'tmdb.apikey',
        'data'     : ['tmdb.apikey'],
        'activate' : ''},
    'trakt-seren': {
        'name'     : 'Trakt - Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'trakt-seren',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'ico-fox-gold-final.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'fanart-fox-gold-final.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'seren_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'trakt.clientid',
        'data'     : ['trakt.clientid', 'trakt.secret'],
        'activate' : ''},
    'tvdb-seren': {
        'name'     : 'TVDB - Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'tvdb-seren',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'ico-fox-gold-final.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'fanart-fox-gold-final.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'seren_tvdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'tvdb.apikey',
        'data'     : ['tvdb.apikey', 'tvdb.jw', 'tvdb.expiry'],
        'activate' : ''},
    'fanart-seren': {
        'name'     : 'Fanart.tv - Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'fanart-seren',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'ico-fox-gold-final.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'fanart-fox-gold-final.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'seren_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'fanart.apikey',
        'data'     : ['fanart.apikey'],
        'activate' : ''},
    'fanart-gaia': {
        'name'     : 'Fanart.tv - Gaia',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'fanart-gaia',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'gaia_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.artwork.fanart.api',
        'data'     : ['accounts.artwork.fanart.enabled', 'accounts.artwork.fanart.api'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=accountSettings)'},
    'imdb-gaia': {
        'name'     : 'IMDb - Gaia',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'imdb-gaia',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'gaia_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.informants.imdb.user',
        'data'     : ['accounts.informants.imdb.enabled', 'accounts.informants.imdb.user'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=accountSettings)'},
    'tmdb-gaia': {
        'name'     : 'TMDb - Gaia',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'tmdb-gaia',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'gaia_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.informants.tmdb.api',
        'data'     : ['accounts.informants.tmdb.enabled', 'accounts.informants.tmdb.api'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=accountSettings)'},
    'login-eis': {
        'name'     : 'TMDb Login - ExtendedInfo Script',
        'plugin'   : 'script.extendedinfo',
        'saved'    : 'login-eis',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.extendedinfo'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.extendedinfo', 'resources/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.extendedinfo', 'resources/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'eis_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'settings.xml'),
        'default'  : 'tmdb_username',
        'data'     : ['tmdb_username', 'tmdb_password'],
        'activate' : ''},
    'tmdb-openinfo': {
        'name'     : 'TMDb - OpenInfo',
        'plugin'   : 'script.extendedinfo',
        'saved'    : 'tmdb-openinfo',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.extendedinfo'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.extendedinfo', 'resources/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.extendedinfo', 'resources/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'openinfo_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'settings.xml'),
        'default'  : 'tmdb_api',
        'data'     : ['tmdb_api'],
        'activate' : ''},
    'tmdb-metahandler': {
        'name'     : 'TMDb - metahandler',
        'plugin'   : 'script.module.metahandler',
        'saved'    : 'tmdb-metahandler',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler', 'icon.png'),
        'fanart'   : '',
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'metahandler_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.metahandler', 'settings.xml'),
        'default'  : 'tmdb_api_key',
        'data'     : ['tmdb_api_key', 'omdb_api_key', 'tvdb_api_key'],
        'activate' : ''},
    'omdb-metahandler': {
        'name'     : 'OMDb - metahandler',
        'plugin'   : 'script.module.metahandler',
        'saved'    : 'omdb-metahandler',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler', 'icon.png'),
        'fanart'   : '',
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'metahandler_omdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.metahandler', 'settings.xml'),
        'default'  : 'omdb_api_key',
        'data'     : ['omdb_api_key'],
        'activate' : ''},
    'tvdb-metahandler': {
        'name'     : 'TVDB - metahandler',
        'plugin'   : 'script.module.metahandler',
        'saved'    : 'tvdb-metahandler',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler', 'icon.png'),
        'fanart'   : '',
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'metahandler_tvdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.metahandler', 'settings.xml'),
        'default'  : 'tvdb_api_key',
        'data'     : ['tvdb_api_key'],
        'activate' : ''},
    'fanart-metadatautils': {
        'name'     : 'Fanart.tv - script.module.metadatautils',
        'plugin'   : 'script.module.metadatautils',
        'saved'    : 'fanart-metadatautils',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.metadatautils'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.metadatautils', 'icon.png'),
        'fanart'   : '',
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'metadatautils_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.metadatautils', 'settings.xml'),
        'default'  : 'fanarttv_apikey',
        'data'     : ['fanarttv_apikey', 'omdbapi_apikey', 'tmdb_apikey'],
        'activate' : ''},
    'omdb-metadatautils': {
        'name'     : 'OMDb - script.module.metadatautils',
        'plugin'   : 'script.module.metadatautils',
        'saved'    : 'omdb-metadatautils',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.metadatautils'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.metadatautils', 'icon.png'),
        'fanart'   : '',
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'metadatautils_omdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.metadatautils', 'settings.xml'),
        'default'  : 'omdbapi_apikey',
        'data'     : ['omdbapi_apikey'],
        'activate' : ''},
    'tmdb-metadatautils': {
        'name'     : 'TMDb - script.module.metadatautils',
        'plugin'   : 'script.module.metadatautils',
        'saved'    : 'tmdb-metadatautils',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.metadatautils'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.metadatautils', 'icon.png'),
        'fanart'   : '',
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'metadatautils_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.metadatautils', 'settings.xml'),
        'default'  : 'tmdb_apikey',
        'data'     : ['tmdb_apikey'],
        'activate' : ''},
    'fanart-exodusredux': {
        'name'     : 'Fanart.tv - Exodus Redux',
        'plugin'   : 'plugin.video.exodusredux',
        'saved'    : 'fanart-exodusredux',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'exodusredux_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'settings.xml'),
        'default'  : 'fanart.tv.user',
        'data'     : ['fanart.tv.user'],
        'activate' : ''},
    'tmdb-exodusredux': {
        'name'     : 'TMDb - Exodus Redux',
        'plugin'   : 'plugin.video.exodusredux',
        'saved'    : 'tmdb-exodusredux',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'exodusredux_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'settings.xml'),
        'default'  : 'tm.user',
        'data'     : ['tm.user'],
        'activate' : ''},
    'imdb-exodusredux': {
        'name'     : 'IMDb - Exodus Redux',
        'plugin'   : 'plugin.video.exodusredux',
        'saved'    : 'imdb-exodusredux',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'exodusredux_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'settings.xml'),
        'default'  : 'imdb.user',
        'data'     : ['imdb.user'],
        'activate' : ''},
    'fanart-venom': {
        'name'     : 'Fanart.tv - Venom',
        'plugin'   : 'plugin.video.venom',
        'saved'    : 'fanart-venom',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.venom'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.venom', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.venom', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'venom_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'settings.xml'),
        'default'  : 'fanart.tv.user',
        'data'     : ['fanart.tv.user'],
        'activate' : ''},
    'tmdb-venom': {
        'name'     : 'TMDb - Venom',
        'plugin'   : 'plugin.video.venom',
        'saved'    : 'tmdb-venom',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.venom'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.venom', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.venom', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'venom_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'settings.xml'),
        'default'  : 'tm.user',
        'data'     : ['tm.user'],
        'activate' : ''},
    'imdb-venom': {
        'name'     : 'IMDb - Venom',
        'plugin'   : 'plugin.video.venom',
        'saved'    : 'imdb-venom',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.venom'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.venom', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.venom', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'venom_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'settings.xml'),
        'default'  : 'imdb.user',
        'data'     : ['imdb.user'],
        'activate' : ''},
    'fanart-thecrew': {
        'name'     : 'Fanart.tv - THE CREW',
        'plugin'   : 'plugin.video.thecrew',
        'saved'    : 'fanart-thecrew',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'thecrew_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'settings.xml'),
        'default'  : 'fanart.tv.user',
        'data'     : ['fanart.tv.user'],
        'activate' : ''},
    'tmdb-thecrew': {
        'name'     : 'TMDb - THE CREW',
        'plugin'   : 'plugin.video.thecrew',
        'saved'    : 'tmdb-thecrew',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'thecrew_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'settings.xml'),
        'default'  : 'tm.user',
        'data'     : ['tm.user'],
        'activate' : ''},
    'imdb-thecrew': {
        'name'     : 'IMDb - THE CREW',
        'plugin'   : 'plugin.video.thecrew',
        'saved'    : 'imdb-thecrew',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'thecrew_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'settings.xml'),
        'default'  : 'imdb.user',
        'data'     : ['imdb.user'],
        'activate' : ''},
    'trakt-openmeta': {
        'name'     : 'Trakt - OpenMeta',
        'plugin'   : 'plugin.video.openmeta',
        'saved'    : 'trakt-openmeta',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta', 'resources/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta', 'resources/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'openmeta_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.openmeta', 'settings.xml'),
        'default'  : 'trakt_api_client_id',
        'data'     : ['trakt_api_client_id', 'trakt_api_client_secret'],
        'activate' : ''},
    'tmdb-openmeta': {
        'name'     : 'TMDb - OpenMeta',
        'plugin'   : 'plugin.video.openmeta',
        'saved'    : 'tmdb-openmeta',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta', 'resources/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta', 'resources/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'openmeta_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.openmeta', 'settings.xml'),
        'default'  : 'tmdb_api',
        'data'     : ['tmdb_api'],
        'activate' : ''},
    'tvdb-openmeta': {
        'name'     : 'TVDB - OpenMeta',
        'plugin'   : 'plugin.video.openmeta',
        'saved'    : 'tvdb-openmeta',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta', 'resources/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.openmeta', 'resources/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'openmeta_tvdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.openmeta', 'settings.xml'),
        'default'  : 'tvdb_api',
        'data'     : ['tvdb_api'],
        'activate' : ''},
    'login-netflix': {
        'name'     : 'Netflix',
        'plugin'   : 'plugin.video.netflix',
        'saved'    : 'login-netflix',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.netflix'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.netflix', 'resources/icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.netflix', 'resources/fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'netflix_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.netflix', 'settings.xml'),
        'default'  : 'email',
        'data'     : ['email', 'password'],
        'activate' : ''},
    'location-yahoo': {
        'name'     : 'Yahoo! Weather',
        'plugin'   : 'weather.yahoo',
        'saved'    : 'location-yahoo',
        'path'     : os.path.join(CONFIG.ADDONS, 'weather.yahoo'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'weather.yahoo', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'weather.yahoo', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'yahoo_location'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'weather.yahoo', 'settings.xml'),
        'default'  : 'Location1',
        'data'     : ['Location1', 'Location1id', 'Location2', 'Location2id', 'Location3', 'Location3id', 'Location4', 'Location4id', 'Location5', 'Location5id'],
        'activate' : ''},
    'login-iagl': {
        'name'     : 'Internet Archive - IAGL',
        'plugin'   : 'plugin.program.iagl',
        'saved'    : 'login-iagl',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.program.iagl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.program.iagl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.program.iagl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'iagl_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.program.iagl', 'settings.xml'),
        'default'  : 'iagl_setting_ia_username',
        'data'     : ['iagl_setting_ia_username', 'iagl_setting_ia_password', 'iagl_setting_enable_login'],
        'activate' : ''},
    'kitsu-wonderfulsubs': {
        'name'     : 'Kitsu - WonderfulSubs',
        'plugin'   : 'plugin.video.wonderfulsubs',
        'saved'    : 'kitsu-wonderfulsubs',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'wonderfulsubs_kitsu'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.wonderfulsubs', 'settings.xml'),
        'default'  : 'kitsu.name',
        'data'     : ['kitsu.name', 'kitsu.password'],
        'activate' : 'RunPlugin(plugin://plugin.video.wonderfulsubs/watchlist_login/kitsu)'},
    'mal-wonderfulsubs': {
        'name'     : 'MyAnimeList - WonderfulSubs',
        'plugin'   : 'plugin.video.wonderfulsubs',
        'saved'    : 'mal-wonderfulsubs',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'wonderfulsubs_mal'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.wonderfulsubs', 'settings.xml'),
        'default'  : 'mal.name',
        'data'     : ['mal.name', 'mal.password'],
        'activate' : 'RunPlugin(plugin://plugin.video.wonderfulsubs/watchlist_login/mal)'},
    'ws-wonderfulsubs': {
        'name'     : 'WonderfulSubs - WonderfulSubs',
        'plugin'   : 'plugin.video.wonderfulsubs',
        'saved'    : 'ws-wonderfulsubs',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.wonderfulsubs', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'wonderfulsubs_ws'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.wonderfulsubs', 'settings.xml'),
        'default'  : 'wonderfulsubs.name',
        'data'     : ['wonderfulsubs.name', 'wonderfulsubs.password'],
        'activate' : ''},
    'fanart-scrubs': {
        'name'     : 'Fanart.tv - Scrubs v2',
        'plugin'   : 'plugin.video.scrubsv2',
        'saved'    : 'fanart-scrubs',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2', 'icon.jpg'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2', 'fanart.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'scrubs_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'settings.xml'),
        'default'  : 'fanart.tv.user',
        'data'     : ['fanart.tv.user'],
        'activate' : ''},
    'tmdb-scrubs': {
        'name'     : 'TMDb - Scrubs v2',
        'plugin'   : 'plugin.video.scrubsv2',
        'saved'    : 'tmdb-scrubs',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2', 'icon.jpg'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2', 'fanart.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'scrubs_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'settings.xml'),
        'default'  : 'tm.user',
        'data'     : ['tm.user'],
        'activate' : ''},
    'imdb-scrubs': {
        'name'     : 'IMDb - Scrubs v2',
        'plugin'   : 'plugin.video.scrubsv2',
        'saved'    : 'imdb-scrubs',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2', 'icon.jpg'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2', 'fanart.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'scrubs_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'settings.xml'),
        'default'  : 'imdb.user',
        'data'     : ['imdb.user'],
        'activate' : ''},
    'fanart-premiumizer': {
        'name'     : 'Fanart.tv - Premiumizer',
        'plugin'   : 'plugin.video.premiumizer',
        'saved'    : 'fanart-premiumizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'premiumizer_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizer', 'settings.xml'),
        'default'  : 'fanart.tv.user',
        'data'     : ['fanart.tv.user', 'fanart.tv.project'],
        'activate' : ''},
    'tmdb-premiumizer': {
        'name'     : 'TMDb - Premiumizer',
        'plugin'   : 'plugin.video.premiumizer',
        'saved'    : 'tmdb-premiumizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'premiumizer_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizer', 'settings.xml'),
        'default'  : 'tmdb.api',
        'data'     : ['tmdb.api'],
        'activate' : ''},
    'imdb-premiumizer': {
        'name'     : 'IMDb - Premiumizer',
        'plugin'   : 'plugin.video.premiumizer',
        'saved'    : 'imdb-premiumizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'premiumizer_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizer', 'settings.xml'),
        'default'  : 'imdb.user',
        'data'     : ['imdb.user'],
        'activate' : ''},
    'tvdb-premiumizer': {
        'name'     : 'TVDB - Premiumizer',
        'plugin'   : 'plugin.video.premiumizer',
        'saved'    : 'tvdb-premiumizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'premiumizer_tvdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizer', 'settings.xml'),
        'default'  : 'tvdb.api',
        'data'     : ['tvdb.api', 'tvdb.token', 'tvdb.refresh'],
        'activate' : 'RunPlugin(plugin://plugin.video.premiumizer/?action=AuthorizeTvdb)'},
    'fanart-realizer': {
        'name'     : 'Fanart.tv - Realizer',
        'plugin'   : 'plugin.video.realizer',
        'saved'    : 'fanart-realizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'realizer_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.realizer', 'settings.xml'),
        'default'  : 'fanart.tv.user',
        'data'     : ['fanart.tv.user', 'fanart.tv.project'],
        'activate' : ''},
    'tmdb-realizer': {
        'name'     : 'TMDb - Realizer',
        'plugin'   : 'plugin.video.realizer',
        'saved'    : 'tmdb-realizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'realizer_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.realizer', 'settings.xml'),
        'default'  : 'tmdb.api',
        'data'     : ['tmdb.api'],
        'activate' : ''},
    'imdb-realizer': {
        'name'     : 'IMDb - Realizer',
        'plugin'   : 'plugin.video.realizer',
        'saved'    : 'imdb-realizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'realizer_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.realizer', 'settings.xml'),
        'default'  : 'imdb.user',
        'data'     : ['imdb.user'],
        'activate' : ''},
    'tvdb-realizer': {
        'name'     : 'TVDB - Realizer',
        'plugin'   : 'plugin.video.realizer',
        'saved'    : 'tvdb-realizer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'realizer_tvdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.realizer', 'settings.xml'),
        'default'  : 'tvdb.api',
        'data'     : ['tvdb.api', 'tvdb.token', 'tvdb.refresh'],
        'activate' : 'RunPlugin(plugin://plugin.video.realizer/?action=AuthorizeTvdb)'},
    'fanart-numbers': {
        'name'     : 'Fanart.tv - NuMb3r5',
        'plugin'   : 'plugin.video.numbersbynumbers',
        'saved'    : 'fanart-numbers',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers', 'fanart.jpg'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'settings.xml'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'numbers_fanart'),
        'default'  : 'fanart.tv.user',
        'data'     : ['fanart.tv.user'],
        'activate' : ''},
    'tmdb-numbers': {
        'name'     : 'TMDb - NuMb3r5',
        'plugin'   : 'plugin.video.numbersbynumbers',
        'saved'    : 'tmdb-numbers',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'numbers_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'settings.xml'),
        'default'  : 'tm.user',
        'data'     : ['tm.user'],
        'activate' : ''},
    'imdb-numbers': {
        'name'     : 'IMDb - NuMb3r5',
        'saved'    : 'imdb-numbers',
        'plugin'   : 'plugin.video.numbersbynumbers',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.numbersbynumbers', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'numbers_imdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'settings.xml'),
        'default'  : 'imdb.user',
        'data'     : ['imdb.user'],
        'activate' : ''},
    'tmdb-tmdbhelper': {
        'name'     : 'TMDb - TheMovieDb Helper',
        'plugin'   : 'plugin.video.themoviedb.helper',
        'saved'    : 'tmdb-tmdbhelper',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'tmdbhelper_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.themoviedb.helper', 'settings.xml'),
        'default'  : 'tmdb_apikey',
        'data'     : ['tmdb_apikey'],
        'activate' : ''},
    'omdb-tmdbhelper': {
        'name'     : 'OMDb - TheMovieDb Helper',
        'saved'    : 'omdb-tmdbhelper',
        'plugin'   : 'plugin.video.themoviedb.helper',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'tmdbhelper_omdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.themoviedb.helper', 'settings.xml'),
        'default'  : 'omdb_apikey',
        'data'     : ['omdb_apikey'],
        'activate' : ''},
    'fanart-tmdbhelper': {
        'name'     : 'Fanart.tv - TheMovieDb Helper',
        'saved'    : 'fanart-tmdbhelper',
        'plugin'   : 'plugin.video.themoviedb.helper',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'tmdbhelper_fanart'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.themoviedb.helper', 'settings.xml'),
        'default'  : 'fanarttv_clientkey',
        'data'     : ['fanarttv_clientkey'],
        'activate' : ''},
    'login-youtube': {
        'name'     : 'Personal API - YouTube',
        'saved'    : 'login-youtube',
        'plugin'   : 'plugin.video.youtube',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.youtube'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.youtube', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.youtube', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'youtube_login'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.youtube', 'settings.xml'),
        'default'  : 'youtube.api.key',
        'data'     : ['youtube.api.enable', 'youtube.api.key', 'youtube.api.id', 'youtube.api.secret'],
        'activate' : ''},
    'tmdb-fen': {
        'name'     : 'TMDb - Fen',
        'saved'    : 'tmdb-fen',
        'plugin'   : 'plugin.video.fen',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'fen_tmdb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'tmdb_api',
        'data'     : ['tmdb_api'],
        'activate' : ''},
    'easynews-fen': {
        'name'     : 'EasyNews - Fen',
        'saved'    : 'easynews-fen',
        'plugin'   : 'plugin.video.fen',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'fen_easynews'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'easynews_user',
        'data'     : ['easynews_user', 'easynews_password'],
        'activate' : ''},
    'furk-fen': {
        'name'     : 'Furk - Fen',
        'saved'    : 'furk-fen',
        'plugin'   : 'plugin.video.fen',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen', 'fanart.png'),
        'file'     : os.path.join(CONFIG.LOGINFOLD, 'fen_furk'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'furk_login',
        'data'     : ['furk_login', 'furk_password', 'furk_api_key'],
        'activate' : ''}
}


def login_user(who):
    user = None
    if LOGINID[who]:
        if os.path.exists(LOGINID[who]['path']):
            try:
                add = tools.get_addon_by_id(LOGINID[who]['plugin'])
                user = add.getSetting(LOGINID[who]['default'])
            except:
                pass
    return user


def login_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.LOGINFOLD):
        os.makedirs(CONFIG.LOGINFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(LOGINID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(LOGINID[log]['plugin'])
                    default = LOGINID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_login(do, log)
                except:
                    pass
            else:
                logging.log('[Login Info] {0}({1}) is not installed'.format(LOGINID[log]['name'], LOGINID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('loginnextsave', tools.get_date(days=3, formatted=True))
    else:
        if LOGINID[who]:
            if os.path.exists(LOGINID[who]['path']):
                update_login(do, who)
        else:
            logging.log('[Login Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)


def clear_saved(who, over=False):
    if who == 'all':
        for login in LOGINID:
            clear_saved(login,  True)
    elif LOGINID[who]:
        file = LOGINID[who]['file']
        if os.path.exists(file):
            os.remove(file)
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, LOGINID[who]['name']),
                               '[COLOR {0}]Login Info: Removed![/COLOR]'.format(CONFIG.COLOR2),
                               2000,
                               LOGINID[who]['icon'])
        CONFIG.set_setting(LOGINID[who]['saved'], '')
    if not over:
        xbmc.executebuiltin('Container.Refresh()')


def update_login(do, who):
    file = LOGINID[who]['file']
    settings = LOGINID[who]['settings']
    data = LOGINID[who]['data']
    addonid = tools.get_addon_by_id(LOGINID[who]['plugin'])
    saved = LOGINID[who]['saved']
    default = LOGINID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = LOGINID[who]['name']
    icon = LOGINID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                root = ElementTree.Element(saved)
                
                for setting in data:
                    login = ElementTree.SubElement(root, 'login')
                    id = ElementTree.SubElement(login, 'id')
                    id.text = setting
                    value = ElementTree.SubElement(login, 'value')
                    value.text = addonid.getSetting(setting)
                  
                tree = ElementTree.ElementTree(root)
                tree.write(file)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('Login Data Saved for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Login Data] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Login Data Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('login'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                    
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('Login Data Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Login Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Login Data Not Found for {0}'.format(name))
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings), level=xbmc.LOGDEBUG)
        if os.path.exists(settings):
            try:
                tree = ElementTree.parse(settings)
                root = tree.getroot()
                
                for setting in root.findall('setting'):
                    if setting.attrib['id'] in data:
                        logging.log('Removing Setting: {0}'.format(setting.attrib))
                        root.remove(setting)
                            
                tree.write(settings)
                
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Addon Data: Cleared![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Trakt Data] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    xbmc.executebuiltin('Container.Refresh()')


def auto_update(who):
    if who == 'all':
        for log in LOGINID:
            if os.path.exists(LOGINID[log]['path']):
                auto_update(log)
    elif LOGINID[who]:
        if os.path.exists(LOGINID[who]['path']):
            u = login_user(who)
            su = CONFIG.get_setting(LOGINID[who]['saved'])
            n = LOGINID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                login_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Login Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n)
                                    +'\n'+"Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u)
                                    +'\n'+"Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
                    login_it('update', who)
            else:
                login_it('update', who)


def import_list(who):
    if who == 'all':
        for log in LOGINID:
            if os.path.exists(LOGINID[log]['file']):
                import_list(log)
    elif LOGINID[who]:
        if os.path.exists(LOGINID[who]['file']):
            file = LOGINID[who]['file']
            addonid = tools.get_addon_by_id(LOGINID[who]['plugin'])
            saved = LOGINID[who]['saved']
            default = LOGINID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = LOGINID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('login'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Login Data: Imported![/COLOR]'.format(CONFIG.COLOR2))


def activate_login(who):
    if LOGINID[who]:
        if os.path.exists(LOGINID[who]['path']):
            act = LOGINID[who]['activate']
            addonid = tools.get_addon_by_id(LOGINID[who]['plugin'])
            if act == '':
                addonid.openSettings()
            else:
                xbmc.executebuiltin(LOGINID[who]['activate'])
        else:
            dialog = xbmcgui.Dialog()

            dialog.ok(CONFIG.ADDONTITLE, '{0} is not currently installed.'.format(LOGINID[who]['name']))
    else:
        xbmc.executebuiltin('Container.Refresh()')
        return

    check = 0
    while not login_user(who) or login_user(who) == "":
        if check == 30:
            break
        check += 1
        time.sleep(10)
    xbmc.executebuiltin('Container.Refresh()')
