import xbmc
import xbmcaddon

import os

import uservar


class Config:
    def __init__(self):
        self.init_meta()
        self.init_uservars()
        self.init_paths()
        self.init_settings()

    def init_meta(self):
        self.ADDON = xbmcaddon.Addon(uservar.ADDON_ID)
        self.ADDON_NAME = self.ADDON.getAddonInfo('name')
        self.ADDON_VERSION = self.ADDON.getAddonInfo('version')
        self.ADDON_PATH = self.ADDON.getAddonInfo('path')
        self.ADDON_ICON = self.ADDON.getAddonInfo('icon')
        self.ADDON_FANART = self.ADDON.getAddonInfo('fanart')
        self.KODIV = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
        self.RAM = int(xbmc.getInfoLabel("System.Memory(total)")[:-2])

    def init_uservars(self):
        # User Edit Variables
        self.ADDON_ID = uservar.ADDON_ID
        self.EXCLUDES = uservar.EXCLUDES
        self.CACHETEXT = uservar.CACHETEXT
        self.CACHEAGE = uservar.CACHEAGE if str(uservar.CACHEAGE).isdigit() else 30
        self.BUILDFILE = uservar.BUILDFILE
        self.UPDATECHECK = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 0
        self.APKFILE = uservar.APKFILE
        self.YOUTUBETITLE = uservar.YOUTUBETITLE
        self.YOUTUBEFILE = uservar.YOUTUBEFILE
        self.ADDONFILE = uservar.ADDONFILE
        self.ADVANCEDFILE = uservar.ADVANCEDFILE

        # Themeing Menu Items
        self.ICONBUILDS = uservar.ICONBUILDS if not uservar.ICONBUILDS.endswith('://') else self.ADDON_ICON
        self.ICONMAINT = uservar.ICONMAINT if not uservar.ICONMAINT.endswith('://') else self.ADDON_ICON
        self.ICONSPEED = uservar.ICONSPEED if not uservar.ICONSPEED.endswith('://') else self.ADDON_ICON
        self.ICONAPK = uservar.ICONAPK if not uservar.ICONAPK.endswith('://') else self.ADDON_ICON
        self.ICONADDONS = uservar.ICONADDONS if not uservar.ICONADDONS.endswith('://') else self.ADDON_ICON
        self.ICONYOUTUBE = uservar.ICONYOUTUBE if not uservar.ICONYOUTUBE.endswith('://') else self.ADDON_ICON
        self.ICONSAVE = uservar.ICONSAVE if not uservar.ICONSAVE.endswith('://') else self.ADDON_ICON
        self.ICONTRAKT = uservar.ICONTRAKT if not uservar.ICONTRAKT.endswith('://') else self.ADDON_ICON
        self.ICONDEBRID = uservar.ICONREAL if not uservar.ICONREAL.endswith('://') else self.ADDON_ICON
        self.ICONLOGIN = uservar.ICONLOGIN if not uservar.ICONLOGIN.endswith('://') else self.ADDON_ICON
        self.ICONCONTACT = uservar.ICONCONTACT if not uservar.ICONCONTACT.endswith('://') else self.ADDON_ICON
        self.ICONSETTINGS = uservar.ICONSETTINGS if not uservar.ICONSETTINGS.endswith('://') else self.ADDON_ICON
        self.HIDESPACERS = uservar.HIDESPACERS
        self.SPACER = uservar.SPACER
        self.COLOR1 = uservar.COLOR1
        self.COLOR2 = uservar.COLOR2
        self.THEME1 = uservar.THEME1
        self.THEME2 = uservar.THEME2
        self.THEME3 = uservar.THEME3
        self.THEME4 = uservar.THEME4
        self.THEME5 = uservar.THEME5
        self.HIDECONTACT = uservar.HIDECONTACT
        self.CONTACT = uservar.CONTACT
        self.CONTACTICON = uservar.CONTACTICON if not uservar.CONTACTICON.endswith('://') else self.ADDON_ICON
        self.CONTACTFANART = uservar.CONTACTFANART if not uservar.CONTACTFANART.endswith('://') else self.ADDON_FANART

        # Auto Update For Those With No Repo
        self.AUTOUPDATE = uservar.AUTOUPDATE
        self.WIZARDFILE = uservar.WIZARDFILE

        # Auto  Install Repo If Not Installed
        self.AUTOINSTALL = uservar.AUTOINSTALL
        self.REPOID = uservar.REPOID
        self.REPOADDONXML = uservar.REPOADDONXML
        self.REPOZIPURL = uservar.REPOZIPURL

        # Notification Window
        self.ENABLE = uservar.ENABLE
        self.NOTIFICATION = uservar.NOTIFICATION
        self.HEADERTYPE = uservar.HEADERTYPE
        self.FONTHEADER = uservar.FONTHEADER
        self.HEADERMESSAGE = uservar.HEADERMESSAGE
        self.HEADERIMAGE = uservar.HEADERIMAGE
        self.FONTSETTINGS = uservar.FONTSETTINGS
        self.BACKGROUND = uservar.BACKGROUND

    def init_paths(self):
        # Static variables
        self.LOGFILES = ['log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log',
                         'tvmc.old.log', 'dmp']
        self.DEFAULTPLUGINS = ['metadata.album.universal', 'metadata.artists.universal',
                               'metadata.common.fanart.tv', 'metadata.common.imdb.com',
                               'metadata.common.musicbrainz.org', 'metadata.themoviedb.org',
                               'metadata.tvdb.com', 'service.xbmc.versioncheck']
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)' \
                          'Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

        # Default special paths
        self.XBMC = xbmc.translatePath('special://xbmc/')
        self.HOME = xbmc.translatePath('special://home/')
        self.TEMP = xbmc.translatePath('special://temp/')
        self.MASTERPROFILE = xbmc.translatePath('special://masterprofile/')
        self.PROFILE = xbmc.translatePath('special://profile/')
        self.SUBTITLES = xbmc.translatePath('special://subtitles/')
        self.USERDATA = xbmc.translatePath('special://userdata/')
        self.DATABASE = xbmc.translatePath('special://database/')
        self.THUMBNAILS = xbmc.translatePath('special://thumbnails/')
        self.RECORDINGS = xbmc.translatePath('special://recordings/')
        self.SCREENSHOTS = xbmc.translatePath('special://screenshots/')
        self.MUSICPLAYLISTS = xbmc.translatePath('special://musicplaylists/')
        self.VIDEOPLAYLISTS = xbmc.translatePath('special://videoplaylists/')
        self.CDRIPS = xbmc.translatePath('special://cdrips/')
        self.SKIN = xbmc.translatePath('special://skin/')
        self.LOGPATH = xbmc.translatePath('special://logpath/')

        # Constructed paths
        self.ADDONS = os.path.join(self.HOME, 'addons')
        self.PLUGIN = os.path.join(self.ADDONS, self.ADDON_ID)
        self.PACKAGES = os.path.join(self.ADDONS, 'packages')
        self.ADDON_DATA = os.path.join(self.USERDATA, 'addon_data')
        self.PLUGIN_DATA = os.path.join(self.ADDON_DATA, self.ADDON_ID)
        self.QRCODES = os.path.join(self.PLUGIN_DATA, 'QRCodes')
        self.TEXTCACHE = os.path.join(self.PLUGIN_DATA, 'Cache')
        self.SPEEDTEST = os.path.join(self.PLUGIN_DATA, 'SpeedTest')
        self.ARCHIVE_CACHE = os.path.join(self.TEMP, 'archive_cache')
        self.ART = os.path.join(self.PLUGIN, 'resources', 'art')

        # File paths
        self.ADVANCED = os.path.join(self.USERDATA, 'advancedsettings.xml')
        self.SOURCES = os.path.join(self.USERDATA, 'sources.xml')
        self.GUISETTINGS = os.path.join(self.USERDATA, 'guisettings.xml')
        self.FAVOURITES = os.path.join(self.USERDATA, 'favourites.xml')
        self.PROFILES = os.path.join(self.USERDATA, 'profiles.xml')
        self.WIZLOG = os.path.join(self.PLUGIN_DATA, 'wizard.log')
        self.WHITELIST = os.path.join(self.PLUGIN_DATA, 'whitelist.txt')

    def init_settings(self):
        # Build variables
        self.BUILDNAME = self.get_setting('buildname')
        self.DEFAULTSKIN = self.get_setting('defaultskin')
        self.DEFAULTNAME = self.get_setting('defaultskinname')
        self.DEFAULTIGNORE = self.get_setting('defaultskinignore')
        self.BUILDVERSION = self.get_setting('buildversion')
        self.BUILDTHEME = self.get_setting('buildtheme')
        self.BUILDLATEST = self.get_setting('latestversion')
        
        # View variables
        self.SHOW15 = self.get_setting('show15')
        self.SHOW16 = self.get_setting('show16')
        self.SHOW17 = self.get_setting('show17')
        self.SHOW18 = self.get_setting('show18')
        self.SHOWADULT = self.get_setting('adult')
        self.SHOWMAINT = self.get_setting('showmaint')
        self.SEPERATE = self.get_setting('seperate')
        self.DEVELOPER = self.get_setting('developer')
        
        # Auto-Clean variables
        self.AUTOCLEANUP = self.get_setting('autoclean')
        self.AUTOCACHE = self.get_setting('clearcache')
        self.AUTOPACKAGES = self.get_setting('clearpackages')
        self.AUTOTHUMBS = self.get_setting('clearthumbs')
        self.AUTOFREQ = self.get_setting('autocleanfreq')
        self.AUTOFREQ = int(float(self.AUTOFREQ)) if self.AUTOFREQ.isdigit() else 0
        self.AUTONEXTRUN = self.get_setting('nextautocleanup')
        
        # Video Cache variables
        self.INCLUDEVIDEO = self.get_setting('includevideo')
        self.INCLUDEALL = self.get_setting('includeall')
        self.INCLUDEPLACENTA = self.get_setting('includeplacenta')
        self.INCLUDEEXODUSREDUX = self.get_setting('includeexodusredux')
        self.INCLUDEGAIA = self.get_setting('includegaia')
        self.INCLUDESEREN = self.get_setting('includeseren')
        self.INCLUDEOVEREASY = self.get_setting('includeovereasy')
        self.INCLUDEYODA = self.get_setting('includeyoda')
        self.INCLUDEVENOM = self.get_setting('includevenom')
        self.INCLUDESCRUBS = self.get_setting('includescrubs')
        
        # Notification variables
        self.NOTIFY = self.get_setting('notify')
        self.NOTEID = self.get_setting('noteid')
        self.NOTEDISMISS = self.get_setting('notedismiss')
        
        # Save Data variables
        self.TRAKTSAVE = self.get_setting('traktlastsave')
        self.REALSAVE = self.get_setting('debridlastsave')
        self.LOGINSAVE = self.get_setting('loginlastsave')
        self.KEEPFAVS = self.get_setting('keepfavourites')
        self.KEEPSOURCES = self.get_setting('keepsources')
        self.KEEPPROFILES = self.get_setting('keepprofiles')
        self.KEEPPLAYERCORE = self.get_setting('keepplayercore')
        self.KEEPADVANCED = self.get_setting('keepadvanced')
        self.KEEPREPOS = self.get_setting('keeprepos')
        self.KEEPSUPER = self.get_setting('keepsuper')
        self.KEEPWHITELIST = self.get_setting('keepwhitelist')
        self.KEEPTRAKT = self.get_setting('keeptrakt')
        self.KEEPREAL = self.get_setting('keepdebrid')
        self.KEEPLOGIN = self.get_setting('keeplogin')
        
        # Third Party Wizard variables
        self.THIRDPARTY = self.get_setting('enable3rd')
        self.THIRD1NAME = self.get_setting('wizard1name')
        self.THIRD1URL = self.get_setting('wizard1url')
        self.THIRD2NAME = self.get_setting('wizard2name')
        self.THIRD2URL = self.get_setting('wizard2url')
        self.THIRD3NAME = self.get_setting('wizard3name')
        self.THIRD3URL = self.get_setting('wizard3url')

        # Backup variables
        self.BACKUPLOCATION = self.get_setting('path') if not self.get_setting('path') == '' else self.HOME
        self.MYBUILDS = os.path.join(self.BACKUPLOCATION, 'My_Builds')
        self.INSTALLMETHOD = self.get_setting('installmethod')
        self.INSTALLMETHOD = int(float(self.INSTALLMETHOD)) if self.INSTALLMETHOD.isdigit() else 2

        # Logging variables
        self.WIZDEBUGGING = self.get_setting('addon_debug')
        self.DEBUGLEVEL = self.get_setting('debuglevel')
        self.ENABLEWIZLOG = self.get_setting('wizardlog')
        self.CLEANWIZLOG = self.get_setting('autocleanwiz')
        self.CLEANWIZLOGBY = self.get_setting('wizlogcleanby')
        self.CLEANDAYS = self.get_setting('wizlogcleandays')
        self.CLEANSIZE = self.get_setting('wizlogcleansize')
        self.CLEANLINES = self.get_setting('wizlogcleanlines')
        self.MAXWIZSIZE = [100, 200, 300, 400, 500, 1000]
        self.MAXWIZLINES = [100, 200, 300, 400, 500]
        self.MAXWIZDATES = [1, 2, 3, 7]

    def get_setting(self, key, id=uservar.ADDON_ID):
        try:
            return xbmcaddon.Addon(id).getSetting(key)
        except:
            return False

    def set_setting(self, key, value, id=uservar.ADDON_ID):
        try:
            return xbmcaddon.Addon(id).setSetting(key, value)
        except:
            return False

    def open_settings(self, id=uservar.ADDON_ID):
        try:
            return xbmcaddon.Addon(id).openSettings()
        except:
            return False

    def clear_setting(self, type):
        build = {'buildname': '', 'buildversion': '', 'buildtheme': '', 'latestversion': '',
                 'lastbuildcheck': '2016-01-01'}
        install = {'installed': 'false', 'extract': '', 'errors': ''}
        default = {'defaultskinignore': 'false', 'defaultskin': '', 'defaultskinname': ''}
        lookfeel = ['default.enablerssfeeds', 'default.font', 'default.rssedit', 'default.skincolors',
                    'default.skintheme',
                    'default.skinzoom', 'default.soundskin', 'default.startupwindow', 'default.stereostrength']
        if type == 'build':
            for element in build:
                self.set_setting(element, build[element])
            for element in install:
                self.set_setting(element, install[element])
            for element in default:
                self.set_setting(element, default[element])
            for element in lookfeel:
                self.set_setting(element, '')
        elif type == 'default':
            for element in default:
                self.set_setting(element, default[element])
            for element in lookfeel:
                self.set_setting(element, '')
        elif type == 'install':
            for element in install:
                self.set_setting(element, install[element])
        elif type == 'lookfeel':
            for element in lookfeel:
                self.set_setting(element, '')


CONFIG = Config()

