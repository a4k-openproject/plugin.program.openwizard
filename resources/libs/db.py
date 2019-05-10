import xbmc

import glob
import os
import re

try:
    from sqlite3 import dbapi2 as database
except ImportError:
    from pysqlite2 import dbapi2 as database

from datetime import datetime

from resources.libs.config import CONFIG
from resources.libs import logging
from resources.libs import tools


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


def kodi_17_fix():
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
                    logging.log("Unabled to enable: {0}".format(folder), level=xbmc.LOGERROR)
    if len(disabledAddons) > 0:
        addon_database(disabledAddons, 1, True)
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]Enabling Addons Complete![/COLOR]".format(CONFIG.COLOR2))
    from resources.libs import update
    update.force_update()
    xbmc.executebuiltin("ReloadSkin()")


def toggle_addon(id, value, over=None):
    logging.log("Toggling {0}".format(id))
    addonid = id
    addonxml = os.path.join(CONFIG.ADDONS, id, 'addon.xml')
    if os.path.exists(addonxml):
        b = tools.read_from_file(addonxml)
        tid = tools.parse_dom(b, 'addon', ret='id')
        tname = tools.parse_dom(b, 'addon', ret='name')
        tservice = tools.parse_dom(b, 'extension', ret='library', attrs={'point': 'xbmc.service'})
        try:
            if len(tid) > 0:
                addonid = tid[0]
            if len(tservice) > 0:
                logging.log("We got a live one, stopping script: {0}".format(tid))
                xbmc.executebuiltin('StopScript({0})'.format(os.path.join(CONFIG.ADDONS, addonid)))
                xbmc.executebuiltin('StopScript({0})'.format(addonid))
                xbmc.executebuiltin('StopScript({0})'.format(os.path.join(CONFIG.ADDONS, addonid, tservice[0])))
                xbmc.sleep(500)
        except:
            pass
    query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"{0}","enabled":{1}}, "id":1}'.format(addonid, value)
    response = xbmc.executeJSONRPC(query)
    if 'error' in response and over is None:
        v = 'Enabling' if value == 'true' else 'Disabling'
        from resources.libs import gui
        gui.DIALOG.ok(CONFIG.ADDONTITLE,
                      "[COLOR {0}]Error {1} [COLOR {2}]{3}[/COLOR]".format(CONFIG.COLOR2, v, CONFIG.COLOR1, id),
                      "Check to make sure the add-on list is up to date and try again.[/COLOR]")
        from resources.libs import update
        update.force_update()
