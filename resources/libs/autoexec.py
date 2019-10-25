################################################################################
#      Copyright (C) 2019  drinfernoo                                       #
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
# Credits 
# ----------
# Tobias Ussing And Henrik Mosgaard Jensen for parseDOM
# WhiteCream thread for clicking yes on dialog for unknown sources

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import os
import glob
import threading

try:
    from sqlite3 import dbapi2 as database
except ImportError:
    from pysqlite2 import dbapi2 as database

from datetime import datetime

from resources.libs.common.config import CONFIG
from resources.libs.common import logging, tools


def main():
    class EnableAll:
        def __init__(self):
            from resources.libs import db
            
            dialog = xbmcgui.Dialog()
            
            self.databasepath = CONFIG.DATABASE
            self.addons = CONFIG.ADDONS
            self.tempauto = os.path.join(CONFIG.USERDATA, 'autoexec_temp.py')
            self.dbfilename = db.latest_db(db="Addons")
            self.dbfilename = os.path.join(self.databasepath, self.dbfilename)
            self.swap_us()
            if not os.path.exists(self.dbfilename):
                dialog.notification("AutoExec.py", "No Addons27.db file")
                logging.log("DB File not found.")

            self.addonlist = glob.glob(os.path.join(self.addons, '*/'))
            self.disabledAddons = []
            for folder in sorted(self.addonlist, key=lambda x: x):
                addonxml = os.path.join(folder, 'addon.xml')
                if os.path.exists(addonxml):
                    fold = folder.replace(self.addons, '')[1:-1]
                    aid = tools.parse_dom(tools.read_from_file(addonxml), 'addon', ret='id')
                    try:
                        if len(aid) > 0:
                            add = aid[0]
                        else:
                            add = fold
                        xadd = xbmcaddon.Addon(id=add)
                    except:
                        try:
                            self.disabledAddons.append(add)
                        except:
                            logging.log("Unable to enable: {0}".format(folder), level=xbmc.LOGERROR)
            if len(self.disabledAddons) > 0:
                self.addon_database(self.disabledAddons, 1, True)
            xbmc.executebuiltin('UpdateAddonRepos()')
            xbmc.executebuiltin('UpdateLocalAddons()')
            xbmc.executebuiltin("ReloadSkin()")

        def swap_us(self):
            dialog = xbmcgui.Dialog()
        
            new = '"addons.unknownsources"'
            value = 'true'
            query = '{{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{{"setting":{0}}}, "id":1}}'.format(new)
            response = xbmc.executeJSONRPC(query)
            logging.log("Unknown Sources Get Settings: {0}".format(str(response)), level=xbmc.LOGDEBUG)
            if 'false' in response:
                threading.Thread(target=self.dialog_watch).start()
                xbmc.sleep(200)
                query = '{{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{{"setting":{0},"value":{1}}, "id":1}}'.format(new, value)
                response = xbmc.executeJSONRPC(query)
                dialog.notification("AutoExec.py", "Unknown Sources: Enabled")
                logging.log("Unknown Sources Set Settings: {0}".format(str(response)), level=xbmc.LOGDEBUG)

        def dialog_watch(self):
            x = 0
            while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 100:
                x += 1
                xbmc.sleep(100)

            if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                xbmc.executebuiltin('SendClick(11)')

        def addon_database(self, addon=None, state=1, array=False):
            installedtime = str(datetime.now())[:-7]
            if os.path.exists(self.dbfilename):
                try:
                    textdb = database.connect(self.dbfilename)
                    textexe = textdb.cursor()
                except Exception as e:
                    logging.log("DB Connection Error: {0}".format(str(e)), level=xbmc.LOGERROR)
                    return False
            else:
                return False
            try:
                if not array:
                    textexe.execute('INSERT or IGNORE into installed (addonID , enabled, installDate) VALUES (?,?,?)', (addon, state, installedtime,))
                    textexe.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (state, addon,))
                else:
                    for item in addon:
                        textexe.execute('INSERT or IGNORE into installed (addonID , enabled, installDate) VALUES (?,?,?)', (item, state, installedtime,))
                        textexe.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (state, item,))
                textdb.commit()
                textexe.close()
            except Exception:
                logging.log("Erroring enabling addon: {0}".format(addon), level=xbmc.LOGERROR)

    dialog = xbmcgui.Dialog()
                
    try:
        dialog.notification("AutoExec.py", "Starting Script...")
        firstRun = EnableAll()
        dialog.notification("AutoExec.py", "All Addons Enabled")
        xbmcvfs.delete('special://userdata/autoexec.py')
        xbmcvfs.copy('special://home/userdata/autoexec_temp.py', 'special://userdata/autoexec.py')
        xbmcvfs.delete('special://userdata/autoexec_temp.py')
    except Exception as e:
        dialog.notification("AutoExec.py", "Error Check LogFile")
        logging.log(str(e), level=xbmc.LOGERROR)
        xbmcvfs.delete('special://userdata/autoexec.py')
        xbmcvfs.copy('special://home/userdata/autoexec_temp.py', 'special://userdata/autoexec.py')
        xbmcvfs.delete('special://userdata/autoexec_temp.py')


if __name__ == '__main__':
    main()
