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

import sys

import uservar
from resources.libs import logging
from resources.libs import tools
from resources.libs import vars
from resources.libs import whitelist


KEEPFAVS = tools.get_setting('keepfavourites')
KEEPSOURCES = tools.get_setting('keepsources')
KEEPPROFILES = tools.get_setting('keepprofiles')
KEEPPLAYERCORE = tools.get_setting('keepplayercore')
KEEPADVANCED = tools.get_setting('keepadvanced')
KEEPSUPER = tools.get_setting('keepsuper')
KEEPREPOS = tools.get_setting('keeprepos')
KEEPWHITELIST = tools.get_setting('keepwhitelist')

if vars.KODIV > 17:
    from resources.libs import zfile as zipfile
else:
    import zipfile

bad_files = ['onechannelcache.db', 'saltscache.db', 'saltscache.db-shm', 'saltscache.db-wal',
             'saltshd.lite.db', 'saltshd.lite.db-shm', 'saltshd.lite.db-wal', 'queue.db', 'commoncache.db',
             'access.log', 'trakt.db', 'video_cache.db']


def all(_in, _out, dp=None, ignore=None, title=None):
    if dp:
        return allWithProgress(_in, _out, dp, ignore, title)
    else:
        return allNoProgress(_in, _out, ignore)


def allNoProgress(_in, _out, ignore):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception as e:
        logging.log(str(e))
        return False
    return True


def allWithProgress(_in, _out, dp, ignore, title):
    count = 0
    errors = 0
    error = ''
    update = 0
    size = 0
    excludes = []

    try:
        zin = zipfile.ZipFile(_in,  'r')
    except Exception as e:
        errors += 1
        error += '%s\n' % e
        logging.log('Error Checking Zip: {0}'.format(str(e)), level=xbmc.LOGERROR)
        return update, errors, error

    white_list = whitelist.whitelist('read')
    for item in white_list:
        try:
            name, id, fold = item
        except:
            pass
        excludes.append(fold)
        if fold.startswith('pvr'):
            tools.set_setting('pvrclient', id)

    nFiles = float(len(zin.namelist()))
    zipsize = tools.convert_size(sum([item.file_size for item in zin.infolist()]))

    zipit = str(_in).replace('\\', '/').split('/')
    title = title if title else zipit[-1].replace('.zip', '')

    for item in zin.infolist():
        try:
            str(item.filename).encode('ascii')
        except UnicodeDecodeError:
            logging.log("[ASCII Check] Illegal character found in file: {0}".format(item.filename))
            continue
        except UnicodeEncodeError:
            logging.log("[ASCII Check] Illegal character found in file: {0}".format(item.filename))
            continue
        count += 1
        prog = int(count / nFiles * 100)
        size += item.file_size
        file = str(item.filename).split('/')
        skip = False
        line1 = '%s [COLOR %s][B][Errors:%s][/B][/COLOR]' % (title, uservar.COLOR2, errors)
        line2 = '[COLOR %s][B]File:[/B][/COLOR] [COLOR %s]%s/%s[/COLOR] ' % (uservar.COLOR2, uservar.COLOR1, count, int(nFiles))
        line2 += '[COLOR %s][B]Size:[/B][/COLOR] [COLOR %s]%s/%s[/COLOR]' % (uservar.COLOR2, uservar.COLOR1, wiz.convertSize(size), zipsize)
        line3 = '[COLOR %s]%s[/COLOR]' % (uservar.COLOR1, item.filename)
        if item.filename == 'userdata/sources.xml' and KEEPSOURCES == 'true': skip = True
        elif item.filename == 'userdata/favourites.xml' and KEEPFAVS == 'true': skip = True
        elif item.filename == 'userdata/profiles.xml' and KEEPPROFILES == 'true': skip = True
        elif item.filename == 'userdata/playercorefactory.xml' and KEEPPLAYERCORE == 'true': skip = True
        elif item.filename == 'userdata/advancedsettings.xml' and KEEPADVANCED == 'true': skip = True
        elif file[0] == 'addons' and file[1] in excludes: skip = True
        elif file[0] == 'userdata' and file[1] == 'addon_data' and file[2] in excludes: skip = True
        elif file[-1] in logging.LOGFILES: skip = True
        elif file[-1] in bad_files: skip = True
        elif file[-1].endswith('.csv'): skip = True
        elif not str(item.filename).find('plugin.program.super.favourites') == -1 and KEEPSUPER == 'true': skip = True
        elif not str(item.filename).find(uservar.ADDON_ID) == -1 and ignore == None: skip = True
        if skip:
            logging.log("Skipping: %s" % item.filename, xbmc.LOGNOTICE)
        else:
            try:
                zin.extract(item, _out)
            except Exception as e:
                errormsg  = "[COLOR %s]File:[/COLOR] [COLOR %s]%s[/COLOR]\n" % (uservar.COLOR2, uservar.COLOR1, file[-1])
                errormsg += "[COLOR %s]Folder:[/COLOR] [COLOR %s]%s[/COLOR]\n" % (uservar.COLOR2, uservar.COLOR1, (item.filename).replace(file[-1],''))
                errormsg += "[COLOR %s]Error:[/COLOR] [COLOR %s]%s[/COLOR]\n\n" % (uservar.COLOR2, uservar.COLOR1, str(e).replace('\\\\','\\').replace("'%s'" % item.filename, ''))
                errors += 1; error += errormsg
                logging.log('Error Extracting: %s(%s)' % (item.filename, str(e)), xbmc.LOGERROR)
                pass
        dp.update(prog, line1, line2, line3)
        if dp.iscanceled(): break
    if dp.iscanceled():
        dp.close()
        logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]Extract Cancelled[/COLOR]" % uservar.COLOR2)
        sys.exit()
    return prog, errors, error
