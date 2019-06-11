import xbmc
import xbmcaddon

import glob
import os
import shutil

from datetime import datetime
from datetime import timedelta

import sqlite3 as database

from resources.libs.config import CONFIG
from resources.libs import logging
from resources.libs import tools


def flush_old_cache():
    if not os.path.exists(CONFIG.TEXTCACHE):
        os.makedirs(CONFIG.TEXTCACHE)
    try:
        age = int(float(CONFIG.CACHEAGE))
    except:
        age = 30
    match = glob.glob(os.path.join(CONFIG.TEXTCACHE, '*.txt'))
    for file in match:
        file_modified = datetime.fromtimestamp(os.path.getmtime(file))
        if datetime.now() - file_modified > timedelta(minutes=age):
            logging.log("Found: {0}".format(file))
            os.remove(file)


def text_cache(url):
    from resources.libs import check

    try:
        age = int(float(CONFIG.CACHEAGE))
    except:
        age = 30
    if CONFIG.CACHETEXT.lower() == 'yes':
        spliturl = url.split('/')
        if not os.path.exists(CONFIG.TEXTCACHE):
            os.makedirs(CONFIG.TEXTCACHE)
        file = xbmc.makeLegalFilename(os.path.join(CONFIG.TEXTCACHE, spliturl[-1]+'_'+spliturl[-2]+'.txt'))
        if os.path.exists(file):
            file_modified = datetime.fromtimestamp(os.path.getmtime(file))
            if datetime.now() - file_modified > timedelta(minutes=age):
                if check.check_url(url):
                    os.remove(file)

        if not os.path.exists(file):
            if not check.check_url(url):
                return False
            textfile = tools.open_url(url)
            content = tools.basecode(textfile, True)
            tools.write_to_file(file, content)

        a = tools.basecode(tools.read_from_file(file), False)
        return a
    else:
        textfile = tools.open_url(url)
        return textfile


def get_cache_size():
    from resources.libs import tools

    PROFILEADDONDATA = os.path.join(CONFIG.PROFILE, 'addon_data')

    dbfiles = [
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'meta.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'cache.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'torrentScrape.db')),
        (os.path.join(CONFIG.ADDON_DATA, 'script.module.simplecache', 'simplecache.db'))]
    cachelist = [
        (CONFIG.ADDON_DATA),
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
        if not os.path.exists(item): continue
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
            if CONFIG.INCLUDEPLACENTA == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'providers.13.db'))
            if CONFIG.INCLUDEYODA == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'providers.13.db'))
            if CONFIG.INCLUDEVENOM == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'providers.13.db'))
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
            if CONFIG.INCLUDEOVEREASY == 'true':
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'providers.13.db'))
        if len(files) > 0:
            for item in files:
                if not os.path.exists(item): continue
                totalsize += os.path.getsize(item)
        else:
            logging.log("Clear Cache: Clear Video Cache Not Enabled", level=xbmc.LOGNOTICE)

    return totalsize


def clear_packages(over=None):
    from resources.libs import tools

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
                        from resources.libs import gui

                        yes = gui.DIALOG.yesno("[COLOR {0}]Delete Package Files".format(CONFIG.COLOR2),
                                           "[COLOR {0}]{1}[/COLOR] files found / [COLOR {2}]{3}[/COLOR] in size.".format(
                                           CONFIG.COLOR1, str(file_count), CONFIG.COLOR1, size),
                                           "Do you want to delete them?[/COLOR]",
                                           nolabel='[B][COLOR red]Don\'t Clear[/COLOR][/B]',
                                           yeslabel='[B][COLOR springgreen]Clear Packages[/COLOR][/B]')
                    if yes:
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                                  '[COLOR {0}]Clear Packages: Success![/COLOR]'.format(CONFIG.COLOR2))
                else:
                    logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                              '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))
        except Exception as e:
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                      '[COLOR {0}]Clear Packages: Error![/COLOR]'.format(CONFIG.COLOR2))
            logging.log("Clear Packages Error: {0}".format(str(e)), level=xbmc.LOGERROR)
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                  '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))


def clear_packages_startup():
    from resources.libs import tools

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
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                          '[COLOR {0}]Clear Packages: Success: {1}[/COLOR]'.format(CONFIG.COLOR2, tools.convert_size(cleanupsize)))
            else:
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                          '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))
        except Exception as e:
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                      '[COLOR {0}]Clear Packages: Error![/COLOR]'.format(CONFIG.COLOR2))
            logging.log("Clear Packages Error: {0}".format(str(e)), level=xbmc.LOGERROR)
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                  '[COLOR {0}]Clear Packages: None Found![/COLOR]'.format(CONFIG.COLOR2))


def clear_archive():
    from resources.libs import gui

    if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                        '[COLOR {0}]Would you like to clear the \'Archive_Cache\' folder?[/COLOR]'.format(CONFIG.COLOR2),
                        nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                        yeslabel='[B][COLOR springgreen]Yes Clear[/COLOR][/B]'):
        if os.path.exists(CONFIG.ARCHIVE_CACHE):
            from resources.libs import tools
            tools.clean_house(CONFIG.ARCHIVE_CACHE)


def clear_function_cache():
    from resources.libs import gui

    if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                        '[COLOR {0}]Would you like to clear resolver function caches?[/COLOR]'.format(CONFIG.COLOR2),
                        nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                        yeslabel='[B][COLOR springgreen]Clear Cache[/COLOR][/B]'):
        if xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)'):
            xbmc.executebuiltin('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')
        if xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)'):
            xbmc.executebuiltin('RunPlugin(plugin://script.module.urlresolver/?mode=reset_cache)')


def clear_cache(over=None):
    from resources.libs import gui

    if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                        '[COLOR {0}]Would you like to clear cache?[/COLOR]'.format(CONFIG.COLOR2),
                        nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                        yeslabel='[B][COLOR springgreen]Clear Cache[/COLOR][/B]'):

        PROFILEADDONDATA = os.path.join(CONFIG.PROFILE, 'addon_data')
        dbfiles = [
            ## TODO: Double check these
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.meta.5.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.providers.13.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'meta.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'meta.5.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.providers.13.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'meta.5.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'cache.providers.13.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'meta.5.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'cache.providers.13.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'meta.5.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.providers.13.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'cache.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'torrentScrape.db')),
            (os.path.join(CONFIG.ADDON_DATA, 'script.module.simplecache', 'simplecache.db'))]

        cachelist = [
            (PROFILEADDONDATA),
            (CONFIG.ADDON_DATA),
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
                                    logging.log("[Wiped] {0}".format(os.path.join(root, f)), level=xbmc.LOGNOTICE)
                                    delfiles += 1
                                except:
                                    pass
                            else:
                                logging.log('Ignore Log File: {0}'.format(f), level=xbmc.LOGNOTICE)
                        for d in dirs:
                            try:
                                shutil.rmtree(os.path.join(root, d))
                                delfiles += 1
                                logging.log("[Success] cleared {0} files from {1}".format(str(file_count), os.path.join(item, d)),
                                            level=xbmc.LOGNOTICE)
                            except:
                                logging.log("[Failed] to wipe cache in: {0}".format(os.path.join(item, d)),
                                            level=xbmc.LOGNOTICE)
            else:
                for root, dirs, files in os.walk(item):
                    dirs[:] = [d for d in dirs if d not in excludes]
                    for d in dirs:
                        if not str(d.lower()).find('cache') == -1:
                            try:
                                shutil.rmtree(os.path.join(root, d))
                                delfiles += 1
                                logging.log("[Success] wiped {0} ".format(os.path.join(root, d)), level=xbmc.LOGNOTICE)
                            except:
                                logging.log("[Failed] to wipe cache in: {0}".format(os.path.join(item, d)), level=xbmc.LOGNOTICE)

        if CONFIG.INCLUDEVIDEO == 'true' and over is None:
            files = []
            if CONFIG.INCLUDEALL == 'true':
                files = dbfiles
            else:
                ## TODO: Double check these
                if CONFIG.INCLUDEPLACENTA == 'true':
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'cache.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'meta.5.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.placenta', 'providers.13.db'))
                if CONFIG.INCLUDEEXODUSREDUX == 'true':
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'cache.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'meta.5.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.exodusredux', 'providers.13.db'))
                if CONFIG.INCLUDEYODA == 'true':
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'cache.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'meta.5.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.yoda', 'providers.13.db'))
                if CONFIG.INCLUDEVENOM == 'true':
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.venom', 'cache.db'))
                if CONFIG.INCLUDESCRUBS == 'true':
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'cache.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'meta.5.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'providers.13.db'))
                if CONFIG.INCLUDEOVEREASY == 'true':
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'cache.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'meta.5.db'))
                    files.append(os.path.join(CONFIG.ADDON_DATA, 'plugin.video.overeasy', 'providers.13.db'))
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
                                logging.log("[Success] wiped {0}".format(item), level=xbmc.LOGNOTICE)
                            except Exception as e:
                                logging.log("[Failed] wiped {0}: {1}".format(item, str(e)), level=xbmc.LOGNOTICE)
                        else:
                            textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
                            for table in textexe.fetchall():
                                try:
                                    textexe.execute("DELETE FROM {0}".format(table[0]))
                                    textexe.execute("VACUUM")
                                    textdb.commit()
                                    logging.log("[Success] wiped {0} in {1}".format(table[0], item), level=xbmc.LOGNOTICE)
                                except Exception as e:
                                    try:
                                        logging.log("[Failed] wiped {0} in {1}: {2}".format(table[0], item, str(e)), level=xbmc.LOGNOTICE)
                                    except:
                                        pass
                            textexe.close()
            else:
                logging.log("Clear Cache: Clear Video Cache Not Enabled", level=xbmc.LOGNOTICE)
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           '[COLOR {0}]Clear Cache: Removed {1} Files[/COLOR]'.format(CONFIG.COLOR2, delfiles))


def old_thumbs():
    from resources.libs import db
    from resources.libs import tools

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
    logging.log("{0} total thumbs cleaned up.".format(str(len(images))), level=xbmc.LOGNOTICE)
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
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           '[COLOR {0}]Clear Thumbs: {1} Files / {2} MB[/COLOR]!'.format(CONFIG.COLOR2, str(len(images)), removed))
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           '[COLOR {0}]Clear Thumbs: None Found![/COLOR]'.format(CONFIG.COLOR2))


def clear_crash():
    files = []
    for file in glob.glob(os.path.join(CONFIG.LOGPATH, '*crashlog*.*')):
        files.append(file)
    if len(files) > 0:
        from resources.libs import gui

        if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                            '[COLOR {0}]Would you like to delete the Crash logs?'.format(CONFIG.COLOR2),
                            '[COLOR {0}]{1}[/COLOR] Files Found[/COLOR]'.format(CONFIG.COLOR1, len(files)),
                            yeslabel="[B][COLOR springgreen]Remove Logs[/COLOR][/B]",
                            nolabel="[B][COLOR red]Keep Logs[/COLOR][/B]"):
            for f in files:
                os.remove(f)
            logging.log_notify('[COLOR 0}]Clear Crash Logs[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]{1} Crash Logs Removed[/COLOR]'.format(CONFIG.COLOR2, len(files)))
        else:
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               '[COLOR {0}]Clear Crash Logs Cancelled[/COLOR]'.format(CONFIG.COLOR2))
    else:
        logging.log_notify('[COLOR {0}]Clear Crash Logs[/COLOR]'.format(CONFIG.COLOR1),
                           '[COLOR {0}]No Crash Logs Found[/COLOR]'.format(CONFIG.COLOR2))


def force_text():
    tools.clean_house(CONFIG.TEXTCACHE)
    logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                       '[COLOR {0}]Text Files Flushed![/COLOR]'.format(CONFIG.COLOR2))


def toggle_cache(state):
    cachelist = ['includevideo', 'includeall', 'includeexodusredux', 'includegaia', 'includeovereasy', 'includeplacenta', 'includescrubs', 'includeseren', 'includevenom', 'includeyoda']
    titlelist = ['Include Video Addons', 'Include All Addons', 'Include Exodus Redux', 'Include Gaia', 'Include Overeasy', 'Include Placenta', 'Include Scrubs v2', 'Include Seren', 'Include Venom', 'Include Yoda']
    if state in ['true', 'false']:
        for item in cachelist:
            CONFIG.set_setting(item, state)
    else:
        if state not in ['includevideo', 'includeall'] and CONFIG.get_setting('includeall') == 'true':
            try:
                from resources.libs import gui

                item = titlelist[cachelist.index(state)]
                gui.DIALOG.ok(CONFIG.ADDONTITLE,
                              "[COLOR {0}]You will need to turn off [COLOR {1}]Include All Addons[/COLOR] to disable[/COLOR] [COLOR {2}]{3}[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1, item))
            except:
                logging.log_notify("[COLOR {0}]Toggle Cache[/COLOR]".format(CONFIG.COLOR1),
                                   "[COLOR {0}]Invalid Add-on ID: {1}[/COLOR]".format(CONFIG.COLOR2, state))
        else:
            new = 'true' if CONFIG.get_setting(state) == 'false' else 'false'
            CONFIG.set_setting(state, new)


def total_clean():
    from resources.libs import gui

    if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                        '[COLOR {0}]Would you like to clear cache, packages and thumbnails?[/COLOR]'.format(CONFIG.COLOR2),
                        nolabel='[B][COLOR red]Cancel Process[/COLOR][/B]',
                        yeslabel='[B][COLOR springgreen]Clean All[/COLOR][/B]'):
        clear_cache()
        clear_function_cache()
        clear_packages('total')
        clear_thumbs('total')


def clear_thumbs(type=None):
    from resources.libs import db
    from resources.libs import gui

    thumb_locations = {CONFIG.THUMBNAILS,
                       os.path.join(CONFIG.ADDON_DATA, 'script.module.metadatautils', 'animatedgifs'),
                       os.path.join(CONFIG.ADDON_DATA, 'script.extendedinfo', 'images')}

    latest = db.latest_db('Textures')
    if type is not None:
        choice = 1
    else:
        choice = gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                                  '[COLOR {0}]Would you like to delete the {1} and related thumbnail folders?'.format(CONFIG.COLOR2, latest),
                                  "They will repopulate on the next startup[/COLOR]",
                                  nolabel='[B][COLOR red]Don\'t Delete[/COLOR][/B]',
                                  yeslabel='[B][COLOR springgreen]Delete Thumbs[/COLOR][/B]')
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


def remove_addon(addon, name, over=False):
    if over is not False:
        yes = 1
    else:
        from resources.libs import gui
        yes = gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                               '[COLOR {0}]Are you sure you want to delete the add-on:'.format(CONFIG.COLOR2),
                               'Name: [COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, name),
                               'ID: [COLOR {0}]{1}[/COLOR][/COLOR]'.format(CONFIG.COLOR1, addon),
                               yeslabel='[B][COLOR springgreen]Remove Add-on[/COLOR][/B]',
                               nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]')
    if yes == 1:
        folder = os.path.join(CONFIG.ADDONS, addon)
        logging.log("Removing Add-on: {0}".format(addon))

        from resources.libs import tools
        tools.clean_house(folder)
        xbmc.sleep(200)
        try:
            shutil.rmtree(folder)
        except Exception as e:
            logging.log("Error removing {0}: {1}".format(addon, str(e)), level=xbmc.LOGNOTICE)
        remove_addon_data(addon, name, over)
    if not over:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]{1} Removed[/COLOR]".format(CONFIG.COLOR2, name))


def remove_addon_data(addon):
    from resources.libs import gui

    if addon == 'all':  # clear ALL addon data
        if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                            '[COLOR {0}]Would you like to remove [COLOR {1}]ALL[/COLOR] addon data stored in your userdata folder?[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1),
                            yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]',
                            nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            tools.clean_house(CONFIG.ADDON_DATA)
        else:
            logging.log_notify('[COLOR {0}]Remove Addon Data[/COLOR]'.format(CONFIG.COLOR1),
                               '[COLOR {0}]Cancelled![/COLOR]'.format(CONFIG.COLOR2))
    elif addon == 'uninstalled':  # clear addon data for uninstalled addons
        if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
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
                else:
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
        if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
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
            if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                                '[COLOR {0}]Would you also like to remove the add-on data for:[/COLOR]'.format(CONFIG.COLOR2),
                                '[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, addon),
                                yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]',
                                nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
                tools.clean_house(addon_data)
                try:
                    shutil.rmtree(addon_data)
                except:
                    logging.log("Error deleting: {0}".format(addon_data))
            else:
                logging.log('Add-on data for {0} was not removed'.format(addon))
    xbmc.executebuiltin('Container.Refresh()')


def remove_addon_menu():
    from resources.libs import gui
    from resources.libs import logging
    from resources.libs import tools
    from resources.libs import update

    fold = glob.glob(os.path.join(CONFIG.ADDONS, '*/'))
    addonnames = []
    addonids = []
    for folder in sorted(fold, key=lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername in CONFIG.EXCLUDES:
            continue
        elif foldername in CONFIG.DEFAULTPLUGINS:
            continue
        elif foldername == 'packages':
            continue
        xml = os.path.join(folder, 'addon.xml')
        if os.path.exists(xml):
            match = tools.parse_dom(tools.read_from_file(xml), 'addon', ret='id')

            addid = foldername if len(match) == 0 else match[0]
            try:
                add = xbmcaddon.Addon(id=addid)
                addonnames.append(add.getAddonInfo('name'))
                addonids.append(addid)
            except:
                pass
    if len(addonnames) == 0:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]No Addons To Remove[/COLOR]".format(CONFIG.COLOR2))
        return
    selected = gui.DIALOG.multiselect("{0}: Select the addons you wish to remove.".format(CONFIG.ADDONTITLE), addonnames)
    if not selected:
        return
    if len(selected) > 0:
        update.addon_updates('set')
        for addon in selected:
            remove_addon(addonids[addon], addonnames[addon], True)

        xbmc.sleep(500)

        if CONFIG.INSTALLMETHOD == 1:
            todo = 1
        elif CONFIG.INSTALLMETHOD == 2:
            todo = 0
        else:
            todo = gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                                    "[COLOR {0}]Would you like to [COLOR {1}]Force close[/COLOR] Kodi or [COLOR {2}]Reload Profile[/COLOR]?[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1),
                                    yeslabel="[B][COLOR springgreen]Reload Profile[/COLOR][/B]",
                                    nolabel="[B][COLOR red]Force Close[/COLOR][/B]")
        if todo == 1:
            tools.reload_fix('remove addon')
        else:
            update.addon_updates('reset')
            tools.kill_kodi(True)
