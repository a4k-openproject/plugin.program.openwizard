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
import fnmatch
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from urlparse import urljoin
from resources.libs import extract, downloader, notify, debridit, traktit, loginit, skinSwitch, uploadLog, yt, speedtest, wizard as wiz

ADDON_ID         = uservar.ADDON_ID
ADDONTITLE       = uservar.ADDONTITLE
ADDON            = wiz.addonId(ADDON_ID)
VERSION          = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH        = wiz.addonInfo(ADDON_ID, 'path')
DIALOG           = xbmcgui.Dialog()
DP               = xbmcgui.DialogProgress()
HOME             = xbmc.translatePath('special://home/')
LOG              = xbmc.translatePath('special://logpath/')
PROFILE          = xbmc.translatePath('special://profile/')
TEMPDIR          = xbmc.translatePath('special://temp')
ADDONS           = os.path.join(HOME,      'addons')
USERDATA         = os.path.join(HOME,      'userdata')
PLUGIN           = os.path.join(ADDONS,    ADDON_ID)
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED         = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES          = os.path.join(USERDATA,  'sources.xml')
FAVOURITES       = os.path.join(USERDATA,  'favourites.xml')
PROFILES         = os.path.join(USERDATA,  'profiles.xml')
GUISETTINGS      = os.path.join(USERDATA,  'guisettings.xml')
THUMBS           = os.path.join(USERDATA,  'Thumbnails')
DATABASE         = os.path.join(USERDATA,  'Database')
FANART           = os.path.join(PLUGIN,    'fanart.jpg')
ICON             = os.path.join(PLUGIN,    'icon.png')
ART              = os.path.join(PLUGIN,    'resources', 'art')
WIZLOG           = os.path.join(ADDONDATA, 'wizard.log')
SPEEDTESTFOLD    = os.path.join(ADDONDATA, 'SpeedTest')
ARCHIVE_CACHE    = os.path.join(TEMPDIR,   'archive_cache')
SKIN             = xbmc.getSkinDir()
BUILDNAME        = wiz.getS('buildname')
DEFAULTSKIN      = wiz.getS('defaultskin')
DEFAULTNAME      = wiz.getS('defaultskinname')
DEFAULTIGNORE    = wiz.getS('defaultskinignore')
BUILDVERSION     = wiz.getS('buildversion')
BUILDTHEME       = wiz.getS('buildtheme')
BUILDLATEST      = wiz.getS('latestversion')
SHOW15           = wiz.getS('show15')
SHOW16           = wiz.getS('show16')
SHOW17           = wiz.getS('show17')
SHOW18           = wiz.getS('show18')
SHOWADULT        = wiz.getS('adult')
SHOWMAINT        = wiz.getS('showmaint')
AUTOCLEANUP      = wiz.getS('autoclean')
AUTOCACHE        = wiz.getS('clearcache')
AUTOPACKAGES     = wiz.getS('clearpackages')
AUTOTHUMBS       = wiz.getS('clearthumbs')
AUTOFEQ          = wiz.getS('autocleanfeq')
AUTONEXTRUN      = wiz.getS('nextautocleanup')
INCLUDEVIDEO     = wiz.getS('includevideo')
INCLUDEALL       = wiz.getS('includeall')
INCLUDEPLACENTA    = wiz.getS('includeplacenta')
INCLUDEEXODUSREDUX    = wiz.getS('includeexodusredux')
INCLUDE13CLOWNS = wiz.getS('include13clowns')
INCLUDEZANNI = wiz.getS('includezanni')
INCLUDEGAIA     = wiz.getS('includegaia')
INCLUDESEREN     = wiz.getS('includeseren')
INCLUDEMAGICALITY   = wiz.getS('includemagicality')
SEPERATE         = wiz.getS('seperate')
NOTIFY           = wiz.getS('notify')
NOTEID           = wiz.getS('noteid')
NOTEDISMISS      = wiz.getS('notedismiss')
TRAKTSAVE        = wiz.getS('traktlastsave')
REALSAVE         = wiz.getS('debridlastsave')
LOGINSAVE        = wiz.getS('loginlastsave')
KEEPFAVS         = wiz.getS('keepfavourites')
KEEPSOURCES      = wiz.getS('keepsources')
KEEPPROFILES     = wiz.getS('keepprofiles')
KEEPADVANCED     = wiz.getS('keepadvanced')
KEEPREPOS        = wiz.getS('keeprepos')
KEEPSUPER        = wiz.getS('keepsuper')
KEEPWHITELIST    = wiz.getS('keepwhitelist')
KEEPTRAKT        = wiz.getS('keeptrakt')
KEEPREAL         = wiz.getS('keepdebrid')
KEEPLOGIN        = wiz.getS('keeplogin')
DEVELOPER        = wiz.getS('developer')
THIRDPARTY       = wiz.getS('enable3rd')
THIRD1NAME       = wiz.getS('wizard1name')
THIRD1URL        = wiz.getS('wizard1url')
THIRD2NAME       = wiz.getS('wizard2name')
THIRD2URL        = wiz.getS('wizard2url')
THIRD3NAME       = wiz.getS('wizard3name')
THIRD3URL        = wiz.getS('wizard3url')
BACKUPLOCATION   = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
BACKUPROMS       = wiz.getS('rompath')
MYBUILDS         = os.path.join(BACKUPLOCATION, 'My_Builds', '')
AUTOFEQ          = int(float(AUTOFEQ)) if AUTOFEQ.isdigit() else 0
TODAY            = date.today()
TOMORROW         = TODAY + timedelta(days=1)
THREEDAYS        = TODAY + timedelta(days=3)

KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if KODIV > 17:
	from resources.libs import zfile as zipfile
else:
	import zipfile

MCNAME           = wiz.mediaCenter()
EXCLUDES         = uservar.EXCLUDES
CACHETEXT        = uservar.CACHETEXT
CACHEAGE         = uservar.CACHEAGE if str(uservar.CACHEAGE).isdigit() else 30
BUILDFILE        = uservar.BUILDFILE
APKFILE          = uservar.APKFILE
YOUTUBETITLE     = uservar.YOUTUBETITLE
YOUTUBEFILE      = uservar.YOUTUBEFILE
ADDONFILE        = uservar.ADDONFILE
ADVANCEDFILE     = uservar.ADVANCEDFILE
UPDATECHECK      = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK        = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION     = uservar.NOTIFICATION
ENABLE           = uservar.ENABLE
HEADERMESSAGE    = uservar.HEADERMESSAGE
AUTOUPDATE       = uservar.AUTOUPDATE
BUILDERNAME      = uservar.BUILDERNAME
WIZARDFILE       = uservar.WIZARDFILE
HIDECONTACT      = uservar.HIDECONTACT
CONTACT          = uservar.CONTACT
CONTACTICON      = uservar.CONTACTICON if not uservar.CONTACTICON == 'http://' else ICON
CONTACTFANART    = uservar.CONTACTFANART if not uservar.CONTACTFANART == 'http://' else FANART
HIDESPACERS      = uservar.HIDESPACERS
COLOR1           = uservar.COLOR1
COLOR2           = uservar.COLOR2
THEME1           = uservar.THEME1
THEME2           = uservar.THEME2
THEME3           = uservar.THEME3
THEME4           = uservar.THEME4
THEME5           = uservar.THEME5
ICONBUILDS       = uservar.ICONBUILDS if not uservar.ICONBUILDS == 'http://' else ICON
ICONMAINT        = uservar.ICONMAINT if not uservar.ICONMAINT == 'http://' else ICON
ICONAPK          = uservar.ICONAPK if not uservar.ICONAPK == 'http://' else ICON
ICONADDONS       = uservar.ICONADDONS if not uservar.ICONADDONS == 'http://' else ICON
ICONYOUTUBE      = uservar.ICONYOUTUBE if not uservar.ICONYOUTUBE == 'http://' else ICON
ICONSAVE         = uservar.ICONSAVE if not uservar.ICONSAVE == 'http://' else ICON
ICONTRAKT        = uservar.ICONTRAKT if not uservar.ICONTRAKT == 'http://' else ICON
ICONREAL         = uservar.ICONREAL if not uservar.ICONREAL == 'http://' else ICON
ICONLOGIN        = uservar.ICONLOGIN if not uservar.ICONLOGIN == 'http://' else ICON
ICONCONTACT      = uservar.ICONCONTACT if not uservar.ICONCONTACT == 'http://' else ICON
ICONSETTINGS     = uservar.ICONSETTINGS if not uservar.ICONSETTINGS == 'http://' else ICON
LOGFILES         = wiz.LOGFILES
TRAKTID          = traktit.TRAKTID
DEBRIDID         = debridit.DEBRIDID
LOGINID          = loginit.LOGINID
MODURL           = 'http://tribeca.tvaddons.ag/tools/maintenance/modules/'
MODURL2          = 'http://mirrors.kodi.tv/addons/jarvis/'
INSTALLMETHODS   = ['Always Ask', 'Reload Profile', 'Force Close']
DEFAULTPLUGINS   = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']
try:
    INSTALLMETHOD    = int(float(wiz.getS('installmethod')))
except:
    INSTALLMETHOD    = 0

###########################
###### Menu Items   #######
###########################
#addDir (display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
#addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)

def index():
    errors = int(errorChecking(count=True))
    errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'

    if AUTOUPDATE == 'Yes':
        wizfile = wiz.textCache(WIZARDFILE)
        if not wizfile == False:
            ver = wiz.checkWizard('version')
            if ver > VERSION: addFile('%s [v%s] [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (ADDONTITLE, VERSION, ver), 'wizardupdate', themeit=THEME2)
            else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
        else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
    else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
    if len(BUILDNAME) > 0:
        version = wiz.checkBuild(BUILDNAME, 'version')
        build = '%s (v%s)' % (BUILDNAME, BUILDVERSION)
        if version > BUILDVERSION: build = '%s [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (build, version)
        addDir(build,'viewbuild', BUILDNAME, themeit=THEME4)
        themefile = wiz.themeCount(BUILDNAME)
        if not themefile == False:
            addFile('None' if BUILDTHEME == "" else BUILDTHEME, 'theme', BUILDNAME, themeit=THEME5)
    else: addDir('None', 'builds', themeit=THEME4)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addDir ('Builds', 'builds',   icon=ICONBUILDS,   themeit=THEME1)
    addDir ('Maintenance', 'maint',    icon=ICONMAINT,    themeit=THEME1)
    if wiz.platform() == 'android' or DEVELOPER == 'true': addDir ('Apk Installer' ,'apk', icon=ICONAPK, themeit=THEME1)
    if not ADDONFILE == 'http://': addDir ('Addon Installer' ,'addons', icon=ICONADDONS, themeit=THEME1)
    if not YOUTUBEFILE == 'http://' and not YOUTUBETITLE == '': addDir (YOUTUBETITLE ,'youtube', icon=ICONYOUTUBE, themeit=THEME1)
    addDir ('Save Data', 'savedata', icon=ICONSAVE,     themeit=THEME1)
    if HIDECONTACT == 'No': addFile('Contact' ,'contact', icon=ICONCONTACT,  themeit=THEME1)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Upload Log File', 'uploadlog',       icon=ICONMAINT, themeit=THEME1)
    addFile('View Errors in Log: %s' % (errorsfound), 'viewerrorlog', icon=ICONMAINT, themeit=THEME1)
    if errors > 0: addFile('View Last Error In Log', 'viewerrorlast', icon=ICONMAINT, themeit=THEME1)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Settings', 'settings', icon=ICONSETTINGS, themeit=THEME1)
    addFile('Force Update Text Files', 'forcetext', icon=ICONMAINT, themeit=THEME1)
    if DEVELOPER == 'true': addDir('Developer Menu', 'developer', icon=ICON, themeit=THEME1)
    setView('files', 'viewType')

def buildMenu():
    bf = wiz.textCache(BUILDFILE)
    if bf == False:
        WORKINGURL = wiz.workingURL(BUILDFILE)
        addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
        addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
        addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
        return
    total, count15, count16, count17, count18, adultcount, hidden = wiz.buildCount()
    third = False; addin = []
    if THIRDPARTY == 'true':
        if not THIRD1NAME == '' and not THIRD1URL == '': third = True; addin.append('1')
        if not THIRD2NAME == '' and not THIRD2URL == '': third = True; addin.append('2')
        if not THIRD3NAME == '' and not THIRD3URL == '': third = True; addin.append('3')
    link  = bf.replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"').replace('adult=""', 'adult="no"')
    match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
    if total == 1 and third == False:
        for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
            if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
            if not DEVELOPER == 'true' and wiz.strTest(name): continue
            viewBuild(match[0][0])
            return
    addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
    addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    if third == True:
        for item in addin:
            name = eval('THIRD%sNAME' % item)
            addDir ("[B]%s[/B]" % name, 'viewthirdparty', item, icon=ICONBUILDS, themeit=THEME3)
    if len(match) >= 1:
        if SEPERATE == 'true':
            for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                if not DEVELOPER == 'true' and wiz.strTest(name): continue
                menu = createMenu('install', '', name)
                addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
        else:
            if count18 > 0:
                state = '+' if SHOW18 == 'false' else '-'
                addFile('[B]%s Leia Builds(%s)[/B]' % (state, count18), 'togglesetting',  'show17', themeit=THEME3)
                if SHOW18 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv == 18:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
            if count17 > 0:
                state = '+' if SHOW17 == 'false' else '-'
                addFile('[B]%s Krypton Builds(%s)[/B]' % (state, count17), 'togglesetting',  'show17', themeit=THEME3)
                if SHOW17 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv == 17:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
            if count16 > 0:
                state = '+' if SHOW16 == 'false' else '-'
                addFile('[B]%s Jarvis Builds(%s)[/B]' % (state, count16), 'togglesetting',  'show16', themeit=THEME3)
                if SHOW16 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv == 16:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
            if count15 > 0:
                state = '+' if SHOW15 == 'false' else '-'
                addFile('[B]%s Isengard and Below Builds(%s)[/B]' % (state, count15), 'togglesetting',  'show15', themeit=THEME3)
                if SHOW15 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv <= 15:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
    elif hidden > 0:
        if adultcount > 0:
            addFile('There is currently only Adult builds', '', icon=ICONBUILDS, themeit=THEME3)
            addFile('Enable Show Adults in Addon Settings > Misc', '', icon=ICONBUILDS, themeit=THEME3)
        else:
            addFile('Currently No Builds Offered from %s' % ADDONTITLE, '', icon=ICONBUILDS, themeit=THEME3)
    else: addFile('Text file for builds not formated correctly.', '', icon=ICONBUILDS, themeit=THEME3)
    setView('files', 'viewType')

def viewBuild(name):
    bf = wiz.textCache(BUILDFILE)
    if bf == False:
        WORKINGURL = wiz.workingURL(BUILDFILE)
        addFile('Url for txt file not valid', '', themeit=THEME3)
        addFile('%s' % WORKINGURL, '', themeit=THEME3)
        return
    if wiz.checkBuild(name, 'version') == False:
        addFile('Error reading the txt file.', '', themeit=THEME3)
        addFile('%s was not found in the builds list.' % name, '', themeit=THEME3)
        return
    link = bf.replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
    match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?inor="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?nfo="(.+?)".+?escription="(.+?)"' % name).findall(link)
    for version, url, minor, gui, kodi, themefile, icon, fanart, preview, adult, info, description in match:
        icon        = icon
        fanart      = fanart
        build       = '%s (v%s)' % (name, version)
        if BUILDNAME == name and version > BUILDVERSION:
            build = '%s [COLOR red][CURRENT v%s][/COLOR]' % (build, BUILDVERSION)
        addFile(build, '', description=description, fanart=fanart, icon=icon, themeit=THEME4)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        addDir ('Save Data Menu',       'savedata', icon=ICONSAVE,     themeit=THEME3)
        addFile('Build Information',    'buildinfo', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
        if not preview == "http://": addFile('View Video Preview', 'buildpreview', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
        temp1 = int(float(KODIV)); temp2 = int(float(kodi))
        if not temp1 == temp2:
            if temp1 == 16 and temp2 <= 15: warning = False
            else: warning = True
        else: warning = False
        if warning == True:
            addFile('[I]Build designed for kodi version %s(installed: %s)[/I]' % (str(kodi), str(KODIV)), '', fanart=fanart, icon=icon, themeit=THEME3)
        addFile(wiz.sep('INSTALL'), '', fanart=fanart, icon=icon, themeit=THEME3)
        addFile('Fresh Install'   , 'install', name, 'fresh'  , description=description, fanart=fanart, icon=icon, themeit=THEME1)
        addFile('Standard Install', 'install', name, 'normal' , description=description, fanart=fanart, icon=icon, themeit=THEME1)
        if not gui == 'http://': addFile('Apply guiFix'    , 'install', name, 'gui'     , description=description, fanart=fanart, icon=icon, themeit=THEME1)
        if not themefile == 'http://':
            themecheck = wiz.textCache(themefile)
            if not themecheck == False:
                addFile(wiz.sep('THEMES'), '', fanart=fanart, icon=icon, themeit=THEME3)
                link  = themecheck.replace('\n','').replace('\r','').replace('\t','')
                match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
                for themename, themeurl, themeicon, themefanart, themeadult, description in match:
                    if not SHOWADULT == 'true' and themeadult.lower() == 'yes': continue
                    themeicon   = themeicon   if themeicon   == 'http://' else icon
                    themefanart = themefanart if themefanart == 'http://' else fanart
                    addFile(themename if not themename == BUILDTHEME else "[B]%s (Installed)[/B]" % themename, 'theme', name, themename, description=description, fanart=themefanart, icon=themeicon, themeit=THEME3)
    setView('files', 'viewType')

def viewThirdList(number):
    name = eval('THIRD%sNAME' % number)
    url  = eval('THIRD%sURL' % number)
    work = wiz.workingURL(url)
    if not work == True:
        addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
        addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
    else:
        type, buildslist = wiz.thirdParty(url)
        addFile("[B]%s[/B]" % name, '', themeit=THEME3)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        if type:
            for name, version, url, kodi, icon, fanart, adult, description in buildslist:
                if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                addFile("[%s] %s v%s" % (kodi, name, version), 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)
        else:
            for name, url, icon, fanart, description in buildslist:
                addFile(name, 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)

def editThirdParty(number):
    name  = eval('THIRD%sNAME' % number)
    url   = eval('THIRD%sURL' % number)
    name2 = wiz.getKeyboard(name, 'Enter the Name of the Wizard')
    url2  = wiz.getKeyboard(url, 'Enter the URL of the Wizard Text')

    wiz.setS('wizard%sname' % number, name2)
    wiz.setS('wizard%surl' % number, url2)

def apkScraper(name=""):
    if name == 'kodi':
        kodiurl1 = 'http://mirrors.kodi.tv/releases/android/arm/'
        kodiurl2 = 'http://mirrors.kodi.tv/releases/android/arm/old/'
        url1 = wiz.openURL(kodiurl1).replace('\n', '').replace('\r', '').replace('\t', '')
        url2 = wiz.openURL(kodiurl2).replace('\n', '').replace('\r', '').replace('\t', '')
        x = 0
        match1 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url1)
        match2 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url2)

        addFile("Official Kodi Apk\'s", themeit=THEME1)
        rc = False
        for url, name, size, date in match1:
            if url in ['../', 'old/']: continue
            if not url.endswith('.apk'): continue
            if not url.find('_') == -1 and rc == True: continue
            try:
                tempname = name.split('-')
                if not url.find('_') == -1:
                    rc = True
                    name2, v2 = tempname[2].split('_')
                else:
                    name2 = tempname[2]
                    v2 = ''
                title = "[COLOR %s]%s v%s%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], v2.upper(), name2, COLOR2, size.replace(' ', ''), COLOR1, date)
                download = urljoin(kodiurl1, url)
                addFile(title, 'apkinstall', "%s v%s%s %s" % (tempname[0].title(), tempname[1], v2.upper(), name2), download)
                x += 1
            except:
                wiz.log("Error on: %s" % name)

        for url, name, size, date in match2:
            if url in ['../', 'old/']: continue
            if not url.endswith('.apk'): continue
            if not url.find('_') == -1: continue
            try:
                tempname = name.split('-')
                title = "[COLOR %s]%s v%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], tempname[2], COLOR2, size.replace(' ', ''), COLOR1, date)
                download = urljoin(kodiurl2, url)
                addFile(title, 'apkinstall', "%s v%s %s" % (tempname[0].title(), tempname[1], tempname[2]), download)
                x += 1
            except:
                wiz.log("Error on: %s" % name)
        if x == 0: addFile("Error Kodi Scraper Is Currently Down.")

def apkMenu(name=None, url=None):
    if url == None:
        addDir ('Official Kodi Apk\'s', 'apkscrape', 'kodi', icon=ICONAPK, themeit=THEME1)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    if not APKFILE == 'http://':
        if url == None:
            TEMPAPKFILE = wiz.textCache(uservar.APKFILE)
            if TEMPAPKFILE == False: APKWORKING  = wiz.workingURL(uservar.APKFILE)
        else:
            TEMPAPKFILE = wiz.textCache(url)
            if TEMPAPKFILE == False: APKWORKING  = wiz.workingURL(url)
        if not TEMPAPKFILE == False:
            link = TEMPAPKFILE.replace('\n','').replace('\r','').replace('\t','')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                x = 0
                for aname, section, url, icon, fanart, adult, description in match:
                    if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                    if section.lower() == 'yes':
                        x += 1
                        addDir ("[B]%s[/B]" % aname, 'apk', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    elif section.lower() == 'yes':
                        x += 1
                        # addFile(aname, 'rominstall', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    else:
                        x += 1
                        addFile(aname, 'apkinstall', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    if x == 0:
                        addFile("No addons adde0d to this menu yet!", '', themeit=THEME2)
            else: wiz.log("[APK Menu] ERROR: Invalid Format.", xbmc.LOGERROR)
        else:
            wiz.log("[APK Menu] ERROR: URL for apk list not working.", xbmc.LOGERROR)
            addFile('Url for txt file not valid', '', themeit=THEME3)
            addFile('%s' % APKWORKING, '', themeit=THEME3)
        return
    else: wiz.log("[APK Menu] No APK list added.")
    setView('files', 'viewType')

def addonMenu(name=None, url=None):
    if not ADDONFILE == 'http://':
        if url == None:
            TEMPADDONFILE = wiz.textCache(uservar.ADDONFILE)
            if TEMPADDONFILE == False: ADDONWORKING  = wiz.workingURL(uservar.ADDONFILE)
        else:
            TEMPADDONFILE = wiz.textCache(url)
            if TEMPADDONFILE == False: ADDONWORKING  = wiz.workingURL(url)
        if not TEMPADDONFILE == False:
            link = TEMPADDONFILE.replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
            match = re.compile('name="(.+?)".+?lugin="(.+?)".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                x = 0
                for aname, plugin, aurl, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
                    if plugin.lower() == 'section':
                        x += 1
                        addDir ("[B]%s[/B]" % aname, 'addons', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    elif plugin.lower() == 'skin':
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        x += 1
                        addFile("[B]%s[/B]" % aname, 'skinpack', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    elif plugin.lower() == 'pack':
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        x += 1
                        addFile("[B]%s[/B]" % aname, 'addonpack', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    else:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        try:
                            add    = xbmcaddon.Addon(id=plugin).getAddonInfo('path')
                            if os.path.exists(add):
                                aname   = "[COLOR springgreen][Installed][/COLOR] %s" % aname
                        except:
                            pass
                        x += 1
                        addFile(aname, 'addoninstall', plugin, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    if x < 1:
                        addFile("No addons added to this menu yet!", '', themeit=THEME2)
            else:
                addFile('Text File not formated correctly!', '', themeit=THEME3)
                wiz.log("[Addon Menu] ERROR: Invalid Format.")
        else:
            wiz.log("[Addon Menu] ERROR: URL for Addon list not working.")
            addFile('Url for txt file not valid', '', themeit=THEME3)
            addFile('%s' % ADDONWORKING, '', themeit=THEME3)
    else: wiz.log("[Addon Menu] No Addon list added.")
    setView('files', 'viewType')

def packInstaller(name, url):
    if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    urlsplits = url.split('/')
    lib = xbmc.makeLegalFilename(os.path.join(PACKAGES, urlsplits[-1]))
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
    DP.update(0, title,'', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
    installed = grabAddons(lib)
    if KODIV >= 17: wiz.addonDatabase(installed, 1, True)
    DP.close()
    wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s: Installed![/COLOR]' % (COLOR2, name))
    wiz.ebi('UpdateAddonRepos()')
    wiz.ebi('UpdateLocalAddons()')
    wiz.refresh()

def skinInstaller(name, url):
    if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    urlsplits = url.split('/')
    lib = xbmc.makeLegalFilename(os.path.join(PACKAGES, urlsplits[-1]))
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
    DP.update(0, title,'', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    percent, errors, error = extract.all(lib,HOME,DP, title=title)
    installed = grabAddons(lib)
    if KODIV >= 17: wiz.addonDatabase(installed, 1, True)
    DP.close()
    wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s: Installed![/COLOR]' % (COLOR2, name))
    wiz.ebi('UpdateAddonRepos()')
    wiz.ebi('UpdateLocalAddons()')
    for item in installed:
        if item.startswith('skin.') == True and not item == 'skin.shortcuts':
            if not BUILDNAME == '' and DEFAULTIGNORE == 'true': wiz.setS('defaultskinignore', 'true')
            wiz.swapSkins(item, 'Skin Installer')
    wiz.refresh()

def addonInstaller(plugin, url):
    if not ADDONFILE == 'http://':
        if url == None: url = ADDONFILE
        ADDONWORKING = wiz.workingURL(url)
        if ADDONWORKING == True:
            link = wiz.textCache(url).replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
            match = re.compile('name="(.+?)".+?lugin="%s".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % plugin).findall(link)
            if len(match) > 0:
                for name, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
                    if os.path.exists(os.path.join(ADDONS, plugin)):
                        do        = ['Launch Addon', 'Remove Addon']
                        selected = DIALOG.select("[COLOR %s]Addon already installed what would you like to do?[/COLOR]" % COLOR2, do)
                        if selected == 0:
                            wiz.ebi('RunAddon(%s)' % plugin)
                            xbmc.sleep(500)
                            return True
                        elif selected == 1:
                            wiz.cleanHouse(os.path.join(ADDONS, plugin))
                            try: wiz.removeFolder(os.path.join(ADDONS, plugin))
                            except: pass
                            if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to remove the addon_data for:" % COLOR2, "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, plugin), yeslabel="[B][COLOR springgreen]Yes Remove[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
                                removeAddonData(plugin)
                            wiz.refresh()
                            return True
                        else:
                            return False
                    repo = os.path.join(ADDONS, repository)
                    if not repository.lower() == 'none' and not os.path.exists(repo):
                        wiz.log("Repository not installed, installing it")
                        if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to install the repository for [COLOR %s]%s[/COLOR]:" % (COLOR2, COLOR1, plugin), "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, repository), yeslabel="[B][COLOR springgreen]Yes Install[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
                            ver = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': repository})
                            if len(ver) > 0:
                                repozip = '%s%s-%s.zip' % (repositoryurl, repository, ver[0])
                                wiz.log(repozip)
                                if KODIV >= 17: wiz.addonDatabase(repository, 1)
                                installAddon(repository, repozip)
                                wiz.ebi('UpdateAddonRepos()')
                                #wiz.ebi('UpdateLocalAddons()')
                                wiz.log("Installing Addon from Kodi")
                                install = installFromKodi(plugin)
                                wiz.log("Install from Kodi: %s" % install)
                                if install:
                                    wiz.refresh()
                                    return True
                            else:
                                wiz.log("[Addon Installer] Repository not installed: Unable to grab url! (%s)" % repository)
                        else: wiz.log("[Addon Installer] Repository for %s not installed: %s" % (plugin, repository))
                    elif repository.lower() == 'none':
                        wiz.log("No repository, installing addon")
                        pluginid = plugin
                        zipurl = url
                        installAddon(plugin, url)
                        wiz.refresh()
                        return True
                    else:
                        wiz.log("Repository installed, installing addon")
                        install = installFromKodi(plugin, False)
                        if install:
                            wiz.refresh()
                            return True
                    if os.path.exists(os.path.join(ADDONS, plugin)): return True
                    ver2 = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': plugin})
                    if len(ver2) > 0:
                        url = "%s%s-%s.zip" % (url, plugin, ver2[0])
                        wiz.log(str(url))
                        if KODIV >= 17: wiz.addonDatabase(plugin, 1)
                        installAddon(plugin, url)
                        wiz.refresh()
                    else:
                        wiz.log("no match"); return False
            else: wiz.log("[Addon Installer] Invalid Format")
        else: wiz.log("[Addon Installer] Text File: %s" % ADDONWORKING)
    else: wiz.log("[Addon Installer] Not Enabled.")

def installFromKodi(plugin, over=True):
    if over == True:
        xbmc.sleep(2000)
    #wiz.ebi('InstallAddon(%s)' % plugin)
    wiz.ebi('RunPlugin(plugin://%s)' % plugin)
    if not wiz.whileWindow('yesnodialog'):
        return False
    xbmc.sleep(500)
    if wiz.whileWindow('okdialog'):
        return False
    wiz.whileWindow('progressdialog')
    if os.path.exists(os.path.join(ADDONS, plugin)): return True
    else: return False

def installAddon(name, url):
    if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    urlsplits = url.split('/')
    lib=os.path.join(PACKAGES, urlsplits[-1])
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
    DP.update(0, title,'', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
    DP.update(0, title,'', '[COLOR %s]Installing Dependencies[/COLOR]' % COLOR2)
    installed(name)
    installlist = grabAddons(lib)
    wiz.log(str(installlist))
    if KODIV >= 17: wiz.addonDatabase(installlist, 1, True)
    installDep(name, DP)
    DP.close()
    wiz.ebi('UpdateAddonRepos()')
    wiz.ebi('UpdateLocalAddons()')
    wiz.refresh()
    for item in installlist:
        if item.startswith('skin.') == True and not item == 'skin.shortcuts':
            if not BUILDNAME == '' and DEFAULTIGNORE == 'true': wiz.setS('defaultskinignore', 'true')
            wiz.swapSkins(item, 'Skin Installer')

def installDep(name, DP=None):
    dep=os.path.join(ADDONS,name,'addon.xml')
    if os.path.exists(dep):
        source = open(dep,mode='r'); link = source.read(); source.close();
        match  = wiz.parseDOM(link, 'import', ret='addon')
        for depends in match:
            if not 'xbmc.python' in depends:
                if not DP == None:
                    DP.update(0, '', '[COLOR %s]%s[/COLOR]' % (COLOR1, depends))
                try:
                    add   = xbmcaddon.Addon(id=depends)
                    name2 = add.getAddonInfo('name')
                except:
                    wiz.createTemp(depends)
                    if KODIV >= 17: wiz.addonDatabase(depends, 1)
                # continue
                # dependspath=os.path.join(ADDONS, depends)
                # if not os.path.exists(dependspath):
                    # zipname = '%s-%s.zip' % (depends, match2[match.index(depends)])
                    # depzip = urljoin("%s%s/" % (MODURL2, depends), zipname)
                    # if not wiz.workingURL(depzip) == True:
                        # depzip = urljoin(MODURL, '%s.zip' % depends)
                        # if not wiz.workingURL(depzip) == True:
                            # wiz.createTemp(depends)
                            # if KODIV >= 17: wiz.addonDatabase(depends, 1)
                            # continue
                    # lib=os.path.join(PACKAGES, '%s.zip' % depends)
                    # try: os.remove(lib)
                    # except: pass
                    # DP.update(0, '[COLOR %s][B]Downloading Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends),'', 'Please Wait')
                    # downloader.download(depzip, lib, DP)
                    # xbmc.sleep(100)
                    # title = '[COLOR %s][B]Installing Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends)
                    # DP.update(0, title,'', 'Please Wait')
                    # percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
                    # if KODIV >= 17: wiz.addonDatabase(depends, 1)
                    # installed(depends)
                    # installDep(depends)
                    # xbmc.sleep(100)
                    # DP.close()

def installed(addon):
    url = os.path.join(ADDONS,addon,'addon.xml')
    if os.path.exists(url):
        try:
            list  = open(url,mode='r'); g = list.read(); list.close()
            name = wiz.parseDOM(g, 'addon', ret='name', attrs = {'id': addon})
            icon  = os.path.join(ADDONS,addon,'icon.png')
            wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, name[0]), '[COLOR %s]Addon Enabled[/COLOR]' % COLOR2, '2000', icon)
        except: pass

def youtubeMenu(name=None, url=None):
    if not YOUTUBEFILE == 'http://':
        if url == None:
            TEMPYOUTUBEFILE = wiz.textCache(uservar.YOUTUBEFILE)
            if TEMPYOUTUBEFILE == False: YOUTUBEWORKING  = wiz.workingURL(uservar.YOUTUBEFILE)
        else:
            TEMPYOUTUBEFILE = wiz.textCache(url)
            if TEMPYOUTUBEFILE == False: YOUTUBEWORKING  = wiz.workingURL(url)
        if not TEMPYOUTUBEFILE == False:
            link = TEMPYOUTUBEFILE.replace('\n','').replace('\r','').replace('\t','')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                for name, section, url, icon, fanart, description in match:
                    if section.lower() == "yes":
                        addDir ("[B]%s[/B]" % name, 'youtube', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    else:
                        addFile(name, 'viewVideo', url=url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
            else: wiz.log("[YouTube Menu] ERROR: Invalid Format.")
        else:
            wiz.log("[YouTube Menu] ERROR: URL for YouTube list not working.")
            addFile('Url for txt file not valid', '', themeit=THEME3)
            addFile('%s' % YOUTUBEWORKING, '', themeit=THEME3)
    else: wiz.log("[YouTube Menu] No YouTube list added.")
    setView('files', 'viewType')

def maintMenu(view=None):
    on = '[B][COLOR springgreen]ON[/COLOR][/B]'; off = '[B][COLOR red]OFF[/COLOR][/B]'
    autoclean   = 'true' if AUTOCLEANUP    == 'true' else 'false'
    cache       = 'true' if AUTOCACHE      == 'true' else 'false'
    packages    = 'true' if AUTOPACKAGES   == 'true' else 'false'
    thumbs      = 'true' if AUTOTHUMBS     == 'true' else 'false'
    maint       = 'true' if SHOWMAINT      == 'true' else 'false'
    includevid  = 'true' if INCLUDEVIDEO   == 'true' else 'false'
    includeall  = 'true' if INCLUDEALL     == 'true' else 'false'
    thirdparty  = 'true' if THIRDPARTY     == 'true' else 'false'
    errors = int(errorChecking(count=True))
    errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'
    wizlogsize = ': [COLOR red]Not Found[/COLOR]' if not os.path.exists(WIZLOG) else ": [COLOR springgreen]%s[/COLOR]" % wiz.convertSize(os.path.getsize(WIZLOG))
    if includeall == 'true':
        includeplacenta = 'true'
        includegaia = 'true'
        includemagicality = 'true'
        includeexodusredux = 'true'
        includeseren = 'true'
        include13clowns = 'true'
        includezanni = 'true'
    else:
        includeexodusredux = 'true' if INCLUDEEXODUSREDUX     == 'true' else 'false'
        includeplacenta = 'true' if INCLUDEPLACENTA == 'true' else 'false'
        includegaia = 'true' if INCLUDEGAIA   == 'true' else 'false'
        includeseren = 'true' if INCLUDESEREN   == 'true' else 'false'
        include13clowns = 'true' if INCLUDE13CLOWNS == 'true' else 'false'
        includezanni = 'true' if INCLUDEZANNI == 'true' else 'false'
        includemagicality = 'true' if INCLUDEMAGICALITY == 'true' else 'false'
    sizepack   = wiz.getSize(PACKAGES)
    sizethumb  = wiz.getSize(THUMBS)
    archive    = wiz.getSize(ARCHIVE_CACHE)
    sizecache  = (wiz.getCacheSize())-archive
    totalsize  = sizepack+sizethumb+sizecache
    feq        = ['Always', 'Daily', '3 Days', 'Weekly']
    addDir ('[B]Cleaning Tools[/B]'       ,'maint', 'clean',  icon=ICONMAINT, themeit=THEME1)
    if view == "clean" or SHOWMAINT == 'true':
        addFile('Total Clean Up: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(totalsize),    'fullclean',       icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Cache: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizecache),       'clearcache',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Packages: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizepack),     'clearpackages',   icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Thumbnails: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizethumb),  'clearthumb',      icon=ICONMAINT, themeit=THEME3)
        if os.path.exists(ARCHIVE_CACHE): addFile('Clear Archive_Cache: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(archive), 'cleararchive',    icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Old Thumbnails', 'oldThumbs',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Crash Logs',               'clearcrash',      icon=ICONMAINT, themeit=THEME3)
        addFile('Purge Databases',                'purgedb',         icon=ICONMAINT, themeit=THEME3)
        addFile('Fresh Start',                    'freshstart',      icon=ICONMAINT, themeit=THEME3)
    addDir ('[B]Addon Tools[/B]',       'maint', 'addon',  icon=ICONMAINT, themeit=THEME1)
    if view == "addon" or SHOWMAINT == 'true':
        addFile('Remove Addons',                  'removeaddons',    icon=ICONMAINT, themeit=THEME3)
        addDir ('Remove Addon Data',              'removeaddondata', icon=ICONMAINT, themeit=THEME3)
        addDir ('Enable/Disable Addons',          'enableaddons',    icon=ICONMAINT, themeit=THEME3)
        addFile('Enable/Disable Adult Addons',    'toggleadult',     icon=ICONMAINT, themeit=THEME3)
        addFile('Force Update Addons',            'forceupdate',     icon=ICONMAINT, themeit=THEME3)
        addFile('Hide Passwords On Keyboard Entry',   'hidepassword',   icon=ICONMAINT, themeit=THEME3)
        addFile('Unhide Passwords On Keyboard Entry', 'unhidepassword', icon=ICONMAINT, themeit=THEME3)
    addDir ('[B]Misc Maintenance[/B]'     ,'maint', 'misc',   icon=ICONMAINT, themeit=THEME1)
    if view == "misc" or SHOWMAINT == 'true':
        addFile('Kodi 17 Fix',                    'kodi17fix',       icon=ICONMAINT, themeit=THEME3)
        addDir ('Speed Test',                     'speedtest',       icon=ICONMAINT, themeit=THEME3)
        addFile('Enable Unknown Sources',         'unknownsources',  icon=ICONMAINT, themeit=THEME3)
        addFile('Reload Skin',                    'forceskin',       icon=ICONMAINT, themeit=THEME3)
        addFile('Reload Profile',                 'forceprofile',    icon=ICONMAINT, themeit=THEME3)
        addFile('Force Close Kodi',               'forceclose',      icon=ICONMAINT, themeit=THEME3)
        addFile('Upload Log File', 'uploadlog',       icon=ICONMAINT, themeit=THEME3)
        addFile('View Errors in Log: %s' % (errorsfound), 'viewerrorlog', icon=ICONMAINT, themeit=THEME3)
        if errors > 0: addFile('View Last Error In Log', 'viewerrorlast', icon=ICONMAINT, themeit=THEME3)
        addFile('View Log File',                  'viewlog',         icon=ICONMAINT, themeit=THEME3)
        addFile('View Wizard Log File',           'viewwizlog',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Wizard Log File%s' % wizlogsize,'clearwizlog',     icon=ICONMAINT, themeit=THEME3)
    addDir ('[B]Back up/Restore[/B]'     ,'maint', 'backup',   icon=ICONMAINT, themeit=THEME1)
    if view == "backup" or SHOWMAINT == 'true':
        addFile('Clean Up Back Up Folder',        'clearbackup',     icon=ICONMAINT,   themeit=THEME3)
        addFile('Back Up Location: [COLOR %s]%s[/COLOR]' % (COLOR2, MYBUILDS),'settings', 'Maintenance', icon=ICONMAINT, themeit=THEME3)
        #addFile('Extract a ZipFile',              'extractazip',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Build',               'backupbuild',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: GuiFix',              'backupgui',       icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Theme',               'backuptheme',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Addon Pack',          'backupaddonpack', icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Addon_data',          'backupaddon',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local Build',         'restorezip',      icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local GuiFix',        'restoregui',      icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local Addon_data',    'restoreaddon',    icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External Build',      'restoreextzip',   icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External GuiFix',     'restoreextgui',   icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External Addon_data', 'restoreextaddon', icon=ICONMAINT,   themeit=THEME3)
    addDir ('[B]System Tweaks/Fixes[/B]',       'maint', 'tweaks', icon=ICONMAINT, themeit=THEME1)
    if view == "tweaks" or SHOWMAINT == 'true':
        if not ADVANCEDFILE == 'http://' and not ADVANCEDFILE == '':
            addDir ('Advanced Settings',            'advancedsetting',  icon=ICONMAINT, themeit=THEME3)
        else:
            if os.path.exists(ADVANCED):
                addFile('View Current AdvancedSettings.xml',   'currentsettings', icon=ICONMAINT, themeit=THEME3)
                addFile('Remove Current AdvancedSettings.xml', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
            addFile('Quick Configure AdvancedSettings.xml',    'autoadvanced',    icon=ICONMAINT, themeit=THEME3)
        addFile('Scan Sources for broken links',  'checksources',    icon=ICONMAINT, themeit=THEME3)
        addFile('Scan For Broken Repositories',   'checkrepos',      icon=ICONMAINT, themeit=THEME3)
        addFile('Fix Addons Not Updating',        'fixaddonupdate',  icon=ICONMAINT, themeit=THEME3)
        addFile('Remove Non-Ascii filenames',     'asciicheck',      icon=ICONMAINT, themeit=THEME3)
        addFile('Convert Paths to special',       'convertpath',     icon=ICONMAINT, themeit=THEME3)
        addDir ('System Information',             'systeminfo',      icon=ICONMAINT, themeit=THEME3)
    addFile('Show All Maintenance: %s' % maint.replace('true',on).replace('false',off) ,'togglesetting', 'showmaint', icon=ICONMAINT, themeit=THEME2)
    addDir ('[I]<< Return to Main Menu[/I]', icon=ICONMAINT, themeit=THEME2)
    addFile('Third Party Wizards: %s' % thirdparty.replace('true',on).replace('false',off) ,'togglesetting', 'enable3rd', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
    if thirdparty == 'true':
        first = THIRD1NAME if not THIRD1NAME == '' else 'Not Set'
        secon = THIRD2NAME if not THIRD2NAME == '' else 'Not Set'
        third = THIRD3NAME if not THIRD3NAME == '' else 'Not Set'
        addFile('Edit Third Party Wizard 1: [COLOR %s]%s[/COLOR]' % (COLOR2, first), 'editthird', '1', icon=ICONMAINT, themeit=THEME3)
        addFile('Edit Third Party Wizard 2: [COLOR %s]%s[/COLOR]' % (COLOR2, secon), 'editthird', '2', icon=ICONMAINT, themeit=THEME3)
        addFile('Edit Third Party Wizard 3: [COLOR %s]%s[/COLOR]' % (COLOR2, third), 'editthird', '3', icon=ICONMAINT, themeit=THEME3)
    addFile('Auto Clean', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
    addFile('Auto Clean Up On Startup: %s' % autoclean.replace('true',on).replace('false',off) ,'togglesetting', 'autoclean',   icon=ICONMAINT, themeit=THEME3)
    if autoclean == 'true':
        addFile('--- Auto Clean Fequency: [B][COLOR springgreen]%s[/COLOR][/B]' % feq[AUTOFEQ], 'changefeq', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Clear Cache on Startup: %s' % cache.replace('true',on).replace('false',off), 'togglesetting', 'clearcache', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Clear Packages on Startup: %s' % packages.replace('true',on).replace('false',off), 'togglesetting', 'clearpackages', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Clear Old Thumbs on Startup: %s' % thumbs.replace('true',on).replace('false',off), 'togglesetting', 'clearthumbs', icon=ICONMAINT, themeit=THEME3)
    addFile('Clear Video Cache', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
    addFile('Include Video Cache in Clear Cache: %s' % includevid.replace('true',on).replace('false',off), 'togglecache', 'includevideo', icon=ICONMAINT, themeit=THEME3)
    if includevid == 'true':
        addFile('--- Include All Video Addons: %s' % includeall.replace('true',on).replace('false',off), 'togglecache', 'includeall', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.13clowns)'): addFile('--- Include 13Clowns: %s' % include13clowns.replace('true',on).replace('false',off), 'togglecache', 'include13clowns', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.exodusredux)'): addFile('--- Include Exodus Redux: %s' % includeexodusredux.replace('true',on).replace('false',off), 'togglecache', 'includeexodusredux', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.gaia)'): addFile('--- Include Gaia: %s' % includegaia.replace('true',on).replace('false',off), 'togglecache', 'includegaia', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.magicality)'): addFile('--- Include Magicality: %s' % includemagicality.replace('true',on).replace('false',off), 'togglecache', 'includemagicality', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.placenta)'): addFile('--- Include Placenta: %s' % includeplacenta.replace('true',on).replace('false',off), 'togglecache', 'includeplacenta', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.seren)'): addFile('--- Include Seren: %s' % includeseren.replace('true',on).replace('false',off), 'togglecache', 'includeseren', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.zanni)'): addFile('--- Include Zanni: %s' % includezanni.replace('true',on).replace('false',off), 'togglecache', 'includezanni', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Enable All Video Addons', 'togglecache', 'true', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Disable All Video Addons', 'togglecache', 'false', icon=ICONMAINT, themeit=THEME3)
    setView('files', 'viewType')

#########################################NET TOOLS#############################################
def net_tools(view=None):
    addDir ('Speed Tester' ,'speedtestM', icon=ICONAPK, themeit=THEME1)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addDir ('View IP Address & MAC Address',        'viewIP',    icon=ICONMAINT, themeit=THEME1)
    setView('files', 'viewType')

def viewIP():
    mac,inter_ip,ip,city,state,country,isp = wiz.net_info()
    addFile('[COLOR %s]Mac:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, mac), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Internal IP: [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, inter_ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]External IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]City:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, city), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]State:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, state), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Country:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, country), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]ISP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, isp), '', icon=ICONMAINT, themeit=THEME2)
    setView('files', 'viewType')

def speedTest():
    addFile('Run Speed Test',             'runspeedtest',      icon=ICONMAINT, themeit=THEME3)
    if os.path.exists(SPEEDTESTFOLD):
        speedimg = glob.glob(os.path.join(SPEEDTESTFOLD, '*.png'))
        speedimg.sort(key=lambda f: os.path.getmtime(f), reverse=True)
        if len(speedimg) > 0:
            addFile('Clear Results',          'clearspeedtest',    icon=ICONMAINT, themeit=THEME3)
            addFile(wiz.sep('Previous Runs'), '', icon=ICONMAINT, themeit=THEME3)
            for item in speedimg:
                created = datetime.fromtimestamp(os.path.getmtime(item)).strftime('%m/%d/%Y %H:%M:%S')
                img = item.replace(os.path.join(SPEEDTESTFOLD, ''), '')
                addFile('[B]%s[/B]: [I]Ran %s[/I]' % (img, created), 'viewspeedtest', img, icon=ICONMAINT, themeit=THEME3)

def clearSpeedTest():
    speedimg = glob.glob(os.path.join(SPEEDTESTFOLD, '*.png'))
    for file in speedimg:
        wiz.removeFile(file)

def viewSpeedTest(img=None):
    img = os.path.join(SPEEDTESTFOLD, img)
    notify.speedTest(img)

def runSpeedTest():
    try:
        found = speedtest.speedtest()
        if not os.path.exists(SPEEDTESTFOLD): os.makedirs(SPEEDTESTFOLD)
        urlsplits = found[0].split('/')
        dest = os.path.join(SPEEDTESTFOLD, urlsplits[-1])
        urllib.urlretrieve(found[0], dest)
        viewSpeedTest(urlsplits[-1])
    except:
        wiz.log("[Speed Test] Error Running Speed Test")
        pass

def advancedWindow(url=None):
    if not ADVANCEDFILE == 'http://':
        if url == None:
            TEMPADVANCEDFILE = wiz.textCache(uservar.ADVANCEDFILE)
            if TEMPADVANCEDFILE == False: ADVANCEDWORKING  = wiz.workingURL(uservar.ADVANCEDFILE)
        else:
            TEMPADVANCEDFILE = wiz.textCache(url)
            if TEMPADVANCEDFILE == False: ADVANCEDWORKING  = wiz.workingURL(url)
        addFile('Quick Configure AdvancedSettings.xml', 'autoadvanced', icon=ICONMAINT, themeit=THEME3)
        if os.path.exists(ADVANCED):
            addFile('View Current AdvancedSettings.xml', 'currentsettings', icon=ICONMAINT, themeit=THEME3)
            addFile('Remove Current AdvancedSettings.xml', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
        if not TEMPADVANCEDFILE == False:
            if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONMAINT, themeit=THEME3)
            link = TEMPADVANCEDFILE.replace('\n','').replace('\r','').replace('\t','')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                for name, section, url, icon, fanart, description in match:
                    if section.lower() == "yes":
                        addDir ("[B]%s[/B]" % name, 'advancedsetting', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    else:
                        addFile(name, 'writeadvanced', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
            else: wiz.log("[Advanced Settings] ERROR: Invalid Format.")
        else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING)
    else: wiz.log("[Advanced Settings] not Enabled")

def writeAdvanced(name, url):
    ADVANCEDWORKING = wiz.workingURL(url)
    if ADVANCEDWORKING == True:
        if os.path.exists(ADVANCED): choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to overwrite your current Advanced Settings with [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR springgreen]Overwrite[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
        else: choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to download and install [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR springgreen]Install[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")

        if choice == 1:
            file = wiz.openURL(url)
            f = open(ADVANCED, 'w');
            f.write(file)
            f.close()
            DIALOG.ok(ADDONTITLE, '[COLOR %s]AdvancedSettings.xml file has been successfully written.  Once you click okay it will force close kodi.[/COLOR]' % COLOR2)
            wiz.killxbmc(True)
        else: wiz.log("[Advanced Settings] install canceled"); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]Write Cancelled![/COLOR]" % COLOR2); return
    else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]URL Not Working[/COLOR]" % COLOR2)

def viewAdvanced():
    f = open(ADVANCED)
    a = f.read().replace('\t', '    ')
    wiz.TextBox(ADDONTITLE, a)
    f.close()

def removeAdvanced():
    if os.path.exists(ADVANCED):
        wiz.removeFile(ADVANCED)
    else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]AdvancedSettings.xml not found[/COLOR]")

def showAutoAdvanced():
    notify.autoConfig()

def getIP():
    site  = 'http://whatismyipaddress.com/'
    if not wiz.workingURL(site): return 'Unknown', 'Unknown', 'Unknown'
    page  = wiz.openURL(site).replace('\n','').replace('\r','')
    if not 'Access Denied' in page:
        ipmatch   = re.compile('whatismyipaddress.com/ip/(.+?)"').findall(page)
        ipfinal   = ipmatch[0] if (len(ipmatch) > 0) else 'Unknown'
        details   = re.compile('"font-size:14px;">(.+?)</td>').findall(page)
        provider  = details[0] if (len(details) > 0) else 'Unknown'
        location  = details[1]+', '+details[2]+', '+details[3] if (len(details) > 2) else 'Unknown'
        return ipfinal, provider, location
    else: return 'Unknown', 'Unknown', 'Unknown'

def systemInfo():
    infoLabel = ['System.FriendlyName',
                 'System.BuildVersion',
                 'System.CpuUsage',
                 'System.ScreenMode',
                 'Network.IPAddress',
                 'Network.MacAddress',
                 'System.Uptime',
                 'System.TotalUptime',
                 'System.FreeSpace',
                 'System.UsedSpace',
                 'System.TotalSpace',
                 'System.Memory(free)',
                 'System.Memory(used)',
                 'System.Memory(total)']
    data      = []; x = 0
    for info in infoLabel:
        temp = wiz.getInfo(info)
        y = 0
        while temp == "Busy" and y < 10:
            temp = wiz.getInfo(info); y += 1; wiz.log("%s sleep %s" % (info, str(y))); xbmc.sleep(200)
        data.append(temp)
        x += 1
    storage_free  = data[8] if 'Una' in data[8] else wiz.convertSize(int(float(data[8][:-8]))*1024*1024)
    storage_used  = data[9] if 'Una' in data[9] else wiz.convertSize(int(float(data[9][:-8]))*1024*1024)
    storage_total = data[10] if 'Una' in data[10] else wiz.convertSize(int(float(data[10][:-8]))*1024*1024)
    ram_free      = wiz.convertSize(int(float(data[11][:-2]))*1024*1024)
    ram_used      = wiz.convertSize(int(float(data[12][:-2]))*1024*1024)
    ram_total     = wiz.convertSize(int(float(data[13][:-2]))*1024*1024)

    picture = []; music = []; video = []; programs = []; repos = []; scripts = []; skins = []

    fold = glob.glob(os.path.join(ADDONS, '*/'))
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername == 'packages': continue
        xml = os.path.join(folder, 'addon.xml')
        if os.path.exists(xml):
            f      = open(xml)
            a      = f.read()
            prov   = re.compile("<provides>(.+?)</provides>").findall(a)
            if len(prov) == 0:
                if foldername.startswith('skin'): skins.append(foldername)
                elif foldername.startswith('repo'): repos.append(foldername)
                else: scripts.append(foldername)
            elif not (prov[0]).find('executable') == -1: programs.append(foldername)
            elif not (prov[0]).find('video') == -1: video.append(foldername)
            elif not (prov[0]).find('audio') == -1: music.append(foldername)
            elif not (prov[0]).find('image') == -1: picture.append(foldername)

    addFile('[B]Media Center Info:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Name:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[0]), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]Version:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[1]), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]Platform:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, wiz.platform().title()), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]CPU Usage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[2]), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]Screen Mode:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[3]), '', icon=ICONMAINT, themeit=THEME3)

    addFile('[B]Uptime:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Current Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[6]), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Total Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[7]), '', icon=ICONMAINT, themeit=THEME2)

    addFile('[B]Local Storage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Used Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_used), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Free Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_free), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Total Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_total), '', icon=ICONMAINT, themeit=THEME2)

    addFile('[B]Ram Usage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Used Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_free), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Free Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_used), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Total Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_total), '', icon=ICONMAINT, themeit=THEME2)

    addFile('[B]Network:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    mac,inter_ip,ip,city,state,country,isp = wiz.net_info()
    addFile('[COLOR %s]Mac:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, mac), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Internal IP: [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, inter_ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]External IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]City:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, city), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]State:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, state), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Country:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, country), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]ISP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, isp), '', icon=ICONMAINT, themeit=THEME2)

    totalcount = len(picture) + len(music) + len(video) + len(programs) + len(scripts) + len(skins) + len(repos)
    addFile('[B]Addons([COLOR %s]%s[/COLOR]):[/B]' % (COLOR1, totalcount), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Video Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(video))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Program Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(programs))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Music Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(music))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Picture Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(picture))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(repos))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Skins:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(skins))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Scripts/Modules:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(scripts))), '', icon=ICONMAINT, themeit=THEME2)

def saveMenu():
    on = '[COLOR springgreen]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
    trakt      = 'true' if KEEPTRAKT     == 'true' else 'false'
    real       = 'true' if KEEPREAL      == 'true' else 'false'
    login      = 'true' if KEEPLOGIN     == 'true' else 'false'
    sources    = 'true' if KEEPSOURCES   == 'true' else 'false'
    advanced   = 'true' if KEEPADVANCED  == 'true' else 'false'
    profiles   = 'true' if KEEPPROFILES  == 'true' else 'false'
    favourites = 'true' if KEEPFAVS      == 'true' else 'false'
    repos      = 'true' if KEEPREPOS     == 'true' else 'false'
    super      = 'true' if KEEPSUPER     == 'true' else 'false'
    whitelist  = 'true' if KEEPWHITELIST == 'true' else 'false'

    addDir ('Keep Trakt Data',               'trakt',                icon=ICONTRAKT, themeit=THEME1)
    addDir ('Keep Debrid',              'realdebrid',           icon=ICONREAL,  themeit=THEME1)
    addDir ('Keep Login Info',               'login',                icon=ICONLOGIN, themeit=THEME1)
    addFile('Import Save Data',              'managedata', 'import', icon=ICONSAVE,  themeit=THEME1)
    addFile('Export Save Data',              'managedata', 'export', icon=ICONSAVE,  themeit=THEME1)
    addFile('- Click to toggle settings -', '', themeit=THEME3)
    addFile('Save Trakt: %s' % trakt.replace('true',on).replace('false',off)                       ,'togglesetting', 'keeptrakt',      icon=ICONTRAKT, themeit=THEME1)
    addFile('Save Debrid: %s' % real.replace('true',on).replace('false',off)                  ,'togglesetting', 'keepdebrid',     icon=ICONREAL,  themeit=THEME1)
    addFile('Save Login Info: %s' % login.replace('true',on).replace('false',off)                  ,'togglesetting', 'keeplogin',      icon=ICONLOGIN, themeit=THEME1)
    addFile('Keep \'Sources.xml\': %s' % sources.replace('true',on).replace('false',off)           ,'togglesetting', 'keepsources',    icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep \'Profiles.xml\': %s' % profiles.replace('true',on).replace('false',off)         ,'togglesetting', 'keepprofiles',   icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep \'Advancedsettings.xml\': %s' % advanced.replace('true',on).replace('false',off) ,'togglesetting', 'keepadvanced',   icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep \'Favourites.xml\': %s' % favourites.replace('true',on).replace('false',off)     ,'togglesetting', 'keepfavourites', icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep Super Favourites: %s' % super.replace('true',on).replace('false',off)            ,'togglesetting', 'keepsuper',      icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep Installed Repo\'s: %s' % repos.replace('true',on).replace('false',off)           ,'togglesetting', 'keeprepos',      icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep My \'WhiteList\': %s' % whitelist.replace('true',on).replace('false',off)        ,'togglesetting', 'keepwhitelist',  icon=ICONSAVE,  themeit=THEME1)
    if whitelist == 'true':
        addFile('Edit My Whitelist',        'whitelist', 'edit',   icon=ICONSAVE,  themeit=THEME1)
        addFile('View My Whitelist',        'whitelist', 'view',   icon=ICONSAVE,  themeit=THEME1)
        addFile('Clear My Whitelist',       'whitelist', 'clear',  icon=ICONSAVE,  themeit=THEME1)
        addFile('Import My Whitelist',      'whitelist', 'import', icon=ICONSAVE,  themeit=THEME1)
        addFile('Export My Whitelist',      'whitelist', 'export', icon=ICONSAVE,  themeit=THEME1)
    setView('files', 'viewType')

def traktMenu():
    trakt = '[COLOR springgreen]ON[/COLOR]' if KEEPTRAKT == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(TRAKTSAVE) if not TRAKTSAVE == '' else 'Trakt hasnt been saved yet.'
    addFile('[I]Register FREE Account at http://trakt.tv[/I]', '', icon=ICONTRAKT, themeit=THEME3)
    addFile('Save Trakt Data: %s' % trakt, 'togglesetting', 'keeptrakt', icon=ICONTRAKT, themeit=THEME3)
    if KEEPTRAKT == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONTRAKT, themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONTRAKT, themeit=THEME3)

    for trakt in traktit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % TRAKTID[trakt]['plugin']):
            name   = TRAKTID[trakt]['name']
            path   = TRAKTID[trakt]['path']
            saved  = TRAKTID[trakt]['saved']
            file   = TRAKTID[trakt]['file']
            user   = wiz.getS(saved)
            auser  = traktit.traktUser(trakt)
            icon   = TRAKTID[trakt]['icon']   if os.path.exists(path) else ICONTRAKT
            fanart = TRAKTID[trakt]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Trakt', trakt)
            menu2 = createMenu('save', 'Trakt', trakt)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=trakt)' %   (ADDON_ID, trakt)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importtrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savetrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Trakt Data',          'savetrakt',    'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Recover All Saved Trakt Data', 'restoretrakt', 'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Import Trakt Data',            'importtrakt',  'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Clear All Addon Trakt Data',         'addontrakt',   'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Clear All Saved Trakt Data',   'cleartrakt',   'all', icon=ICONTRAKT,  themeit=THEME3)
    setView('files', 'viewType')

def realMenu():
    real = '[COLOR springgreen]ON[/COLOR]' if KEEPREAL == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(REALSAVE) if not REALSAVE == '' else 'Real Debrid hasnt been saved yet.'
    addFile('[I]http://real-debrid.com is a PAID service.[/I]', '', icon=ICONREAL, themeit=THEME3)
    addFile('Save Real Debrid Data: %s' % real, 'togglesetting', 'keepdebrid', icon=ICONREAL, themeit=THEME3)
    if KEEPREAL == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONREAL, themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONREAL, themeit=THEME3)

    for debrid in debridit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % DEBRIDID[debrid]['plugin']):
            name   = DEBRIDID[debrid]['name']
            path   = DEBRIDID[debrid]['path']
            saved  = DEBRIDID[debrid]['saved']
            file   = DEBRIDID[debrid]['file']
            user   = wiz.getS(saved)
            auser  = debridit.debridUser(debrid)
            icon   = DEBRIDID[debrid]['icon']   if os.path.exists(path) else ICONREAL
            fanart = DEBRIDID[debrid]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Debrid', debrid)
            menu2 = createMenu('save', 'Debrid', debrid)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=debrid)' %   (ADDON_ID, debrid)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importdebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savedebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Debrid Data',          'savedebrid',    'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Recover All Saved Debrid Data', 'restoredebrid', 'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Import Debrid Data',            'importdebrid',  'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Clear All Addon Debrid Data',               'addondebrid',   'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Clear All Saved Debrid Data',   'cleardebrid',   'all', icon=ICONREAL,  themeit=THEME3)
    setView('files', 'viewType')

def loginMenu():
    login = '[COLOR springgreen]ON[/COLOR]' if KEEPLOGIN == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(LOGINSAVE) if not LOGINSAVE == '' else 'Login data hasnt been saved yet.'
    addFile('[I]Several of these addons are PAID services.[/I]', '', icon=ICONLOGIN, themeit=THEME3)
    addFile('Save API Keys: %s' % login, 'togglesetting', 'keeplogin', icon=ICONLOGIN, themeit=THEME3)
    if KEEPLOGIN == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONLOGIN, themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONLOGIN, themeit=THEME3)

    for login in loginit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % LOGINID[login]['plugin']):
            name   = LOGINID[login]['name']
            path   = LOGINID[login]['path']
            saved  = LOGINID[login]['saved']
            file   = LOGINID[login]['file']
            user   = wiz.getS(saved)
            auser  = loginit.loginUser(login)
            icon   = LOGINID[login]['icon']   if os.path.exists(path) else ICONLOGIN
            fanart = LOGINID[login]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Login', login)
            menu2 = createMenu('save', 'Login', login)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=login)' %   (ADDON_ID, login)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authlogin', login, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authlogin', login, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importlogin', login, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savelogin', login, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Login Info',          'savelogin',    'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Recover All Saved Login Info', 'restorelogin', 'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Import Login Info',            'importlogin',  'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Clear All Addon Login Info',         'addonlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Clear All Saved Login Info',   'clearlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
    setView('files', 'viewType')

def fixUpdate():
    if KODIV < 17:
        dbfile = os.path.join(DATABASE, wiz.latestDB('Addons'))
        try:
            os.remove(dbfile)
        except Exception, e:
            wiz.log("Unable to remove %s, Purging DB" % dbfile)
            wiz.purgeDb(dbfile)
    else:
        if os.path.exists(os.path.join(USERDATA, 'autoexec.py')):
            temp = os.path.join(USERDATA, 'autoexec_temp.py')
            if os.path.exists(temp): xbmcvfs.delete(temp)
            xbmcvfs.rename(os.path.join(USERDATA, 'autoexec.py'), temp)
        xbmcvfs.copy(os.path.join(PLUGIN, 'resources', 'libs', 'autoexec.py'), os.path.join(USERDATA, 'autoexec.py'))
        dbfile = os.path.join(DATABASE, wiz.latestDB('Addons'))
        try:
            os.remove(dbfile)
        except Exception, e:
            wiz.log("Unable to remove %s, Purging DB" % dbfile)
            wiz.purgeDb(dbfile)
        wiz.killxbmc(True)

def removeAddonMenu():
    fold = glob.glob(os.path.join(ADDONS, '*/'))
    addonnames = []; addonids = []
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername in EXCLUDES: continue
        elif foldername in DEFAULTPLUGINS: continue
        elif foldername == 'packages': continue
        xml = os.path.join(folder, 'addon.xml')
        if os.path.exists(xml):
            f      = open(xml)
            a      = f.read()
            match  = wiz.parseDOM(a, 'addon', ret='id')

            addid  = foldername if len(match) == 0 else match[0]
            try:
                add = xbmcaddon.Addon(id=addid)
                addonnames.append(add.getAddonInfo('name'))
                addonids.append(addid)
            except:
                pass
    if len(addonnames) == 0:
        wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Addons To Remove[/COLOR]" % COLOR2)
        return
    if KODIV > 16:
        selected = DIALOG.multiselect("%s: Select the addons you wish to remove." % ADDONTITLE, addonnames)
    else:
        selected = []; choice = 0
        tempaddonnames = ["-- Click here to Continue --"] + addonnames
        while not choice == -1:
            choice = DIALOG.select("%s: Select the addons you wish to remove." % ADDONTITLE, tempaddonnames)
            if choice == -1: break
            elif choice == 0: break
            else:
                choice2 = (choice-1)
                if choice2 in selected:
                    selected.remove(choice2)
                    tempaddonnames[choice] = addonnames[choice2]
                else:
                    selected.append(choice2)
                    tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
    if selected == None: return
    if len(selected) > 0:
        wiz.addonUpdates('set')
        for addon in selected:
            removeAddon(addonids[addon], addonnames[addon], True)

        xbmc.sleep(500)

        if INSTALLMETHOD == 1: todo = 1
        elif INSTALLMETHOD == 2: todo = 0
        else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR red]Force Close[/COLOR][/B]")
        if todo == 1: wiz.reloadFix('remove addon')
        else: wiz.addonUpdates('reset'); wiz.killxbmc(True)

def removeAddonDataMenu():
    if os.path.exists(ADDOND):
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data', 'removedata', 'all', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data for Uninstalled Addons', 'removedata', 'uninstalled', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Empty Folders in Addon_Data', 'removedata', 'empty', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] %s Addon_Data' % ADDONTITLE, 'resetaddon', themeit=THEME2)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        fold = glob.glob(os.path.join(ADDOND, '*/'))
        for folder in sorted(fold, key = lambda x: x):
            foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
            icon = os.path.join(folder.replace(ADDOND, ADDONS), 'icon.png')
            fanart = os.path.join(folder.replace(ADDOND, ADDONS), 'fanart.png')
            folderdisplay = foldername
            replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR springgreen][SCRIPT] [/COLOR]', 'service.':'[COLOR springgreen][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
            for rep in replace:
                folderdisplay = folderdisplay.replace(rep, replace[rep])
            if foldername in EXCLUDES: folderdisplay = '[COLOR springgreen][B][PROTECTED][/B][/COLOR] %s' % folderdisplay
            else: folderdisplay = '[COLOR red][B][REMOVE][/B][/COLOR] %s' % folderdisplay
            addFile(' %s' % folderdisplay, 'removedata', foldername, icon=icon, fanart=fanart, themeit=THEME2)
    else:
        addFile('No Addon data folder found.', '', themeit=THEME3)
    setView('files', 'viewType')

def enableAddons():
    addFile("[I][B][COLOR red]!!Notice: Disabling Some Addons Can Cause Issues!![/COLOR][/B][/I]", '', icon=ICONMAINT)
    fold = glob.glob(os.path.join(ADDONS, '*/'))
    x = 0
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername in EXCLUDES: continue
        if foldername in DEFAULTPLUGINS: continue
        addonxml = os.path.join(folder, 'addon.xml')
        if os.path.exists(addonxml):
            x += 1
            fold   = folder.replace(ADDONS, '')[1:-1]
            f      = open(addonxml)
            a      = f.read().replace('\n','').replace('\r','').replace('\t','')
            match  = wiz.parseDOM(a, 'addon', ret='id')
            match2 = wiz.parseDOM(a, 'addon', ret='name')
            try:
                pluginid = match[0]
                name = match2[0]
            except:
                continue
            try:
                add    = xbmcaddon.Addon(id=pluginid)
                state  = "[COLOR springgreen][Enabled][/COLOR]"
                goto   = "false"
            except:
                state  = "[COLOR red][Disabled][/COLOR]"
                goto   = "true"
                pass
            icon   = os.path.join(folder, 'icon.png') if os.path.exists(os.path.join(folder, 'icon.png')) else ICON
            fanart = os.path.join(folder, 'fanart.jpg') if os.path.exists(os.path.join(folder, 'fanart.jpg')) else FANART
            addFile("%s %s" % (state, name), 'toggleaddon', fold, goto, icon=icon, fanart=fanart)
            f.close()
    if x == 0:
        addFile("No Addons Found to Enable or Disable.", '', icon=ICONMAINT)
    setView('files', 'viewType')

def changeFeq():
    feq        = ['Every Startup', 'Every Day', 'Every Three Days', 'Every Weekly']
    change     = DIALOG.select("[COLOR %s]How often would you list to Auto Clean on Startup?[/COLOR]" % COLOR2, feq)
    if not change == -1:
        wiz.setS('autocleanfeq', str(change))
        wiz.LogNotify('[COLOR %s]Auto Clean Up[/COLOR]' % COLOR1, '[COLOR %s]Fequency Now %s[/COLOR]' % (COLOR2, feq[change]))

def developer():
    # addFile('Convert Text Files to 0.1.7',         'converttext',           themeit=THEME1)
    addFile('Create QR Code',                      'createqr',              themeit=THEME1)
    addFile('Test Notifications',                  'testnotify',            themeit=THEME1)
    addFile('Test Update',                         'testupdate',            themeit=THEME1)
    addFile('Test First Run',                      'testfirst',             themeit=THEME1)
    addFile('Test First Run Settings',             'testfirstrun',          themeit=THEME1)
    setView('files', 'viewType')

###########################
###### Build Install ######
###########################
def buildWizard(name, type, theme=None, over=False):
    if over == False:
        testbuild = wiz.checkBuild(name, 'url')
        if testbuild == False:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Unabled to find build[/COLOR]" % COLOR2)
            return
        testworking = wiz.workingURL(testbuild)
        if testworking == False:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Build Zip Error: %s[/COLOR]" % (COLOR2, testworking))
            return
    if type == 'gui':
        if name == BUILDNAME:
            if over == True: yes = 1
            else: yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to apply the guifix for:' % COLOR2, '[COLOR %s]%s[/COLOR]?[/COLOR]' % (COLOR1, name), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Apply Fix[/COLOR][/B]')
        else:
            yes = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, "[COLOR %s][COLOR %s]%s[/COLOR] community build is not currently installed." % (COLOR2, COLOR1, name), "Would you like to apply the guiFix anyways?.[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Apply Fix[/COLOR][/B]')
        if yes:
            buildzip = wiz.checkBuild(name,'gui')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Invalid Zip Url![/COLOR]' % COLOR2); return
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading GuiFix:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s_guisettings.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(buildzip, lib, DP)
            xbmc.sleep(500)
            title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
            DP.update(0, title,'', 'Please Wait')
            extract.all(lib,USERDATA,DP, title=title)
            DP.close()
            wiz.defaultSkin()
            wiz.lookandFeelData('save')
            if KODIV >= 17:
                installed = grabAddons(lib)
                wiz.addonDatabase(installed, 1, True)
            if INSTALLMETHOD == 1: todo = 1
            elif INSTALLMETHOD == 2: todo = 0
            else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Gui fix has been installed.  Would you like to Reload the profile or Force Close Kodi?[/COLOR]" % COLOR2, yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
            if todo == 1: wiz.reloadFix()
            else: DIALOG.ok(ADDONTITLE, "[COLOR %s]To save changes you now need to force close Kodi, Press OK to force close Kodi[/COLOR]" % COLOR2); wiz.killxbmc('true')
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Cancelled![/COLOR]' % COLOR2)
    elif type == 'fresh':
        freshStart(name)
    elif type == 'normal':
        if url == 'normal':
            if KEEPTRAKT == 'true':
                traktit.autoUpdate('all')
                wiz.setS('traktlastsave', str(THREEDAYS))
            if KEEPREAL == 'true':
                debridit.autoUpdate('all')
                wiz.setS('debridlastsave', str(THREEDAYS))
            if KEEPLOGIN == 'true':
                loginit.autoUpdate('all')
                wiz.setS('loginlastsave', str(THREEDAYS))
        temp_kodiv = int(KODIV); buildv = int(float(wiz.checkBuild(name, 'kodi')))
        if not temp_kodiv == buildv:
            if temp_kodiv == 16 and buildv <= 15: warning = False
            else: warning = True
        else: warning = False
        if warning == True:
            yes_pressed = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, '[COLOR %s]There is a chance that the skin will not appear correctly' % COLOR2, 'When installing a %s build on a Kodi %s install' % (wiz.checkBuild(name, 'kodi'), KODIV), 'Would you still like to install: [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Yes, Install[/COLOR][/B]')
        else:
            if not over == False: yes_pressed = 1
            else: yes_pressed = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to Download and Install:' % COLOR2, '[COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Yes, Install[/COLOR][/B]')
        if yes_pressed:
            wiz.clearS('build')
            buildzip = wiz.checkBuild(name, 'url')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Build Install: Invalid Zip Url![/COLOR]' % COLOR2); return
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(buildzip, lib, DP)
            xbmc.sleep(500)
            title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version'))
            DP.update(0, title,'', 'Please Wait')
            percent, errors, error = extract.all(lib,HOME,DP, title=title)
            if int(float(percent)) > 0:
                wiz.fixmetas()
                wiz.lookandFeelData('save')
                wiz.defaultSkin()
                #wiz.addonUpdates('set')
                wiz.setS('buildname', name)
                wiz.setS('buildversion', wiz.checkBuild( name,'version'))
                wiz.setS('buildtheme', '')
                wiz.setS('latestversion', wiz.checkBuild( name,'version'))
                wiz.setS('lastbuildcheck', str(NEXTCHECK))
                wiz.setS('installed', 'true')
                wiz.setS('extract', str(percent))
                wiz.setS('errors', str(errors))
                wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
                try: os.remove(lib)
                except: pass
                if int(float(errors)) > 0:
                    yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B][COLOR red]No Thanks[/COLOR][/B]', yeslabel='[B][COLOR springgreen]View Errors[/COLOR][/B]')
                    if yes:
                        if isinstance(errors, unicode):
                            error = error.encode('utf-8')
                        wiz.TextBox(ADDONTITLE, error)
                DP.close()
                themefile = wiz.themeCount(name)
                if not themefile == False:
                    buildWizard(name, 'theme')
                if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
                if INSTALLMETHOD == 1: todo = 1
                elif INSTALLMETHOD == 2: todo = 0
                else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
                if todo == 1: wiz.reloadFix()
                else: wiz.killxbmc(True)
            else:
                if isinstance(errors, unicode):
                    error = error.encode('utf-8')
                wiz.TextBox("%s: Error Installing Build" % ADDONTITLE, error)
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Build Install: Cancelled![/COLOR]' % COLOR2)
    elif type == 'theme':
        if theme == None:
            themefile = wiz.checkBuild(name, 'theme')
            themelist = []
            if not themefile == 'http://' and wiz.workingURL(themefile) == True:
                themelist = wiz.themeCount(name, False)
                if len(themelist) > 0:
                    if DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Build [COLOR %s]%s[/COLOR] comes with [COLOR %s]%s[/COLOR] different themes" % (COLOR2, COLOR1, name, COLOR1, len(themelist)), "Would you like to install one now?[/COLOR]", yeslabel="[B][COLOR springgreen]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]"):
                        wiz.log("Theme List: %s " % str(themelist))
                        ret = DIALOG.select(ADDONTITLE, themelist)
                        wiz.log("Theme install selected: %s" % ret)
                        if not ret == -1: theme = themelist[ret]; installtheme = True
                        else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
                    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
            else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: None Found![/COLOR]' % COLOR2)
        else: installtheme = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to install the theme:' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, theme), 'for [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), yeslabel="[B][COLOR springgreen]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]")
        if installtheme:
            themezip = wiz.checkTheme(name, theme, 'url')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(themezip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Invalid Zip Url![/COLOR]' % COLOR2); return False
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(themezip, lib, DP)
            xbmc.sleep(500)
            DP.update(0,"", "Installing %s " % name)
            test = False
            if url not in ["fresh", "normal"]:
                test = testTheme(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
                test2 = testGui(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
                if test == True:
                    wiz.lookandFeelData('save')
                    swap = wiz.skinToDefault('Theme Install')
                    if swap == False: return False
                    xbmc.sleep(500)
            title = '[COLOR %s][B]Installing Theme:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme)
            DP.update(0, title,'', 'Please Wait')
            percent, errors, error = extract.all(lib,HOME,DP, title=title)
            wiz.setS('buildtheme', theme)
            wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
            DP.close()
            if url not in ["fresh", "normal"]:
                wiz.forceUpdate()
                if KODIV >= 17:
                    installed = grabAddons(lib)
                    wiz.addonDatabase(installed, 1, True)
                if test2 == True:
                    wiz.lookandFeelData('save')
                    wiz.defaultSkin()
                    gotoskin = wiz.getS('defaultskin')
                    wiz.swapSkins(gotoskin, "Theme Installer")
                    wiz.lookandFeelData('restore')
                elif test == True:
                    wiz.lookandFeelData('save')
                    wiz.defaultSkin()
                    gotoskin = wiz.getS('defaultskin')
                    wiz.swapSkins(gotoskin, "Theme Installer")
                    wiz.lookandFeelData('restore')
                else:
                    wiz.ebi("ReloadSkin()")
                    xbmc.sleep(1000)
                    wiz.ebi("Container.Refresh")
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2)

def thirdPartyInstall(name, url):
    if not wiz.workingURL(url):
        LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Invalid URL for Build[/COLOR]' % COLOR2); return
    type = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to preform a [COLOR %s]Fresh Install[/COLOR] or [COLOR %s]Normal Install[/COLOR] for:[/COLOR]" % (COLOR2, COLOR1, COLOR1), "[COLOR %s]%s[/COLOR]" % (COLOR1, name), yeslabel="[B][COLOR springgreen]Fresh Install[/COLOR][/B]", nolabel="[B][COLOR red]Normal Install[/COLOR][/B]")
    if type == 1:
        freshStart('third', True)
    wiz.clearS('build')
    zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name),'', 'Please Wait')
    lib=os.path.join(PACKAGES, '%s.zip' % zipname)
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    xbmc.sleep(500)
    title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
    DP.update(0, title,'', 'Please Wait')
    percent, errors, error = extract.all(lib,HOME,DP, title=title)
    if int(float(percent)) > 0:
        wiz.fixmetas()
        wiz.lookandFeelData('save')
        wiz.defaultSkin()
        #wiz.addonUpdates('set')
        wiz.setS('installed', 'true')
        wiz.setS('extract', str(percent))
        wiz.setS('errors', str(errors))
        wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
        try: os.remove(lib)
        except: pass
        if int(float(errors)) > 0:
            yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B][COLOR red]No Thanks[/COLOR][/B]',yeslabel='[B][COLOR springgreen]View Errors[/COLOR][/B]')
            if yes:
                if isinstance(errors, unicode):
                    error = error.encode('utf-8')
                wiz.TextBox(ADDONTITLE, error)
    DP.close()
    if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
    if INSTALLMETHOD == 1: todo = 1
    elif INSTALLMETHOD == 2: todo = 0
    else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR red]Force Close[/COLOR][/B]")
    if todo == 1: wiz.reloadFix()
    else: wiz.killxbmc(True)

def testTheme(path):
    zfile = zipfile.ZipFile(path)
    for item in zfile.infolist():
        wiz.log(str(item.filename))
        if '/settings.xml' in item.filename:
            return True
    return False

def testGui(path):
    zfile = zipfile.ZipFile(path)
    for item in zfile.infolist():
        if '/guisettings.xml' in item.filename:
            return True
    return False

def grabAddons(path):
    zfile = zipfile.ZipFile(path)
    addonlist = []
    for item in zfile.infolist():
        if str(item.filename).find('addon.xml') == -1: continue
        info = str(item.filename).split('/')
        if not info[-2] in addonlist:
            addonlist.append(info[-2])
    return addonlist

def apkInstaller(apk, url):
    wiz.log(apk)
    wiz.log(url)
    if wiz.platform() == 'android':
        yes = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to download and install:" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, apk), yeslabel="[B][COLOR springgreen]Download[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
        if not yes: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Install Cancelled[/COLOR]' % COLOR2); return
        display = apk
        if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
        if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]APK Installer: Invalid Apk Url![/COLOR]' % COLOR2); return
        DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, display),'', 'Please Wait')
        lib=os.path.join(PACKAGES, "%s.apk" % apk.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', ''))
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, DP)
        xbmc.sleep(100)
        DP.close()
        notify.apkInstaller(apk)
        wiz.ebi('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+lib+'")')
    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: None Android Device[/COLOR]' % COLOR2)

def romInstaller(name, url):
    myroms = xbmc.translatePath(BACKUPROMS)
    if myroms == '':
        if DIALOG.yesno(ADDONTITLE, "[COLOR %s]It seems that you do not have an extract location setup for Rom Packs" % COLOR2, "Would you like to set one?[/COLOR]", yeslabel="[COLOR springgreen][B]Set Location[/B][/COLOR]", nolabel="[COLOR red][B]Cancel Download[/B][/COLOR]"):
            wiz.openS()
            myroms = wiz.getS('rompath')
            if myroms == '': return
    yes = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Are you sure you would like to download and extract [COLOR %s]%s[/COLOR] to:" % (COLOR2, COLOR1, name), "[COLOR %s]%s[/COLOR]" % (COLOR1, myroms), yeslabel="[B][COLOR springgreen]Download[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
    if not yes: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Install Cancelled[/COLOR]' % COLOR2); return
    display = name
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]APK Installer: Invalid Rom Url![/COLOR]' % COLOR2); return
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, display),'', 'Please Wait')
    lib=os.path.join(PACKAGES, "%s.zip" % name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', ''))
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    xbmc.sleep(100)
    percent, errors, error = extract.all(lib,myroms,DP, title=display)
    try: os.remove(lib)
    except: pass
    wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Rom Pack Installed[/COLOR]' % COLOR2)
    DP.close()

###########################
###### Misc Functions######
###########################

def createMenu(type, add, name):
    if   type == 'saveaddon':
        menu_items=[]
        add2  = urllib.quote_plus(add.lower().replace(' ', ''))
        add3  = add.replace('Debrid', 'Real Debrid')
        name2 = urllib.quote_plus(name.lower().replace(' ', ''))
        name = name.replace('url', 'URL Resolver')
        menu_items.append((THEME2 % name.title(),             ' '))
        menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Clear %s Data' % add3,              'RunPlugin(plugin://%s/?mode=clear%s&name=%s)' %   (ADDON_ID, add2, name2)))
    elif type == 'save'    :
        menu_items=[]
        add2  = urllib.quote_plus(add.lower().replace(' ', ''))
        add3  = add.replace('Debrid', 'Real Debrid')
        name2 = urllib.quote_plus(name.lower().replace(' ', ''))
        name = name.replace('url', 'URL Resolver')
        menu_items.append((THEME2 % name.title(),             ' '))
        menu_items.append((THEME3 % 'Register %s' % add3,                'RunPlugin(plugin://%s/?mode=auth%s&name=%s)' %    (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Import %s Data' % add3,             'RunPlugin(plugin://%s/?mode=import%s&name=%s)' %  (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Clear Addon %s Data' % add3,        'RunPlugin(plugin://%s/?mode=addon%s&name=%s)' %   (ADDON_ID, add2, name2)))
    elif type == 'install'  :
        menu_items=[]
        name2 = urllib.quote_plus(name)
        menu_items.append((THEME2 % name,                                'RunAddon(%s, ?mode=viewbuild&name=%s)'  % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Fresh Install',                     'RunPlugin(plugin://%s/?mode=install&name=%s&url=fresh)'  % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Normal Install',                    'RunPlugin(plugin://%s/?mode=install&name=%s&url=normal)' % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Apply guiFix',                      'RunPlugin(plugin://%s/?mode=install&name=%s&url=gui)'    % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Build Information',                 'RunPlugin(plugin://%s/?mode=buildinfo&name=%s)'  % (ADDON_ID, name2)))
    menu_items.append((THEME2 % '%s Settings' % ADDONTITLE,              'RunPlugin(plugin://%s/?mode=settings)' % ADDON_ID))
    return menu_items

def toggleCache(state):
    cachelist = ['includevideo', 'includeall', 'include13clowns', 'includeexodusredux', 'includegaia', 'includemagicality', 'includeplacenta', 'includeseren', 'includezanni' ]
    titlelist = ['Include Video Addons', 'Include All Addons', 'Include 13Clowns', 'Include Exodus Redux', 'Include Gaia', 'Include Magicality', 'Include Placenta', 'Include Seren', 'Include Zanni']
    if state in ['true', 'false']:
        for item in cachelist:
            wiz.setS(item, state)
    else:
        if not state in ['includevideo', 'includeall'] and wiz.getS('includeall') == 'true':
            try:
                item = titlelist[cachelist.index(state)]
                DIALOG.ok(ADDONTITLE, "[COLOR %s]You will need to turn off [COLOR %s]Include All Addons[/COLOR] to disable[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, COLOR1, item))
            except:
                wiz.LogNotify("[COLOR %s]Toggle Cache[/COLOR]" % COLOR1, "[COLOR %s]Invalid id: %s[/COLOR]" % (COLOR2, state))
        else:
            new = 'true' if wiz.getS(state) == 'false' else 'false'
            wiz.setS(state, new)

def playVideo(url):
    if 'watch?v=' in url:
        a, b = url.split('?')
        find = b.split('&')
        for item in find:
            if item.startswith('v='):
                url = item[2:]
                break
            else: continue
    elif 'embed' in url or 'youtu.be' in url:
        a = url.split('/')
        if len(a[-1]) > 5:
            url = a[-1]
        elif len(a[-2]) > 5:
            url = a[-2]
    wiz.log("YouTube URL: %s" % url)
    if wiz.getCond('System.HasAddon(plugin.video.youtube)') == 1:
        url = 'plugin://plugin.video.youtube/play/?video_id=%s' % url
        xbmc.Player().play(url)
    xbmc.sleep(2000)
    if xbmc.Player().isPlayingVideo() == 0:
        yt.PlayVideo(url)

def viewLogFile():
    mainlog = wiz.Grab_Log(True)
    oldlog  = wiz.Grab_Log(True, True)
    which = 0; logtype = mainlog
    if not oldlog == False and not mainlog == False:
        which = DIALOG.select(ADDONTITLE, ["View %s" % mainlog.replace(LOG, ""), "View %s" % oldlog.replace(LOG, "")])
        if which == -1: wiz.LogNotify('[COLOR %s]View Log[/COLOR]' % COLOR1, '[COLOR %s]View Log Cancelled![/COLOR]' % COLOR2); return
    elif mainlog == False and oldlog == False:
        wiz.LogNotify('[COLOR %s]View Log[/COLOR]' % COLOR1, '[COLOR %s]No Log File Found![/COLOR]' % COLOR2)
        return
    elif not mainlog == False: which = 0
    elif not oldlog == False: which = 1

    logtype = mainlog if which == 0 else oldlog
    msg     = wiz.Grab_Log(False) if which == 0 else wiz.Grab_Log(False, True)

    wiz.TextBox("%s - %s" % (ADDONTITLE, logtype), msg)

def errorList(file):
    errors = []
    a=open(file).read()
    b=a.replace('\n','[CR]').replace('\r','')
    match = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(b)
    for item in match:
        errors.append(item)
    return errors

def errorChecking(log=None, count=None, last=None):
    errors = []; error1 = []; error2 = [];
    if log == None:
        curr = wiz.Grab_Log(True, False)
        old = wiz.Grab_Log(True, True)
        if old == False and curr == False:
            if count == None:
                wiz.LogNotify('[COLOR %s]View Error Log[/COLOR]' % COLOR1, '[COLOR %s]No Log File Found![/COLOR]' % COLOR2)
                return
            else:
                return 0
        if not curr == False:
            error1 = errorList(curr)
        if not old == False:
            error2 = errorList(old)
        if len(error2) > 0:
            for item in error2: errors = [item] + errors
        if len(error1) > 0:
            for item in error1: errors = [item] + errors
    else:
        error1 = errorList(log)
        if len(error1) > 0:
            for item in error1: errors = [item] + errors
    if not count == None:
        return len(errors)
    elif len(errors) > 0:
        if last == None:
            i = 0; string = ''
            for item in errors:
                i += 1
                string += "[B][COLOR red]ERROR NUMBER %s:[/B][/COLOR]%s\n" % (str(i), item.replace(HOME, '/').replace('                                        ', ''))
        else:
            string = "[B][COLOR red]Last Error in Log:[/B][/COLOR]%s\n" % (errors[0].replace(HOME, '/').replace('                                        ', ''))
        wiz.TextBox("%s: Errors in Log" % ADDONTITLE, string)
    else:
        wiz.LogNotify('[COLOR %s]View Error Log[/COLOR]' % COLOR1, '[COLOR %s]No Errors Found![/COLOR]' % COLOR2)

ACTION_PREVIOUS_MENU            =  10   ## ESC action
ACTION_NAV_BACK                 =  92   ## Backspace action
ACTION_MOVE_LEFT                =   1   ## Left arrow key
ACTION_MOVE_RIGHT               =   2   ## Right arrow key
ACTION_MOVE_UP                  =   3   ## Up arrow key
ACTION_MOVE_DOWN                =   4   ## Down arrow key
ACTION_MOUSE_WHEEL_UP           = 104   ## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN         = 105   ## Mouse wheel down
ACTION_MOVE_MOUSE               = 107   ## Down arrow key
ACTION_SELECT_ITEM              =   7   ## Number Pad Enter
ACTION_BACKSPACE                = 110   ## ?
ACTION_MOUSE_LEFT_CLICK         = 100
ACTION_MOUSE_LONG_CLICK         = 108

def LogViewer(default=None):
    class LogViewer(xbmcgui.WindowXMLDialog):
        def __init__(self,*args,**kwargs):
            self.default = kwargs['default']

        def onInit(self):
            self.title      = 101
            self.msg        = 102
            self.scrollbar  = 103
            self.upload     = 201
            self.kodi       = 202
            self.kodiold    = 203
            self.wizard     = 204
            self.okbutton   = 205
            f = open(self.default, 'r')
            self.logmsg = f.read()
            f.close()
            self.titlemsg = "%s: %s" % (ADDONTITLE, self.default.replace(LOG, '').replace(ADDONDATA, ''))
            self.showdialog()

        def showdialog(self):
            self.getControl(self.title).setLabel(self.titlemsg)
            self.getControl(self.msg).setText(wiz.highlightText(self.logmsg))
            self.setFocusId(self.scrollbar)

        def onClick(self, controlId):
            if   controlId == self.okbutton: self.close()
            elif controlId == self.upload: self.close(); uploadLog.Main()
            elif controlId == self.kodi:
                newmsg = wiz.Grab_Log(False)
                filename = wiz.Grab_Log(True)
                if newmsg == False:
                    self.titlemsg = "%s: View Log Error" % ADDONTITLE
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(wiz.highlightText(newmsg))
                    self.setFocusId(self.scrollbar)
            elif controlId == self.kodiold:
                newmsg = wiz.Grab_Log(False, True)
                filename = wiz.Grab_Log(True, True)
                if newmsg == False:
                    self.titlemsg = "%s: View Log Error" % ADDONTITLE
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(wiz.highlightText(newmsg))
                    self.setFocusId(self.scrollbar)
            elif controlId == self.wizard:
                newmsg = wiz.Grab_Log(False, False, True)
                filename = wiz.Grab_Log(True, False, True)
                if newmsg == False:
                    self.titlemsg = "%s: View Log Error" % ADDONTITLE
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(ADDONDATA, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(wiz.highlightText(newmsg))
                    self.setFocusId(self.scrollbar)

        def onAction(self, action):
            if   action == ACTION_PREVIOUS_MENU: self.close()
            elif action == ACTION_NAV_BACK: self.close()
    if default == None: default = wiz.Grab_Log(True)
    lv = LogViewer( "LogViewer.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', default=default)
    lv.doModal()
    del lv

def removeAddon(addon, name, over=False):
    if not over == False:
        yes = 1
    else:
        yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Are you sure you want to delete the addon:'% COLOR2, 'Name: [COLOR %s]%s[/COLOR]' % (COLOR1, name), 'ID: [COLOR %s]%s[/COLOR][/COLOR]' % (COLOR1, addon), yeslabel='[B][COLOR springgreen]Remove Addon[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]')
    if yes == 1:
        folder = os.path.join(ADDONS, addon)
        wiz.log("Removing Addon %s" % addon)
        wiz.cleanHouse(folder)
        xbmc.sleep(200)
        try: shutil.rmtree(folder)
        except Exception ,e: wiz.log("Error removing %s" % addon, xbmc.LOGNOTICE)
        removeAddonData(addon, name, over)
    if over == False:
        wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Removed[/COLOR]" % (COLOR2, name))

def removeAddonData(addon, name=None, over=False):
    if addon == 'all':
        if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in you Userdata folder?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            wiz.cleanHouse(ADDOND)
        else: wiz.LogNotify('[COLOR %s]Remove Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
    elif addon == 'uninstalled':
        if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in you Userdata folder for uninstalled addons?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            total = 0
            for folder in glob.glob(os.path.join(ADDOND, '*')):
                foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
                if foldername in EXCLUDES: pass
                elif os.path.exists(os.path.join(ADDONS, foldername)): pass
                else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
            wiz.LogNotify('[COLOR %s]Clean up Uninstalled[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
        else: wiz.LogNotify('[COLOR %s]Remove Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
    elif addon == 'empty':
        if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] empty addon data folders in you Userdata folder?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            total = wiz.emptyfolder(ADDOND)
            wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
        else: wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
    else:
        addon_data = os.path.join(USERDATA, 'addon_data', addon)
        if addon in EXCLUDES:
            wiz.LogNotify("[COLOR %s]Protected Plugin[/COLOR]" % COLOR1, "[COLOR %s]Not allowed to remove Addon_Data[/COLOR]" % COLOR2)
        elif os.path.exists(addon_data):
            if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you also like to remove the addon data for:[/COLOR]' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, addon), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
                wiz.cleanHouse(addon_data)
                try:
                    shutil.rmtree(addon_data)
                except:
                    wiz.log("Error deleting: %s" % addon_data)
            else:
                wiz.log('Addon data for %s was not removed' % addon)
    wiz.refresh()

def restoreit(type):
    if type == 'build':
        x = freshStart('restore')
        if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Local Restore Cancelled[/COLOR]" % COLOR2); return
    if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
        wiz.skinToDefault('Restore Backup')
    wiz.restoreLocal(type)

def restoreextit(type):
    if type == 'build':
        x = freshStart('restore')
        if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore Cancelled[/COLOR]" % COLOR2); return
    wiz.restoreExternal(type)

def buildInfo(name):
    if wiz.workingURL(BUILDFILE) == True:
        if wiz.checkBuild(name, 'url'):
            name, version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description = wiz.checkBuild(name, 'all')
            adult = 'Yes' if adult.lower() == 'yes' else 'No'
            extend = False
            if not info == "http://":
                try:
                    tname, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts = wiz.checkInfo(info)
                    extend = True
                except:
                    extend = False
            if extend == True:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] v[COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, version)
                msg += "[COLOR %s]Latest Update:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, created)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Extracted Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(extracted))))
                msg += "[COLOR %s]Zip Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(zipsize))))
                msg += "[COLOR %s]Skin Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, skin)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, description)
                msg += "[COLOR %s]Programs:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, programs)
                msg += "[COLOR %s]Video:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, video)
                msg += "[COLOR %s]Music:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, music)
                msg += "[COLOR %s]Pictures:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, picture)
                msg += "[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, repos)
                msg += "[COLOR %s]Scripts:[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, scripts)
            else:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, version)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, description)

            wiz.TextBox(ADDONTITLE, msg)
        else: wiz.log("Invalid Build Name!")
    else: wiz.log("Build text file not working: %s" % WORKINGURL)

def buildVideo(name):
    if wiz.workingURL(BUILDFILE) == True:
        videofile = wiz.checkBuild(name, 'preview')
        if videofile and not videofile == 'http://': playVideo(videofile)
        else: wiz.log("[%s]Unable to find url for video preview" % name)
    else: wiz.log("Build text file not working: %s" % WORKINGURL)

def dependsList(plugin):
    addonxml = os.path.join(ADDONS, plugin, 'addon.xml')
    if os.path.exists(addonxml):
        source = open(addonxml,mode='r'); link = source.read(); source.close();
        match  = wiz.parseDOM(link, 'import', ret='addon')
        items  = []
        for depends in match:
            if not 'xbmc.python' in depends:
                items.append(depends)
        return items
    return []

def manageSaveData(do):
    if do == 'import':
        TEMP = os.path.join(ADDONDATA, 'temp')
        if not os.path.exists(TEMP): os.makedirs(TEMP)
        source = DIALOG.browse(1, '[COLOR %s]Select the location of the SaveData.zip[/COLOR]' % COLOR2, 'files', '.zip', False, False, HOME)
        if not source.endswith('.zip'):
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
            return
        source   = xbmc.translatePath(source)
        tempfile = xbmc.translatePath(os.path.join(MYBUILDS, 'SaveData.zip'))
        if not tempfile == source:
            goto = xbmcvfs.copy(source, tempfile)
        if extract.all(xbmc.translatePath(tempfile), TEMP) == False:
            wiz.log("Error trying to extract the zip file!")
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
            return
        trakt  = os.path.join(TEMP, 'trakt')
        login  = os.path.join(TEMP, 'login')
        debrid = os.path.join(TEMP, 'debrid')
        super  = os.path.join(TEMP, 'plugin.program.super.favourites')
        xmls   = os.path.join(TEMP, 'xmls')
        x = 0
        overwrite = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you rather we overwrite all Save Data files or ask you for each file being imported?[/COLOR]" % (COLOR2), yeslabel="[B][COLOR springgreen]Overwrite All[/COLOR][/B]", nolabel="[B][COLOR red]No Ask[/COLOR][/B]")
        if os.path.exists(trakt):
            x += 1
            files = os.listdir(trakt)
            if not os.path.exists(traktit.TRAKTFOLD): os.makedirs(traktit.TRAKTFOLD)
            for item in files:
                old  = os.path.join(traktit.TRAKTFOLD, item)
                temp = os.path.join(trakt, item)
                if os.path.exists(old):
                    if overwrite == 1: os.remove(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: os.remove(old)
                shutil.copy(temp, old)
            traktit.importlist('all')
            traktit.traktIt('restore', 'all')
        if os.path.exists(login):
            x += 1
            files = os.listdir(login)
            if not os.path.exists(loginit.LOGINFOLD): os.makedirs(loginit.LOGINFOLD)
            for item in files:
                old  = os.path.join(loginit.LOGINFOLD, item)
                temp = os.path.join(login, item)
                if os.path.exists(old):
                    if overwrite == 1: os.remove(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: os.remove(old)
                shutil.copy(temp, old)
            loginit.importlist('all')
            loginit.loginIt('restore', 'all')
        if os.path.exists(debrid):
            x += 1
            files = os.listdir(debrid)
            if not os.path.exists(debridit.REALFOLD): os.makedirs(debridit.REALFOLD)
            for item in files:
                old  = os.path.join(debridit.REALFOLD, item)
                temp = os.path.join(debrid, item)
                if os.path.exists(old):
                    if overwrite == 1: os.remove(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: os.remove(old)
                shutil.copy(temp, old)
            debridit.importlist('all')
            debridit.debridIt('restore', 'all')
        if os.path.exists(xmls):
            x += 1
            files = ['advancedsettings.xml', 'sources.xml', 'favourites.xml', 'profiles.xml']
            for item in files:
                old = os.path.join(USERDATA, item)
                new = os.path.join(xmls, item)
                if not os.path.exists(new): continue
                if os.path.exists(old):
                    if not overwrite == 1:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                os.remove(old)
                shutil.copy(new, old)
        if os.path.exists(super):
            x += 1
            old = os.path.join(ADDOND, 'plugin.program.super.favourites')
            if os.path.exists(old):
                cont = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]Super Favourites[/COLOR] addon_data folder with the new one?" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]")
            else: cont = 1
            if cont == 1:
                wiz.cleanHouse(old)
                wiz.removeFolder(old)
                xbmcvfs.copy(super, old)
        wiz.cleanHouse(TEMP)
        wiz.removeFolder(TEMP)
        if not tempfile == source:
            xbmcvfs.delete(tempfile)
        if x == 0: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Failed[/COLOR]" % COLOR2)
        else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Complete[/COLOR]" % COLOR2)
    elif do == 'export':
        mybuilds = xbmc.translatePath(MYBUILDS)
        dir   = [traktit.TRAKTFOLD, debridit.REALFOLD, loginit.LOGINFOLD]
        xmls  = ['advancedsettings.xml', 'sources.xml', 'favourites.xml', 'profiles.xml']
        keepx = [KEEPADVANCED, KEEPSOURCES, KEEPFAVS, KEEPPROFILES]
        traktit.traktIt('update', 'all')
        loginit.loginIt('update', 'all')
        debridit.debridIt('update', 'all')
        source = DIALOG.browse(3, '[COLOR %s]Select where you wish to export the savedata zip?[/COLOR]' % COLOR2, 'files', '', False, True, HOME)
        source = xbmc.translatePath(source)
        tempzip = os.path.join(mybuilds, 'SaveData.zip')
        superfold = os.path.join(ADDOND, 'plugin.program.super.favourites')
        zipf = zipfile.ZipFile(tempzip, mode='w')
        for fold in dir:
            if os.path.exists(fold):
                files = os.listdir(fold)
                for file in files:
                    fn = os.path.join(fold, file)
                    zipf.write(fn, fn[len(ADDONDATA):], zipfile.ZIP_DEFLATED)
        if KEEPSUPER == 'true' and os.path.exists(superfold):
            for base, dirs, files in os.walk(superfold):
                for file in files:
                    fn = os.path.join(base, file)
                    zipf.write(fn, fn[len(ADDOND):], zipfile.ZIP_DEFLATED)
        for item in xmls:
            if keepx[xmls.index(item)] == 'true' and os.path.exists(os.path.join(USERDATA, item)):
                zipf.write(os.path.join(USERDATA, item), os.path.join('xmls', item), zipfile.ZIP_DEFLATED)
        zipf.close()
        if source == mybuilds:
            DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))
        else:
            try:
                xbmcvfs.copy(tempzip, os.path.join(source, 'SaveData.zip'))
                DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, os.path.join(source, 'SaveData.zip')))
            except:
                DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))

###########################
###### Fresh Install ######
###########################
def freshStart(install=None, over=False):
    if KEEPTRAKT == 'true':
        traktit.autoUpdate('all')
        wiz.setS('traktlastsave', str(THREEDAYS))
    if KEEPREAL == 'true':
        debridit.autoUpdate('all')
        wiz.setS('debridlastsave', str(THREEDAYS))
    if KEEPLOGIN == 'true':
        loginit.autoUpdate('all')
        wiz.setS('loginlastsave', str(THREEDAYS))
    if over == True: yes_pressed = 1
    elif install == 'restore': yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you wish to restore your" % COLOR2, "Kodi configuration to default settings", "Before installing the local backup?[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    elif install: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you wish to restore your" % COLOR2, "Kodi configuration to default settings", "Before installing [COLOR %s]%s[/COLOR]?" % (COLOR1, install), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    else: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you wish to restore your" % COLOR2, "Kodi configuration to default settings?[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    if yes_pressed:
        if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
            swap = wiz.skinToDefault('Fresh Install')
            if swap == False: return False
            xbmc.sleep(1000)
        if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Skin Swap Failed![/COLOR]' % COLOR2)
            return
        wiz.addonUpdates('set')
        xbmcPath=os.path.abspath(HOME)
        DP.create(ADDONTITLE,"[COLOR %s]Calculating files and folders" % COLOR2,'', 'Please Wait![/COLOR]')
        total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0
        DP.update(0, "[COLOR %s]Gathering Excludes list." % COLOR2)
        EXCLUDES.append('My_Builds')
        EXCLUDES.append('archive_cache')
        if KEEPREPOS == 'true':
            repos = glob.glob(os.path.join(ADDONS, 'repo*/'))
            for item in repos:
                repofolder = os.path.split(item[:-1])[1]
                if not repofolder == EXCLUDES:
                    EXCLUDES.append(repofolder)
        if KEEPSUPER == 'true':
            EXCLUDES.append('plugin.program.super.favourites')
        if KEEPWHITELIST == 'true':
            pvr = ''
            whitelist = wiz.whiteList('read')
            if len(whitelist) > 0:
                for item in whitelist:
                    try: name, id, fold = item
                    except: pass
                    if fold.startswith('pvr'): pvr = id
                    depends = dependsList(fold)
                    for plug in depends:
                        if not plug in EXCLUDES:
                            EXCLUDES.append(plug)
                        depends2 = dependsList(plug)
                        for plug2 in depends2:
                            if not plug2 in EXCLUDES:
                                EXCLUDES.append(plug2)
                    if not fold in EXCLUDES:
                        EXCLUDES.append(fold)
                if not pvr == '': wiz.setS('pvrclient', fold)
        if wiz.getS('pvrclient') == '':
            for item in EXCLUDES:
                if item.startswith('pvr'):
                    wiz.setS('pvrclient', item)
        DP.update(0, "[COLOR %s]Clearing out files and folders:" % COLOR2)
        latestAddonDB = wiz.latestDB('Addons')
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in files:
                del_file += 1
                fold = root.replace('/','\\').split('\\')
                x = len(fold)-1
                if name == 'sources.xml' and fold[-1] == 'userdata' and KEEPSOURCES == 'true': wiz.log("Keep Sources: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name == 'favourites.xml' and fold[-1] == 'userdata' and KEEPFAVS == 'true': wiz.log("Keep Favourites: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name == 'profiles.xml' and fold[-1] == 'userdata' and KEEPPROFILES == 'true': wiz.log("Keep Profiles: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and KEEPADVANCED == 'true':  wiz.log("Keep Advanced Settings: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name in LOGFILES: wiz.log("Keep Log File: %s" % name, xbmc.LOGNOTICE)
                elif name.endswith('.db'):
                    try:
                        if name == latestAddonDB and KODIV >= 17: wiz.log("Ignoring %s on v%s" % (name, KODIV), xbmc.LOGNOTICE)
                        else: os.remove(os.path.join(root,name))
                    except Exception, e:
                        if not name.startswith('Textures13'):
                            wiz.log('Failed to delete, Purging DB', xbmc.LOGNOTICE)
                            wiz.log("-> %s" % (str(e)), xbmc.LOGNOTICE)
                            wiz.purgeDb(os.path.join(root,name))
                else:
                    DP.update(int(wiz.percentage(del_file, total_files)), '', '[COLOR %s]File: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '')
                    try: os.remove(os.path.join(root,name))
                    except Exception, e:
                        wiz.log("Error removing %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                        wiz.log("-> / %s" % (str(e)), xbmc.LOGNOTICE)
            if DP.iscanceled():
                DP.close()
                wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
                return False
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in dirs:
                DP.update(100, '', 'Cleaning Up Empty Folder: [COLOR %s]%s[/COLOR]' % (COLOR1, name), '')
                if name not in ["Database","userdata","temp","addons","addon_data"]:
                    shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
            if DP.iscanceled():
                DP.close()
                wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
                return False
        DP.close()
        wiz.clearS('build')
        if over == True:
            return True
        elif install == 'restore':
            return True
        elif install:
            buildWizard(install, 'normal', over=True)
        else:
            if INSTALLMETHOD == 1: todo = 1
            elif INSTALLMETHOD == 2: todo = 0
            else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
            if todo == 1: wiz.reloadFix('fresh')
            else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
    else:
        if not install == 'restore':
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Cancelled![/COLOR]' % COLOR2)
            wiz.refresh()

#############################
###DELETE CACHE##############
####THANKS GUYS @ NaN #######
def clearCache():
    if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear cache?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Clear Cache[/COLOR][/B]'):
        wiz.clearCache()

def clearArchive():
    if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear the \'Archive_Cache\' folder?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Yes Clear[/COLOR][/B]'):
        wiz.clearArchive()

def totalClean():
    if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear cache, packages and thumbnails?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]Cancel Process[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Clean All[/COLOR][/B]'):
        wiz.clearCache()
        wiz.clearPackages('total')
        clearThumb('total')

def clearThumb(type=None):
    thumb_locations = {THUMBS,
        os.path.join(ADDOND, 'script.module.metadatautils','animatedgifs'),
        os.path.join(ADDOND, 'script.extendedinfo', 'images')}
    
    latest = wiz.latestDB('Textures')
    if not type == None: choice = 1
    else: choice = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to delete the %s and related thumbnail folders?' % (COLOR2, latest), "They will repopulate on the next startup[/COLOR]", nolabel='[B][COLOR red]Don\'t Delete[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Delete Thumbs[/COLOR][/B]')
    if choice == 1:
        try: wiz.removeFile(os.join(DATABASE, latest))
        except: wiz.log('Failed to delete, Purging DB.'); wiz.purgeDb(latest)
        for i in thumb_locations:
            wiz.removeFolder(i)
        #if not type == 'total': wiz.killxbmc()
    else: wiz.log('Clear thumbnames cancelled')
    wiz.redoThumbs()

def purgeDb():
    DB = []; display = []
    for dirpath, dirnames, files in os.walk(HOME):
        for f in fnmatch.filter(files, '*.db'):
            if f != 'Thumbs.db':
                found = os.path.join(dirpath, f)
                DB.append(found)
                dir = found.replace('\\', '/').split('/')
                display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
    if KODIV >= 16:
        choice = DIALOG.multiselect("[COLOR %s]Select DB File to Purge[/COLOR]" % COLOR2, display)
        if choice == None: wiz.LogNotify("[COLOR %s]Purge Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelled[/COLOR]" % COLOR2)
        elif len(choice) == 0: wiz.LogNotify("[COLOR %s]Purge Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelled[/COLOR]" % COLOR2)
        else:
            for purge in choice: wiz.purgeDb(DB[purge])
    else:
        choice = DIALOG.select("[COLOR %s]Select DB File to Purge[/COLOR]" % COLOR2, display)
        if choice == -1: wiz.LogNotify("[COLOR %s]Purge Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelled[/COLOR]" % COLOR2)
        else: wiz.purgeDb(DB[purge])

##########################
### DEVELOPER MENU #######
##########################
def testnotify():
    url = wiz.workingURL(NOTIFICATION)
    if url == True:
        try:
            id, msg = wiz.splitNotify(NOTIFICATION)
            if id == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Notification: Not Formated Correctly[/COLOR]" % COLOR2); return
            notify.notification(msg, True)
        except Exception, e:
            wiz.log("Error on Notifications Window: %s" % str(e), xbmc.LOGERROR)
    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Invalid URL for Notification[/COLOR]" % COLOR2)

def testupdate():
    if BUILDNAME == "":
        notify.updateWindow()
    else:
        notify.updateWindow(BUILDNAME, BUILDVERSION, BUILDLATEST, wiz.checkBuild(BUILDNAME, 'icon'), wiz.checkBuild(BUILDNAME, 'fanart'))

def testfirst():
    notify.firstRun()

def testfirstRun():
    notify.firstRunSettings()

###########################
## Making the Directory####
###########################

def addDir(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
    u = sys.argv[0]
    if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
    if not name == None: u += "&name="+urllib.quote_plus(name)
    if not url == None: u += "&url="+urllib.quote_plus(url)
    ok=True
    if themeit: display = themeit % display
    liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
    liz.setProperty( "Fanart_Image", fanart )
    if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
    u = sys.argv[0]
    if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
    if not name == None: u += "&name="+urllib.quote_plus(name)
    if not url == None: u += "&url="+urllib.quote_plus(url)
    ok=True
    if themeit: display = themeit % display
    liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
    liz.setProperty( "Fanart_Image", fanart )
    if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

        return param

################KODI VERSION##########################################
def KodiVer():
    if KODIV >= 16.0 and KODIV <= 16.9:vername = 'Jarvis'
    elif KODIV >= 17.0 and KODIV <= 17.9:vername = 'Krypton'
    elif KODIV >= 18.0 and KODIV <= 18.9:vername = 'Leia'
    else: vername = "Unknown"
    return vername
######################################################################################################################
######################################################################################################################
params=get_params()
url=None
name=None
mode=None

try:     mode=urllib.unquote_plus(params["mode"])
except:  pass
try:     name=urllib.unquote_plus(params["name"])
except:  pass
try:     url=urllib.unquote_plus(params["url"])
except:  pass

wiz.log('[ Version : \'%s\' ] [ Mode : \'%s\' ] [ Name : \'%s\' ] [ Url : \'%s\' ]' % (VERSION, mode if not mode == '' else None, name, url))

def setView(content, viewType):
    if wiz.getS('auto-view')=='true':
        views = wiz.getS(viewType)
        if views == '50' and KODIV >= 17 and SKIN == 'skin.estuary': views = '55'
        if views == '500' and KODIV >= 17 and SKIN == 'skin.estuary': views = '50'
        wiz.ebi("Container.SetViewMode(%s)" %  views)

if   mode==None             : index()

elif mode=='wizardupdate'   : wiz.wizardUpdate()
elif mode=='builds'         : buildMenu()
elif mode=='viewbuild'      : viewBuild(name)
elif mode=='buildinfo'      : buildInfo(name)
elif mode=='buildpreview'   : buildVideo(name)
elif mode=='install'        : buildWizard(name, url)
elif mode=='theme'          : buildWizard(name, mode, url)
elif mode=='viewthirdparty' : viewThirdList(name)
elif mode=='installthird'   : thirdPartyInstall(name, url)
elif mode=='editthird'      : editThirdParty(name); wiz.refresh()

elif mode=='maint'          : maintMenu(name)
elif mode=='kodi17fix'      : wiz.kodi17Fix()
elif mode=='unknownsources' : skinSwitch.swapUS()
elif mode=='advancedsetting': advancedWindow(name)
elif mode=='autoadvanced'   : showAutoAdvanced(); wiz.refresh()
elif mode=='removeadvanced' : removeAdvanced(); wiz.refresh()
elif mode=='asciicheck'     : wiz.asciiCheck()
elif mode=='extractazip'    : wiz.extractAZip()
elif mode=='backupbuild'    : wiz.backUpOptions('build')
elif mode=='backupgui'      : wiz.backUpOptions('guifix')
elif mode=='backuptheme'    : wiz.backUpOptions('theme')
elif mode=='backupaddonpack': wiz.backUpOptions('addon pack')
elif mode=='backupaddon'    : wiz.backUpOptions('addondata')
elif mode=='oldThumbs'      : wiz.oldThumbs()
elif mode=='clearbackup'    : wiz.cleanupBackup()
elif mode=='convertpath'    : wiz.convertSpecial(HOME)
elif mode=='currentsettings': viewAdvanced()
elif mode=='fullclean'      : totalClean(); wiz.refresh()
elif mode=='clearcache'     : clearCache(); wiz.refresh()
elif mode=='clearpackages'  : wiz.clearPackages(); wiz.refresh()
elif mode=='clearcrash'     : wiz.clearCrash(); wiz.refresh()
elif mode=='clearthumb'     : clearThumb(); wiz.refresh()
elif mode=='cleararchive'   : clearArchive(); wiz.refresh()
elif mode=='checksources'   : wiz.checkSources(); wiz.refresh()
elif mode=='checkrepos'     : wiz.checkRepos(); wiz.refresh()
elif mode=='freshstart'     : freshStart()
elif mode=='forceupdate'    : wiz.forceUpdate()
elif mode=='forceprofile'   : wiz.reloadProfile(wiz.getInfo('System.ProfileName'))
elif mode=='forceclose'     : wiz.killxbmc()
elif mode=='forceskin'      : wiz.ebi("ReloadSkin()"); wiz.refresh()
elif mode=='hidepassword'   : wiz.hidePassword()
elif mode=='unhidepassword' : wiz.unhidePassword()
elif mode=='enableaddons'   : enableAddons()
elif mode=='toggleaddon'    : wiz.toggleAddon(name, url); wiz.refresh()
elif mode=='togglecache'    : toggleCache(name); wiz.refresh()
elif mode=='toggleadult'    : wiz.toggleAdult(); wiz.refresh()
elif mode=='changefeq'      : changeFeq(); wiz.refresh()
elif mode=='uploadlog'      : uploadLog.Main()
elif mode=='viewlog'        : LogViewer()
elif mode=='viewwizlog'     : LogViewer(WIZLOG)
elif mode=='viewerrorlog'   : errorChecking()
elif mode=='viewerrorlast'  : errorChecking(last=True)
elif mode=='clearwizlog'    : f = open(WIZLOG, 'w'); f.close(); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Wizard Log Cleared![/COLOR]" % COLOR2)
elif mode=='purgedb'        : purgeDb()
elif mode=='fixaddonupdate' : fixUpdate()
elif mode=='removeaddons'   : removeAddonMenu()
elif mode=='removeaddon'    : removeAddon(name)
elif mode=='removeaddondata': removeAddonDataMenu()
elif mode=='removedata'     : removeAddonData(name)
elif mode=='resetaddon'     : total = wiz.cleanHouse(ADDONDATA, ignore=True); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Addon_Data reset[/COLOR]" % COLOR2)
elif mode=='systeminfo'     : systemInfo()
elif mode=='restorezip'     : restoreit('build')
elif mode=='restoregui'     : restoreit('gui')
elif mode=='restoreaddon'   : restoreit('addondata')
elif mode=='restoreextzip'  : restoreextit('build')
elif mode=='restoreextgui'  : restoreextit('gui')
elif mode=='restoreextaddon': restoreextit('addondata')
elif mode=='writeadvanced'  : writeAdvanced(name, url)
elif mode=='speedtest'      : net_tools()
elif mode=='runspeedtest'   : runSpeedTest(); wiz.refresh()
elif mode=='clearspeedtest' : clearSpeedTest(); wiz.refresh()
elif mode=='viewspeedtest'  : viewSpeedTest(name); wiz.refresh()
elif mode=="viewIP"         : viewIP();

elif mode=='speedtestM'     : speedTest()

elif mode=='apk'            : apkMenu(name, url)
elif mode=='apkscrape'      : apkScraper(name)
elif mode=='apkinstall'     : apkInstaller(name, url)
elif mode=='rominstall'     : romInstaller(name, url)

elif mode=='youtube'        : youtubeMenu(name, url)
elif mode=='viewVideo'      : playVideo(url)

elif mode=='addons'         : addonMenu(name, url)
elif mode=='addonpack'      : packInstaller(name, url)
elif mode=='skinpack'       : skinInstaller(name, url)
elif mode=='addoninstall'   : addonInstaller(name, url)

elif mode=='savedata'       : saveMenu()
elif mode=='togglesetting'  : wiz.setS(name, 'false' if wiz.getS(name) == 'true' else 'true'); wiz.refresh()
elif mode=='managedata'     : manageSaveData(name)
elif mode=='whitelist'      : wiz.whiteList(name)

elif mode=='trakt'          : traktMenu()
elif mode=='savetrakt'      : traktit.traktIt('update',      name)
elif mode=='restoretrakt'   : traktit.traktIt('restore',     name)
elif mode=='addontrakt'     : traktit.traktIt('clearaddon',  name)
elif mode=='cleartrakt'     : traktit.clearSaved(name)
elif mode=='authtrakt'      : traktit.activateTrakt(name); wiz.refresh()
elif mode=='updatetrakt'    : traktit.autoUpdate('all')
elif mode=='importtrakt'    : traktit.importlist(name); wiz.refresh()

elif mode=='realdebrid'     : realMenu()
elif mode=='savedebrid'     : debridit.debridIt('update',      name)
elif mode=='restoredebrid'  : debridit.debridIt('restore',     name)
elif mode=='addondebrid'    : debridit.debridIt('clearaddon',  name)
elif mode=='cleardebrid'    : debridit.clearSaved(name)
elif mode=='authdebrid'     : debridit.activateDebrid(name); wiz.refresh()
elif mode=='updatedebrid'   : debridit.autoUpdate('all')
elif mode=='importdebrid'   : debridit.importlist(name); wiz.refresh()

elif mode=='login'          : loginMenu()
elif mode=='savelogin'      : loginit.loginIt('update',      name)
elif mode=='restorelogin'   : loginit.loginIt('restore',     name)
elif mode=='addonlogin'     : loginit.loginIt('clearaddon',  name)
elif mode=='clearlogin'     : loginit.clearSaved(name)
elif mode=='authlogin'      : loginit.activateLogin(name); wiz.refresh()
elif mode=='updatelogin'    : loginit.autoUpdate('all')
elif mode=='importlogin'    : loginit.importlist(name); wiz.refresh()

elif mode=='contact'        : notify.contact(CONTACT)
elif mode=='settings'       : wiz.openS(name); wiz.refresh()
elif mode=='forcetext'      : wiz.forceText()
elif mode=='opensettings'   : id = eval(url.upper()+'ID')[name]['plugin']; addonid = wiz.addonId(id); addonid.openSettings(); wiz.refresh()

elif mode=='developer'      : developer()
elif mode=='converttext'    : wiz.convertText()
elif mode=='createqr'       : wiz.createQR()
elif mode=='testnotify'     : testnotify()
elif mode=='testupdate'     : testupdate()
elif mode=='testfirst'      : testfirst()
elif mode=='testfirstrun'   : testfirstRun()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
