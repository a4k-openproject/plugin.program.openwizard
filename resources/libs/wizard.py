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
import xbmcaddon
import xbmcvfs

import sys
import HTMLParser
import glob
import shutil
import re
import os

import urllib2
import urllib

try:
	from sqlite3 import dbapi2 as database
except ImportError:
	from pysqlite2 import dbapi2 as database

from datetime import datetime

from resources.libs.config import CONFIG
from resources.libs import downloader
from resources.libs import extract

KODIV = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if KODIV > 17:
	from resources.libs import zfile as zipfile
else:
	import zipfile

###########################
###### Display Items ######
###########################

# MIGRATION: move into gui
def highlightText(msg):
	msg = msg.replace('\n', '[NL]')
	matches = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(msg)
	for item in matches:
		string = '-->Python callback/script returned the following error<--%s-->End of Python script error report<--' % item
		msg    = msg.replace(string, '[COLOR red]%s[/COLOR]' % string)
	msg = msg.replace('WARNING', '[COLOR yellow]WARNING[/COLOR]').replace('ERROR', '[COLOR red]ERROR[/COLOR]').replace('[NL]', '\n').replace(': EXCEPTION Thrown (PythonToCppException) :', '[COLOR red]: EXCEPTION Thrown (PythonToCppException) :[/COLOR]')
	msg = msg.replace('\\\\', '\\').replace(HOME, '')
	return msg

###########################
###### Build Info #########
###########################

# MIGRATION: move into check
def buildCount(ver=None):
	link  = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?odi="(.+?)".+?dult="(.+?)"').findall(link)
	total = 0; count15 = 0; count16 = 0; count17 = 0; count18 = 0; hidden = 0; adultcount = 0
	if len(match) > 0:
		for name, kodi, adult in match:
			if not SHOWADULT == 'true' and adult.lower() == 'yes': hidden += 1; adultcount +=1; continue
			if not DEVELOPER == 'true' and strTest(name): hidden += 1; continue
			kodi = int(float(kodi))
			total += 1
			if kodi == 18: count18 += 1
			elif kodi == 17: count17 += 1
			elif kodi == 16: count16 += 1
			elif kodi <= 15: count15 += 1
	return total, count15, count16, count17, count18, adultcount, hidden


# MIGRATION: move into check
def themeCount(name, count=True):
	themefile = checkBuild(name, 'theme')
	if themefile == 'http://' or not themefile: return False
	link = openURL(themefile).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?dult="(.+?)"').findall(link)
	if len(match) == 0: return False
	themes = []
	for item, adult in match:
		if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
		themes.append(item)
	if len(themes) > 0:
		if count: return len(themes)
		else: return themes
	else: return False


# MIGRATION: move into db
def toggleDependency(name, DP=None):
	dep=os.path.join(ADDONS, name, 'addon.xml')
	if os.path.exists(dep):
		source = open(dep,mode='r'); link=source.read(); source.close();
		match  = parseDOM(link, 'import', ret='addon')
		for depends in match:
			if not 'xbmc.python' in depends:
				dependspath=os.path.join(ADDONS, depends)
				if not DP is None:
					DP.update("","Checking Dependency [COLOR yellow]%s[/COLOR] for [COLOR yellow]%s[/COLOR]" % (depends, name),"")
				if os.path.exists(dependspath):
					toggleAddon(name, 'true')
			xbmc.sleep(100)

# MIGRATION: move into db
def toggleAdult():
	do = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Enable[/COLOR] or [COLOR %s]Disable[/COLOR] all Adult addons?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Enable[/COLOR][/B]", nolabel="[B][COLOR red]Disable[/COLOR][/B]")
	state = 'true' if do == 1 else 'false'
	goto = 'Enabling' if do == 1 else 'Disabling'
	link = openURL('http://noobsandnerds.com/TI/AddonPortal/adult.php').replace('\n','').replace('\r','').replace('\t','')
	list = re.compile('i="(.+?)"').findall(link)
	found = []
	for item in list:
		fold = os.path.join(ADDONS, item)
		if os.path.exists(fold):
			found.append(item)
			toggleAddon(item, state, True)
			log("[Toggle Adult] %s %s" % (goto, item), xbmc.LOGNOTICE)
	if len(found) > 0:
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to view a list of the addons that where %s?[/COLOR]" % (COLOR2, goto.replace('ing', 'ed')), yeslabel="[B][COLOR springgreen]View List[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
			editlist = '[CR]'.join(found)
			TextBox(ADDONTITLE, "[COLOR %s]Here are a list of the addons that where %s for Adult Content:[/COLOR][CR][CR][COLOR %s]%s[/COLOR]" % (COLOR1, goto.replace('ing', 'ed'), COLOR2, editlist))
		else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s][COLOR %s]%d[/COLOR] Adult Addons %s[/COLOR]" % (COLOR2, COLOR1, count, goto.replace('ing', 'ed')))
		forceUpdate(True)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Adult Addons Found[/COLOR]" % COLOR2)

# MIGRATION: move into db
def createTemp(plugin):
	temp   = os.path.join(PLUGIN, 'resources', 'tempaddon.xml')
	f      = open(temp, 'r'); r = f.read(); f.close()
	plugdir = os.path.join(ADDONS, plugin)
	if not os.path.exists(plugdir): os.makedirs(plugdir)
	a = open(os.path.join(plugdir, 'addon.xml'), 'w')
	a.write(r.replace('testid', plugin).replace('testversion', '0.0.1'))
	a.close()
	log("%s: wrote addon.xml" % plugin)

# MIGRATION: move into db
def fixmetas():
	idlist = []
	#temp   = os.path.join(PLUGIN, 'resources', 'tempaddon.xml')
	#f      = open(temp, 'r'); r = f.read(); f.close()
	for item in idlist:
		fold = os.path.join(ADDOND, item)
		if os.path.exists(fold):
			storage = os.path.join(fold, '.storage')
			if os.path.exists(storage):
				cleanHouse(storage)
				removeFolder(storage)
			#if not os.path.exists(os.path.join(fold, 'addon.xml')): continue
			#a = open(os.path.join(fold, 'addon.xml'), 'w')
			#a.write(r.replace('testid', item).replace('testversion', '0.0.1'))
			#a.close()
			#log("%s: re-wrote addon.xml" % item)

# MIGRATION: move into gui
def whileWindow(window, active=False, count=0, counter=15):
	windowopen = getCond('Window.IsActive(%s)' % window)
	log("%s is %s" % (window, windowopen), xbmc.LOGDEBUG)
	while not windowopen and count < counter:
		log("%s is %s(%s)" % (window, windowopen, count))
		windowopen = getCond('Window.IsActive(%s)' % window)
		count += 1
		xbmc.sleep(500)

	while windowopen:
		active = True
		log("%s is %s" % (window, windowopen), xbmc.LOGDEBUG)
		windowopen = getCond('Window.IsActive(%s)' % window)
		xbmc.sleep(250)
	return active

# MIGRATION: move into backup
def cleanupBackup():
	mybuilds = xbmc.translatePath(MYBUILDS)
	folder = glob.glob(os.path.join(mybuilds, "*"))
	list = []; filelist = []
	if len(folder) == 0:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Backup Location: Empty[/COLOR]" % (COLOR2))
		return
	for item in sorted(folder, key=os.path.getmtime):
		filelist.append(item)
		base = item.replace(mybuilds, '')
		if os.path.isdir(item):
			list.append('/%s/' % base)
		elif os.path.isfile(item):
			list.append(base)
	list = ['--- Remove All Items ---'] + list
	selected = DIALOG.select("%s: Select the items to remove from 'MyBuilds'." % ADDONTITLE, list)

	if selected == -1:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Clean Up Cancelled![/COLOR]" % COLOR2)
	elif selected == 0:
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to clean up all items in your 'My_Builds' folder?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, MYBUILDS), yeslabel="[B][COLOR springgreen]Clean Up[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
			clearedfiles, clearedfolders = cleanHouse(xbmc.translatePath(MYBUILDS))
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Removed Files: [COLOR %s]%s[/COLOR] / Folders:[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, clearedfiles, COLOR1, clearedfolders))
		else:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Clean Up Cancelled![/COLOR]" % COLOR2)
	else:
		path = filelist[selected-1]; passed = False
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to remove [COLOR %s]%s[/COLOR] from 'My_Builds' folder?[/COLOR]" % (COLOR2, COLOR1, list[selected]), "[COLOR %s]%s[/COLOR]" % (COLOR1, path), yeslabel="[B][COLOR springgreen]Clean Up[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
			if os.path.isfile(path):
				try:
					os.remove(path)
					passed = True
				except:
					log("Unable to remove: %s" % path)
			else:
				cleanHouse(path)
				try:
					shutil.rmtree(path)
					passed = True
				except Exception as e:
					log("Error removing %s" % path, xbmc.LOGNOTICE)
			if passed: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Removed![/COLOR]" % (COLOR2, list[selected]))
			else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Error Removing %s![/COLOR]" % (COLOR2, list[selected]))
		else:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Clean Up Cancelled![/COLOR]" % COLOR2)

# MIGRATION: move into tools
def convertSpecial(url, over=False):
	total = fileCount(url); start = 0
	DP.create(ADDONTITLE, "[COLOR %s]Changing Physical Paths To Special" % COLOR2, "", "Please Wait[/COLOR]")
	for root, dirs, files in os.walk(url):
		for file in files:
			start += 1
			perc = int(percentage(start, total))
			if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
				DP.update(perc, "[COLOR %s]Scanning: [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, root.replace(HOME, '')), "[COLOR %s]%s[/COLOR]" % (COLOR1, file), "Please Wait[/COLOR]")
				a = open(os.path.join(root, file)).read()
				encodedpath  = urllib.quote(HOME)
				encodedpath2  = urllib.quote(HOME).replace('%3A','%3a').replace('%5C','%5c')
				b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
				f = open((os.path.join(root, file)), mode='w')
				f.write(str(b))
				f.close()
				if DP.iscanceled():
					DP.close()
					LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Convert Path Cancelled[/COLOR]" % COLOR2)
					sys.exit()
	DP.close()
	log("[Convert Paths to Special] Complete", xbmc.LOGNOTICE)
	if not over: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Convert Paths to Special: Complete![/COLOR]" % COLOR2)

# MIGRATION: move into db?
def hidePassword():
	if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]hide[/COLOR] all passwords when typing in the add-on settings menus?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Hide Passwords[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = parseDOM(f, 'addon', ret='id')
				for line in match:
					if 'pass' in line:
						if not 'option="hidden"' in line:
							try:
								change = line.replace('/', 'option="hidden" /')
								f.replace(line, change)
								count += 1
								log("[Hide Passwords] found in %s on %s" % (sett.replace(HOME, ''), line), xbmc.LOGDEBUG)
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("[COLOR %s]Hide Passwords[/COLOR]" % COLOR1, "[COLOR %s]%s items changed[/COLOR]" % (COLOR2, count))
		log("[Hide Passwords] %s items changed" % count, xbmc.LOGNOTICE)
	else: log("[Hide Passwords] Cancelled", xbmc.LOGNOTICE)

# MIGRATION: move into db?
def unhidePassword():
	if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]unhide[/COLOR] all passwords when typing in the add-on settings menus?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Unhide Passwords[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = parseDOM(f, 'addon', ret='id')
				for line in match:
					if 'pass' in line:
						if 'option="hidden"' in line:
							try:
								change = line.replace('option="hidden"', '')
								f.replace(line, change)
								count += 1
								log("[Unhide Passwords] found in %s on %s" % (sett.replace(HOME, ''), line), xbmc.LOGDEBUG)
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("[COLOR %s]Unhide Passwords[/COLOR]" % COLOR1, "[COLOR %s]%s items changed[/COLOR]" % (COLOR2, count))
		log("[Unhide Passwords] %s items changed" % count, xbmc.LOGNOTICE)
	else: log("[Unhide Passwords] Cancelled", xbmc.LOGNOTICE)


# MIGRATION: move into tools?
def asciiCheck(use=None, over=False):
	if use is None:
		source = DIALOG.browse(3, '[COLOR %s]Select the folder you want to scan[/COLOR]' % COLOR2, 'files', '', False, False, HOME)
		if over:
			yes = 1
		else:
			yes = DIALOG.yesno(ADDONTITLE,'[COLOR %s]Do you want to [COLOR %s]delete[/COLOR] all filenames with special characters or would you rather just [COLOR %s]scan and view[/COLOR] the results in the log?[/COLOR]' % (COLOR2, COLOR1, COLOR1), yeslabel='[B][COLOR springgreen]Delete[/COLOR][/B]', nolabel='[B][COLOR red]Scan[/COLOR][/B]')
	else:
		source = use
		yes = 1

	if source == "":
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: Cancelled[/COLOR]" % COLOR2)
		return

	files_found  = os.path.join(ADDONDATA, 'asciifiles.txt')
	files_fails  = os.path.join(ADDONDATA, 'asciifails.txt')
	afiles       = open(files_found, mode='w+')
	afails       = open(files_fails, mode='w+')
	f1           = 0; f2           = 0
	items        = fileCount(source)
	msg          = ''
	prog         = []
	log("Source file: (%s)" % str(source), xbmc.LOGNOTICE)

	DP.create(ADDONTITLE, 'Please wait...')
	for base, dirs, files in os.walk(source):
		dirs[:] = [d for d in dirs]
		files[:] = [f for f in files]
		for file in files:
			prog.append(file)
			prog2 = int(len(prog) / float(items) * 100)
			DP.update(prog2,"[COLOR %s]Checking for non ASCII files" % COLOR2,'[COLOR %s]%s[/COLOR]' % (COLOR1, d), 'Please Wait[/COLOR]')
			try:
				file.encode('ascii')
			except UnicodeEncodeError:
				log("[ASCII Check] Illegal character found in file: {0}".format(file))
			except UnicodeDecodeError:
				log("[ASCII Check] Illegal character found in file: {0}".format(file))
				badfile = os.path.join(base, file)
				if yes:
					try:
						os.remove(badfile)
						for chunk in chunks(badfile, 75):
							afiles.write(chunk+'\n')
						afiles.write('\n')
						f1 += 1
						log("[ASCII Check] File Removed: %s " % badfile, xbmc.LOGERROR)
					except:
						for chunk in chunks(badfile, 75):
							afails.write(chunk+'\n')
						afails.write('\n')
						f2 += 1
						log("[ASCII Check] File Failed: %s " % badfile, xbmc.LOGERROR)
				else:
					for chunk in chunks(badfile, 75):
						afiles.write(chunk+'\n')
					afiles.write('\n')
					f1 += 1
					log("[ASCII Check] File Found: %s " % badfile, xbmc.LOGERROR)
				pass
		if DP.iscanceled():
			DP.close()
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Ascii Check Cancelled[/COLOR]" % COLOR2)
			sys.exit()
	DP.close(); afiles.close(); afails.close()
	total = int(f1) + int(f2)
	if total > 0:
		if os.path.exists(files_found): afiles = open(files_found, mode='r'); msg = afiles.read(); afiles.close()
		if os.path.exists(files_fails): afails = open(files_fails, mode='r'); msg2 = afails.read(); afails.close()
		if yes:
			if use:
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: %s Removed / %s Failed.[/COLOR]" % (COLOR2, f1, f2))
			else:
				TextBox(ADDONTITLE, "[COLOR yellow][B]%s Files Removed:[/B][/COLOR]\n %s\n\n[COLOR yellow][B]%s Files Failed:[B][/COLOR]\n %s" % (f1, msg, f2, msg2))
		else:
			TextBox(ADDONTITLE, "[COLOR yellow][B]%s Files Found:[/B][/COLOR]\n %s" % (f1, msg))
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: None Found.[/COLOR]" % COLOR2)

def fileCount(home, excludes=True):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'packages', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'library', 'keymaps']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	item = []
	for base, dirs, files in os.walk(home):
		if excludes:
			dirs[:] = [d for d in dirs if d not in exclude_dirs]
			files[:] = [f for f in files if f not in exclude_files]
		for file in files:
			item.append(file)
	return len(item)

# MIGRATION: move into advanced?
def convertAdvanced():
	if os.path.exists(ADVANCED):
		f = open(ADVANCED)
		a = f.read()
		if KODIV >= 17:
			return
		else:
			return
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]AdvancedSettings.xml not found[/COLOR]")

##########################
###BACK UP/RESTORE #######
##########################
def backUpOptions(type, name=""):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'keymaps', 'cdm']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	## TODO: fix these
	bad_files     = [
					(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.gaia', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.gaia', 'meta.db')),
					(os.path.join(ADDOND, 'plugin.video.seren', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.seren', 'torrentScrape.db')),
					(os.path.join(ADDOND, 'script.module.simplecache', 'simplecache.db'))]

	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	try:
		if not os.path.exists(backup): xbmcvfs.mkdirs(backup)
		if not os.path.exists(mybuilds): xbmcvfs.mkdirs(mybuilds)
	except Exception as e:
		DIALOG.ok(ADDONTITLE, "[COLOR %s]Error making Back Up directories:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
		return
	if type == "addon pack":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Are you sure you wish to create an Addon Pack?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Cancel Backup[/COLOR][/B]", yeslabel="[B][COLOR springgreen]Create Pack[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Please enter a name for the %s zip" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			name = '%s.zip' % name; tempzipname = ''
			zipname = os.path.join(mybuilds, name)
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Unable to create %s.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]We are unable to write to the current backup directory, would you like to change the location?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Change Directory[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
						openS()
						return
					else:
						return
			fold = glob.glob(os.path.join(ADDONS, '*/'))
			addonnames = []; addonfolds = []
			for folder in sorted(fold, key = lambda x: x):
				foldername = os.path.split(folder[:-1])[1]
				if foldername in EXCLUDES: continue
				elif foldername in DEFAULTPLUGINS: continue
				elif foldername == 'packages': continue
				xml = os.path.join(folder, 'addon.xml')
				if os.path.exists(xml):
					f      = open(xml)
					a      = f.read()
					match  = parseDOM(a, 'addon', ret='name')
					if len(match) > 0:
						addonnames.append(match[0])
						addonfolds.append(foldername)
					else:
						addonnames.append(foldername)
						addonfolds.append(foldername)
			if KODIV > 16:
				selected = DIALOG.multiselect("%s: Select the addons you wish to add to the zip." % ADDONTITLE, addonnames)
				if selected is None: selected = []
			else:
				selected = []; choice = 0
				tempaddonnames = ["-- Click here to Continue --"] + addonnames
				while not choice == -1:
					choice = DIALOG.select("%s: Select the addons you wish to add to the zip." % ADDONTITLE, tempaddonnames)
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
			log(selected)
			DP.create(ADDONTITLE,'[COLOR %s][B]Creating Zip File:[/B][/COLOR]' % COLOR2,'', 'Please Wait')
			if len(selected) > 0:
				added = []
				for item in selected:
					added.append(addonfolds[item])
					DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, addonfolds[item]))
					for base, dirs, files in os.walk(os.path.join(ADDONS,addonfolds[item])):
						files[:] = [f for f in files if f not in exclude_files]
						for file in files:
							if file.endswith('.pyo'): continue
							DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, addonfolds[item]), "[COLOR %s]%s[/COLOR]" % (COLOR1, file))
							fn = os.path.join(base, file)
							zipf.write(fn, fn[len(ADDONS):], zipfile.ZIP_DEFLATED)
					dep=os.path.join(ADDONS,addonfolds[item],'addon.xml')
					if os.path.exists(dep):
						source = open(dep,mode='r'); link = source.read(); source.close();
						match  = parseDOM(link, 'import', ret='addon')
						for depends in match:
							if 'xbmc.python' in depends: continue
							if depends in added: continue
							DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, depends))
							for base, dirs, files in os.walk(os.path.join(ADDONS,depends)):
								files[:] = [f for f in files if f not in exclude_files]
								for file in files:
									if file.endswith('.pyo'): continue
									DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, depends), "[COLOR %s]%s[/COLOR]" % (COLOR1, file))
									fn = os.path.join(base, file)
									zipf.write(fn, fn[len(ADDONS):], zipfile.ZIP_DEFLATED)
									added.append(depends)
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]backup successful:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "build":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Are you sure you wish to backup the current build?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Cancel Backup[/COLOR][/B]", yeslabel="[B][COLOR springgreen]Backup Build[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Please enter a name for the %s zip" % type)
				if not name: return False
				name = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			name = urllib.quote_plus(name); tempzipname = ''
			zipname = os.path.join(mybuilds, '%s.zip' % name)
			for_progress  = 0
			ITEM          = []
			if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you want to include your addon_data folder?" % COLOR2, 'This contains [COLOR %s]ALL[/COLOR] addon settings including passwords but may also contain important information such as skin shortcuts. We recommend [COLOR %s]MANUALLY[/COLOR] removing the addon_data folders that aren\'t required.' % (COLOR1, COLOR1), '[COLOR %s]%s[/COLOR] addon_data is ignored[/COLOR]' % (COLOR1, ADDON_ID), yeslabel='[B][COLOR springgreen]Include data[/COLOR][/B]',nolabel='[B][COLOR red]Don\'t Include[/COLOR][/B]'):
				exclude_dirs.append('addon_data')
			convertSpecial(HOME, True)
			asciiCheck(HOME, True)
			extractsize = 0
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Unable to create %s.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]We are unable to write to the current backup directory, would you like to change the location?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Change Directory[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
						openS()
						return
					else:
						return
			DP.create("[COLOR %s]%s[/COLOR][COLOR %s]: Creating Zip[/COLOR]" % (COLOR1, ADDONTITLE,COLOR2), "[COLOR %s]Creating back up zip" % COLOR2, "", "Please Wait...[/COLOR]")
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			picture = []; music = []; video = []; programs = []; repos = []; scripts = []; skins = []
			fold = glob.glob(os.path.join(ADDONS, '*/'))
			idlist = []
			for folder in sorted(fold, key = lambda x: x):
				foldername = os.path.split(folder[:-1])[1]
				if foldername == 'packages': continue
				xml = os.path.join(folder, 'addon.xml')
				if os.path.exists(xml):
					f      = open(xml)
					a      = f.read()
					prov   = re.compile("<provides>(.+?)</provides>").findall(a)
					match  = parseDOM(a, 'addon', ret='id')

					addid  = foldername if len(match) == 0 else match[0]
					if addid in idlist:
						continue
					idlist.append(addid)
					try:
						add   = xbmcaddon.Addon(id=addid)
						aname = add.getAddonInfo('name')
						aname = aname.replace('[', '<').replace(']', '>')
						aname = str(re.sub('<[^<]+?>', '', aname)).lstrip()
					except:
						aname = foldername
					if len(prov) == 0:
						if   foldername.startswith('skin'): skins.append(aname)
						elif foldername.startswith('repo'): repos.append(aname)
						else: scripts.append(aname)
						continue
					if not (prov[0]).find('executable') == -1: programs.append(aname)
					if not (prov[0]).find('video') == -1: video.append(aname)
					if not (prov[0]).find('audio') == -1: music.append(aname)
					if not (prov[0]).find('image') == -1: picture.append(aname)
			fixmetas()
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM)
						DP.update(int(progress), '[COLOR %s]Creating back up zip: [COLOR%s]%s[/COLOR] / [COLOR%s]%s[/COLOR]' % (COLOR2, COLOR1, for_progress, COLOR1, N_ITEM), '[COLOR %s]%s[/COLOR]' % (COLOR1, file), '')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(ADDONS, 'inputstream.adaptive') in fn: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.pyo'): continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
								if not file == latestDB(temp):  log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
							extractsize += os.path.getsize(fn)
						except Exception as e:
							log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
							log("%s / %s" % (Exception, e))
						if DP.iscanceled():
							DP.close()
							LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Backup Cancelled[/COLOR]" % COLOR2)
							sys.exit()
					except Exception as e:
						log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
						log("Build Backup Error: %s" % str(e), xbmc.LOGNOTICE)
			if 'addon_data' in exclude_dirs:
				match = glob.glob(os.path.join(ADDOND,'skin.*', ''))
				for fold in match:
					fd = os.path.split(fold[:-1])[1]
					if not fd in ['skin.confluence', 'skin.re-touch', 'skin.estuary', 'skin.estouchy']:
						for base, dirs, files in os.walk(os.path.join(ADDOND,fold)):
							files[:] = [f for f in files if f not in exclude_files]
							for file in files:
								fn = os.path.join(base, file)
								zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
								extractsize += os.path.getsize(fn)
						xml   = os.path.join(ADDONS, fd, 'addon.xml')
						if os.path.exists(xml):
							source   = open(xml,mode='r'); link = source.read(); source.close();
							matchxml = parseDOM(link, 'import', ret='addon')
							if 'script.skinshortcuts' in matchxml:
								for base, dirs, files in os.walk(os.path.join(ADDOND,'script.skinshortcuts')):
									files[:] = [f for f in files if f not in exclude_files]
									for file in files:
										fn = os.path.join(base, file)
										zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
										extractsize += os.path.getsize(fn)
			zipf.close()
			xbmc.sleep(500)
			DP.close()
			backUpOptions('guifix', name)
			if not tempzipname == '':
				success = xbmcvfs.rename(tempzipname, zipname)
				if success == 0:
					xbmcvfs.copy(tempzipname, zipname)
					xbmcvfs.delete(tempzipname)
			info = zipname.replace('.zip', '.txt')
			f = open(info, 'w'); f.close()
			with open(info, 'a') as f:
				f.write('name="%s"\n' % name)
				f.write('extracted="%s"\n' % extractsize)
				f.write('zipsize="%s"\n' % os.path.getsize(xbmc.translatePath(zipname)))
				f.write('skin="%s"\n' % currSkin())
				f.write('created="%s"\n' % datetime.now().date())
				f.write('programs="%s"\n' % ', '.join(programs) if len(programs) > 0 else 'programs="none"\n')
				f.write('video="%s"\n' % ', '.join(video) if len(video) > 0 else 'video="none"\n')
				f.write('music="%s"\n' % ', '.join(music) if len(music) > 0 else 'music="none"\n')
				f.write('picture="%s"\n' % ', '.join(picture) if len(picture) > 0 else 'picture="none"\n')
				f.write('repos="%s"\n' % ', '.join(repos) if len(repos) > 0 else 'repos="none"\n')
				f.write('scripts="%s"\n' % ', '.join(scripts) if len(scripts) > 0 else 'scripts="none"\n')
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]backup successful:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "guifix":
		if name == "":
			guiname = getKeyboard("","Please enter a name for the %s zip" % type)
			if not guiname: return False
			convertSpecial(USERDATA, True)
			asciiCheck(USERDATA, True)
		else: guiname = name
		guiname = urllib.quote_plus(guiname); tempguizipname = ''
		guizipname = xbmc.translatePath(os.path.join(mybuilds, '%s_guisettings.zip' % guiname))
		if os.path.exists(GUISETTINGS):
			try:
				zipf = zipfile.ZipFile(guizipname, mode='w')
			except:
				try:
					tempguizipname = os.path.join(PACKAGES, '%s_guisettings.zip' % guiname)
					zipf = zipfile.ZipFile(tempguizipname, mode='w')
				except:
					log("Unable to create %s_guisettings.zip" % guiname, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]We are unable to write to the current backup directory, would you like to change the location?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Change Directory[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
						openS()
						return
					else:
						return
			try:
				zipf.write(GUISETTINGS, 'guisettings.xml', zipfile.ZIP_DEFLATED)
				zipf.write(PROFILES,    'profiles.xml',    zipfile.ZIP_DEFLATED)
				match = glob.glob(os.path.join(ADDOND,'skin.*', ''))
				for fold in match:
					fd = os.path.split(fold[:-1])[1]
					if not fd in ['skin.confluence', 'skin.re-touch', 'skin.estuary', 'skin.estouchy']:
						if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to add the following skin folder to the GuiFix Zip File?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, fd), yeslabel="[B][COLOR springgreen]Add Skin[/COLOR][/B]", nolabel="[B][COLOR red]Skip Skin[/COLOR][/B]"):
							for base, dirs, files in os.walk(os.path.join(ADDOND,fold)):
								files[:] = [f for f in files if f not in exclude_files]
								for file in files:
									fn = os.path.join(base, file)
									zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
							xml   = os.path.join(ADDONS, fd, 'addon.xml')
							if os.path.exists(xml):
								source   = open(xml,mode='r'); link = source.read(); source.close();
								matchxml = parseDOM(link, 'import', ret='addon')
								if 'script.skinshortcuts' in matchxml:
									for base, dirs, files in os.walk(os.path.join(ADDOND,'script.skinshortcuts')):
										files[:] = [f for f in files if f not in exclude_files]
										for file in files:
											fn = os.path.join(base, file)
											zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
						else: log("[Back Up] Type = '%s': %s ignored" % (type, fold), xbmc.LOGNOTICE)
			except Exception as e:
				log("[Back Up] Type = '%s': %s" % (type, e), xbmc.LOGNOTICE)
				pass
			zipf.close()
			if not tempguizipname == '':
				success = xbmcvfs.rename(tempguizipname, guizipname)
				if success == 0:
					xbmcvfs.copy(tempguizipname, guizipname)
					xbmcvfs.delete(tempguizipname)
		else: log("[Back Up] Type = '%s': guisettings.xml not found" % type, xbmc.LOGNOTICE)
		if name == "":
			DIALOG.ok(ADDONTITLE, "[COLOR %s]GuiFix backup successful:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, guizipname))
	elif type == "theme":
		if not DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to create a theme backup?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Continue[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"): LogNotify("Theme Backup", "Cancelled!"); return False
		if name == "":
			themename = getKeyboard("","Please enter a name for the %s zip" % type)
			if not themename: return False
		else: themename = name
		themename = urllib.quote_plus(themename); tempzipname = ''
		zipname = os.path.join(mybuilds, '%s.zip' % themename)
		try:
			zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
		except:
			try:
				tempzipname = os.path.join(PACKAGES, '%s.zip' % themename)
				zipf = zipfile.ZipFile(tempzipname, mode='w')
			except:
				log("Unable to create %s.zip" % themename, xbmc.LOGERROR)
				if DIALOG.yesno(ADDONTITLE, "[COLOR %s]We are unable to write to the current backup directory, would you like to change the location?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Change Directory[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
					openS()
					return
				else:
					return
		convertSpecial(USERDATA, True)
		asciiCheck(USERDATA, True)
		try:
			if not SKIN == 'skin.confluence':
				skinfold = os.path.join(ADDONS, SKIN, 'media')
				match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
				if len(match2) > 1:
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to go through the Texture Files for?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Add Textures[/COLOR][/B]", nolabel="[B][COLOR red]Skip Textures[/COLOR][/B]"):
						skinfold = os.path.join(ADDONS, SKIN, 'media')
						match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
						for xbt in match2:
							if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to add the Texture File [COLOR %s]%s[/COLOR]?" % (COLOR1, COLOR2, xbt.replace(skinfold, "")[1:]), "from [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Add Textures[/COLOR][/B]", nolabel="[B][COLOR red]Skip Textures[/COLOR][/B]"):
								fn  = xbt
								fn2 = fn.replace(HOME, "")
								zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				else:
					for xbt in match2:
						if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to add the Texture File [COLOR %s]%s[/COLOR]?" % (COLOR2, COLOR1, xbt.replace(skinfold, "")[1:]), "from [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Add Textures[/COLOR][/B]", nolabel="[B][COLOR red]Skip Textures[/COLOR][/B]"):
							fn  = xbt
							fn2 = fn.replace(HOME, "")
							zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				ad_skin = os.path.join(ADDOND, SKIN, 'settings.xml')
				if os.path.exists(ad_skin):
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to go add the [COLOR %s]settings.xml[/COLOR] in [COLOR %s]/addon_data/[/COLOR] for?" % (COLOR2, COLOR1, COLOR1), "[COLOR %s]%s[/COLOR]"  % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Add Settings[/COLOR][/B]", nolabel="[B][COLOR red]Skip Settings[/COLOR][/B]"):
						skinfold = os.path.join(ADDOND, SKIN)
						zipf.write(ad_skin, ad_skin.replace(HOME, ""), zipfile.ZIP_DEFLATED)
				f = open(os.path.join(ADDONS, SKIN, 'addon.xml')); r = f.read(); f.close()
				match  = parseDOM(r, 'import', ret='addon')
				if 'script.skinshortcuts' in match:
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to go add the [COLOR %s]settings.xml[/COLOR] for [COLOR %s]script.skinshortcuts[/COLOR]?" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Add Settings[/COLOR][/B]", nolabel="[B][COLOR red]Skip Settings[/COLOR][/B]"):
						for base, dirs, files in os.walk(os.path.join(ADDOND,'script.skinshortcuts')):
							files[:] = [f for f in files if f not in exclude_files]
							for file in files:
								fn = os.path.join(base, file)
								zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to include a [COLOR %s]Backgrounds[/COLOR] folder?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Yes Include[/COLOR][/B]", nolabel="[B][COLOR red]No Continue[/COLOR][/B]"):
				fn = DIALOG.browse(0, 'Select location of backgrounds', 'files', '', True, False, HOME, False)
				if not fn == HOME:
					for base, dirs, files in os.walk(fn):
						dirs[:] = [d for d in dirs if d not in exclude_dirs]
						files[:] = [f for f in files if f not in exclude_files]
						for file in files:
							try:
								fn2 = os.path.join(base, file)
								zipf.write(fn2, fn2[len(HOME):], zipfile.ZIP_DEFLATED)
							except Exception as e:
								log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
								log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
				text = latestDB('Textures')
				if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to include the [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, text), yeslabel="[B][COLOR springgreen]Yes Include[/COLOR][/B]", nolabel="[B][COLOR red]No Continue[/COLOR][/B]"):
					zipf.write(os.path.join(DATABASE, text), '/userdata/Database/%s' % text, zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to include any addons?[/COLOR]" % (COLOR2), yeslabel="[B][COLOR springgreen]Yes Include[/COLOR][/B]", nolabel="[B][COLOR red]No Continue[/COLOR][/B]"):
				fold = glob.glob(os.path.join(ADDONS, '*/'))
				addonnames = []; addonfolds = []
				for folder in sorted(fold, key = lambda x: x):
					foldername = os.path.split(folder[:-1])[1]
					if foldername in EXCLUDES: continue
					elif foldername in DEFAULTPLUGINS: continue
					elif foldername == 'packages': continue
					xml = os.path.join(folder, 'addon.xml')
					if os.path.exists(xml):
						f      = open(xml)
						a      = f.read()
						match  = parseDOM(a, 'addon', ret='name')
						if len(match) > 0:
							addonnames.append(match[0])
							addonfolds.append(foldername)
						else:
							addonnames.append(foldername)
							addonfolds.append(foldername)
				if KODIV > 16:
					selected = DIALOG.multiselect("%s: Select the addons you wish to add to the zip." % ADDONTITLE, addonnames)
					if selected == None: selected = []
				else:
					selected = []; choice = 0
					tempaddonnames = ["-- Click here to Continue --"] + addonnames
					while not choice == -1:
						choice = DIALOG.select("%s: Select the addons you wish to add to the zip." % ADDONTITLE, tempaddonnames)
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
				if len(selected) > 0:
					added = []
					for item in selected:
						added.append(addonfolds[item])
						for base, dirs, files in os.walk(os.path.join(ADDONS,addonfolds[item])):
							files[:] = [f for f in files if f not in exclude_files]
							for file in files:
								if file.endswith('.pyo'): continue
								fn = os.path.join(base, file)
								zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
						dep=os.path.join(ADDONS,addonfolds[item],'addon.xml')
						if os.path.exists(dep):
							source = open(dep,mode='r'); link = source.read(); source.close();
							match  = parseDOM(link, 'import', ret='addon')
							for depends in match:
								if 'xbmc.python' in depends: continue
								if depends in added: continue
								for base, dirs, files in os.walk(os.path.join(ADDONS,depends)):
									files[:] = [f for f in files if f not in exclude_files]
									for file in files:
										if file.endswith('.pyo'): continue
										fn = os.path.join(base, file)
										zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
										added.append(depends)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]Would you like to include the [COLOR %s]guisettings.xml[/COLOR]?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Yes Include[/COLOR][/B]", nolabel="[B][COLOR red]No Continue[/COLOR][/B]"):
				zipf.write(GUISETTINGS, '/userdata/guisettings.xml', zipfile.ZIP_DEFLATED)
		except Exception as e:
			zipf.close()
			log("[Back Up] Type = '%s': %s" % (type, str(e)), xbmc.LOGNOTICE)
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] theme zip failed:[/COLOR]" % (COLOR1, themename, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
			if not tempzipname == '':
				try: os.remove(xbmc.translatePath(tempzipname))
				except Exception as e: log(str(e))
			else:
				try: os.remove(xbmc.translatePath(zipname))
				except Exception as e: log(str(e))
			return
		zipf.close()
		if not tempzipname == '':
			success = xbmcvfs.rename(tempzipname, zipname)
			if success == 0:
				xbmcvfs.copy(tempzipname, zipname)
				xbmcvfs.delete(tempzipname)
		DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] theme zip successful:[/COLOR]" % (COLOR1, themename, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "addondata":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Are you sure you wish to backup the current addon_data?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Cancel Backup[/COLOR][/B]", yeslabel="[B][COLOR springgreen]Backup Addon_Data[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Please enter a name for the %s zip" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			name = '%s_addondata.zip' % name; tempzipname = ''
			zipname = os.path.join(mybuilds, name)
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Unable to create %s_addondata.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]We are unable to write to the current backup directory, would you like to change the location?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Change Directory[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
						openS()
						return
					else:
						return
			for_progress  = 0
			ITEM          = []
			convertSpecial(ADDOND, True)
			asciiCheck(ADDOND, True)
			DP.create("[COLOR %s]%s[/COLOR][COLOR %s]: Creating Zip[/COLOR]" % (COLOR1, ADDONTITLE,COLOR2), "[COLOR %s]Creating back up zip" % COLOR2, "", "Please Wait...[/COLOR]")
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM)
						DP.update(int(progress), '[COLOR %s]Creating back up zip: [COLOR%s]%s[/COLOR] / [COLOR%s]%s[/COLOR]' % (COLOR2, COLOR1, for_progress, COLOR1, N_ITEM), '[COLOR %s]%s[/COLOR]' % (COLOR1, file), '')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
								if not file == latestDB(temp):  log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(ADDOND):], zipfile.ZIP_DEFLATED)
						except Exception as e:
							log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
							log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
					except Exception as e:
						log("[Back Up] Type = '%s': Unable to backup %s" % (type, file), xbmc.LOGNOTICE)
						log("Backup Error: %s" % str(e), xbmc.LOGNOTICE)
			zipf.close()
			if not tempzipname == '':
				success = xbmcvfs.rename(tempzipname, zipname)
				if success == 0:
					xbmcvfs.copy(tempzipname, zipname)
					xbmcvfs.delete(tempzipname)
			DP.close()
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]backup successful:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))

def restoreLocal(type):
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	try:
		if not os.path.exists(backup): xbmcvfs.mkdirs(backup)
		if not os.path.exists(mybuilds): xbmcvfs.mkdirs(mybuilds)
	except Exception as e:
		DIALOG.ok(ADDONTITLE, "[COLOR %s]Error making Back Up directories:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
		return
	file = DIALOG.browse(1, '[COLOR %s]Select the backup file you want to restore[/COLOR]' % COLOR2, 'files', '.zip', False, False, mybuilds)
	log("[RESTORE BACKUP %s] File: %s " % (type.upper(), file), xbmc.LOGNOTICE)
	if file == "" or not file.endswith('.zip'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Local Restore: Cancelled[/COLOR]" % COLOR2)
		return
	DP.create(ADDONTITLE,'[COLOR %s]Installing Local Backup' % COLOR2,'', 'Please Wait[/COLOR]')
	if not os.path.exists(USERDATA): os.makedirs(USERDATA)
	if not os.path.exists(ADDOND): os.makedirs(ADDOND)
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	if type == "gui": loc = USERDATA
	elif type == "addondata":
		loc = ADDOND
	else : loc = HOME
	log("Restoring to %s" % loc, xbmc.LOGNOTICE)
	display = os.path.split(file)
	fn = display[1]
	try:
		zipfile.ZipFile(file,  'r')
	except:
		DP.update(0, '[COLOR %s]Unable to read zipfile from current location.' % COLOR2, 'Copying file to packages')
		pack = os.path.join('special://home', 'addons', 'packages', fn)
		xbmcvfs.copy(file, pack)
		file = xbmc.translatePath(pack)
		DP.update(0, '', 'Copying file to packages: Complete')
		zipfile.ZipFile(file, 'r')
	percent, errors, error = extract.all(file,loc,DP)
	fixmetas()
	clearS('build')
	DP.close()
	defaultSkin()
	lookandFeelData('save')
	if not file.find('packages') == -1:
		try: os.remove(file)
		except: pass
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, fn), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B][COLOR red]No Thanks[/COLOR][/B]',yeslabel='[B][COLOR springgreen]View Errors[/COLOR][/B]')
		if yes:
			if isinstance(errors, unicode):
				error = error.encode('utf-8')
			TextBox(ADDONTITLE, error.replace('\t',''))
	setS('installed', 'true')
	setS('extract', str(percent))
	setS('errors', str(errors))
	if INSTALLMETHOD == 1: todo = 1
	elif INSTALLMETHOD == 2: todo = 0
	else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
	if todo == 1: reloadFix()
	else: killxbmc(True)

def restoreExternal(type):
	source = DIALOG.browse(1, '[COLOR %s]Select the backup file you want to restore[/COLOR]' % COLOR2, 'files', '.zip', False, False)
	if source == "" or not source.endswith('.zip'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore: Cancelled[/COLOR]" % COLOR2)
		return
	if not source.startswith('http'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore: Invalid URL[/COLOR]" % COLOR2)
		return
	try:
		work = workingURL(source)
	except:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore: Error Valid URL[/COLOR]" % COLOR2)
		log("Not a working url, if source was local then use local restore option", xbmc.LOGNOTICE)
		log("External Source: %s" % source, xbmc.LOGNOTICE)
		return
	log("[RESTORE EXT BACKUP %s] File: %s " % (type.upper(), source), xbmc.LOGNOTICE)
	zipit = os.path.split(source); zname = zipit[1]
	DP.create(ADDONTITLE,'[COLOR %s]Downloading Zip file' % COLOR2,'', 'Please Wait[/COLOR]')
	if type == "gui": loc = USERDATA
	elif type == "addondata": loc = ADDOND
	else : loc = HOME
	if not os.path.exists(USERDATA): os.makedirs(USERDATA)
	if not os.path.exists(ADDOND): os.makedirs(ADDOND)
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	file = os.path.join(PACKAGES, zname)
	downloader.download(source, file, DP)
	DP.update(0,'Installing External Backup','', 'Please Wait')
	percent, errors, error = extract.all(file,loc,DP)
	fixmetas()
	clearS('build')
	DP.close()
	defaultSkin()
	lookandFeelData('save')
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, zname), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B][COLOR red]No Thanks[/COLOR][/B]',yeslabel='[B][COLOR springgreen]View Errors[/COLOR][/B]')
		if yes:
			TextBox(ADDONTITLE, error.replace('\t',''))
	setS('installed', 'true')
	setS('extract', str(percent))
	setS('errors', str(errors))
	try: os.remove(file)
	except: pass
	if INSTALLMETHOD == 1: todo = 1
	elif INSTALLMETHOD == 2: todo = 0
	else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
	if todo == 1: reloadFix()
	else: killxbmc(True)

##########################
###DETERMINE PLATFORM#####
##########################

# MIGRATION: move into check
def checkSources():
	if not os.path.exists(SOURCES):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Sources.xml File Found![/COLOR]" % COLOR2)
		return False
	x      = 0
	bad    = []
	remove = []
	f      = open(SOURCES)
	a      = f.read()
	temp   = a.replace('\r','').replace('\n','').replace('\t','')
	match  = re.compile('<files>.+?</files>').findall(temp)
	f.close()
	if len(match) > 0:
		match2  = re.compile('<source>.+?<name>(.+?)</name>.+?<path pathversion="1">(.+?)</path>.+?<allowsharing>(.+?)</allowsharing>.+?</source>').findall(match[0])
		DP.create(ADDONTITLE, "[COLOR %s]Scanning Sources for Broken links[/COLOR]" % COLOR2)
		for name, path, sharing in match2:
			x     += 1
			perc   = int(percentage(x, len(match2)))
			DP.update(perc, '', "[COLOR %s]Checking [COLOR %s]%s[/COLOR]:[/COLOR]" % (COLOR2, COLOR1, name), "[COLOR %s]%s[/COLOR]" % (COLOR1, path))
			if 'http' in path:
				working = workingURL(path)
				if not working:
					bad.append([name, path, sharing, working])

		log("Bad Sources: %s" % len(bad), xbmc.LOGNOTICE)
		if len(bad) > 0:
			choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] Source(s) have been found Broken" % (COLOR1, len(bad), COLOR2),"Would you like to Remove all or choose one by one?[/COLOR]", yeslabel="[B][COLOR springgreen]Remove All[/COLOR][/B]", nolabel="[B][COLOR red]Choose to Delete[/COLOR][/B]")
			if choice == 1:
				remove = bad
			else:
				for name, path, sharing, working in bad:
					log("%s sources: %s, %s" % (name, path, working), xbmc.LOGNOTICE)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] was reported as non working" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, path), "[COLOR %s]%s[/COLOR]" % (COLOR1, working), yeslabel="[B][COLOR springgreen]Remove Source[/COLOR][/B]", nolabel="[B][COLOR red]Keep Source[/COLOR][/B]"):
						remove.append([name, path, sharing, working])
						log("Removing Source %s" % name, xbmc.LOGNOTICE)
					else: log("Source %s was not removed" % name, xbmc.LOGNOTICE)
			if len(remove) > 0:
				for name, path, sharing, working in remove:
					a = a.replace('\n        <source>\n            <name>%s</name>\n            <path pathversion="1">%s</path>\n            <allowsharing>%s</allowsharing>\n        </source>' % (name, path, sharing), '')
					log("Removing Source %s" % name, xbmc.LOGNOTICE)

				f = open(SOURCES, mode='w')
				f.write(str(a))
				f.close()
				alive = len(match) - len(bad)
				kept = len(bad) - len(remove)
				removed = len(remove)
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Checking sources for broken paths has been completed" % COLOR2, "Working: [COLOR %s]%s[/COLOR] | Kept: [COLOR %s]%s[/COLOR] | Removed: [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR2, COLOR1, alive, COLOR1, kept, COLOR1, removed))
			else: log("No Bad Sources to be removed.", xbmc.LOGNOTICE)
		else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]All Sources Are Working[/COLOR]" % COLOR2)
	else: log("No Sources Found", xbmc.LOGNOTICE)

def checkRepos():
	DP.create(ADDONTITLE, '[COLOR %s]Checking Repositories...[/COLOR]' % COLOR2)
	badrepos = []
	ebi('UpdateAddonRepos')
	repolist = glob.glob(os.path.join(ADDONS,'repo*'))
	if len(repolist) == 0:
		DP.close()
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Repositories Found![/COLOR]" % COLOR2)
		return
	sleeptime = len(repolist); start = 0;
	while start < sleeptime:
		start += 1
		if DP.iscanceled(): break
		perc = int(percentage(start, sleeptime))
		DP.update(perc, '', '[COLOR %s]Checking: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, repolist[start-1].replace(ADDONS, '')[1:]))
		xbmc.sleep(1000)
	if DP.iscanceled():
		DP.close()
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Enabling Addons Cancelled[/COLOR]" % COLOR2)
		sys.exit()
	DP.close()
	logfile = Grab_Log(False)
	fails = re.compile('CRepositoryUpdateJob(.+?)failed').findall(logfile)
	for item in fails:
		log("Bad Repository: %s " % item, xbmc.LOGNOTICE)
		brokenrepo = item.replace('[','').replace(']','').replace(' ','').replace('/','').replace('\\','')
		if not brokenrepo in badrepos:
			badrepos.append(brokenrepo)
	if len(badrepos) > 0:
		msg  = "[COLOR %s]Below is a list of Repositories that did not resolve.  This does not mean that they are Depreciated, sometimes hosts go down for a short period of time.  Please do serveral scans of your repository list before removing a repository just to make sure it is broken.[/COLOR][CR][CR][COLOR %s]" % (COLOR2, COLOR1)
		msg += '[CR]'.join(badrepos)
		msg += '[/COLOR]'
		TextBox("%s: Bad Repositories" % ADDONTITLE, msg)
	else:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]All Repositories Working![/COLOR]" % COLOR2)

#############################
####KILL XBMC ###############
#####THANKS BRACKETS ########

# MIGRATION: move into tools
def redoThumbs():
	if not os.path.exists(THUMBS): os.makedirs(THUMBS)
	thumbfolders = '0123456789abcdef'
	videos = os.path.join(THUMBS, 'Video', 'Bookmarks')
	for item in thumbfolders:
		foldname = os.path.join(THUMBS, item)
		if not os.path.exists(foldname): os.makedirs(foldname)
	if not os.path.exists(videos): os.makedirs(videos)

def reloadFix(default=None):
	DIALOG.ok(ADDONTITLE, "[COLOR %s]WARNING: Sometimes Reloading the Profile causes Kodi to crash.  While Kodi is Reloading the Profile Please Do Not Press Any Buttons![/COLOR]" % COLOR2)
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	if default is None:
		lookandFeelData('save')
	redoThumbs()
	ebi('ActivateWindow(Home)')
	reloadProfile()
	xbmc.sleep(10000)
	if KODIV >= 17: kodi17Fix()
	if default is None:
		log("Switching to: %s" % getS('defaultskin'))
		gotoskin = getS('defaultskin')
		swapSkins(gotoskin)
		lookandFeelData('restore')
	addonUpdates('reset')
	forceUpdate()
	ebi("ReloadSkin()")

# MIGRATION: move into tools
def data_type(str):
	datatype = type(str).__name__
	return datatype

def net_info():
	import json
	infoLabel = ['Network.IPAddress',
				 'Network.MacAddress',]
	data      = []; x = 0
	for info in infoLabel:
		temp = getInfo(info)
		y = 0
		while temp == "Busy" and y < 10:
			temp = getInfo(info); y += 1; log("%s sleep %s" % (info, str(y))); xbmc.sleep(200)
		data.append(temp)
		x += 1
	try:
		url = 'http://extreme-ip-lookup.com/json/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		geo = json.load(response)
	except:
		url = 'http://ip-api.com/json'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		geo = json.load(response)
	mac = data[1]
	inter_ip = data[0]
	ip=geo['query']
	isp=geo['org']
	city = geo['city']
	country=geo['country']
	state=geo['region']
	return mac,inter_ip,ip,city,state,country,isp

##########################
### PURGE DATABASE #######
##########################

# MIGRATION: move into tools?
def replaceHTMLCodes(txt):
	txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
	txt = HTMLParser.HTMLParser().unescape(txt)
	txt = txt.replace("&quot;", "\"")
	txt = txt.replace("&amp;", "&")
	return txt
