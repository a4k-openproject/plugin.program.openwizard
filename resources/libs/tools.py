import xbmc
import xbmcaddon

import glob
import os
import re
import shutil

try:
    from sqlite3 import dbapi2 as database
    from urllib.request import urlopen
    from urllib.request import Request
except ImportError:
    from pysqlite2 import dbapi2 as database
    from urllib2 import urlopen
    from urllib2 import Request

from datetime import date
from datetime import datetime
from datetime import timedelta

import uservar
from resources.libs import check
from resources.libs import downloader
from resources.libs import extract
from resources.libs import gui
from resources.libs import logging
from resources.libs import notify
from resources.libs import vars

#########################
#  Settings Functions   #
#########################


def get_setting(name):
    try:
        return vars.ADDON.getSetting(name)
    except:
        return False


def set_setting(name, value):
    try:
        vars.ADDON.setSetting(name, value)
    except:
        return False


def clear_setting(type):
    build = {'buildname': '', 'buildversion': '', 'buildtheme': '', 'latestversion': '', 'lastbuildcheck': '2016-01-01'}
    install = {'installed': 'false', 'extract': '', 'errors': ''}
    default = {'defaultskinignore': 'false', 'defaultskin': '', 'defaultskinname': ''}
    lookfeel = ['default.enablerssfeeds', 'default.font', 'default.rssedit', 'default.skincolors', 'default.skintheme',
                'default.skinzoom', 'default.soundskin', 'default.startupwindow', 'default.stereostrength']
    if type == 'build':
        for element in build:
            set_setting(element, build[element])
        for element in install:
            set_setting(element, install[element])
        for element in default:
            set_setting(element, default[element])
        for element in lookfeel:
            set_setting(element, '')
    elif type == 'default':
        for element in default:
            set_setting(element, default[element])
        for element in lookfeel:
            set_setting(element, '')
    elif type == 'install':
        for element in install:
            set_setting(element, install[element])
    elif type == 'lookfeel':
        for element in lookfeel:
            set_setting(element, '')

#########################
#  File Functions       #
#########################


def read_from_file(file):
    f = open(file)
    a = f.read()
    f.close()
    return a


def write_to_file(file, content):
    f = open(file, 'w')
    f.write(content)
    f.close()


def remove_folder(path):
    logging.log("Deleting Folder: {0}".format(path), level=xbmc.LOGNOTICE)
    try:
        shutil.rmtree(path, ignore_errors=True, onerror=None)
    except:
        return False


def remove_file(path):
    logging.log("Deleting File: {0}".format(path), level=xbmc.LOGNOTICE)
    try:
        os.remove(path)
    except:
        return False


def clean_house(folder, ignore=False):
    logging.log(folder)
    total_files = 0
    total_folds = 0
    for root, dirs, files in os.walk(folder):
        if not ignore: dirs[:] = [d for d in dirs if d not in uservar.EXCLUDES]
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
        except Exception as err:
            errors.extend(err.args[0])
        except EnvironmentError as why:
            errors.append((srcname, dstname, str(why)))
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
    if not now:
        if days == 0:
            return date.today()
        else:
            return date.today() + timedelta(days)
    else:
        return datetime.now()


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

#########################
#  URL Functions        #
#########################


def working_url(url):
    if url in ['http://', 'https://', '']:
        return False
    check = 0
    status = ''
    while check < 3:
        check += 1
        try:
            req = Request(url)
            req.add_header('User-Agent', vars.USER_AGENT)
            response = urlopen(req)
            response.close()
            status = True
            break
        except Exception as e:
            status = str(e)
            logging.log("Working Url Error: %s [%s]" % (e, url))
            xbmc.sleep(500)
    return status


def open_url(url):
    req = Request(url)
    req.add_header('User-Agent', vars.USER_AGENT)
    response = urlopen(req)
    link = response.read()
    response.close()
    return link

#########################
#  Update Functions     #
#########################


def force_update(silent=False):
    xbmc.executebuiltin('UpdateAddonRepos()')
    xbmc.executebuiltin('UpdateLocalAddons()')
    if not silent:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                           '[COLOR {0}]Forcing Addon Updates[/COLOR]'.format(uservar.COLOR2))


def wizard_update(startup=None):
    if working_url(uservar.WIZARDFILE):
        try:
            wid, ver, zip = check.check_wizard('all')
        except:
            return
        if ver > vars.VERSION:
            yes = gui.DIALOG.yesno(uservar.ADDONTITLE,
                                   '[COLOR {0}]There is a new version of the [COLOR {1}]{2}[/COLOR]!'.format(uservar.COLOR2, uservar.COLOR1, uservar.ADDONTITLE),
                                   'Would you like to download [COLOR {0}]v{1}[/COLOR]?[/COLOR]'.format(uservar.COLOR1, ver),
                                   nolabel='[B][COLOR red]Remind Me Later[/COLOR][/B]',
                                   yeslabel="[B][COLOR springgreen]Update Wizard[/COLOR][/B]")
            if yes:
                logging.log("[Auto Update Wizard] Installing wizard v{0}".format(ver), level=xbmc.LOGNOTICE)
                gui.DP.create(uservar.ADDONTITLE, '[COLOR {0}]Downloading Update...'.format(uservar.COLOR2), '',
                              'Please Wait[/COLOR]')
                lib = os.path.join(vars.PACKAGES, '{0}-{1}.zip'.format(uservar.ADDON_ID, ver))
                try:
                    os.remove(lib)
                except:
                    pass
                downloader.download(zip, lib, DP)
                xbmc.sleep(2000)
                gui.DP.update(0, "", "Installing {0} update".format(uservar.ADDONTITLE))
                percent, errors, error = extract.all(lib, vars.ADDONS, gui.DP, True)
                gui.DP.close()
                xbmc.sleep(1000)
                force_update()
                xbmc.sleep(1000)
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                                   '[COLOR {0}]Add-on updated[/COLOR]'.format(uservar.COLOR2))
                logging.log("[Auto Update Wizard] Wizard updated to v{0}".format(ver), level=xbmc.LOGNOTICE)
                remove_file(os.path.join(uservar.ADDONDATA, 'settings.xml'))
                notify.firstRunSettings()
                if startup:
                    xbmc.executebuiltin('RunScript({0}/startup.py)'.format(vars.PLUGIN))
                return
            else:
                logging.log("[Auto Update Wizard] Install New Wizard Ignored: {0}".format(ver), level=xbmc.LOGNOTICE)
        else:
            if not startup:
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                                   "[COLOR {0}]No New Version of Wizard[/COLOR]".format(uservar.COLOR2))
            logging.log("[Auto Update Wizard] No New Version v{0}".format(ver), level=xbmc.LOGNOTICE)
    else:
        logging.log("[Auto Update Wizard] Url for wizard file not valid: {0}".format(uservar.WIZARDFILE), level=xbmc.LOGNOTICE)


def addon_updates(do=None):
    setting = '"general.addonupdates"'
    if do == 'set':
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % setting
        response = xbmc.executeJSONRPC(query)
        match = re.compile('{"value":(.+?)}').findall(response)
        if len(match) > 0:
            default = match[0]
        else:
            default = 0
        set_setting('default.addonupdate', str(default))
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, '2')
        response = xbmc.executeJSONRPC(query)
    elif do == 'reset':
        try:
            value = int(float(get_setting('default.addonupdate')))
        except:
            value = 0
        if value not in [0, 1, 2]:
            value = 0
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
        response = xbmc.executeJSONRPC(query)

#########################
#  Add-on Functions     #
#########################


def get_info(label):
    try:
        return xbmc.getInfoLabel(label)
    except:
        return False


def addon_database(addon=None, state=1, array=False):
    dbfile = latest_db('Addons')
    dbfile = os.path.join(vars.DATABASE, dbfile)
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
    if db in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
        match = glob.glob(os.path.join(vars.DATABASE, '{0}*.db'.format(db)))
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
    addonlist = glob.glob(os.path.join(vars.ADDONS, '*/'))
    disabledAddons = []
    for folder in sorted(addonlist, key=lambda x: x):
        addonxml = os.path.join(folder, 'addon.xml')
        if os.path.exists(addonxml):
            fold = folder.replace(vars.ADDONS, '')[1:-1]
            aid = parse_dom(read_from_file(addonxml), 'addon', ret='id')
            try:
                if len(aid) > 0: addonid = aid[0]
                else: addonid = fold
                add = xbmcaddon.Addon(id=addonid)
            except:
                try:
                    logging.log("{0} was disabled".format(aid[0]), level=xbmc.LOGDEBUG)
                    disabledAddons.append(addonid)
                except:
                    logging.log("Unabled to enable: {0}".format(folder), level=xbmc.LOGERROR)
    if len(disabledAddons) > 0:
        addon_database(disabledAddons, 1, True)
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                           "[COLOR {0}]Enabling Addons Complete![/COLOR]".format(uservar.COLOR2))
    force_update()
    xbmc.executebuiltin("ReloadSkin()")


def toggle_addon(id, value, over=None):
    logging.log("Toggling {0}".format(id))
    addonid = id
    addonxml = os.path.join(vars.ADDONS, id, 'addon.xml')
    if os.path.exists(addonxml):
        b = read_from_file(addonxml)
        tid = parse_dom(b, 'addon', ret='id')
        tname = parse_dom(b, 'addon', ret='name')
        tservice = parse_dom(b, 'extension', ret='library', attrs={'point': 'xbmc.service'})
        try:
            if len(tid) > 0:
                addonid = tid[0]
            if len(tservice) > 0:
                logging.log("We got a live one, stopping script: {0}".format(match[0]), level=xbmc.LOGDEBUG)
                xbmc.executebuiltin('StopScript(%s)' % os.path.join(vars.ADDONS, addonid))
                xbmc.executebuiltin('StopScript(%s)' % addonid)
                xbmc.executebuiltin('StopScript(%s)' % os.path.join(vars.ADDONS, addonid, tservice[0]))
                xbmc.sleep(500)
        except:
            pass
    query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":%s}, "id":1}' % (addonid, value)
    response = xbmc.executeJSONRPC(query)
    if 'error' in response and over is None:
        v = 'Enabling' if value == 'true' else 'Disabling'
        gui.DIALOG.ok(uservar.ADDONTITLE,
                      "[COLOR {0}]Error {1} [COLOR {2}]{3}[/COLOR]".format(uservar.COLOR2, v, uservar.COLOR1, id),
                      "Check to make sure the add-on list is up to date and try again.[/COLOR]")
        force_update()


def addon_id(add):
    try:
        return xbmcaddon.Addon(id=add)
    except:
        return False


def addon_info(add, info):
    addon = addon_id(add)
    if addon:
        return addon.getAddonInfo(info)
    else:
        return False
