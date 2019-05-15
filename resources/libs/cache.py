import xbmc

import glob
import os
import shutil

from datetime import datetime
from datetime import timedelta

import sqlite3 as database

from resources.libs.config import CONFIG
from resources.libs import db
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
    if os.path.exists(CONFIG.ARCHIVE_CACHE):
        from resources.libs import tools
        tools.clean_house(CONFIG.ARCHIVE_CACHE)


def clear_function_cache():
    if xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)'):
        xbmc.executebuiltin('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')
    if xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)'):
        xbmc.executebuiltin('RunPlugin(plugin://script.module.urlresolver/?mode=reset_cache)')


def clear_cache(over=None):
    PROFILEADDONDATA = os.path.join(CONFIG.PROFILE, 'addon_data')
    dbfiles = [
        ## TODO: Double check these
        (os.path.join(CONFIG.ADDOND, 'plugin.video.placenta', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.placenta', 'cache.meta.5.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.placenta', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.gaia', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.gaia', 'meta.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.exodusredux', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.exodusredux', 'meta.5.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.exodusredux', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.overeasy', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.overeasy', 'meta.5.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.overeasy', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.venom', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.yoda', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.yoda', 'meta.5.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.yoda', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.scrubsv2', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.scrubsv2', 'meta.5.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.scrubsv2', 'cache.providers.13.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.seren', 'cache.db')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.seren', 'torrentScrape.db')),
        (os.path.join(CONFIG.ADDOND, 'script.module.simplecache', 'simplecache.db'))]

    cachelist = [
        (PROFILEADDONDATA),
        (CONFIG.ADDOND),
        (os.path.join(CONFIG.HOME, 'cache')),
        (os.path.join(CONFIG.HOME, 'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(CONFIG.ADDOND, 'script.module.simple.downloader')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.itv', 'Images')),
        (os.path.join(PROFILEADDONDATA, 'script.module.simple.downloader')),
        (os.path.join(PROFILEADDONDATA, 'plugin.video.itv', 'Images')),
        (os.path.join(CONFIG.ADDOND, 'script.extendedinfo', 'images')),
        (os.path.join(CONFIG.ADDOND, 'script.extendedinfo', 'TheMovieDB')),
        (os.path.join(CONFIG.ADDOND, 'script.extendedinfo', 'YouTube')),
        (os.path.join(CONFIG.ADDOND, 'plugin.program.autocompletion', 'Google')),
        (os.path.join(CONFIG.ADDOND, 'plugin.program.autocompletion', 'Bing')),
        (os.path.join(CONFIG.ADDOND, 'plugin.video.openmeta', '.storage'))]

    delfiles = 0
    excludes = ['meta_cache', 'archive_cache']
    for item in cachelist:
        if not os.path.exists(item):
            continue
        if item not in [CONFIG.ADDOND, PROFILEADDONDATA]:
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
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.placenta', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.placenta', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.placenta', 'providers.13.db'))
            if CONFIG.INCLUDEEXODUSREDUX == 'true':
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.exodusredux', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.exodusredux', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.exodusredux', 'providers.13.db'))
            if CONFIG.INCLUDEYODA == 'true':
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.yoda', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.yoda', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.yoda', 'providers.13.db'))
            if CONFIG.INCLUDEVENOM == 'true':
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.venom', 'cache.db'))
            if CONFIG.INCLUDESCRUBS == 'true':
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.scrubsv2', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.scrubsv2', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.scrubsv2', 'providers.13.db'))
            if CONFIG.INCLUDEOVEREASY == 'true':
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.overeasy', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.overeasy', 'meta.5.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.overeasy', 'providers.13.db'))
            if CONFIG.INCLUDEGAIA == 'true':
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.gaia', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.gaia', 'meta.db'))
            if CONFIG.INCLUDESEREN == 'true':
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.seren', 'cache.db'))
                files.append(os.path.join(CONFIG.ADDOND, 'plugin.video.seren', 'torrentScrape.db'))
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
            textdb = database.connect(dbfile)
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
        path = os.path.join(CONFIG.THUMBNAILSS, image)
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
