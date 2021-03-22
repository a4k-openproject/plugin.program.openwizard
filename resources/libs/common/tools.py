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
import xbmcaddon
import xbmcgui

import os
import random
import re
import shutil
import string
import sys

if sys.version_info[0] > 2:
    # Python 3
    pass
else:
    # Python 2
    import codecs
    import warnings

    def open(file, mode='r', buffering=-1, encoding='utf-8', errors=None, newline=None, closefd=True, opener=None):
        if newline is not None:
            warnings.warn('newline is not supported in py2')
        if not closefd:
            warnings.warn('closefd is not supported in py2')
        if opener is not None:
            warnings.warn('opener is not supported in py2')
        return codecs.open(filename=file, mode=mode, encoding=encoding, errors=errors, buffering=buffering)

try:  # Python 3
    from urllib.parse import quote
    from urllib.parse import urlparse
    from html.parser import HTMLParser
except ImportError:  # Python 2
    from urllib import quote
    from urlparse import urlparse
    import HTMLParser

from contextlib import contextmanager

from resources.libs.common.config import CONFIG


#########################
#  File Functions       #
#########################


def read_from_file(file, mode='r'):
    f = open(file, mode, encoding='utf-8')
    a = f.read()
    f.close()
    return a

def read_from_file_old(file, mode='r'):
    f = open(file, mode, encoding=None)
    a = f.read()
    f.close()
    return a


def write_to_file(file, content, mode='w'):
    f = open(file, mode, encoding='utf-8')
    f.write(content)
    f.close()


def remove_folder(path):
    from resources.libs.common import logging

    logging.log("Deleting Folder: {0}".format(path))
    try:
        shutil.rmtree(path, ignore_errors=True, onerror=None)
    except:
        return False


def remove_file(path):
    from resources.libs.common import logging

    logging.log("Deleting File: {0}".format(path))
    try:
        os.remove(path)
    except:
        return False


def empty_folder(folder):
    total = 0
    for root, dirs, files in os.walk(folder, topdown=True):
        dirs[:] = [d for d in dirs if d not in CONFIG.EXCLUDES]
        file_count = 0
        file_count += len(files) + len(dirs)
        if file_count == 0:
            shutil.rmtree(os.path.join(root))
            total += 1

            from resources.libs.common import logging
            logging.log("Empty Folder: {0}".format(root))
    return total


def clean_house(folder, ignore=False):
    from resources.libs.common import logging

    logging.log(folder)
    total_files = 0
    total_folds = 0
    for root, dirs, files in os.walk(folder):
        if not ignore:
            dirs[:] = [d for d in dirs if d not in CONFIG.EXCLUDES]
        file_count = 0
        file_count += len(files)
        if file_count >= 0:
            for f in files:
                try:
                    os.unlink(os.path.join(root, f))
                    total_files += 1
                except:
                    try:
                        shutil.rmtree(os.path.join(root, f))
                    except:
                        logging.log("Error Deleting {0}".format(f), level=xbmc.LOGERROR)
            for d in dirs:
                total_folds += 1
                try:
                    shutil.rmtree(os.path.join(root, d))
                    total_folds += 1
                except:
                    logging.log("Error Deleting {0}".format(d), level=xbmc.LOGERROR)
    return total_files, total_folds


def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    if not os.path.isdir(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
        except EnvironmentError as why:
            errors.append((srcname, dstname, str(why)))
        except Exception as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Exception


def file_count(home, excludes=True):
    item = []
    for base, dirs, files in os.walk(home):
        if excludes:
            dirs[:] = [d for d in dirs if os.path.join(base, d) not in CONFIG.EXCLUDE_DIRS]
            files[:] = [f for f in files if f not in CONFIG.EXCLUDE_FILES]
        for file in files:
            item.append(file)
    return len(item)
    

def ensure_folders(folder=None):
    import xbmcvfs

    name = ''
    folders = [CONFIG.BACKUPLOCATION, CONFIG.MYBUILDS, CONFIG.PLUGIN_DATA,
               CONFIG.USERDATA, CONFIG.ADDON_DATA, CONFIG.PACKAGES]

    try:
        if folder is not None and not os.path.exists(folder):
            name = folder
            xbmcvfs.mkdirs(folder)
            return

        for f in folders:
            if not os.path.exists(f):
                name = f
                xbmcvfs.mkdirs(f)

    except Exception as e:
        dialog = xbmcgui.Dialog()

        dialog.ok(CONFIG.ADDONTITLE,
                      "[COLOR {0}]Error creating add-on directories:[/COLOR]".format(CONFIG.COLOR2)
                      +'\n'+"[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name))

#########################
#  Utility Functions    #
#########################


@contextmanager
def busy_dialog():
    xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    try:
        yield
    finally:
        xbmc.executebuiltin('Dialog.Close(busydialognocancel)')


def convert_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G']:
        if abs(num) < 1024.0:
            return "%3.02f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.02f %s%s" % (num, 'G', suffix)


def get_keyboard(default="", heading="", hidden=False):
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    return default


def get_size(path, total=0):
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total


def percentage(part, whole):
    return 100 * float(part)/float(whole)


def parse_dom(html, name=u"", attrs={}, ret=False):
    if isinstance(html, str):
        try:
            html = html.decode("utf-8")
        except:
            html = html
    elif not isinstance(html, list):
        return u""

    if not name.strip():
        return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item:
            item = item.replace(match, match.replace("\n", " "))

        lst = []
        for key in attrs:
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
            if len(lst2) == 0 and attrs[key].find(" ") == -1:
                lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

            if len(lst) == 0:
                lst = lst2
                lst2 = []
            else:
                test = range(len(lst))
                test.reverse()
                for i in test:
                    if not lst[i] in lst2:
                        del(lst[i])

        if len(lst) == 0 and attrs == {}:
            lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
            if len(lst) == 0:
                lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                attr_lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
                if len(attr_lst) == 0:
                    attr_lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
                for tmp in attr_lst:
                    cont_char = tmp[0]
                    if cont_char in "'\"":
                        if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                            tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

                        if tmp.rfind(cont_char, 1) > -1:
                            tmp = tmp[1:tmp.rfind(cont_char)]
                    else:
                        if tmp.find(" ") > 0:
                            tmp = tmp[:tmp.find(" ")]
                        elif tmp.find("/") > 0:
                            tmp = tmp[:tmp.find("/")]
                        elif tmp.find(">") > 0:
                            tmp = tmp[:tmp.find(">")]

                    lst2.append(tmp.strip())
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                endstr = u"</" + name

                start = item.find(match)
                end = item.find(endstr, start)
                pos = item.find("<" + name, start + 1 )

                while pos < end and pos != -1:
                    tend = item.find(endstr, end + len(endstr))
                    if tend != -1:
                        end = tend
                    pos = item.find("<" + name, pos + 1)

                if start == -1 and end == -1:
                    temp = u""
                elif start > -1 and end > -1:
                    temp = item[start + len(match):end]
                elif end > -1:
                    temp = item[:end]
                elif start > -1:
                    temp = item[start + len(match):]

                if ret:
                    endstr = item[end:item.find(">", item.find(endstr)) + 1]
                    temp = match + temp + endstr

                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst


def get_date(days=0, formatted=False):
    import time

    value = time.time() + (days * 24 * 60 * 60)  # days * 24h * 60m * 60s

    return value if not formatted else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))


def basecode(text, encode=True):
    import base64
    if encode:
        msg = base64.encodestring(text)
    else:
        msg = base64.decodestring(text)
    return msg


def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
    elif xbmc.getCondVisibility('system.platform.darwin'):
        return 'ios'


def kodi_version():
    if 19.0 <= CONFIG.KODIV <= 19.9:
        vername = 'Matrix'
    else:
        vername = "Unknown"
    return vername


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def kill_kodi(msg=None, over=None):
    if over:
        choice = 1
    else:
        dialog = xbmcgui.Dialog()
        
        if not msg:
            msg = '[COLOR {0}]You are about to close Kodi. Would you like to continue?[/COLOR]'.format(CONFIG.COLOR2)
        
        choice = dialog.yesno('Force Close Kodi',
                                  msg,
                                  nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',
                                  yeslabel='[B][COLOR springgreen]Force Close Kodi[/COLOR][/B]')
    if choice == 1:
        from resources.libs.common import logging
        logging.log("Force Closing Kodi: Platform[{0}]".format(str(platform())))
        os._exit(1)


def reload_profile(profile=None):
    if profile is None:
        xbmc.executebuiltin('LoadProfile(Master user)')
    else:
        xbmc.executebuiltin('LoadProfile({0})'.format(profile))


def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]


def convert_special(url, over=False):
    from resources.libs.common import logging

    progress_dialog = xbmcgui.DialogProgress()
    
    total = file_count(url)
    start = 0
    progress_dialog.create(CONFIG.ADDONTITLE, "[COLOR {0}]Changing Physical Paths To Special".format(CONFIG.COLOR2) + "\n" + "Please Wait[/COLOR]")
    for root, dirs, files in os.walk(url):
        for file in files:
            start += 1
            perc = int(percentage(start, total))
            if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
                progress_dialog.update(perc, "[COLOR {0}]Scanning: [COLOR {1}]{2}[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, root.replace(CONFIG.HOME, '')) + '\n' + "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, file) + '\n' + "Please Wait[/COLOR]")
                a = read_from_file(os.path.join(root, file))
                encodedpath = quote(CONFIG.HOME)
                encodedpath2 = quote(CONFIG.HOME).replace('%3A', '%3a').replace('%5C', '%5c')
                b = a.replace(CONFIG.HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
                
                try:
                    write_to_file(os.path.join(root, file), b)
                except IOError as e:
                    logging.log('Unable to open file to convert special paths: {}'.format(os.path.join(root, file)))

                if progress_dialog.iscanceled():
                    progress_dialog.close()
                    logging.log_notify(CONFIG.ADDONTITLE,
                                       "[COLOR {0}]Convert Path Cancelled[/COLOR]".format(CONFIG.COLOR2))
                    sys.exit()
    progress_dialog.close()
    logging.log("[Convert Paths to Special] Complete")
    if not over:
        logging.log_notify(CONFIG.ADDONTITLE,
                           "[COLOR {0}]Convert Paths to Special: Complete![/COLOR]".format(CONFIG.COLOR2))


def redo_thumbs():
    if not os.path.exists(CONFIG.THUMBNAILS):
        os.makedirs(CONFIG.THUMBNAILS)
    thumbfolders = '0123456789abcdef'
    videos = os.path.join(CONFIG.THUMBNAILS, 'Video', 'Bookmarks')
    for item in thumbfolders:
        foldname = os.path.join(CONFIG.THUMBNAILS, item)
        if not os.path.exists(foldname):
            os.makedirs(foldname)
    if not os.path.exists(videos):
        os.makedirs(videos)


def reload_fix(default=None):
    from resources.libs import db
    from resources.libs.common import logging
    from resources.libs import skin
    from resources.libs import update

    dialog = xbmcgui.Dialog()
    
    dialog.ok(CONFIG.ADDONTITLE,
                  "[COLOR {0}]WARNING: Sometimes Reloading the Profile causes Kodi to crash. While Kodi is Reloading the Profile Please Do Not Press Any Buttons![/COLOR]".format(CONFIG.COLOR2))
                  
    if not os.path.exists(CONFIG.PACKAGES):
        os.makedirs(CONFIG.PACKAGES)
    if default is None:
        skin.look_and_feel_data('save')
    redo_thumbs()
    xbmc.executebuiltin('ActivateWindow(Home)')
    reload_profile()
    xbmc.sleep(10000)
    if CONFIG.KODIV >= 17:
        db.kodi_17_fix()
    if default is None:
        logging.log("Switching to: {0}".format(CONFIG.get_setting('defaultskin')))
        gotoskin = CONFIG.get_setting('defaultskin')
        skin.switch_to_skin(gotoskin)
        skin.look_and_feel_data('restore')
    update.addon_updates('reset')
    update.force_update()
    xbmc.executebuiltin("ReloadSkin()")


def data_type(str):
    datatype = type(str).__name__
    return datatype


def replace_html_codes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    return txt


def ascii_check(use=None, over=False):
    from resources.libs.common import logging
    from resources.libs.gui import window
    
    dialog = xbmcgui.Dialog()
    progress_dialog = xbmcgui.DialogProgress()

    if use is None:
        source = dialog.browse(3,
                                   '[COLOR {0}]Select the folder you want to scan[/COLOR]'.format(CONFIG.COLOR2),
                                   'files', '', False, False, CONFIG.HOME)
        if over:
            yes = 1
        else:
            yes = dialog.yesno(CONFIG.ADDONTITLE,
                                   '[COLOR {0}]Do you want to [COLOR {1}]delete[/COLOR] all filenames with special characters or would you rather just [COLOR {2}]scan and view[/COLOR] the results in the log?[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1),
                                   yeslabel='[B][COLOR springgreen]Delete[/COLOR][/B]',
                                   nolabel='[B][COLOR red]Scan[/COLOR][/B]')
    else:
        source = use
        yes = 1

    if source == "":
        logging.log_notify(CONFIG.ADDONTITLE,
                           "[COLOR {0}]ASCII Check: Cancelled[/COLOR]".format(CONFIG.COLOR2))
        return

    files_found = os.path.join(CONFIG.PLUGIN_DATA, 'asciifiles.txt')
    files_fails = os.path.join(CONFIG.PLUGIN_DATA, 'asciifails.txt')
    afiles = open(files_found, mode='w+')
    afails = open(files_fails, mode='w+')
    f1 = 0
    f2 = 0
    items = file_count(source)
    msg = ''
    prog = []
    logging.log("Source file: ({0})".format(str(source)))

    progress_dialog.create(CONFIG.ADDONTITLE, 'Please wait...')
    for base, dirs, files in os.walk(source):
        dirs[:] = [d for d in dirs]
        files[:] = [f for f in files]
        for file in files:
            prog.append(file)
            prog2 = int(len(prog) / float(items) * 100)
            progress_dialog.update(prog2, "[COLOR {0}]Checking for non ASCII files".format(CONFIG.COLOR2) + '\n' + '[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, file) + '\n' + 'Please Wait[/COLOR]')
            try:
                file.encode('ascii')
            except UnicodeEncodeError:
                logging.log("[ASCII Check] Illegal character found in file: {0}".format(file))
            except UnicodeDecodeError:
                logging.log("[ASCII Check] Illegal character found in file: {0}".format(file))
                badfile = os.path.join(base, file)
                if yes:
                    try:
                        os.remove(badfile)
                        for chunk in chunks(badfile, 75):
                            afiles.write(chunk+'\n')
                        afiles.write('\n')
                        f1 += 1
                        logging.log("[ASCII Check] File Removed: {0} ".format(badfile), level=xbmc.LOGERROR)
                    except:
                        for chunk in chunks(badfile, 75):
                            afails.write(chunk+'\n')
                        afails.write('\n')
                        f2 += 1
                        logging.log("[ASCII Check] File Failed: {0} ".format(badfile), level=xbmc.LOGERROR)
                else:
                    for chunk in chunks(badfile, 75):
                        afiles.write(chunk+'\n')
                    afiles.write('\n')
                    f1 += 1
                    logging.log("[ASCII Check] File Found: {0} ".format(badfile), level=xbmc.LOGERROR)
                pass
        if progress_dialog.iscanceled():
            progress_dialog.close()
            logging.log_notify(CONFIG.ADDONTITLE,
                               "[COLOR {0}]ASCII Check Cancelled[/COLOR]".format(CONFIG.COLOR2))
            sys.exit()
    progress_dialog.close()
    afiles.close()
    afails.close()
    total = int(f1) + int(f2)
    if total > 0:
        if os.path.exists(files_found):
            msg = read_from_file(files_found)
        if os.path.exists(files_fails):
            msg2 = read_from_file(files_fails)
        if yes:
            if use:
                logging.log_notify(CONFIG.ADDONTITLE,
                                 "[COLOR {0}]ASCII Check: {1} Removed / {2} Failed.[/COLOR]".format(CONFIG.COLOR2, f1, f2))
            else:
                window.show_text_box("Viewing Removed ASCII Files",
                                  "[COLOR yellow][B]{0} Files Removed:[/B][/COLOR]\n {1}\n\n[COLOR yellow][B]{2} Files Failed:[B][/COLOR]\n {3}".format(f1, msg, f2, msg2))
        else:
            window.show_text_box("Viewing Found ASCII Files", "[COLOR yellow][B]{0} Files Found:[/B][/COLOR]\n {1}".format(f1, msg))
    else:
        logging.log_notify(CONFIG.ADDONTITLE,
                           "[COLOR {0}]ASCII Check: None Found.[/COLOR]".format(CONFIG.COLOR2))


def clean_text(text):
    return text.replace('\n', '')\
                .replace('\r', '')\
                .replace('\t', '')\
                .replace('gui=""', 'gui="http://"')\
                .replace('theme=""', 'theme="http://"')\
                .replace('adult=""', 'adult="no"')
                


#########################
#  Add-on Functions     #
#########################


def get_addon_by_id(id):
    try:
        return xbmcaddon.Addon(id=id)
    except:
        return False


def get_addon_info(id, info):
    addon = get_addon_by_id(id)
    if addon:
        return addon.getAddonInfo(info)
    else:
        return False


def get_info_label(label):
    try:
        return xbmc.getInfoLabel(label)
    except:
        return False

#########################
#  URL Functions        #
#########################


def _is_url(url):
    try:  # Python 3
        from urllib.parse import urlparse
    except ImportError:  # Python 2
        from urlparse import urlparse

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def _check_url(url, cred):
    import requests
    from resources.libs.common import logging

    if _is_url(url):
        try:
            response = requests.head(url, headers={'user-agent': CONFIG.USER_AGENT}, allow_redirects=True, auth=cred)
            
            if response.status_code < 300:
                logging.log("URL check passed for {0}: Status code [{1}]".format(url, response.status_code), level=xbmc.LOGDEBUG)
                return True
            elif response.status_code < 400:
                logging.log("URL check redirected from {0} to {1}: Status code [{2}]".format(url, response.headers['Location'], response.status_code), level=xbmc.LOGDEBUG)
                return _check_url(response.headers['Location'])
            elif response.status_code == 401:
                logging.log("URL requires authentication for {0}: Status code [{1}]".format(url, response.status_code), level=xbmc.LOGDEBUG)
                return 'auth'
            else:
                logging.log("URL check failed for {0}: Status code [{1}]".format(url, response.status_code), level=xbmc.LOGDEBUG)
                return False
        except Exception as e:
            logging.log("URL check error for {0}: [{1}]".format(url, e), level=xbmc.LOGDEBUG)
            return False
    else:
        logging.log("URL is not of a valid schema: {0}".format(url), level=xbmc.LOGDEBUG)
        return False
        

def open_url(url, stream=False, check=False, cred=None, count=0):
    import requests

    if not url:
        return False

    dialog = xbmcgui.Dialog()
    user_agent = {'user-agent': CONFIG.USER_AGENT}
    count = 0
    
    valid = _check_url(url, cred)

    if not valid:
        return False
    else:
        if check:
            return True if valid else False
            
        if valid == 'auth' and not cred:
            cred = (get_keyboard(heading='Username'), get_keyboard(heading='Password'))
            
        response = requests.get(url, headers=user_agent, timeout=10.000, stream=stream, auth=cred)

        if response.status_code == 401:
            retry = dialog.yesno(CONFIG.ADDONTITLE, 'Either the username or password were invalid. Would you like to try again?', yeslabel='Try Again', nolabel='Cancel')
            
            if retry and count < 3:
                count += 1
                cred = (get_keyboard(heading='Username'), get_keyboard(heading='Password'))
                
                response = open_url(url, stream, check, cred, count)
            else:
                dialog.ok(CONFIG.ADDONTITLE, 'Authentication Failed.')
                return False
        
        return response
