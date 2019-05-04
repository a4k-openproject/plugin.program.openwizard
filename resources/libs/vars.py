import xbmc
import xbmcaddon

import os

import uservar

# Add-on metadata-related variables
ADDON = xbmcaddon.Addon(uservar.ADDON_ID)
VERSION = ADDON.getAddonInfo('version')
KODIV = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
PATH = ADDON.getAddonInfo('path')


# Path-related variables
HOME = xbmc.translatePath('special://home/')
XBMC = xbmc.translatePath('special://xbmc/')
LOG = xbmc.translatePath('special://logpath/')
PROFILE = xbmc.translatePath('special://profile/')
TEMPDIR = xbmc.translatePath('special://temp')
DATABASE = xbmc.translatePath('special://database/')

ADDONS = os.path.join(HOME, 'addons')
USERDATA = os.path.join(HOME, 'userdata')
PLUGIN = os.path.join(ADDONS, uservar.ADDON_ID)
PACKAGES = os.path.join(ADDONS, 'packages')
ADDOND = os.path.join(USERDATA, 'addon_data')
ADDONDATA = os.path.join(USERDATA, 'addon_data', uservar.ADDON_ID)
THUMBS = os.path.join(USERDATA, 'Thumbnails')
QRCODES = os.path.join(ADDONDATA, 'QRCodes')
TEXTCACHE = os.path.join(ADDONDATA, 'Cache')
ARCHIVE_CACHE = os.path.join(TEMPDIR, 'archive_cache')
ART = os.path.join(PLUGIN, 'resources', 'art')
SKIN = xbmc.getSkinDir()


# File-related variables
ADVANCED = os.path.join(USERDATA, 'advancedsettings.xml')
SOURCES = os.path.join(USERDATA, 'sources.xml')
GUISETTINGS = os.path.join(USERDATA, 'guisettings.xml')
FAVOURITES = os.path.join(USERDATA, 'favourites.xml')
PROFILES = os.path.join(USERDATA, 'profiles.xml')
FANART = os.path.join(PLUGIN, 'fanart.jpg')
ICON = os.path.join(PLUGIN, 'icon.png')
WIZLOG = os.path.join(ADDONDATA, 'wizard.log')
WHITELIST = os.path.join(ADDONDATA, 'whitelist.txt')


# Misc variables
DEFAULTPLUGINS = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv',
                  'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org',
                  'metadata.tvdb.com', 'service.xbmc.versioncheck']
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
