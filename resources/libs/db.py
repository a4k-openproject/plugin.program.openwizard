################################################################################
#      Copyright (C) 2019 drinfernoo                                           #
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
import xbmcgui
import xbmcvfs

import glob
import os
import re
try:  # Python 3
    import zipfile
except ImportError:  # Python 2
    from resources.libs import zipfile

from sqlite3 import dbapi2 as database

from datetime import datetime

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools


def addon_database(addon=None, state=1, array=False):
    dbfile = latest_db('Addons')
    dbfile = os.path.join(CONFIG.DATABASE, dbfile)
    installedtime = str(datetime.now())[:-7]

    if os.path.exists(dbfile):
        try:
            textdb = database.connect(dbfile)
            textexe = textdb.cursor()
        except Exception as e:
            logging.log("DB Connection Error: {0}".format(str(e)), level=xbmc.LOGERROR)
            return False
    else:
        return False

    if state == 2:
        try:
            textexe.execute("DELETE FROM installed WHERE addonID = ?", (addon,))
            textdb.commit()
            textexe.close()
        except:
            logging.log("Error Removing {0} from DB".format(addon))
        return True

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
    except:
        logging.log("Erroring enabling addon: {0}".format(addon))


def latest_db(db):
    if db in CONFIG.DB_FILES:
        match = glob.glob(os.path.join(CONFIG.DATABASE, '{0}*.db'.format(db)))
        comp = '{0}(.+?).db'.format(db[1:])
        highest = 0
        for file in match:
            try:
                check = int(re.compile(comp).findall(file)[0])
            except:
                check = 0
            if highest < check:
                highest = check
        return '{0}{1}.db'.format(db, highest)
    else:
        return False
        
        
def force_check_updates(auto=False, over=False):
    import time
    
    if not over:
        logging.log_notify(CONFIG.ADDONTITLE,
                           '[COLOR {0}]Force Checking for Updates[/COLOR]'.format(CONFIG.COLOR2))

    dbfile = latest_db('Addons')
    dbfile = os.path.join(CONFIG.DATABASE, dbfile)
    sqldb = database.connect(dbfile)
    sqlexe = sqldb.cursor()
    
    # force rollback all installed repos
    sqlexe.execute("UPDATE repo SET version = ?, checksum = ?, lastcheck = ?", ('', '', '',))
    sqldb.commit()

    # trigger kodi to check them for updates
    xbmc.executebuiltin('UpdateAddonRepos')

    # wait until they have finished updating
    with tools.busy_dialog():
        installed_repos = sqlexe.execute('SELECT addonID FROM repo')

        start_time = time.time()
        checked_time = 0
        for repo in installed_repos.fetchall():
            repo = repo[0]
            logging.log('Force checking {0}...'.format(repo), level=xbmc.LOGDEBUG)
            while checked_time < start_time:
                if time.time() >= start_time + 20:
                    logging.log('{0} timed out during repo force check.'.format(repo), level=xbmc.LOGDEBUG)
                    break
                
                lastcheck = sqlexe.execute('SELECT lastcheck FROM repo WHERE addonID = ?', (repo,))
                
                if lastcheck:
                    checked_time = lastcheck.fetchone()[0]
                    checked_time = time.mktime(time.strptime(checked_time, '%Y-%m-%d %H:%M:%S')) if checked_time else 0
                    
                xbmc.sleep(1000)
            checked_time = 0
            logging.log('{0} successfully force checked.'.format(repo), level=xbmc.LOGDEBUG)
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]{1} successfully force checked.[/COLOR]".format(CONFIG.COLOR2, repo))
            
    sqlexe.close()
                    
    if auto:
        xbmc.executebuiltin('UpdateLocalAddons')


def purge_db_file(name):
    logging.log('Purging DB {0}.'.format(name))
    if os.path.exists(name):
        try:
            textdb = database.connect(name)
            textexe = textdb.cursor()
        except Exception as e:
            logging.log("DB Connection Error: {0}".format(str(e)), level=xbmc.LOGERROR)
            return False
    else:
        logging.log('{0} not found.'.format(name), level=xbmc.LOGERROR)
        return False
    textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    for table in textexe.fetchall():
        if table[0] == 'version':
            logging.log('Data from table `{0}` skipped.'.format(table[0]))
        else:
            try:
                textexe.execute("DELETE FROM {0}".format(table[0]))
                textdb.commit()
                logging.log('Data from table `{0}` cleared.'.format(table[0]))
            except Exception as e:
                logging.log("DB Remove Table `{0}` Error: {1}".format(table[0], str(e)), level=xbmc.LOGERROR)
    textexe.close()
    logging.log('{0} DB Purging Complete.'.format(name))
    show = name.replace('\\', '/').split('/')
    logging.log_notify("[COLOR {0}]Purge Database[/COLOR]".format(CONFIG.COLOR1),
                       "[COLOR {0}]{1} Complete[/COLOR]".format(CONFIG.COLOR2, show[len(show)-1]))


def depends_list(plugin):
    addonxml = os.path.join(CONFIG.ADDONS, plugin, 'addon.xml')
    if os.path.exists(addonxml):

        match  = tools.parse_dom(tools.read_from_file(addonxml), 'import', ret='addon')
        items  = []
        for depends in match:
            if not 'xbmc.python' in depends:
                items.append(depends)
        return items
    return []


def purge_db():
    dialog = xbmcgui.Dialog()

    DB = []
    display = []
    for dirpath, dirnames, files in os.walk(CONFIG.HOME):
        import fnmatch

        for f in fnmatch.filter(files, '*.db'):
            if f != 'Thumbs.db':
                found = os.path.join(dirpath, f)
                DB.append(found)
                dir = found.replace('\\', '/').split('/')
                display.append('({0}) {1}'.format(dir[len(dir)-2], dir[len(dir)-1]))
    choice = dialog.multiselect("[COLOR {0}]Select DB File to Purge[/COLOR]".format(CONFIG.COLOR2), display)
    if choice is None or len(choice) == 0:
        logging.log_notify("[COLOR {0}]Purge Database[/COLOR]".format(CONFIG.COLOR1),
                           "[COLOR {0}]Cancelled[/COLOR]".format(CONFIG.COLOR2))
    else:
        for purge in choice:
            purge_db_file(DB[purge])


def kodi_17_fix():
    from resources.libs.common import tools
    from resources.libs import update

    addonlist = glob.glob(os.path.join(CONFIG.ADDONS, '*/'))
    disabledAddons = []
    for folder in sorted(addonlist, key=lambda x: x):
        addonxml = os.path.join(folder, 'addon.xml')
        if os.path.exists(addonxml):
            fold = folder.replace(CONFIG.ADDONS, '')[1:-1]
            aid = tools.parse_dom(tools.read_from_file(addonxml), 'addon', ret='id')
            try:
                if len(aid) > 0:
                    addonid = aid[0]
                else:
                    addonid = fold
            except:
                try:
                    logging.log("{0} was disabled".format(aid[0]))
                    disabledAddons.append(addonid)
                except:
                    logging.log("Unable to enable: {0}".format(folder), level=xbmc.LOGERROR)
    if len(disabledAddons) > 0:
        addon_database(disabledAddons, 1, True)
        logging.log_notify(CONFIG.ADDONTITLE,
                           "[COLOR {0}]Enabling Addons Complete![/COLOR]".format(CONFIG.COLOR2))
    update.force_update()
    xbmc.executebuiltin("ReloadSkin()")


def toggle_addon(id, value, over=None):
    from resources.libs.common import tools

    from xml.etree import ElementTree

    logging.log("Toggling {0}".format(id))
    addonid = id
    addonxml = os.path.join(CONFIG.ADDONS, id, 'addon.xml')
    if os.path.exists(addonxml):
        root = ElementTree.parse(addonxml).getroot()
        tid = root.get('id')
        tname = root.get('name')
        tservice = root.find('extension').get('point')
        
        try:
            if len(tid) > 0:
                addonid = tid
            if tservice == 'xbmc.service':
                logging.log("We got a live one, stopping script: {0}".format(tid))
                xbmc.executebuiltin('StopScript({0})'.format(os.path.join(CONFIG.ADDONS, addonid)))
                xbmc.executebuiltin('StopScript({0})'.format(addonid))
                xbmc.executebuiltin('StopScript({0})'.format(os.path.join(CONFIG.ADDONS, addonid, tservice[0])))
                xbmc.sleep(500)
        except:
            pass
            
    query = '{{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{{"addonid":"{0}","enabled":{1}}}, "id":1}}'.format(addonid, value)
    response = xbmc.executeJSONRPC(query)
    
    if 'error' in response and over is None:
        dialog = xbmcgui.Dialog()
        
        v = 'Enabling' if value == 'true' else 'Disabling'
        dialog.ok(CONFIG.ADDONTITLE,
                      "[COLOR {0}]Error {1} [COLOR {2}]{3}[/COLOR]".format(CONFIG.COLOR2, v, CONFIG.COLOR1, id) + '\n' +
                      "Check to make sure the add-on list is up to date and try again.[/COLOR]")


def toggle_dependency(name, dp=None):
    from resources.libs.common import tools

    dep = os.path.join(CONFIG.ADDONS, name, 'addon.xml')
    if os.path.exists(dep):
        match = tools.parse_dom(tools.read_from_file(dep), 'import', ret='addon')
        for depends in match:
            if 'xbmc.python' not in depends:
                dependspath = os.path.join(CONFIG.ADDONS, depends)
                if dp is not None:
                    dp.update("",
                              "Checking Dependency [COLOR yellow]{0}[/COLOR] for [COLOR yellow]{1}[/COLOR]".format(depends, name),
                              "")
                if os.path.exists(dependspath):
                    toggle_addon(name, 'true')
            xbmc.sleep(100)


# NOT CURRENTLY IN USE, BROKEN DUE TO DEAD NaN LINK
# def toggle_adult():
#     from resources.libs import gui
#     from resources.libs.common import tools
#
#     do = gui.DIALOG.yesno(CONFIG.ADDONTITLE,
#                           "[COLOR {0}]Would you like to [COLOR {1}]Enable[/COLOR] or [COLOR {2}]Disable[/COLOR] all Adult add-ons?[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1),
#                           yeslabel="[B][COLOR springgreen]Enable[/COLOR][/B]",
#                           nolabel="[B][COLOR red]Disable[/COLOR][/B]")
#     state = 'true' if do == 1 else 'false'
#     goto = 'Enabling' if do == 1 else 'Disabling'
#     link = tools.open_url('http://noobsandnerds.com/TI/AddonPortal/adult.php').replace('\n', '').replace('\r', '').replace('\t', '')
#     list = re.compile('i="(.+?)"').findall(link)
#     found = []
#     for item in list:
#         fold = os.path.join(CONFIG.ADDONS, item)
#         if os.path.exists(fold):
#             found.append(item)
#             toggle_addon(item, state, True)
#             logging.log("[Toggle Adult] {0} {1}".format(goto, item))
#     if len(found) > 0:
#         if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
#                             "[COLOR {0}]Would you like to view a list of the add-ons that where {1}?[/COLOR]".format(CONFIG.COLOR2, goto.replace('ing', 'ed')),
#                             yeslabel="[B][COLOR springgreen]View List[/COLOR][/B]",
#                             nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
#             editlist = '[CR]'.join(found)
#             gui.show_text_box(CONFIG.ADDONTITLE,
#                               "[COLOR {0}]Here are a list of the add-ons that where {1} for Adult Content:[/COLOR][CR][CR][COLOR {2}]{3}[/COLOR]".format(CONFIG.COLOR1, goto.replace('ing', 'ed'), CONFIG.COLOR2, editlist))
#         else:
#             logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
#                                "[COLOR {0}[COLOR {1}]{2}[/COLOR] Adult Addons {3}[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, count, goto.replace('ing', 'ed')))
#         from resources.libs import update
#         update.force_update(True)
#     else:
#         logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
#                            "[COLOR {0}]No Adult Addons Found[/COLOR]".format(CONFIG.COLOR2))


def create_temp(plugin):
    from resources.libs.common import tools

    temp = os.path.join(CONFIG.PLUGIN, 'resources', 'tempaddon.xml')
    r = tools.read_from_file(temp)
    plugdir = os.path.join(CONFIG.ADDONS, plugin)
    if not os.path.exists(plugdir):
        os.makedirs(plugdir)

    tools.write_to_file(os.path.join(plugdir, 'addon.xml'), r.replace('testid', plugin).replace('testversion', '0.0.1'))
    logging.log("{0}: wrote addon.xml".format(plugin))


def fix_metas():
    from resources.libs.common import tools

    idlist = []
    for item in idlist:
        fold = os.path.join(CONFIG.ADDOND, item)
        if os.path.exists(fold):
            storage = os.path.join(fold, '.storage')
            if os.path.exists(storage):
                tools.clean_house(storage)
                tools.remove_folder(storage)


# def hide_password():
#     from resources.libs.common import tools
#     from resources.libs.common import logging
#
#     dialog = xbmcgui.Dialog()
#
#     if dialog.yesno(CONFIG.ADDONTITLE,
#                         "[COLOR {0}]Would you like to [COLOR {1}]hide[/COLOR] all passwords when typing in the add-on settings menus?[/COLOR]".format(CONFIG.COLOR2),
#                         yeslabel="[B][COLOR springgreen]Hide Passwords[/COLOR][/B]",
#                         nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
#         count = 0
#         for folder in glob.glob(os.path.join(CONFIG.ADDONS, '*/')):
#             sett = os.path.join(folder, 'resources', 'settings.xml')
#             if os.path.exists(sett):
#                 f = tools.read_from_file(sett)
#                 match = tools.parse_dom(f, 'addon', ret='id')
#                 for line in match:
#                     if 'pass' in line:
#                         if 'option="hidden"' not in line:
#                             try:
#                                 change = line.replace('/', 'option="hidden" /')
#                                 f.replace(line, change)
#                                 count += 1
#                                 logging.log("[Hide Passwords] found in {0} on {1}".format(sett.replace(CONFIG.HOME, ''), line))
#                             except:
#                                 pass
#                 tools.write_to_file(sett, f)
#         logging.log_notify("[COLOR {0}]Hide Passwords[/COLOR]".format(CONFIG.COLOR1),
#                            "[COLOR {0}]{1} items changed[/COLOR]".format(CONFIG.COLOR2, count))
#         logging.log("[Hide Passwords] {0} items changed".format(count))
#     else:
#         logging.log("[Hide Passwords] Cancelled")
#
#
# def unhide_password():
#     from resources.libs.common import tools
#     from resources.libs.common import logging
#
#     dialog = xbmcgui.Dialog()
#
#     if dialog.yesno(CONFIG.ADDONTITLE,
#                         "[COLOR {0}]Would you like to [COLOR {1}]unhide[/COLOR] all passwords when typing in the add-on settings menus?[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1),
#                         yeslabel="[B][COLOR springgreen]Unhide Passwords[/COLOR][/B]",
#                         nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
#         count = 0
#         for folder in glob.glob(os.path.join(CONFIG.ADDONS, '*/')):
#             sett = os.path.join(folder, 'resources', 'settings.xml')
#             if os.path.exists(sett):
#                 f = tools.read_from_file(sett)
#                 match = tools.parse_dom(f, 'addon', ret='id')
#                 for line in match:
#                     if 'pass' in line:
#                         if 'option="hidden"' in line:
#                             try:
#                                 change = line.replace('option="hidden"', '')
#                                 f.replace(line, change)
#                                 count += 1
#                                 logging.log("[Unhide Passwords] found in {0} on {1}".format(sett.replace(CONFIG.HOME, ''), line))
#                             except:
#                                 pass
#                 tools.write_to_file(sett, f)
#         logging.log_notify("[COLOR {0}]Unhide Passwords[/COLOR]".format(CONFIG.COLOR1),
#                            "[COLOR {0}]{1} items changed[/COLOR]".format(CONFIG.COLOR2, count))
#         logging.log("[Unhide Passwords] {0} items changed".format(count))
#     else:
#         logging.log("[Unhide Passwords] Cancelled")


def fix_update():
    if os.path.exists(os.path.join(CONFIG.USERDATA, 'autoexec.py')):
        temp = os.path.join(CONFIG.USERDATA, 'autoexec_temp.py')
        if os.path.exists(temp):
            xbmcvfs.delete(temp)
        xbmcvfs.rename(os.path.join(CONFIG.USERDATA, 'autoexec.py'), temp)
    xbmcvfs.copy(os.path.join(CONFIG.PLUGIN, 'resources', 'libs', 'autoexec.py'),
                 os.path.join(CONFIG.USERDATA, 'autoexec.py'))
    dbfile = os.path.join(CONFIG.DATABASE, latest_db('Addons'))
    try:
        os.remove(dbfile)
    except:
        logging.log("Unable to remove {0}, Purging DB".format(dbfile))
        purge_db_file(dbfile)

    from resources.libs.common import tools
    tools.kill_kodi(over=True)


def grab_addons(path):
    zfile = zipfile.ZipFile(path, allowZip64=True)
    addonlist = []
    for item in zfile.infolist():
        if str(item.filename).find('addon.xml') == -1:
            continue
        info = str(item.filename).split('/')
        if not info[-2] in addonlist:
            addonlist.append(info[-2])
    return addonlist

    
def find_binary_addons(addon='all'):
    from xml.etree import ElementTree
    
    dialog = xbmcgui.Dialog()
    logging.log('Checking {} for platform-dependence...'.format(addon), level=xbmc.LOGDEBUG)
    
    if addon == 'all':
        addonfolders = glob.iglob(os.path.join(CONFIG.ADDONS, '*/'))
        addonids = []
        addonnames = []
        
        for folder in addonfolders:
            foldername = os.path.split(folder[:-1])[1]
            
            if foldername in CONFIG.EXCLUDES:
                continue
            elif foldername in CONFIG.DEFAULTPLUGINS:
                continue
            elif foldername == 'packages':
                continue    
            
            xml = os.path.join(folder, 'addon.xml')
            
            if os.path.exists(xml):
                root = ElementTree.parse(xml).getroot()
                addonid = root.get('id')
                addonname = root.get('name')
                extension = root.find('extension')
                
                try:
                    ext_attrs = extension.keys()
                except:
                    continue
                
                for attr in ext_attrs:
                    if attr.startswith('library_'):
                        try:
                            addonnames.append(addonname)
                            addonids.append(addonid)
                        except:
                            pass
        
        dialog.ok(CONFIG.ADDONTITLE, "[COLOR {0}]Found [COLOR {1}]{2}[/COLOR] platform-specific addons installed:[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, len(addonnames)), "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, addonnames))
        
        return addonids, addonnames
    else:
        if addon in CONFIG.EXCLUDES:
            return None, None
        elif addon in CONFIG.DEFAULTPLUGINS:
            return None, None
        
        xml = os.path.join(CONFIG.ADDONS, addon, 'addon.xml')
        
        if os.path.exists(xml):
            logging.log('Checking {0}'.format(xml), level=xbmc.LOGINFO)
            root = ElementTree.parse(xml).getroot()
            addonid = root.get('id')
            addonname = root.get('name')
            extension = root.find('extension')
            
            try:
                ext_attrs = extension.keys()
            except:
                return None, None
            
            for attr in ext_attrs:
                if attr.startswith('library_'):
                    return addonid, addonname
                        
        return None, None