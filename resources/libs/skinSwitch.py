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


import xbmc
import xbmcaddon

import os
import re
import thread

try:
    import json as simplejson
except ImportError:
    import simplejson

import uservar
from resources.libs import logging
from resources.libs import tools
from resources.libs import vars


def get_old(old):
    try:
        old = '"%s"' % old
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":{0}}, "id":1}'.format(old)
        response = xbmc.executeJSONRPC(query)
        response = simplejson.loads(response)
        if response.has_key('result'):
            if response['result'].has_key('value'):
                return response['result']['value']
    except:
        pass
    return None


def set_new(new, value):
    try:
        new = '"%s"' % new
        value = '"%s"' % value
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
        response = xbmc.executeJSONRPC(query)
    except:
        pass
    return None


def swap_skins(skin):
    if skin == 'skin.confluence':
        skinfold = os.path.join(vars.HOME, 'userdata', 'addon_data', 'skin.confluence')
        settings = os.path.join(skinfold, 'settings.xml')
        if not os.path.exists(settings):
            string = '<settings>\n    <setting id="FirstTimeRun" type="bool">true</setting>\n</settings>'
            os.makedirs(skinfold)
            tools.write_to_file(settings, string)
        else:
            xbmcaddon.Addon(id='skin.confluence').setSetting('FirstTimeRun', 'true')
    old = 'lookandfeel.skin'
    value = skin
    current = get_old(old)
    new = old
    set_new(new, value)


def switch_to_skin(goto, title="Error"):
    swap_skins(goto)
    x = 0
    xbmc.sleep(1000)
    while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
        x += 1
        xbmc.sleep(100)

    if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
        xbmc.executebuiltin('SendClick(11)')
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                           '[COLOR {0}]{1}: Skin Swap Timed Out![/COLOR]'.format(uservar.COLOR2, title))
        return False
    return True


def skin_to_default(title):
    if vars.SKIN not in ['skin.confluence', 'skin.estuary']:
        skin = 'skin.confluence' if vars.KODIV < 17 else 'skin.estuary'
    return switch_to_skin(skin, title)


def look_and_feel_data(do='save'):
    scan = ['lookandfeel.enablerssfeeds', 'lookandfeel.font', 'lookandfeel.rssedit', 'lookandfeel.skincolors',
            'lookandfeel.skintheme', 'lookandfeel.skinzoom', 'lookandfeel.soundskin', 'lookandfeel.startupwindow',
            'lookandfeel.stereostrength']
    if do == 'save':
        for item in scan:
            query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"%s"}, "id":1}' % item
            response = xbmc.executeJSONRPC(query)
            if 'error' not in response:
                match = re.compile('{"value":(.+?)}').findall(str(response))
                tools.set_setting(item.replace('lookandfeel', 'default'), match[0])
                logging.log("%s saved to %s" % (item, match[0]), level=xbmc.LOGNOTICE)
    else:
        for item in scan:
            value = tools.get_setting(item.replace('lookandfeel', 'default'))
            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"%s","value":%s}, "id":1}' % (item, value)
            response = xbmc.executeJSONRPC(query)
            logging.log("{0} restored to {1}".format(item, value), level=xbmc.LOGNOTICE)


def swap_us():
    new = '"addons.unknownsources"'
    value = 'true'
    query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % new
    response = xbmc.executeJSONRPC(query)
    logging.log("Unknown Sources Get Settings: {0}".format(str(response)), level=xbmc.LOGDEBUG)
    if 'false' in response:
        thread.start_new_thread(dialog_watch, ())
        xbmc.sleep(200)
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
        response = xbmc.executeJSONRPC(query)
        logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), '[COLOR %s]Unknown Sources:[/COLOR] [COLOR %s]Enabled[/COLOR]' % (uservar.COLOR1, uservar.COLOR2))
        logging.log("Unknown Sources Set Settings: %s" % str(response), xbmc.LOGDEBUG)


def dialog_watch():
    x = 0
    while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 100:
        x += 1
        xbmc.sleep(100)

    if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
        xbmc.executebuiltin('SendClick(11)')
