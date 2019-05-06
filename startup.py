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

import xbmc
import xbmcvfs

import os
import sys
import glob
import urllib
import re

from datetime import datetime
from datetime import timedelta

import uservar
from resources.libs import addon
from resources.libs import cache
from resources.libs import check
from resources.libs import gui
from resources.libs import logging
from resources.libs import notify
from resources.libs import skinSwitch
from resources.libs import tools
from resources.libs import update
from resources.libs import vars

SKINCHECK = ['skin.aftermath.zephyr', 'skin.aftermath.silvo', 'skin.aftermath.simple', 'skin.ccm.aftermath']
FAILED = False

########################
#    Check Updates     #
########################


def check_update():
	BUILDNAME = tools.get_setting('buildname')
	BUILDVERSION = tools.get_setting('buildversion')
	DISABLEUPDATE = tools.get_setting('disableupdate')

	bf = cache.text_cache(uservar.BUILDFILE)
	if not bf:
		return
	link = bf.replace('\n', '').replace('\r', '').replace('\t', '')
	match = re.compile('name="%s".+?ersion="(.+?)".+?con="(.+?)".+?anart="(.+?)"' % BUILDNAME).findall(link)
	if len(match) > 0:
		version = match[0][0]
		icon = match[0][1]
		fanart = match[0][2]
		tools.set_setting('latestversion', version)
		if version > BUILDVERSION:
			if DISABLEUPDATE == 'false':
				logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] Opening Update Window".format(BUILDVERSION, version), level=xbmc.LOGNOTICE)
				notify.updateWindow(BUILDNAME, BUILDVERSION, version, icon, fanart)
			else:
				logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] Update Window Disabled".format(BUILDVERSION, version), level=xbmc.LOGNOTICE)
		else:
			logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}]".format(BUILDVERSION, version), level=xbmc.LOGNOTICE)
	else:
		logging.log("[Check Updates] ERROR: Unable to find build version in build text file", level=xbmc.LOGERROR)


def check_installed():
	current = ''
	for skin in SKINCHECK:
		skinpath = os.path.join(vars.ADDONS, skin)
		if os.path.exists(skinpath):
			current = skin
	if current == SKINCHECK[0]:
		yes_pressed = gui.DIALOG.yesno(uservar.ADDONTITLE, "[COLOR dodgerblue]Aftermath[/COLOR] Zephyr is currently outdated and is no longer being updated.",
									   "Please download one of the newer community builds.",
									   yeslabel="Build Menu",
									   nolabel="Ignore")
		if yes_pressed:
			xbmc.executebuiltin('ActivateWindow(10025 , "plugin://%s/?mode=builds", return)' % uservar.ADDON_ID)
		else:
			gui.DIALOG.ok(uservar.ADDONTITLE, 'You can still install a community build from the [COLOR dodgerblue]Aftermath[/COLOR] Wizard.')
	elif current == SKINCHECK[1]:
		yes_pressed = gui.DIALOG.yesno(uservar.ADDONTITLE,"[COLOR dodgerblue]Aftermath[/COLOR] Silvo is currently outdated and is no longer being updated.", "Please download one of the newer community builds.", yeslabel="Build Menu", nolabel="Ignore")
		if yes_pressed:
			xbmc.executebuiltin('ActivateWindow(10025 , "plugin://%s/?mode=builds", return)' % uservar.ADDON_ID)
		else:
			gui.DIALOG.ok(uservar.ADDONTITLE, 'You can still install a community build from the [COLOR dodgerblue]Aftermath[/COLOR] Wizard.')
	elif current == SKINCHECK[2]:
		if vars.KODIV >= 16:
			gui_xml = os.path.join(vars.ADDOND, SKINCHECK[2], 'settings.xml')
			g = tools.read_from_file(gui_xml)
			match = re.compile('<setting id=\"SubSettings.3.Label\" type=\"string\">(.+?)<\/setting>').findall(g)
			if len(match):
				name, build, ver = match[0].replace('[COLOR dodgerblue]', '').replace('[/COLOR]', '').split(' ')
			else:
				build = "Simple"
				ver = "v0.1"
		else:
			gui_xml = os.path.join(vars.USERDATA,'guisettings.xml')
			g = tools.read_from_file(gui_xml)
			match = re.compile('<setting type=\"string\" name=\"skin.aftermath.simple.SubSettings.3.Label\">(.+?)<\/setting>').findall(g)
			name, build, ver = match[0].replace('[COLOR dodgerblue]', '').replace('[/COLOR]', '').split(' ')

		UPDATECHECK = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
		tools.set_setting('buildname', 'Aftermath {0}'.format(build))
		tools.set_setting('buildversion', ver[1:])
		tools.set_setting('lastbuildcheck', str(tools.get_date(days=UPDATECHECK)))
		check_update()
	elif current == SKINCHECK[3]:
		yes_pressed = gui.DIALOG.yesno(uservar.ADDONTITLE,"[COLOR dodgerblue]Aftermath[/COLOR] CCM is currently outdated and is no longer being updated.", "Please download one of the newer community builds.", yeslabel="Build Menu", nolabel="Ignore")
		if yes_pressed:	xbmc.executebuiltin('ActivateWindow(10025 , "plugin://%s/?mode=builds", return)' % uservar.ADDON_ID)
		else: gui.DIALOG.ok(uservar.ADDONTITLE, 'You can still install a community build from the [COLOR dodgerblue]Aftermath[/COLOR] Wizard.')
	else:
		notify.firstRunSettings()
		notify.firstRun()


def writeAdvanced():
	if vars.RAM > 1536: buffer = '209715200'
	else: buffer = '104857600'
	with open(vars.ADVANCED, 'w+') as f:
		f.write('<advancedsettings>\n')
		f.write('	<network>\n')
		f.write('		<buffermode>2</buffermode>\n')
		f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % buffer)
		f.write('		<readbufferfactor>5</readbufferfactor>\n')
		f.write('		<curlclienttimeout>10</curlclienttimeout>\n')
		f.write('		<curllowspeedtime>10</curllowspeedtime>\n')
		f.write('	</network>\n')
		f.write('</advancedsettings>\n')
	f.close()


def checkSkin():
	logging.log("[Build Check] Invalid Skin Check Start")
	DEFAULTSKIN   = tools.get_setting('defaultskin')
	DEFAULTNAME   = tools.get_setting('defaultskinname')
	DEFAULTIGNORE = tools.get_setting('defaultskinignore')
	gotoskin = False
	if not DEFAULTSKIN == '':
		if os.path.exists(os.path.join(vars.ADDONS, DEFAULTSKIN)):
			if gui.DIALOG.yesno(uservar.ADDONTITLE, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (uservar.COLOR2, uservar.COLOR1, vars.SKIN[5:].title()), "Would you like to set the skin back to:[/COLOR]", '[COLOR %s]%s[/COLOR]' % (uservar.COLOR1, DEFAULTNAME)):
				gotoskin = DEFAULTSKIN
				gotoname = DEFAULTNAME
			else:
				logging.log("Skin was not reset", level=xbmc.LOGNOTICE)
				tools.set_setting('defaultskinignore', 'true')
				gotoskin = False
		else: tools.set_setting('defaultskin', ''); tools.set_setting('defaultskinname', ''); DEFAULTSKIN = ''; DEFAULTNAME = ''
	if DEFAULTSKIN == '':
		skinname = []
		skinlist = []
		for folder in glob.glob(os.path.join(vars.ADDONS, 'skin.*/')):
			xml = "%s/addon.xml" % folder
			if os.path.exists(xml):
				g = tools.read_from_file(xml).replace('\n','').replace('\r','').replace('\t','')
				match = tools.parse_dom(g, 'addon', ret='id')
				match2 = tools.parse_dom(g, 'addon', ret='name')
				logging.log("%s: %s" % (folder, str(match[0])), xbmc.LOGNOTICE)
				if len(match) > 0: skinlist.append(str(match[0])); skinname.append(str(match2[0]))
				else: logging.log("ID not found for %s" % folder, xbmc.LOGNOTICE)
			else: logging.log("ID not found for %s" % folder, xbmc.LOGNOTICE)
		if len(skinlist) > 0:
			if len(skinlist) > 1:
				if gui.DIALOG.yesno(uservar.ADDONTITLE, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (uservar.COLOR2, uservar.COLOR1, vars.SKIN[5:].title()), "Would you like to view a list of avaliable skins?[/COLOR]"):
					choice = gui.DIALOG.select("Select skin to switch to!", skinname)
					if choice == -1: logging.log("Skin was not reset", xbmc.LOGNOTICE); tools.set_setting('defaultskinignore', 'true')
					else:
						gotoskin = skinlist[choice]
						gotoname = skinname[choice]
				else: logging.log("Skin was not reset", xbmc.LOGNOTICE); tools.set_setting('defaultskinignore', 'true')
			else:
				if gui.DIALOG.yesno(uservar.ADDONTITLE, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (uservar.COLOR2, uservar.COLOR1, vars.SKIN[5:].title()), "Would you like to set the skin back to:[/COLOR]", '[COLOR %s]%s[/COLOR]' % (uservar.COLOR1, skinname[0])):
					gotoskin = skinlist[0]
					gotoname = skinname[0]
				else: logging.log("Skin was not reset", xbmc.LOGNOTICE); tools.set_setting('defaultskinignore', 'true')
		else: logging.log("No skins found in addons folder.", xbmc.LOGNOTICE); tools.set_setting('defaultskinignore', 'true'); gotoskin = False
	if gotoskin:
		if skinSwitch.switch_to_skin(gotoskin):
			skinSwitch.look_and_feel_data('restore')
	logging.log("[Build Check] Invalid Skin Check End", xbmc.LOGNOTICE)


while xbmc.Player().isPlayingVideo():
	xbmc.sleep(1000)


if vars.KODIV >= 17:
	NOW = datetime.now()
	temp = tools.get_setting('kodi17iscrap')
	if not temp == '':
		if temp > str(NOW - timedelta(minutes=2)):
			logging.log("Killing Start Up Script")
			sys.exit()
	logging.log("%s" % (NOW))
	tools.set_setting('kodi17iscrap', str(NOW))
	xbmc.sleep(1000)
	if not tools.get_setting('kodi17iscrap') == str(NOW):
		logging.log("Killing Start Up Script")
		sys.exit()
	else:
		logging.log("Continuing Start Up Script")

logging.log("[Path Check] Started", xbmc.LOGNOTICE)
path = os.path.split(vars.PATH)
if not vars.ADDONID == path[1]: gui.DIALOG.ok(uservar.ADDONTITLE, '[COLOR %s]Please make sure that the plugin folder is the same as the ADDON_ID.[/COLOR]' % uservar.COLOR2, '[COLOR %s]Plugin ID:[/COLOR] [COLOR %s]%s[/COLOR]' % (uservar.COLOR2, uservar.COLOR1, vars.ADDONID), '[COLOR %s]Plugin Folder:[/COLOR] [COLOR %s]%s[/COLOR]' % (uservar.COLOR2, uservar.COLOR1, path)); logging.log("[Path Check] ADDON_ID and plugin folder doesnt match. %s / %s " % (vars.ADDONID, path))
else: logging.log("[Path Check] Good!", xbmc.LOGNOTICE)

if vars.KODIADDONS in vars.PATH:
	logging.log("Copying path to addons dir", xbmc.LOGNOTICE)
	if not os.path.exists(vars.ADDONS): os.makedirs(vars.ADDONS)
	newpath = vars.PLUGIN
	if os.path.exists(newpath):
		logging.log("Folder already exists, cleaning House", xbmc.LOGNOTICE)
		tools.clean_house(newpath)
		tools.remove_folder(newpath)
	try:
		tools.copytree(vars.PATH, newpath)
	except Exception:
		pass
	update.force_update(silent=True)

try:
	BACKUPLOCATION = tools.get_setting('path') if tools.get_setting('path') else vars.HOME
	MYBUILDS = os.path.join(BACKUPLOCATION, 'My_Builds')
	if not os.path.exists(MYBUILDS): xbmcvfs.mkdirs(MYBUILDS)
except:
	pass

logging.log("Flushing Aged Cached Text Files")
cache.flush_old_cache()

logging.log("[Auto Install Repo] Started", xbmc.LOGNOTICE)
if uservar.AUTOINSTALL == 'Yes' and not os.path.exists(os.path.join(vars.ADDONS, uservar.REPOID)):
	workingxml = check.check_url(uservar.REPOADDONXML)
	if workingxml:
		ver = tools.parse_dom(tools.open_url(uservar.REPOADDONXML), 'addon', ret='version', attrs={'id': uservar.REPOID})
		if len(ver) > 0:
			installzip = '%s-%s.zip' % (uservar.REPOID, ver[0])
			workingrepo = check.check_url(uservar.REPOZIPURL+installzip)
			if workingrepo:
				gui.DP.create(uservar.ADDONTITLE,'Downloading Repo...', '', 'Please Wait')
				if not os.path.exists(vars.PACKAGES):
					os.makedirs(vars.PACKAGES)
				lib = os.path.join(vars.PACKAGES, installzip)
				try:
					os.remove(lib)
				except:
					pass
				from resources.libs import downloader
				from resources.libs import extract
				downloader.download(uservar.REPOZIPURL+installzip,lib, gui.DP)
				extract.all(lib, vars.ADDONS, gui.DP)
				try:
					f = open(os.path.join(vars.ADDONS, uservar.REPOID, 'addon.xml'), mode='r'); g = f.read(); f.close()
					name = tools.parse_dom(g, 'addon', ret='name', attrs = {'id': uservar.REPOID})
					logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, name[0]), "[COLOR %s]Add-on updated[/COLOR]" % uservar.COLOR2, icon=os.path.join(vars.ADDONS, uservar.REPOID, 'icon.png'))
				except:
					pass
				if vars.KODIV >= 17:
					tools.addon_database(uservar.REPOID, 1)
				gui.DP.close()
				xbmc.sleep(500)
				update.force_update(silent=True)
				logging.log("[Auto Install Repo] Successfully Installed", xbmc.LOGNOTICE)
			else:
				logging.log_notify("[COLOR %s]Repo Install Error[/COLOR]" % uservar.COLOR1, "[COLOR %s]Invalid url for zip![/COLOR]" % uservar.COLOR2)
				logging.log("[Auto Install Repo] Was unable to create a working url for repository. %s" % workingrepo, xbmc.LOGERROR)
		else:
			logging.log("Invalid URL for Repo Zip", xbmc.LOGERROR)
	else:
		logging.log_notify("[COLOR %s]Repo Install Error[/COLOR]" % uservar.COLOR1, "[COLOR %s]Invalid addon.xml file![/COLOR]" % uservar.COLOR2)
		logging.log("[Auto Install Repo] Unable to read the addon.xml file.", xbmc.LOGERROR)
elif not uservar.AUTOINSTALL == 'Yes': logging.log("[Auto Install Repo] Not Enabled", xbmc.LOGNOTICE)
elif os.path.exists(os.path.join(vars.ADDONS, uservar.REPOID)): logging.log("[Auto Install Repo] Repository already installed")

logging.log("[Auto Update Wizard] Started", xbmc.LOGNOTICE)
if uservar.AUTOUPDATE == 'Yes':
	update.wizard_update('startup')
else: logging.log("[Auto Update Wizard] Not Enabled", xbmc.LOGNOTICE)

logging.log("[Notifications] Started", xbmc.LOGNOTICE)
if uservar.ENABLE == 'Yes':
	NOTIFY = tools.get_setting('notify')
	if not NOTIFY == 'true':
		url = check.check_url(uservar.NOTIFICATION)
		if url:
			id, msg = notify.split_notify(uservar.NOTIFICATION)
			if id:
				try:
					NOTEID = tools.get_setting('noteid')
					NOTEID = 0 if NOTEID == "" else int(NOTEID)
					id = int(id)
					if id == NOTEID:
						NOTEDISMISS = tools.get_setting('notedismiss')
						if NOTEDISMISS == 'false':
							notify.notification(msg)
						else: logging.log("[Notifications] id[%s] Dismissed" % int(id), xbmc.LOGNOTICE)
					elif id > NOTEID:
						logging.log("[Notifications] id: %s" % str(id), xbmc.LOGNOTICE)
						tools.set_setting('noteid', str(id))
						tools.set_setting('notedismiss', 'false')
						notify.notification(msg=msg)
						logging.log("[Notifications] Complete", xbmc.LOGNOTICE)
				except Exception as e:
					logging.log("Error on Notifications Window: %s" % str(e), xbmc.LOGERROR)
			else: logging.log("[Notifications] Text File not formated Correctly")
		else: logging.log("[Notifications] URL(%s): %s" % (uservar.NOTIFICATION, url), xbmc.LOGNOTICE)
	else: logging.log("[Notifications] Turned Off", xbmc.LOGNOTICE)
else: logging.log("[Notifications] Not Enabled", xbmc.LOGNOTICE)

logging.log("[Installed Check] Started", xbmc.LOGNOTICE)
INSTALLED = tools.get_setting('installed')
EXTRACT = tools.get_setting('extract')
EXTERROR = tools.get_setting('errors')

if INSTALLED == 'true':
	BUILDNAME = tools.get_setting('buildname')
	if vars.KODIV >= 17:
		addon.kodi_17_fix()
		if vars.SKIN in ['skin.confluence', 'skin.estuary']:
			checkSkin()
		FAILED = True
	elif not EXTRACT == '100' and not BUILDNAME == "":
		logging.log("[Installed Check] Build was extracted %s/100 with [ERRORS: %s]" % (EXTRACT, EXTERROR), xbmc.LOGNOTICE)
		yes = gui.DIALOG.yesno(uservar.ADDONTITLE, '[COLOR %s]%s[/COLOR] [COLOR %s]was not installed correctly!' % (uservar.COLOR1, uservar.COLOR2, BUILDNAME), 'Installed: [COLOR %s]%s[/COLOR] / Error Count: [COLOR %s]%s[/COLOR]' % (uservar.COLOR1, EXTRACT, uservar.COLOR1, EXTERROR), 'Would you like to try again?[/COLOR]', nolabel='[B]No Thanks![/B]', yeslabel='[B]Retry Install[/B]')
		tools.clear_setting('build')
		FAILED = True
		if yes:
			xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=fresh)" % (uservar.ADDON_ID, urllib.quote_plus(BUILDNAME)))
			logging.log("[Installed Check] Fresh Install Re-activated", xbmc.LOGNOTICE)
		else: logging.log("[Installed Check] Reinstall Ignored")
	elif vars.SKIN in ['skin.confluence', 'skin.estuary']:
		logging.log("[Installed Check] Incorrect skin: %s" % vars.SKIN, xbmc.LOGNOTICE)
		defaults = tools.get_setting('defaultskin')
		if not defaults == '':
			if os.path.exists(os.path.join(vars.ADDONS, defaults)):
				if skinSwitch.swap_to_skin(defaults):
					skinSwitch.look_and_feel_data('restore')
		if not vars.SKIN == defaults and not BUILDNAME == "":
			gui_xml = check.check_build(BUILDNAME, 'gui')
			FAILED = True
			if gui_xml == 'http://':
				logging.log("[Installed Check] Guifix was set to http://", xbmc.LOGNOTICE)
				gui.DIALOG.ok(uservar.ADDONTITLE, "[COLOR %s]It looks like the skin settings was not applied to the build." % uservar.COLOR2, "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close[/COLOR]")
			elif check.check_url(gui):
				yes = gui.DIALOG.yesno(uservar.ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'It looks like the skin settings was not applied to the build.', 'Would you like to apply the GuiFix?', nolabel='[B]No, Cancel[/B]', yeslabel='[B]Apply Fix[/B]')
				if yes: xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=gui)" % (uservar.ADDON_ID, urllib.quote_plus(BUILDNAME))); logging.log("[Installed Check] Guifix attempting to install")
				else: logging.log('[Installed Check] Guifix url working but cancelled: %s' % gui, xbmc.LOGNOTICE)
			else:
				gui.DIALOG.ok(uservar.ADDONTITLE, "[COLOR %s]It looks like the skin settings was not applied to the build." % uservar.COLOR2, "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close[/COLOR]")
				logging.log('[Installed Check] Guifix url not working: %s' % gui, xbmc.LOGNOTICE)
	else:
		logging.log('[Installed Check] Install seems to be completed correctly', xbmc.LOGNOTICE)
	if not tools.get_setting('pvrclient') == "":
		addon.toggle_addon(tools.get_setting('pvrclient'), 1)
		xbmc.executebuiltin('StartPVRManager')
	update.addon_updates('reset')

	KEEPTRAKT = tools.get_setting('keeptrakt')
	KEEPREAL = tools.get_setting('keepdebrid')
	KEEPLOGIN = tools.get_setting('keeplogin')

	if KEEPTRAKT == 'true':
		from resources.libs import traktit
		traktit.traktIt('restore', 'all')
		logging.log('[Installed Check] Restoring Trakt Data', level=xbmc.LOGNOTICE)
	if KEEPREAL == 'true':
		from resources.libs import debridit
		debridit.debridIt('restore', 'all')
		logging.log('[Installed Check] Restoring Real Debrid Data', level=xbmc.LOGNOTICE)
	if KEEPLOGIN == 'true':
		from resources.libs import loginit
		loginit.loginIt('restore', 'all')
		logging.log('[Installed Check] Restoring Login Data', level=xbmc.LOGNOTICE)
	tools.clear_setting('install')
else: logging.log("[Installed Check] Not Enabled", level=xbmc.LOGNOTICE)

if not FAILED:
	logging.log("[Build Check] Started", level=xbmc.LOGNOTICE)
	DEFAULTIGNORE = tools.get_setting('defaultskinignore')
	BUILDCHECK = tools.get_setting('lastbuildcheck')
	BUILDNAME = tools.get_setting('buildname')
	UPDATECHECK = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1

	if not check.check_url(uservar.BUILDFILE):
		logging.log("[Build Check] Not a valid URL for Build File: %s" % uservar.BUILDFILE, level=xbmc.LOGNOTICE)
	elif BUILDCHECK == '' and BUILDNAME == '':
		logging.log("[Build Check] First Run", level=xbmc.LOGNOTICE)
		check_installed()
		tools.set_setting('lastbuildcheck', str(tools.get_date(days=UPDATECHECK)))
	elif not BUILDNAME == '':
		logging.log("[Build Check] Build Installed", level=xbmc.LOGNOTICE)
		if vars.SKIN in ['skin.confluence', 'skin.estuary'] and not DEFAULTIGNORE == 'true':
			checkSkin()
			logging.log("[Build Check] Build Installed: Checking Updates", level=xbmc.LOGNOTICE)
			tools.set_setting('lastbuildcheck', str(tools.get_date(days=UPDATECHECK)))
			check_update()
		elif BUILDCHECK <= str(tools.get_date()):
			logging.log("[Build Check] Build Installed: Checking Updates", level=xbmc.LOGNOTICE)
			tools.set_setting('lastbuildcheck', str(tools.get_date(days=UPDATECHECK)))
			check_update()
		else:
			logging.log("[Build Check] Build Installed: Next check isn't until: %s / TODAY is: %s" % (BUILDCHECK, str(tools.get_date())), level=xbmc.LOGNOTICE)

logging.log("[Trakt Data] Started", level=xbmc.LOGNOTICE)

TRAKTSAVE = tools.get_setting('traktlastsave')
REALSAVE = tools.get_setting('debridlastsave')
LOGINSAVE = tools.get_setting('loginlastsave')
KEEPTRAKT = tools.get_setting('keeptrakt')
KEEPREAL = tools.get_setting('keepdebrid')
KEEPLOGIN = tools.get_setting('keeplogin')

if KEEPTRAKT == 'true':
	if TRAKTSAVE <= str(tools.get_date()):
		from resources.libs import traktit
		logging.log("[Trakt Data] Saving all Data", level=xbmc.LOGNOTICE)
		traktit.autoUpdate('all')
		tools.set_setting('traktlastsave', str(tools.get_date(days=3)))
	else:
		logging.log("[Trakt Data] Next Auto Save isn't until: %s / TODAY is: %s" % (TRAKTSAVE, str(tools.get_date())), level=xbmc.LOGNOTICE)
else: logging.log("[Trakt Data] Not Enabled", level=xbmc.LOGNOTICE)

logging.log("[Debrid Data] Started", level=xbmc.LOGNOTICE)
if KEEPREAL == 'true':
	if REALSAVE <= str(tools.get_date()):
		from resources.libs import debridit
		logging.log("[Debrid Data] Saving all Data", level=xbmc.LOGNOTICE)
		debridit.autoUpdate('all')
		tools.set_setting('debridlastsave', str(tools.get_date(days=3)))
	else:
		logging.log("[Debrid Data] Next Auto Save isn't until: %s / TODAY is: %s" % (REALSAVE, str(tools.get_date())), level=xbmc.LOGNOTICE)
else:
	logging.log("[Debrid Data] Not Enabled", level=xbmc.LOGNOTICE)

logging.log("[Login Info] Started", level=xbmc.LOGNOTICE)
if KEEPLOGIN == 'true':
	if LOGINSAVE <= str(tools.get_date()):
		from resources.libs import loginit
		logging.log("[Login Info] Saving all Data", level=xbmc.LOGNOTICE)
		loginit.autoUpdate('all')
		tools.set_setting('loginlastsave', str(tools.get_date(days=3)))
	else:
		logging.log("[Login Info] Next Auto Save isn't until: %s / TODAY is: %s" % (LOGINSAVE, str(tools.get_date())), level=xbmc.LOGNOTICE)
else: logging.log("[Login Info] Not Enabled", level=xbmc.LOGNOTICE)

logging.log("[Auto Clean Up] Started", level=xbmc.LOGNOTICE)
AUTOCLEANUP = tools.get_setting('autoclean')

if AUTOCLEANUP == 'true':
	service = False
	days = [tools.get_date(), tools.get_date(days=1), tools.get_date(days=3), tools.get_date(days=7)]

	AUTOFEQ = tools.get_setting('autocleanfeq')
	AUTOFEQ = int(AUTOFEQ) if AUTOFEQ.isdigit() else 0
	feq = int(float(AUTOFEQ))

	AUTONEXTRUN = tools.get_setting('nextautocleanup')
	if AUTONEXTRUN <= str(tools.get_date()) or feq == 0:
		service = True
		next_run = days[feq]
		tools.set_setting('nextautocleanup', str(next_run))
	else:
		logging.log("[Auto Clean Up] Next Clean Up %s" % AUTONEXTRUN, level=xbmc.LOGNOTICE)
	if service:
		AUTOCACHE = tools.get_setting('clearcache')
		AUTOPACKAGES = tools.get_setting('clearpackages')
		AUTOTHUMBS = tools.get_setting('clearthumbs')
		if AUTOCACHE == 'true':
			logging.log('[Auto Clean Up] Cache: On', level=xbmc.LOGNOTICE)
			cache.clear_cache(True)
		else:
			logging.log('[Auto Clean Up] Cache: Off', level=xbmc.LOGNOTICE)
		if AUTOTHUMBS == 'true':
			logging.log('[Auto Clean Up] Old Thumbs: On', level=xbmc.LOGNOTICE)
			cache.old_thumbs()
		else:
			logging.log('[Auto Clean Up] Old Thumbs: Off', level=xbmc.LOGNOTICE)
		if AUTOPACKAGES == 'true':
			logging.log('[Auto Clean Up] Packages: On', level=xbmc.LOGNOTICE)
			cache.clear_packages_startup()
		else:
			logging.log('[Auto Clean Up] Packages: Off', level=xbmc.LOGNOTICE)
else:
	logging.log('[Auto Clean Up] Turned off', level=xbmc.LOGNOTICE)

