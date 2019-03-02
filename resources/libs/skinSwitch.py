################################################################################
#      Copyright (C) 2015 OpenELEQ                                             #
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

import os, re, shutil, time, xbmc, xbmcaddon, thread, wizard as wiz, uservar
try:
	import json as simplejson 
except:
	import simplejson

KODIV  = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
COLOR1 = uservar.COLOR1
COLOR2 = uservar.COLOR2

def getOld(old):
	try:
		old = '"%s"' % old 
		query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (old)
		response = xbmc.executeJSONRPC(query)
		response = simplejson.loads(response)
		if response.has_key('result'):
			if response['result'].has_key('value'):
				return response ['result']['value'] 
	except:
		pass
	return None

def setNew(new, value):
	try:
		new = '"%s"' % new
		value = '"%s"' % value
		query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
		response = xbmc.executeJSONRPC(query)
	except:
		pass
	return None

def swapSkins(skin):
	if skin == 'skin.confluence':
		HOME     = xbmc.translatePath('special://home/')
		skinfold = os.path.join(HOME, 'userdata', 'addon_data', 'skin.confluence')
		settings = os.path.join(skinfold, 'settings.xml')
		if not os.path.exists(settings):
			string = '<settings>\n    <setting id="FirstTimeRun" type="bool">true</setting>\n</settings>'
			os.makedirs(skinfold)
			f = open(settings, 'w'); f.write(string); f.close()
		else: xbmcaddon.Addon(id='skin.confluence').setSetting('FirstTimeRun', 'true')
	old = 'lookandfeel.skin'
	value = skin
	current = getOld(old)
	new = old
	setNew(new, value)
	#	if not xbmc.getCondVisibility(Skin.HasSetting(FirstTimeRun)):
	#		while xbmc.getCondVisibility('Window.IsVisible(1112)'):
	#			xbmc.executebuiltin('SendClick(100)')

def swapUS():
	new = '"addons.unknownsources"'
	value = 'true'
	query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (new)
	response = xbmc.executeJSONRPC(query)
	wiz.log("Unknown Sources Get Settings: %s" % str(response), xbmc.LOGDEBUG)
	if 'false' in response:
		thread.start_new_thread(dialogWatch, ())
		xbmc.sleep(200)
		query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
		response = xbmc.executeJSONRPC(query)
		wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Unknown Sources:[/COLOR] [COLOR %s]Enabled[/COLOR]' % (COLOR1, COLOR2))
		wiz.log("Unknown Sources Set Settings: %s" % str(response), xbmc.LOGDEBUG)
		
def dialogWatch():
	x = 0
	while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 100:
		x += 1
		xbmc.sleep(100)
	
	if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
		xbmc.executebuiltin('SendClick(11)')