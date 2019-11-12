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
TRAKTFOLD      = os.path.join(ADDONDATA, 'trakt')
ICON           = os.path.join(PLUGIN,    'icon.png')
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
KEEPTRAKT      = wiz.getS('keeptrakt')
TRAKTSAVE      = wiz.getS('traktlastsave')
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
ORDER          = ['exodusredux', 'gaia', 'numbers', 'openmeta', 'overeasy', 'placenta', 'premiumizer', 'realizer', 'scrubs', 'seren', 'thecrew', 'trakt', 'venom', 'yoda']

TRAKTID = {
    'placenta': {
        'name'     : 'Placenta',
        'plugin'   : 'plugin.video.placenta',
        'saved'    : 'placenta',
        'path'     : os.path.join(ADDONS, 'plugin.video.placenta'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.placenta', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.placenta', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'placenta_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.placenta', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.placenta/?action=authTrakt)'},
     'thecrew': {
        'name'     : 'THE CREW',
        'plugin'   : 'plugin.video.thecrew',
        'saved'    : 'thecrew',
        'path'     : os.path.join(ADDONS, 'plugin.video.thecrew'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'thecrew_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.thecrew', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.thecrew/?action=authTrakt)'},
    'gaia': {
        'name'     : 'Gaia',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'gaia',
        'path'     : os.path.join(ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'gaia_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.informants.trakt.user',
        'data'     : ['accounts.informants.trakt.user', 'accounts.informants.trakt.refresh', 'accounts.informants.trakt.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=traktAuthorize)'},
    'numbers': {
        'name'     : 'NuMb3r5',
        'plugin'   : 'plugin.video.numbersbynumbers',
        'saved'    : 'numbers',
        'path'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.numbersbynumbers', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'numbers_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.numbersbynumbers', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.numbersbynumbers/?action=authTrakt)'},
    'overeasy': {
        'name'     : 'Overeasy',
        'plugin'   : 'plugin.video.overeasy',
        'saved'    : 'overeasy',
        'path'     : os.path.join(ADDONS, 'plugin.video.overeasy'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.overeasy', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.overeasy', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'overeasy_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.overeasy', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
        'activate' : 'RunPlugin(plugin://plugin.video.overeasy/?action=authTrakt)'},
    'seren': {
        'name'     : 'Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'seren',
        'path'     : os.path.join(ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.seren', 'temp-icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
        'file'     : os.path.join(TRAKTFOLD, 'seren_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'trakt.username',
        'data'     : ['trakt.auth', 'trakt.refresh', 'trakt.username'],
        'activate' : 'RunPlugin(plugin://plugin.video.seren/?action=authTrakt)'},
    'trakt': {
        'name'     : 'Trakt',
        'plugin'   : 'script.trakt',
        'saved'    : 'trakt',
        'path'     : os.path.join(ADDONS, 'script.trakt'),
        'icon'     : os.path.join(ADDONS, 'script.trakt', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'script.trakt', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'trakt_trakt'),
        'settings' : os.path.join(ADDOND, 'script.trakt', 'settings.xml'),
        'default'  : 'user',
        'data'     : ['authorization', 'user'],
        'activate' : 'RunScript(script.trakt, action=auth_info)'},
    'exodusredux': {
        'name'     : 'Exodus Redux',
        'plugin'   : 'plugin.video.exodusredux',
        'saved'    : 'exodusredux',
        'path'     : os.path.join(ADDONS, 'plugin.video.exodusredux'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.exodusredux', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.exodusredux', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'exodusredux_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.exodusredux', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.user', 'trakt.refresh', 'trakt.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.exodusredux/?action=authTrakt)'},
    'openmeta': {
        'name'     : 'OpenMeta',
        'plugin'   : 'plugin.video.openmeta',
        'saved'    : 'openmeta',
        'path'     : os.path.join(ADDONS, 'plugin.video.openmeta'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.openmeta', 'resources/fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'openmeta_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.openmeta', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_access_token', 'trakt_refresh_token', 'trakt_expires_at    '],
        'activate' : 'RunPlugin(plugin://plugin.video.openmeta/authenticate_trakt)'},
    'yoda': {
        'name'     : 'Yoda',
        'plugin'   : 'plugin.video.yoda',
        'saved'    : 'yoda',
        'path'     : os.path.join(ADDONS, 'plugin.video.yoda'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.yoda', 'icon.jpg'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.yoda', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'yoda_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.yoda', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.token', 'trakt.refresh', 'trakt.user'],
        'activate' : 'RunPlugin(plugin://plugin.video.yoda/?action=authTrakt)'},
    'venom': {
        'name'     : 'Venom',
        'plugin'   : 'plugin.video.venom',
        'saved'    : 'venom',
        'path'     : os.path.join(ADDONS, 'plugin.video.venom'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.venom', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.venom', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'venom_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.venom', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.token', 'trakt.refresh', 'trakt.user'],
        'activate' : 'RunPlugin(plugin://plugin.video.venom/?action=authTrakt&opensettings=tru&query=10.2)'},
    'scrubs': {
        'name'     : 'Scrubs v2',
        'plugin'   : 'plugin.video.scrubsv2',
        'saved'    : 'scrubs',
        'path'     : os.path.join(ADDONS, 'plugin.video.scrubsv2'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'icon.jpg'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.scrubsv2', 'fanart.png'),
        'file'     : os.path.join(TRAKTFOLD, 'scrubs_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.scrubs', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.user', 'trakt.user2', 'trakt.token', 'trakt.refresh', 'trakt.auth'],
        'activate' : 'RunPlugin(plugin://plugin.video.scrubsv2/?action=authTrakt)'},
    'premiumizer': {
        'name'     : 'Premiumizer',
        'plugin'   : 'plugin.video.premiumizer',
        'saved'    : 'premiumizer',
        'path'     : os.path.join(ADDONS, 'plugin.video.premiumizer'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.premiumizer', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'premiumizer_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.premiumizer', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.token', 'trakt.refresh', 'trakt.user'],
        'activate' : 'RunPlugin(plugin://plugin.video.premiumizer/?action=authTrakt)'},
    'realizer': {
        'name'     : 'Realizer',
        'plugin'   : 'plugin.video.realizer',
        'saved'    : 'realizer',
        'path'     : os.path.join(ADDONS, 'plugin.video.realizer'),
        'icon'     : os.path.join(ADDONS, 'plugin.video.realizer', 'icon.png'),
        'fanart'   : os.path.join(ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
        'file'     : os.path.join(TRAKTFOLD, 'realizer_trakt'),
        'settings' : os.path.join(ADDOND, 'plugin.video.realizer', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.token', 'trakt.refresh', 'trakt.user'],
        'activate' : 'RunPlugin(plugin://plugin.video.realizer/?action=authTrakt)'}
}

def traktUser(who):
	user=None
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			try:
				add = wiz.addonId(TRAKTID[who]['plugin'])
				user = add.getSetting(TRAKTID[who]['default'])
			except:
				return None
	return user

def traktIt(do, who):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(TRAKTFOLD): os.makedirs(TRAKTFOLD)
	if who == 'all':
		for log in ORDER:
			if os.path.exists(TRAKTID[log]['path']):
				try:
					addonid   = wiz.addonId(TRAKTID[log]['plugin'])
					default   = TRAKTID[log]['default']
					user      = addonid.getSetting(default)
					if user == '' and do == 'update': continue
					updateTrakt(do, log)
				except: pass
			else: wiz.log('[Trakt Data] %s(%s) is not installed' % (TRAKTID[log]['name'],TRAKTID[log]['plugin']), xbmc.LOGERROR)
		wiz.setS('traktlastsave', str(THREEDAYS))
	else:
		if TRAKTID[who]:
			if os.path.exists(TRAKTID[who]['path']):
				updateTrakt(do, who)
		else: wiz.log('[Trakt Data] Invalid Entry: %s' % who, xbmc.LOGERROR)

def clearSaved(who, over=False):
	if who == 'all':
		for trakt in TRAKTID:
			clearSaved(trakt,  True)
	elif TRAKTID[who]:
		file = TRAKTID[who]['file']
		if os.path.exists(file):
			os.remove(file)
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, TRAKTID[who]['name']),'[COLOR %s]Trakt Data: Removed![/COLOR]' % COLOR2, 2000, TRAKTID[who]['icon'])
		wiz.setS(TRAKTID[who]['saved'], '')
	if over == False: wiz.refresh()

def updateTrakt(do, who):
	file      = TRAKTID[who]['file']
	settings  = TRAKTID[who]['settings']
	data      = TRAKTID[who]['data']
	addonid   = wiz.addonId(TRAKTID[who]['plugin'])
	saved     = TRAKTID[who]['saved']
	default   = TRAKTID[who]['default']
	user      = addonid.getSetting(default)
	suser     = wiz.getS(saved)
	name      = TRAKTID[who]['name']
	icon      = TRAKTID[who]['icon']

	if do == 'update':
		if not user == '':
			try:
				with open(file, 'w') as f:
					for trakt in data:
						f.write('<trakt>\n\t<id>%s</id>\n\t<value>%s</value>\n</trakt>\n' % (trakt, addonid.getSetting(trakt)))
					f.close()
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Data: Saved![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Data] Unable to Update %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt Data: Not Registered![/COLOR]' % COLOR2, 2000, icon)
	elif do == 'restore':
		if os.path.exists(file):
			f = open(file,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			match = re.compile('<trakt><id>(.+?)</id><value>(.+?)</value></trakt>').findall(g)
			try:
				if len(match) > 0:
					for trakt, value in match:
						addonid.setSetting(trakt, value)
				user = addonid.getSetting(default)
				wiz.setS(saved, user)
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, name), '[COLOR %s]Trakt: Restored![/COLOR]' % COLOR2, 2000, icon)
			except Exception, e:
				wiz.log("[Trakt Data] Unable to Restore %s (%s)" % (who, str(e)), xbmc.LOGERROR)
		#else: wiz.LogNotify(name,'Trakt Data: [COLOR red]Not Found![/COLOR]', 2000, icon)
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
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['path']):
				autoUpdate(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			u  = traktUser(who)
			su = wiz.getS(TRAKTID[who]['saved'])
			n = TRAKTID[who]['name']
			if u == None or u == '': return
			elif su == '': traktIt('update', who)
			elif not u == su:
				if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to save the [COLOR %s]Trakt Data[/COLOR] for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "Addon: [COLOR springgreen][B]%s[/B][/COLOR]" % u, "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
					traktIt('update', who)
			else: traktIt('update', who)

def importlist(who):
	if who == 'all':
		for log in TRAKTID:
			if os.path.exists(TRAKTID[log]['file']):
				importlist(log)
	elif TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['file']):
			d  = TRAKTID[who]['default']
			sa = TRAKTID[who]['saved']
			su = wiz.getS(sa)
			n  = TRAKTID[who]['name']
			f  = open(TRAKTID[who]['file'],mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
			m  = re.compile('<trakt><id>%s</id><value>(.+?)</value></trakt>' % d).findall(g)
			if len(m) > 0:
				if not m[0] == su:
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to import the [COLOR %s]Trakt Data[/COLOR] for [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, COLOR1, n), "File: [COLOR springgreen][B]%s[/B][/COLOR]" % m[0], "Saved:[/COLOR] [COLOR red][B]%s[/B][/COLOR]" % su if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]', yeslabel="[B]Save Data[/B]", nolabel="[B]No Cancel[/B]"):
						wiz.setS(sa, m[0])
						wiz.log('[Import Data] %s: %s' % (who, str(m)), xbmc.LOGNOTICE)
					else: wiz.log('[Import Data] Declined Import(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
				else: wiz.log('[Import Data] Duplicate Entry(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)
			else: wiz.log('[Import Data] No Match(%s): %s' % (who, str(m)), xbmc.LOGNOTICE)

def activateTrakt(who):
	if TRAKTID[who]:
		if os.path.exists(TRAKTID[who]['path']):
			act     = TRAKTID[who]['activate']
			addonid = wiz.addonId(TRAKTID[who]['plugin'])
			if act == '': addonid.openSettings()
			else: url = xbmc.executebuiltin(TRAKTID[who]['activate'])
		else: DIALOG.ok(ADDONTITLE, '%s is not currently installed.' % TRAKTID[who]['name'])
	else:
		wiz.refresh()
		return
	check = 0
	while traktUser(who) == None:
		if check == 30: break
		check += 1
		time.sleep(10)
	wiz.refresh()
