import xbmc
import xbmcaddon

import os
import random
import re
import shutil
import string

try:  # Python 3
    from urllib.request import urlopen
    from urllib.request import Request
except ImportError:  # Python 3
    from urllib2 import urlopen
    from urllib2 import Request

from resources.libs.config import CONFIG


#########################
#  File Functions       #
#########################


def read_from_file(file):
    f = open(file)
    a = f.read()
    f.close()
    return a


def write_to_file(file, content, mode='w'):
    f = open(file, mode)
    f.write(content)
    f.close()


def remove_folder(path):
    from resources.libs import logging

    logging.log("Deleting Folder: {0}".format(path), level=xbmc.LOGNOTICE)
    try:
        shutil.rmtree(path, ignore_errors=True, onerror=None)
    except:
        return False


def remove_file(path):
    from resources.libs import logging

    logging.log("Deleting File: {0}".format(path), level=xbmc.LOGNOTICE)
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

            from resources.libs import logging
            logging.log("Empty Folder: {0}".format(root), level=xbmc.LOGNOTICE)
    return total


def clean_house(folder, ignore=False):
    from resources.libs import logging

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

#########################
#  Utility Functions    #
#########################


def convert_size(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G']:
        if abs(num) < 1024.0:
            return "%3.02f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.02f %s%s" % (num, 'G', suffix)


def get_keyboard( default="", heading="", hidden=False ):
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if keyboard.isConfirmed():
        return unicode(keyboard.getText(), "utf-8")
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
            html = [html.decode("utf-8")]
        except:
            html = [html]
    elif isinstance(html, unicode):
        html = [html]
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


def get_date(days=0, now=False):
    from datetime import date
    from datetime import datetime
    from datetime import timedelta

    if now:
        return datetime.now()
    else:
        if days == 0:
            return date.today()
        else:
            return date.today() + timedelta(days)


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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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


def open_url(url):
    req = Request(url)
    req.add_header('User-Agent', CONFIG.USER_AGENT)
    response = urlopen(req)
    link = response.read()
    response.close()
    return link
