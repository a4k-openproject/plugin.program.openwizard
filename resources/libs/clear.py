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

import glob
import os
import shutil

from datetime import datetime
from datetime import timedelta

import sqlite3 as database

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools


def get_cache_size():
    from resources.libs.common import tools

    PROFILEADDONDATA = os.path.join(CONFIG.PROFILE, 'addon_data')

    dbfiles = [
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'meta.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'torrentScrape.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.module.simplecache', 'simplecache.db'))]
    cachelist = [
        CONFIG.ADDON_DATA,
        (os.path.join(CONFIG.HOME, 'cache')),
        (os.path.join(CONFIG.HOME, 'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(CONFIG.ADDON_DATA,'script.module.simple.downloader')),
        (os.path.join(CONFIG.ADDON_DATA,'plugin.video.itv','Images')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'images')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'TheMovieDB')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'YouTube')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.program.autocompletion', 'Google')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.program.autocompletion', 'Bing')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.openmeta', '.storage'))]
    if not PROFILEADDONDATA == CONFIG.ADDON_DATA:
        cachelist.append(os.path.join(PROFILEADDONDATA, 'script.module.simple.downloader'))
        cachelist.append(os.path.join(PROFILEADDONDATA, 'plugin.video.itv','Images'))
        cachelist.append(os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'images'))
        cachelist.append(os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'TheMovieDB')),
        cachelist.append(os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'YouTube')),
        cachelist.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.program.autocompletion', 'Google')),
        cachelist.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.program.autocompletion', 'Bing')),
        cachelist.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.openmeta', '.storage')),
        cachelist.append(PROFILEADDONDATA)

    totalsize = 0

    for item in cachelist:
        if not os.path.exists(item):
            continue
        if item not in [CONFIG.ADDON_DATA, PROFILEADDONDATA]:
            totalsize = tools.get_size(item, totalsize)
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'cache' in d.lower() and d.lower() not in ['meta_cache']:
                        totalsize = tools.get_size(os.path.join(root, d), totalsize)

    if CONFIG.INCLUDEVIDEO == 'true':
        files = []
        if CONFIG.INCLUDEALL == 'true':
            files = dbfiles
        else:
            if CONFIG.INCLUDEEXODUSREDUX == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'providers.13.db'))
            if CONFIG.INCLUDEVENOM == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'providers.13.db'))
            if CONFIG.INCLUDENUMBERS == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'providers.13.db'))
            if CONFIG.INCLUDESCRUBS == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'providers.13.db'))
            if CONFIG.INCLUDEGAIA == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'meta.db'))
            if CONFIG.INCLUDESEREN == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'torrentScrape.db'))
            if CONFIG.INCLUDETHECREW == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'providers.13.db'))
        if len(files) > 0:
            for item in files:
                if not os.path.exists(item):
                    continue
                totalsize += os.path.getsize(item)
        else:
            logging.log("Clear Cache: Clear Video Cache Not Enabled")

    return totalsize


def clear_packages(over=None):
    from resources.libs.common import tools

    if os.path.exists(CONFIG.PACKAGES):
        try:
            for root, dirs, files in os.walk(CONFIG.PACKAGES):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    size = tools.convert_size(tools.get_size(CONFIG.PACKAGES))
                    if over:
                        yes = 1
                    else:
                        dialog = xbmcgui.Dialog()
                    
                        yes = dialog.yesno("[COLOR {0}]Delete Package Files[/COLOR]".format(CONFIG.COLOR2), "[COLOR {0}]{1}[/COLOR] files found / [COLOR {2}]{3}[/COLOR] in size.".format(CONFIG.COLOR1, str(file_count),CONFIG.COLOR1, size) + '\n' + "Do you want to delete them?", nolabel='[B][COLOR red]Don\'t Clear[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Clear Packages[/COLOR][/B]')
                    if yes:
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                        logging.log_notify(CONFIG.ADDONTITLE,
                                  '[COLOR {0}]Clear Packages: Success![/COLOR]'.format(CONFIG.COLOR2))
                else:
                    logging.log_notify(CONFIG.ADDONTITLE,
                              '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))
        except Exception as e:
            logging.log_notify(CONFIG.ADDONTITLE,
                      '[COLOR {0}]Clear Packages: Error![/COLOR]'.format(CONFIG.COLOR2))
            logging.log("Clear Packages Error: {0}".format(str(e)), level=xbmc.LOGERROR)
    else:
        logging.log_notify(CONFIG.ADDONTITLE,
                  '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))


def clear_packages_startup():
    from resources.libs.common import tools

    start = datetime.utcnow() - timedelta(minutes=3)
    file_count = 0
    cleanupsize = 0
    if os.path.exists(CONFIG.PACKAGES):
        pack = os.listdir(CONFIG.PACKAGES)
        pack.sort(key=lambda f: os.path.getmtime(os.path.join(CONFIG.PACKAGES, f)))
        try:
            for item in pack:
                file = os.path.join(CONFIG.PACKAGES, item)
                lastedit = datetime.utcfromtimestamp(os.path.getmtime(file))
                if lastedit <= start:
                    if os.path.isfile(file):
                        file_count += 1
                        cleanupsize += os.path.getsize(file)
                        os.unlink(file)
                    elif os.path.isdir(file):
                        cleanupsize += tools.get_size(file)
                        cleanfiles, cleanfold = tools.clean_house(file)
                        file_count += cleanfiles + cleanfold
                        try:
                            shutil.rmtree(file)
                        except Exception as e:
                            logging.log("Failed to remove {0}: {1}".format(file, str(e), xbmc.LOGERROR))
            if file_count > 0:
                logging.log_notify(CONFIG.ADDONTITLE,
                          '[COLOR {0}]Clear Packages: Success: {1}[/COLOR]'.format(CONFIG.COLOR2, tools.convert_size(cleanupsize)))
            else:
                logging.log_notify(CONFIG.ADDONTITLE,
                          '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))
        except Exception as e:
            logging.log_notify(CONFIG.ADDONTITLE,
                      '[COLOR {0}]Clear Packages: Error![/COLOR]'.format(CONFIG.COLOR2))
            logging.log("Clear Packages Error: {0}".format(str(e)), level=xbmc.LOGERROR)
    else:
        logging.log_notify(CONFIG.ADDONTITLE,
                  '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))


def clear_archive():
    dialog = xbmcgui.Dialog()

    if dialog.yesno(CONFIG.ADDONTITLE,
                        '[COLOR {0}]Would you like to clear the \'Archive_Cache\' folder?[/COLOR]'.format(CONFIG.COLOR2),
                        nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                        yeslabel='[B][COLOR springgreen]Yes Clear[/COLOR][/B]'):
        if os.path.exists(CONFIG.ARCHIVE_CACHE):
            from resources.libs.common import tools
            tools.clean_house(CONFIG.ARCHIVE_CACHE)


def clear_function_cache(over=False):
    dialog = xbmcgui.Dialog()

    if not over:
        if dialog.yesno(CONFIG.ADDONTITLE,
                            '[COLOR {0}]Would you like to clear resolver function caches?[/COLOR]'.format(CONFIG.COLOR2),
                            nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                            yeslabel='[B][COLOR springgreen]Clear Cache[/COLOR][/B]'):
            clear = True
    else:
        clear = True
        
    if clear:
        if xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)'):
                xbmc.executebuiltin('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')
        if xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)'):
            xbmc.executebuiltin('RunPlugin(plugin://script.module.urlresolver/?mode=reset_cache)')


def clear_cache(over=None):
    PROFILEADDONDATA = os.path.join(CONFIG.PROFILE, 'addon_data')
    dbfiles = [
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'meta.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'torrentScrape.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.module.simplecache', 'simplecache.db'))]

    cachelist = [
        PROFILEADDONDATA,
        CONFIG.ADDON_DATA,
        (os.path.join(CONFIG.HOME, 'cache')),
        (os.path.join(CONFIG.HOME, 'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.module.simple.downloader')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.itv', 'Images')),
        (os.path.join(PROFILEADDONDATA, 'script.module.simple.downloader')),
        (os.path.join(PROFILEADDONDATA, 'plugin.video.itv', 'Images')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'images')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'TheMovieDB')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'YouTube')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.program.autocompletion', 'Google')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.program.autocompletion', 'Bing')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.openmeta', '.storage'))]

    delfiles = 0
    excludes = ['meta_cache', 'archive_cache']
    for item in cachelist:
        if not os.path.exists(item):
            continue
        if item not in [CONFIG.ADDON_DATA, PROFILEADDONDATA]:
            for root, dirs, files in os.walk(item):
                dirs[:] = [d for d in dirs if d not in excludes]
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        if f not in CONFIG.LOGFILES:
                            try:
                                os.unlink(os.path.join(root, f))
                                logging.log("[Wiped] {0}".format(os.path.join(root, f)))
                                delfiles += 1
                            except:
                                pass
                        else:
                            logging.log('Ignore Log File: {0}'.format(f))
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            delfiles += 1
                            logging.log("[Success] cleared {0} files from {1}".format(str(file_count), os.path.join(item, d)),
                                        level=xbmc.LOGINFO)
                        except:
                            logging.log("[Failed] to wipe cache in: {0}".format(os.path.join(item, d)),
                                        level=xbmc.LOGINFO)
        else:
            for root, dirs, files in os.walk(item):
                dirs[:] = [d for d in dirs if d not in excludes]
                for d in dirs:
                    if not str(d.lower()).find('cache') == -1:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            delfiles += 1
                            logging.log("[Success] wiped {0} ".format(os.path.join(root, d)))
                        except:
                            logging.log("[Failed] to wipe cache in: {0}".format(os.path.join(item, d)))

    if CONFIG.INCLUDEVIDEO == 'true' and over is None:
        files = []
        if CONFIG.INCLUDEALL == 'true':
            files = dbfiles
        else:
            if CONFIG.INCLUDEEXODUSREDUX == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'providers.13.db'))
            if CONFIG.INCLUDEVENOM == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'providers.13.db'))
            if CONFIG.INCLUDENUMBERS == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.numbersbynumbers', 'providers.13.db'))
            if CONFIG.INCLUDESCRUBS == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'providers.13.db'))
            if CONFIG.INCLUDETHECREW == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'providers.13.db'))
            if CONFIG.INCLUDEGAIA == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'meta.db'))
            if CONFIG.INCLUDESEREN == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'torrentScrape.db'))
        if len(files) > 0:
            for item in files:
                if os.path.exists(item):
                    delfiles += 1
                    try:
                        textdb = database.connect(item)
                        textexe = textdb.cursor()
                    except Exception as e:
                        logging.log("DB Connection error: {0}".format(str(e)), level=xbmc.LOGERROR)
                        continue
                    if 'Database' in item:
                        try:
                            textexe.execute("DELETE FROM url_cache")
                            textexe.execute("VACUUM")
                            textdb.commit()
                            textexe.close()
                            logging.log("[Success] wiped {0}".format(item))
                        except Exception as e:
                            logging.log("[Failed] wiped {0}: {1}".format(item, str(e)))
                    else:
                        textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
                        for table in textexe.fetchall():
                            try:
                                textexe.execute("DELETE FROM {0}".format(table[0]))
                                textexe.execute("VACUUM")
                                textdb.commit()
                                logging.log("[Success] wiped {0} in {1}".format(table[0], item))
                            except Exception as e:
                                try:
                                    logging.log("[Failed] wiped {0} in {1}: {2}".format(table[0], item, str(e)))
                                except:
                                    pass
                        textexe.close()
        else:
            logging.log("Clear Cache: Clear Video Cache Not Enabled")
    logging.log_notify(CONFIG.ADDONTITLE,
                       '[COLOR {0}]Clear Cache: Removed {1} Files[/COLOR]'.format(CONFIG.COLOR2, delfiles))


def old_thumbs():
    from resources.libs import db
    from resources.libs.common import tools

    dbfile = os.path.join(CONFIG.DATABASE, db.latest_db('Textures'))
    use = 30
    week = tools.get_date(days=-7)
    ids = []
    images = []
    size = 0
    if os.path.exists(dbfile):
        try:
            textdb = database.connect(dbfile, isolation_level=None)
            textexe = textdb.cursor()
        except Exception as e:
            logging.log("DB Connection Error: {0}".format(str(e)), level=xbmc.LOGERROR)
            return False
    else:
        logging.log('{0} not found.'.format(dbfile), level=xbmc.LOGERROR)
        return False
    textexe.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (use, str(week)))
    found = textexe.fetchall()
    for rows in found:
        idfound = rows[0]
        ids.append(idfound)
        textexe.execute("SELECT cachedurl FROM texture WHERE id = ?", (idfound, ))
        found2 = textexe.fetchall()
        for rows2 in found2:
            images.append(rows2[0])
    logging.log("{0} total thumbs cleaned up.".format(str(len(images))))
    for id in ids:
        textexe.execute("DELETE FROM sizes WHERE idtexture = ?", (id, ))
        textexe.execute("DELETE FROM texture WHERE id = ?", (id, ))
    textexe.execute("VACUUM")
    textdb.commit()
    textexe.close()
    for image in images:
        path = os.path.join(CONFIG.THUMBNAILS, image)
        try:
            imagesize = os.path.getsize(path)
            os.remove(path)
            size += imagesize
        except:
            pass
    removed = tools.convert_size(size)
    if len(images) > 0:
        logging.log_notify(CONFIG.ADDONTITLE,
                           '[COLOR {0}]Clear Thumbs: {1} Files / {2} MB[/COLOR]!'.format(CONFIG.COLOR2, str(len(images)), removed))
    else:
        logging.log_notify(CONFIG.ADDONTITLE,
                           '[COLOR {0}]Clear Thumbs: None Found![/COLOR]'.format(CONFIG.COLOR2))


def clear_crash():
    files = []
    for file in glob.glob(os.path.join(CONFIG.LOGPATH, '*crashlog*.*')):
        files.append(file)
    if len(files) > 0:
        dialog = xbmcgui.Dialog()

        if dialog.yesno(CONFIG.ADDONTITLE,
                            '[COLOR {0}]Would you like to delete the Crash logs?'.format(CONFIG.COLOR2)
                            +'\n'+'[COLOR {0}]{1}[/COLOR] Files Found[/COLOR]'.format(CONFIG.COLOR1, len(files)),
                            yeslabel="[B][COLOR springgreen]Remove Logs[/COLOR][/B]",
                            nolabel="[B][COLOR red]Keep Logs[/COLOR][/B]"):
            for f in files:
                os.remove(f)
            logging.log_notify('[COLOR {0}]Clear Crash Logs[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]{1} Crash Logs Removed[/COLOR]'.format(CONFIG.COLOR2, len(files)))
        else:
            logging.log_notify(CONFIG.ADDONTITLE,
                               '[COLOR {0}]Clear Crash Logs Cancelled[/COLOR]'.format(CONFIG.COLOR2))
    else:
        logging.log_notify('[COLOR {0}]Clear Crash Logs[/COLOR]'.format(CONFIG.COLOR1),
                           '[COLOR {0}]No Crash Logs Found[/COLOR]'.format(CONFIG.COLOR2))


def force_text():
    tools.clean_house(CONFIG.TEXTCACHE)
    logging.log_notify(CONFIG.ADDONTITLE,
                       '[COLOR {0}]Text Files Flushed![/COLOR]'.format(CONFIG.COLOR2))


def toggle_cache(state):
    cachelist = ['includevideo', 'includeall', 'includeexodusredux', 'includegaia', 'includenumbers', 'includescrubs', 'includeseren', 'includethecrew', 'includevenom']
    titlelist = ['Include Video Addons', 'Include All Addons', 'Include Exodus Redux', 'Include Gaia', 'Include NuMb3r5', 'Include Scrubs v2', 'Include Seren', 'Include THE CREW', 'Include Venom']
    if state in ['true', 'false']:
        for item in cachelist:
            CONFIG.set_setting(item, state)
    else:
        if state not in ['includevideo', 'includeall'] and CONFIG.get_setting('includeall') == 'true':
            try:
                dialog = xbmcgui.Dialog()

                item = titlelist[cachelist.index(state)]
                dialog.ok(CONFIG.ADDONTITLE,
                              "[COLOR {0}]You will need to turn off [COLOR {1}]Include All Addons[/COLOR] to disable[/COLOR] [COLOR {2}]{3}[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1, item))
            except:
                logging.log_notify("[COLOR {0}]Toggle Cache[/COLOR]".format(CONFIG.COLOR1),
                                   "[COLOR {0}]Invalid Add-on ID: {1}[/COLOR]".format(CONFIG.COLOR2, state))
        else:
            new = 'true' if CONFIG.get_setting(state) == 'false' else 'false'
            CONFIG.set_setting(state, new)


def total_clean():
    dialog = xbmcgui.Dialog()

    if dialog.yesno(CONFIG.ADDONTITLE,
                        '[COLOR {0}]Would you like to clear cache, packages and thumbnails?[/COLOR]'.format(CONFIG.COLOR2),
                        nolabel='[B][COLOR red]Cancel Process[/COLOR][/B]',
                        yeslabel='[B][COLOR springgreen]Clean All[/COLOR][/B]'):
        clear_archive()
        clear_cache()
        clear_function_cache(over=True)
        clear_packages('total')
        clear_thumbs('total')


def clear_thumbs(type=None):
    from resources.libs import db
    
    dialog = xbmcgui.Dialog()

    thumb_locations = {CONFIG.THUMBNAILS,
                       os.path.join(CONFIG.ADDON_DATA, 'script.module.metadatautils', 'animatedgifs'),
                       os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'images')}

    latest = db.latest_db('Textures')
    if type is not None:
        choice = 1
    else:
        choice = dialog.yesno(CONFIG.ADDONTITLE, '[COLOR {0}]Would you like to delete the {1} and related thumbnail folders?'.format(CONFIG.COLOR2, latest) + '\n' + "They will repopulate on the next startup[/COLOR]", nolabel='[B][COLOR red]Don\'t Delete[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Delete Thumbs[/COLOR][/B]')
    if choice == 1:
        try:
            tools.remove_file(os.path.join(CONFIG.DATABASE, latest))
        except:
            logging.log('Failed to delete, Purging DB.')
            db.purge_db_file(latest)
        for i in thumb_locations:
            tools.remove_folder(i)
    else:
        logging.log('Clear thumbnames cancelled')

    tools.redo_thumbs()


def remove_addon(addon, name, over=False, data=True):
    import sqlite3
    from resources.libs import db
    
    if over:
        yes = 1
    else:
        dialog = xbmcgui.Dialog()
        
        yes = dialog.yesno(CONFIG.ADDONTITLE,
                               '[COLOR {0}]Are you sure you want to delete the add-on:'.format(CONFIG.COLOR2)
                               +'\n'+'Name: [COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, name)
                               +'\n'+'ID: [COLOR {0}]{1}[/COLOR][/COLOR]'.format(CONFIG.COLOR1, addon),
                               yeslabel='[B][COLOR springgreen]Remove Add-on[/COLOR][/B]',
                               nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]')
    if yes == 1:
        folder = os.path.join(CONFIG.ADDONS, addon)
        logging.log("Removing Add-on: {0}".format(addon))

        from resources.libs.common import tools
        tools.clean_house(folder)
        xbmc.sleep(200)
        
        xbmc.executebuiltin('StopScript({0})'.format(addon))
        
        sqldb = sqlite3.connect(os.path.join(CONFIG.DATABASE, db.latest_db('Addons')))
        sqlexe = sqldb.cursor()
        query = "DELETE FROM {0} WHERE addonID = '{1}'"
        
        for table in ['addons', 'installed', 'package']:
            sqlexe.execute(query.format(table, addon))
        
        try:
            shutil.rmtree(folder)
        except Exception as e:
            logging.log("Error removing {0}: {1}".format(addon, str(e)))
        
        if data:
            remove_addon_data(addon)
            
        return True
            
    if not over:
        logging.log_notify(CONFIG.ADDONTITLE,
                           "[COLOR {0}]{1} Removed[/COLOR]".format(CONFIG.COLOR2, name))


def remove_addon_data(addon):
    dialog = xbmcgui.Dialog()

    if addon == 'all':  # clear ALL addon data
        if dialog.yesno(CONFIG.ADDONTITLE,
                            '[COLOR {0}]Would you like to remove [COLOR {1}]ALL[/COLOR] addon data stored in your userdata folder?[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1),
                            yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]',
                            nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            tools.clean_house(CONFIG.ADDON_DATA)
        else:
            logging.log_notify('[COLOR {0}]Remove Addon Data[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]Cancelled![/COLOR]'.format(CONFIG.COLOR2))
    elif addon == 'uninstalled':  # clear addon data for uninstalled addons
        if dialog.yesno(CONFIG.ADDONTITLE,
                            '[COLOR {0}]Would you like to remove [COLOR {1}]ALL[/COLOR] addon data stored in your userdata folder for uninstalled addons?[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1),
                            yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]',
                            nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
                            
            total = 0
            
            for folder in glob.glob(os.path.join(CONFIG.ADDON_DATA, '*')):
                foldername = folder.replace(CONFIG.ADDON_DATA, '').replace('\\', '').replace('/', '')
                if foldername in CONFIG.EXCLUDES:
                    pass
                elif os.path.exists(os.path.join(CONFIG.ADDONS, foldername)):
                    pass
                elif os.path.isdir(folder):
                    tools.clean_house(folder)
                    total += 1
                    logging.log(folder)
                    shutil.rmtree(folder)
            logging.log_notify('[COLOR {0}]Clean up Uninstalled[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]{1} Folders(s) Removed[/COLOR]'.format(CONFIG.COLOR2, total))
        else:
            logging.log_notify('[COLOR {0}]Remove Add-on Data[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]Cancelled![/COLOR]'.format(CONFIG.COLOR2))
    elif addon == 'empty':  # clear empty folders from addon_data
        if dialog.yesno(CONFIG.ADDONTITLE,
                            '[COLOR {0}]Would you like to remove [COLOR {1}]ALL[/COLOR] empty addon data folders in your userdata folder?[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1),
                            yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]',
                            nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            total = tools.empty_folder(CONFIG.ADDON_DATA)
            logging.log_notify('[COLOR {0}]Remove Empty Folders[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]{1} Folders(s) Removed[/COLOR]'.format(CONFIG.COLOR2, total))
        else:
            logging.log_notify('[COLOR {0}]Remove Empty Folders[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]Cancelled![/COLOR]'.format(CONFIG.COLOR2))
    else:  # clear addon data for a specific addon
        addon_data = os.path.join(CONFIG.ADDON_DATA, addon)
        if addon in CONFIG.EXCLUDES:
            logging.log_notify("[COLOR {0}]Protected Plugin[/COLOR]".format(CONFIG.COLOR1),
                               "[COLOR {0}]Not allowed to remove add-on data[/COLOR]".format(CONFIG.COLOR2))
        elif os.path.exists(addon_data):
            if dialog.yesno(CONFIG.ADDONTITLE, '[COLOR {0}]Would you also like to remove the add-on data for:[/COLOR]'.format(CONFIG.COLOR2) + '\n' + '[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, addon), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
                tools.clean_house(addon_data)
                try:
                    shutil.rmtree(addon_data)
                except:
                    logging.log("Error deleting: {0}".format(addon_data))
            else:
                logging.log('Add-on data for {0} was not removed'.format(addon))
    xbmc.executebuiltin('Container.Refresh()')

    
def remove_addon_menu():
    from resources.libs.common import logging
    from resources.libs.common import tools
    from resources.libs import update
    
    from xml.etree import ElementTree
    
    dialog = xbmcgui.Dialog()

    addonfolders = glob.iglob(os.path.join(CONFIG.ADDONS, '*/'))
    addonnames = []
    addonids = []
    
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
            
            try:
                addonnames.append(addonname)
                addonids.append(addonid)
            except:
                pass
                
    if len(addonnames) == 0:
        logging.log_notify(CONFIG.ADDONTITLE,
                           "[COLOR {0}]No Addons To Remove[/COLOR]".format(CONFIG.COLOR2))
        return
    selected = dialog.multiselect("{0}: Select the addons you wish to remove.".format(CONFIG.ADDONTITLE), addonnames)
    if not selected:
        return
    if len(selected) > 0:
        update.addon_updates('set')
        for addon in selected:
            remove_addon(addon=addonids[addon], name=addonnames[addon], over=True)

        xbmc.sleep(500)

        dialog.ok(CONFIG.ADDONTITLE, "[COLOR {0}]To save changes you now need to force close Kodi, Press OK to force close Kodi[/COLOR]".format(CONFIG.COLOR2))
        
        update.addon_updates('reset')
        tools.kill_kodi(over=True)
