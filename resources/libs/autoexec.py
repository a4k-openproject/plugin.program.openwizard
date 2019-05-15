################################################################################
#      Copyright (C) 2015 Surfacingx/NaN                                       #
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
import xbmcvfs
import xbmcaddon

import os
import glob
import thread

try:
    from sqlite3 import dbapi2 as database
except ImportError:
    from pysqlite2 import dbapi2 as database

from datetime import datetime

from resources.libs.config import CONFIG
from resources.libs import logging


def main():
    class enableAll():
        def __init__(self):
            from resources.libs import db
            self.addons = vars.ADDONS
            self.tempauto = os.path.join(vars.USERDATA, 'autoexec_temp.py')
            self.dbfilename = self.latestDB()
            self.dbfilename = os.path.join(self.databasepath, self.dbfilename)
            self.swap_us()
            if not os.path.exists(os.path.join(self.databasepath, self.dbfilename)):
                from resources.libs import gui
                gui.DIALOG.notification("AutoExec.py", "No Addons27.db file")
                logging.log("DB File not found.")

            self.addonlist = glob.glob(os.path.join(self.addons, '*/'))
            self.disabledAddons = []
            for folder in sorted(self.addonlist, key=lambda x: x):
                addonxml = os.path.join(folder, 'addon.xml')
                if os.path.exists(addonxml):
                    fold = folder.replace(self.addons, '')[1:-1]
                    from resources.libs import tools
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

        def latestDB(self, db="Addons"):
            match = glob.glob(os.path.join(self.databasepath,'{0}*.db'.format(db)))
            comp = '{0}(.+?).db'.format(db[1:])
            highest = 0
            for file in match:
                try:
                    check = int(re.compile(comp).findall(file)[0])
                except Exception as e:
                    check = 0
                    logging.log(str(e))
                if highest < check:
                    highest = check
            return '{0}{1}.db'.format(db, highest)

        def swap_us(self):
            new = '"addons.unknownsources"'
            value = 'true'
            query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":{0}}, "id":1}'.format(new)
            response = xbmc.executeJSONRPC(query)
            logging.log("Unknown Sources Get Settings: {0}".format(str(response)), level=xbmc.LOGDEBUG)
            if 'false' in response:
                thread.start_new_thread(self.dialog_watch, ())
                xbmc.sleep(200)
                query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (new, value)
                response = xbmc.executeJSONRPC(query)
                gui.DIALOG.notification("AutoExec.py", "Unknown Sources: Enabled")
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

    from resources.libs import gui
    try:
        gui.DIALOG.notification("AutoExec.py", "Starting Script...")
        firstRun = enableAll()
        gui.DIALOG.notification("AutoExec.py", "All Addons Enabled")
        xbmcvfs.delete('special://userdata/autoexec.py')
        xbmcvfs.copy('special://home/userdata/autoexec_temp.py', 'special://userdata/autoexec.py')
        xbmcvfs.delete('special://userdata/autoexec_temp.py')
    except Exception as e:
        gui.DIALOG.notification("AutoExec.py", "Error Check LogFile")
        logging.log(str(e), level=xbmc.LOGERROR)
        xbmcvfs.delete('special://userdata/autoexec.py')
        xbmcvfs.copy('special://home/userdata/autoexec_temp.py', 'special://userdata/autoexec.py')
        xbmcvfs.delete('special://userdata/autoexec_temp.py')


if __name__ == '__main__':
    main()
