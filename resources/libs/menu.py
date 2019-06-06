import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import glob
import os
import re
import sys

try:  # Python 3
    from urllib.parse import quote_plus
    from urllib.parse import urljoin
    from urllib.request import urlretrieve
except ImportError:  # Python 2
    from urllib import quote_plus
    from urllib import urlretrieve
    from urlparse import urljoin

from resources.libs.config import CONFIG

###########################
#      Menu Items         #
###########################


def main_menu():
    from resources.libs import check
    from resources.libs import clear
    from resources.libs import logging
    from resources.libs import tools

    errors = int(logging.error_checking(count=True))
    errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'

    if CONFIG.AUTOUPDATE == 'Yes':
        wizfile = clear.text_cache(CONFIG.BUILDFILE)
        if wizfile:
            ver = check.check_wizard('version')
            if ver > CONFIG.VERSION:
                add_file('{0} [v{1}] [COLOR red][B][UPDATE v{2}][/B][/COLOR]'.format(CONFIG.ADDONTITLE, CONFIG.VERSION, ver), 'wizardupdate', themeit=CONFIG.THEME2)
            else:
                add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.VERSION), '', themeit=CONFIG.THEME2)
        else:
            add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.VERSION), '', themeit=CONFIG.THEME2)
    else:
        add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.VERSION), '', themeit=CONFIG.THEME2)
    if len(CONFIG.BUILDNAME) > 0:
        version = check.check_build(CONFIG.BUILDNAME, 'version')
        build = '{0} (v{1})'.format(CONFIG.BUILDNAME, CONFIG.BUILDVERSION)
        if version > CONFIG.BUILDVERSION:
            build = '{0} [COLOR red][B][UPDATE v{1}][/B][/COLOR]'.format(build, version)
        add_dir(build, 'viewbuild', CONFIG.BUILDNAME, themeit=CONFIG.THEME4)
        themefile = check.theme_count(CONFIG.BUILDNAME)
        if themefile:
            add_file('None' if CONFIG.BUILDTHEME == "" else CONFIG.BUILDTHEME, 'theme', CONFIG.BUILDNAME, themeit=CONFIG.THEME5)
    else:
        add_dir('None', 'builds', themeit=CONFIG.THEME4)
    add_separator()
    add_dir('Builds', 'builds', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME1)
    add_dir('Maintenance', 'maint', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if (tools.platform() == 'android' or CONFIG.DEVELOPER == 'true') and CONFIG.KODIV < 18:
        add_dir('Apk Installer','apk', icon=CONFIG.ICONAPK, themeit=CONFIG.THEME1)
    if not CONFIG.ADDONFILE == 'http://':
        add_dir('Addon Installer', 'addons', icon=CONFIG.ICONADDONS, themeit=CONFIG.THEME1)
    if not CONFIG.YOUTUBEFILE == 'http://' and not CONFIG.YOUTUBETITLE == '':
        add_dir (CONFIG.YOUTUBETITLE, 'youtube', icon=CONFIG.ICONYOUTUBE, themeit=CONFIG.THEME1)
    add_dir('Save Data', 'savedata', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    if CONFIG.HIDECONTACT == 'No':
        add_file('Contact', 'contact', icon=CONFIG.ICONCONTACT, themeit=CONFIG.THEME1)
    add_separator()
    add_file('Upload Log File', 'uploadlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    add_file('View Errors in Log: {0}'.format(errorsfound), 'viewerrorlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if errors > 0:
        add_file('View Last Error In Log', 'viewerrorlast', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    add_separator()
    add_file('Settings', 'settings', icon=CONFIG.ICONSETTINGS, themeit=CONFIG.THEME1)
    add_file('Force Update Text Files', 'forcetext', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if CONFIG.DEVELOPER == 'true':
        add_dir('Developer Menu', 'developer', icon=CONFIG.ICON, themeit=CONFIG.THEME1)
    set_view()


def build_menu():
    from resources.libs import check
    from resources.libs import clear
    from resources.libs import test

    bf = clear.text_cache(CONFIG.BUILDFILE)
    if not bf:
        add_file('Kodi Version: {0}'.format(CONFIG.KODIV), '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
        add_dir('Save Data Menu', 'savedata', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME3)
        add_separator()
        add_file('URL for txt file not valid', '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
        add_file('{0}'.format(CONFIG.BUILDFILE), '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
        return

    total, count17, count18, adultcount, hidden = check.build_count()
    link = bf.replace('\n', '').replace('\r', '').replace('\t', '').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"').replace('adult=""', 'adult="no"')
    match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
    if total == 1:
        for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
            if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                continue
            if not CONFIG.DEVELOPER == 'true' and test.str_test(name):
                continue
            view_build(match[0][0])
            return
    add_file('Kodi Version: {0}'.format(CONFIG.KODIV), '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
    add_dir('Save Data Menu', 'savedata', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME3)
    add_separator()
    if len(match) >= 1:
        if CONFIG.SEPERATE == 'true':
            for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                    continue
                if not CONFIG.DEVELOPER == 'true' and test.str_test(name):
                    continue
                menu = create_install_menu(name)
                add_dir('[{0}] {1} (v{2})'.format(float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart, icon=icon, menu=menu, themeit=CONFIG.THEME2)
        else:
            if count18 > 0:
                state = '+' if CONFIG.SHOW18 == 'false' else '-'
                add_file('[B]{0} Leia Builds ({1})[/B]'.format(state, count18), 'togglesetting',  'show18', themeit=CONFIG.THEME3)
                if CONFIG.SHOW18 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                            continue
                        if not CONFIG.DEVELOPER == 'true' and test.str_test(name):
                            continue
                        if CONFIG.KODIV >= 18:
                            menu = create_install_menu(name)
                            add_dir('[{0}] {1} (v{2})'.format(float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart, icon=icon, menu=menu, themeit=CONFIG.THEME2)
            if count17 > 0:
                state = '+' if CONFIG.SHOW17 == 'false' else '-'
                add_file('[B]{0} Krypton Builds ({1})[/B]'.format(state, count17), 'togglesetting',  'show17', themeit=CONFIG.THEME3)
                if CONFIG.SHOW17 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                            continue
                        if not CONFIG.DEVELOPER == 'true' and test.str_test(name):
                            continue
                        if CONFIG.KODIV >= 17:
                            menu = create_install_menu(name)
                            add_dir('[{0}] {1} (v{2})'.format(float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart, icon=icon, menu=menu, themeit=CONFIG.THEME2)
    elif hidden > 0:
        if adultcount > 0:
            add_file('There is currently only Adult builds', '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
            add_file('Enable Show Adults in Addon Settings > Misc', '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
        else:
            add_file('Currently No Builds Offered from {0}'.format(CONFIG.ADDONTITLE), '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
    else:
        add_file('Text file for builds not formatted correctly.', '', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)

    set_view()


def view_build(name):
    from resources.libs import check
    from resources.libs import clear

    bf = clear.text_cache(CONFIG.BUILDFILE)
    if not bf:
        add_file('URL for txt file not valid', '', themeit=CONFIG.THEME3)
        add_file('{0}'.format(CONFIG.BUILDFILE), '', themeit=CONFIG.THEME3)
        return
    if not check.check_build(name, 'version'):
        add_file('Error reading the txt file.', '', themeit=CONFIG.THEME3)
        add_file('{0} was not found in the builds list.'.format(name), '', themeit=CONFIG.THEME3)
        return
    link = bf.replace('\n', '').replace('\r', '').replace('\t', '').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
    match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?inor="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?nfo="(.+?)".+?escription="(.+?)"' % name).findall(link)
    for version, url, minor, gui, kodi, themefile, icon, fanart, preview, adult, info, description in match:
        icon = icon
        fanart = fanart
        build = '{0} (v{1})'.format(name, version)
        if CONFIG.BUILDNAME == name and version > CONFIG.BUILDVERSION:
            build = '{0} [COLOR red][CURRENT v{1}][/COLOR]'.format(build, CONFIG.BUILDVERSION)
        add_file(build, '', description=description, fanart=fanart, icon=icon, themeit=CONFIG.THEME4)
        add_separator()
        add_dir('Save Data Menu', 'savedata', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME3)
        add_file('Build Information', 'buildinfo', name, description=description, fanart=fanart, icon=icon, themeit=CONFIG.THEME3)
        if not preview == "http://":
            add_file('View Video Preview', 'buildpreview', name, description=description, fanart=fanart, icon=icon, themeit=CONFIG.THEME3)
        temp1 = int(float(CONFIG.KODIV))
        temp2 = int(float(kodi))
        if not temp1 == temp2:
            warning = True
        else:
            warning = False
        if warning:
            add_file('[I]Build designed for Kodi v{0} (installed: v{1})[/I]'.format(str(kodi), str(CONFIG.KODIV)), '', fanart=fanart, icon=icon, themeit=CONFIG.THEME3)
        add_separator('INSTALL')
        add_file('Fresh Install', 'install', name, 'fresh', description=description, fanart=fanart, icon=icon, themeit=CONFIG.THEME1)
        add_file('Standard Install', 'install', name, 'normal', description=description, fanart=fanart, icon=icon, themeit=CONFIG.THEME1)
        if not gui == 'http://':
            add_file('Apply guiFix', 'install', name, 'gui', description=description, fanart=fanart, icon=icon, themeit=CONFIG.THEME1)
        if not themefile == 'http://':
            themecheck = clear.text_cache(themefile)
            if themecheck:
                add_separator('THEMES', fanart=fanart, icon=icon)
                link = themecheck.replace('\n', '').replace('\r', '').replace('\t', '')
                match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
                for themename, themeurl, themeicon, themefanart, themeadult, description in match:
                    if CONFIG.SHOWADULT != 'true' and themeadult.lower() == 'yes':
                        continue
                    themeicon = themeicon if themeicon == 'http://' else icon
                    themefanart = themefanart if themefanart == 'http://' else fanart
                    add_file(themename if not themename == CONFIG.BUILDTHEME else "[B]{0} (Installed)[/B]".format(themename), 'theme', name, themename, description=description, fanart=themefanart, icon=themeicon, themeit=CONFIG.THEME3)

    set_view()


# commented lines in this method are for x64 apks
def apk_scraper():
    from resources.libs import logging
    from resources.libs import tools

    kodiurl1 = 'https://mirrors.kodi.tv/releases/android/arm/'
    kodiurl2 = 'https://mirrors.kodi.tv/releases/android/arm/old/'
    # kodiurl3 = 'https://mirrors.kodi.tv/releases/android/arm64-v8a/'
    # kodiurl4 = 'https://mirrors.kodi.tv/releases/android/arm64-v8a/old/'

    url1 = tools.open_url(kodiurl1).replace('\n', '').replace('\r', '').replace('\t', '')
    url2 = tools.open_url(kodiurl2).replace('\n', '').replace('\r', '').replace('\t', '')
    # url3 = tools.open_url(kodiurl3).replace('\n', '').replace('\r', '').replace('\t', '')
    # url4 = tools.open_url(kodiurl4).replace('\n', '').replace('\r', '').replace('\t', '')

    x = 0
    match1 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url1)
    match2 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url2)
    # match3 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url3)
    # match4 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url4)

    add_file("Official Kodi Apk\'s", themeit=CONFIG.THEME1)
    rc = False
    for url, name, size, date in match1:
        if url in ['../', 'old/']:
            continue
        if not url.endswith('.apk'):
            continue
        if not url.find('_') == -1 and rc:
            continue
        try:
            tempname = name.split('-')
            if not url.find('_') == -1:
                rc = True
                name2, v2 = tempname[2].split('_')
            else:
                name2 = tempname[2]
                v2 = ''
            title = "[COLOR {0}]{1} v{2}{3} {4}[/COLOR] [COLOR {5}]{6}[/COLOR] [COLOR {7}]{8}[/COLOR]".format(CONFIG.COLOR1, tempname[0].title(), tempname[1], v2.upper(), name2, CONFIG.COLOR2, size.replace(' ', ''), CONFIG.COLOR1, date)
            download = urljoin(kodiurl1, url)
            add_file(title, 'apkinstall', "{0} v{1}{2} {3}".format(tempname[0].title(), tempname[1], v2.upper(), name2), download)
            x += 1
        except Exception as e:
            logging.log("Error on APK scraping: {0}".format(str(e)))

    for url, name, size, date in match2:
        if url in ['../', 'old/']:
            continue
        if not url.endswith('.apk'):
            continue
        if not url.find('_') == -1:
            continue
        try:
            tempname = name.split('-')
            title = "[COLOR {0}]{1} v{2} {3}[/COLOR] [COLOR {4}]{5}[/COLOR] [COLOR {6}]{7}[/COLOR]".format(CONFIG.COLOR1, tempname[0].title(), tempname[1], tempname[2], CONFIG.COLOR2, size.replace(' ', ''), CONFIG.COLOR1, date)
            download = urljoin(kodiurl2, url)
            add_file(title, 'apkinstall', "{0} v{1} {2}".format(tempname[0].title(), tempname[1], tempname[2]), download)
            x += 1
        except Exception as e:
            logging.log("Error on APK  scraping: {0}".format(str(e)))

    # for url, name, size, date in match3:
    #     if url in ['../', 'old/']:
    #         continue
    #     if not url.endswith('.apk'):
    #         continue
    #     if not url.find('_') == -1:
    #         continue
    #     try:
    #         tempname = name.split('-')
    #         title = "[COLOR {0}]{1} v{2} {3}[/COLOR] [COLOR {4}]{5}[/COLOR] [COLOR {6}]{7}[/COLOR]".format(CONFIG.COLOR1, tempname[0].title(), tempname[1], tempname[2], CONFIG.COLOR2, size.replace(' ', ''), CONFIG.COLOR1, date)
    #         download = urljoin(kodiurl2, url)
    #         add_file(title, 'apkinstall', "{0} v{1} {2}".format(tempname[0].title(), tempname[1], tempname[2]), download)
    #         x += 1
    #     except Exception as e:
    #         logging.log("Error on APK  scraping: {0}".format(str(e)))
    #
    # for url, name, size, date in match4:
    #     if url in ['../', 'old/']:
    #         continue
    #     if not url.endswith('.apk'):
    #         continue
    #     if not url.find('_') == -1:
    #         continue
    #     try:
    #         tempname = name.split('-')
    #         title = "[COLOR {0}]{1} v{2} {3}[/COLOR] [COLOR {4}]{5}[/COLOR] [COLOR {6}]{7}[/COLOR]".format(CONFIG.COLOR1, tempname[0].title(), tempname[1], tempname[2], CONFIG.COLOR2, size.replace(' ', ''), CONFIG.COLOR1, date)
    #         download = urljoin(kodiurl2, url)
    #         add_file(title, 'apkinstall', "{0} v{1} {2}".format(tempname[0].title(), tempname[1], tempname[2]), download)
    #         x += 1
    #     except Exception as e:
    #         logging.log("Error on APK  scraping: {0}".format(str(e)))

    if x == 0:
        add_file("Error Kodi Scraper Is Currently Down.")


def apk_menu(url=None):
    from resources.libs import clear
    from resources.libs import check
    from resources.libs import logging

    if not url:
        add_dir('Official Kodi Apk\'s', 'apkscrape', 'kodi', icon=CONFIG.ICONAPK, themeit=CONFIG.THEME1)
        add_separator()
    if not CONFIG.APKFILE == 'http://':
        if not url:
            TEMPAPKFILE = clear.text_cache(CONFIG.APKFILE)
            if not TEMPAPKFILE:
                APKWORKING = check.check_url(CONFIG.APKFILE)
        else:
            TEMPAPKFILE = clear.text_cache(url)
            if not TEMPAPKFILE:
                APKWORKING = check.check_url(url)
        if TEMPAPKFILE:
            link = TEMPAPKFILE.replace('\n', '').replace('\r', '').replace('\t', '')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                x = 0
                for aname, section, url, icon, fanart, adult, description in match:
                    if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                        continue
                    if section.lower() == 'yes':
                        x += 1
                        add_dir("[B]{0}[/B]".format(aname), 'apk', aname, url, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
                    else:
                        x += 1
                        add_file(aname, 'apkinstall', aname, url, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
                    if x == 0:
                        add_file("No addons added to this menu yet!", '', themeit=CONFIG.THEME2)
            else:
                logging.log("[APK Menu] ERROR: Invalid Format.", level=xbmc.LOGERROR)
        else:
            logging.log("[APK Menu] ERROR: URL for apk list not working.", level=xbmc.LOGERROR)
            add_file('Url for txt file not valid', '', themeit=CONFIG.THEME3)
            add_file('{0}'.format(CONFIG.APKFILE), '', themeit=CONFIG.THEME3)
        return
    else:
        logging.log("[APK Menu] No APK list added.")

    set_view()


def addon_menu(url=None):
    from resources.libs import clear
    from resources.libs import check
    from resources.libs import logging

    if not CONFIG.ADDONFILE == 'http://':
        if not url:
            TEMPADDONFILE = clear.text_cache(CONFIG.ADDONFILE)
            if not TEMPADDONFILE:
                ADDONWORKING = check.check_url(CONFIG.ADDONFILE)
        else:
            TEMPADDONFILE = clear.text_cache(url)
            if not TEMPADDONFILE:
                ADDONWORKING = check.check_url(url)
        if TEMPADDONFILE:
            link = TEMPADDONFILE.replace('\n', '').replace('\r', '').replace('\t', '').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
            match = re.compile('name="(.+?)".+?lugin="(.+?)".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                x = 0
                for aname, plugin, aurl, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
                    if plugin.lower() == 'section':
                        x += 1
                        add_dir("[B]{0}[/B]".format(aname), 'addons', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
                    elif plugin.lower() == 'skin':
                        if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                            continue
                        x += 1
                        add_file("[B]{0}[/B]".format(aname), 'skinpack', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
                    elif plugin.lower() == 'pack':
                        if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                            continue
                        x += 1
                        add_file("[B]{0}[/B]".format(aname), 'addonpack', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
                    else:
                        if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                            continue
                        try:
                            add = xbmcaddon.Addon(id=plugin).getAddonInfo('path')
                            if os.path.exists(add):
                                aname = "[COLOR springgreen][Installed][/COLOR] {0}".format(aname)
                        except:
                            pass
                        x += 1
                        add_file(aname, 'addoninstall', plugin, url, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
                    if x < 1:
                        add_file("No addons added to this menu yet!", '', themeit=CONFIG.THEME2)
            else:
                add_file('Text File not formated correctly!', '', themeit=CONFIG.THEME3)
                logging.log("[Addon Menu] ERROR: Invalid Format.")
        else:
            logging.log("[Addon Menu] ERROR: URL for Addon list not working.")
            add_file('Url for txt file not valid', '', themeit=CONFIG.THEME3)
            add_file('{0}'.format(CONFIG.ADDONFILE), '', themeit=CONFIG.THEME3)
    else:
        logging.log("[Addon Menu] No Addon list added.")

    set_view()


def youtube_menu(url=None):
    from resources.libs import clear
    from resources.libs import check
    from resources.libs import logging

    if not CONFIG.YOUTUBEFILE == 'http://':
        if not url:
            TEMPYOUTUBEFILE = clear.text_cache(CONFIG.YOUTUBEFILE)
            if not TEMPYOUTUBEFILE:
                YOUTUBEWORKING = check.check_url(CONFIG.YOUTUBEFILE)
        else:
            TEMPYOUTUBEFILE = clear.text_cache(url)
            if not TEMPYOUTUBEFILE:
                YOUTUBEWORKING = check.check_url(url)
        if TEMPYOUTUBEFILE:
            link = TEMPYOUTUBEFILE.replace('\n', '').replace('\r', '').replace('\t', '')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                for name, section, url, icon, fanart, description in match:
                    if section.lower() == "yes":
                        add_dir("[B]{0}[/B]".format(name), 'youtube', name, url, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
                    else:
                        add_file(name, 'viewVideo', url=url, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
            else:
                logging.log("[YouTube Menu] ERROR: Invalid Format.")
        else:
            logging.log("[YouTube Menu] ERROR: URL for YouTube list not working.")
            add_file('Url for txt file not valid', '', themeit=CONFIG.THEME3)
            add_file('{0}'.format(CONFIG.YOUTUBEFILE), '', themeit=CONFIG.THEME3)
    else:
        logging.log("[YouTube Menu] No YouTube list added.")

    set_view()


def maint_menu(view=None):
    from resources.libs import clear
    from resources.libs import logging
    from resources.libs import tools

    on = '[B][COLOR springgreen]ON[/COLOR][/B]'
    off = '[B][COLOR red]OFF[/COLOR][/B]'

    autoclean = 'true' if CONFIG.AUTOCLEANU == 'true' else 'false'
    cache = 'true' if CONFIG.AUTOCACHE == 'true' else 'false'
    packages = 'true' if CONFIG.AUTOPACKAGES == 'true' else 'false'
    thumbs = 'true' if CONFIG.AUTOTHUMBS == 'true' else 'false'
    maint = 'true' if CONFIG.SHOWMAINT == 'true' else 'false'
    includevid = 'true' if CONFIG.INCLUDEVIDEO == 'true' else 'false'
    includeall = 'true' if CONFIG.INCLUDEALL == 'true' else 'false'
    errors = int(logging.error_checking(count=True))
    errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'
    wizlogsize = ': [COLOR red]Not Found[/COLOR]' if not os.path.exists(CONFIG.WIZLOG) else ": [COLOR springgreen]%s[/COLOR]".format(tools.convert_size(os.path.getsize(CONFIG.WIZLOG)))

    if includeall == 'true':
        includeplacenta = 'true'
        includegaia = 'true'
        includeexodusredux = 'true'
        includeovereasy = 'true'
        includeyoda = 'true'
        includevenom = 'true'
        includescrubs = 'true'
        includeseren = 'true'
    else:
        includeexodusredux = 'true' if CONFIG.INCLUDEEXODUSREDUX == 'true' else 'false'
        includegaia = 'true' if CONFIG.INCLUDEGAIA == 'true' else 'false'
        includeovereasy = 'true' if CONFIG.INCLUDEOVEREASY == 'true' else 'false'
        includeplacenta = 'true' if CONFIG.INCLUDEPLACENTA == 'true' else 'false'
        includeyoda = 'true' if CONFIG.INCLUDEYODA == 'true' else 'false'
        includevenom = 'true' if CONFIG.INCLUDEVENOM == 'true' else 'false'
        includescrubs = 'true' if CONFIG.INCLUDESCRUBS == 'true' else 'false'
        includeseren = 'true' if CONFIG.INCLUDESEREN == 'true' else 'false'

    sizepack = tools.get_size(CONFIG.PACKAGES)
    sizethumb = tools.get_size(CONFIG.THUMBS)
    archive = tools.get_size(CONFIG.ARCHIVE_CACHE)
    sizecache = (clear.get_cache_size())-archive
    totalsize = sizepack+sizethumb+sizecache

    add_dir('[B]Cleaning Tools[/B]', 'maint', 'clean', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if view == "clean" or CONFIG.SHOWMAINT == 'true':
        add_file('Total Clean Up: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(totalsize)), 'fullclean', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Clear Cache: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizecache)), 'clearcache', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if (xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)') or xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)')):
            add_file('Clear Resolver Function Caches', 'clearfunctioncache', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Clear Packages: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizepack)), 'clearpackages', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Clear Thumbnails: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizethumb)), 'clearthumb', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if os.path.exists(CONFIG.ARCHIVE_CACHE):
            add_file('Clear Archive_Cache: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(archive)), 'cleararchive', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Clear Old Thumbnails', 'oldThumbs', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Clear Crash Logs', 'clearcrash', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Purge Databases', 'purgedb', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Fresh Start', 'freshstart', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_dir('[B]Addon Tools[/B]', 'maint', 'addon',  icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if view == "addon" or CONFIG.SHOWMAINT == 'true':
        add_file('Remove Addons', 'removeaddons', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_dir('Remove Addon Data', 'removeaddondata', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_dir('Enable/Disable Addons', 'enableaddons', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Enable/Disable Adult Addons', 'toggleadult', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Force Update Addons', 'forceupdate', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        # addFile('Hide Passwords On Keyboard Entry',   'hidepassword',   icon=ICONMAINT, themeit=THEME3)
        # addFile('Unhide Passwords On Keyboard Entry', 'unhidepassword', icon=ICONMAINT, themeit=THEME3)
    add_dir('[B]Misc Maintenance[/B]', 'maint', 'misc', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if view == "misc" or CONFIG.SHOWMAINT == 'true':
        add_file('Kodi 17 Fix', 'kodi17fix', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_dir('Speed Test', 'speedtest', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Enable Unknown Sources', 'unknownsources', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Reload Skin', 'forceskin', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Reload Profile', 'forceprofile', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Force Close Kodi', 'forceclose', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Upload Log File', 'uploadlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('View Errors in Log: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(errorsfound), 'viewerrorlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if errors > 0:
            add_file('View Last Error In Log', 'viewerrorlast', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('View Log File', 'viewlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('View Wizard Log File', 'viewwizlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Clear Wizard Log File: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(wizlogsize), 'clearwizlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_dir('[B]Back up/Restore[/B]', 'maint', 'backup', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if view == "backup" or CONFIG.SHOWMAINT == 'true':
        add_file('Clean Up Back Up Folder', 'clearbackup', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Back Up Location: [COLOR {0]]{1}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.MYBUILDS), 'settings', 'Maintenance', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Back Up]: Build', 'backupbuild', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Back Up]: GuiFix', 'backupgui', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Back Up]: Theme', 'backuptheme', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Back Up]: Addon Pack', 'backupaddonpack', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Back Up]: Addon_data', 'backupaddon', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Restore]: Local Build', 'restorezip', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Restore]: Local GuiFix', 'restoregui', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Restore]: Local Addon_data', 'restoreaddon', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Restore]: External Build', 'restoreextzip', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Restore]: External GuiFix', 'restoreextgui', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('[Restore]: External Addon_data', 'restoreextaddon', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_dir('[B]System Tweaks/Fixes[/B]', 'maint', 'tweaks', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    if view == "tweaks" or CONFIG.SHOWMAINT == 'true':
        if not CONFIG.ADVANCEDFILE == 'http://' and not CONFIG.ADVANCEDFILE == '':
            add_dir('Advanced Settings', 'advancedsetting', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        else:
            if os.path.exists(CONFIG.ADVANCED):
                add_file('View Current AdvancedSettings.xml', 'currentsettings', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
                add_file('Remove Current AdvancedSettings.xml', 'removeadvanced', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            add_file('Quick Configure AdvancedSettings.xml', 'autoadvanced', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Scan Sources for broken links', 'checksources', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Scan For Broken Repositories', 'checkrepos', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Fix Addons Not Updating', 'fixaddonupdate', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Remove Non-Ascii filenames', 'asciicheck', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('Convert Paths to special', 'convertpath', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_dir('System Information', 'systeminfo', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_file('Show All Maintenance: {0}'.format(maint.replace('true', on).replace('false', off)), 'togglesetting', 'showmaint', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_dir('[I]<< Return to Main Menu[/I]', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('Auto Clean', '', fanart=CONFIG.FANART, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    add_file('Auto Clean Up On Startup: {0}'.format(autoclean.replace('true', on).replace('false', off)), 'togglesetting', 'autoclean', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    if autoclean == 'true':
        add_file('--- Auto Clean Frequency: [B][COLOR springgreen]{0}[/COLOR][/B]'.format(CONFIG.CLEANFREQ[CONFIG.AUTOFREQ]), 'changefeq', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('--- Clear Cache on Startup: {0}'.format(cache.replace('true', on).replace('false', off)), 'togglesetting', 'clearcache', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('--- Clear Packages on Startup: {0}'.format(packages.replace('true', on).replace('false', off)), 'togglesetting', 'clearpackages', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('--- Clear Old Thumbs on Startup: {0}'.format(thumbs.replace('true', on).replace('false', off)), 'togglesetting', 'clearthumbs', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_file('Clear Video Cache', '', fanart=CONFIG.FANART, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
    add_file('Include Video Cache in Clear Cache: {0}'.format(includevid.replace('true', on).replace('false', off)), 'togglecache', 'includevideo', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    if includevid == 'true':
        add_file('--- Include All Video Addons: {0}'.format(includeall.replace('true', on).replace('false', off)), 'togglecache', 'includeall', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.exodusredux)'):
            add_file('--- Include Exodus Redux: {0}'.format(includeexodusredux.replace('true', on).replace('false', off)), 'togglecache', 'includeexodusredux', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.gaia)'):
            add_file('--- Include Gaia: {0}'.format(includegaia.replace('true', on).replace('false', off)), 'togglecache', 'includegaia', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.overeasy)'):
            add_file('--- Include Overeasy: {0}'.format(includeovereasy.replace('true', on).replace('false', off)), 'togglecache', 'includeovereasy', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.placenta)'):
            add_file('--- Include Placenta: {0}'.format(includeplacenta.replace('true', on).replace('false', off)), 'togglecache', 'includeplacenta', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.scrubsv2)'):
            add_file( '--- Include Scrubs v2: {0}'.format(includescrubs.replace('true', on).replace('false', off)), 'togglecache', 'includescrubs', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.seren)'):
            add_file('--- Include Seren: {0}'.format(includeseren.replace('true', on).replace('false', off)), 'togglecache', 'includeseren', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.venom)'):
            add_file('--- Include Venom: {0}'.format(includevenom.replace('true', on).replace('false', off)), 'togglecache', 'includevenom', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.yoda)'):
            add_file('--- Include Yoda: {0}'.format(includeyoda.replace('true', on).replace('false', off)), 'togglecache', 'includeyoda', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('--- Enable All Video Addons', 'togglecache', 'true', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        add_file('--- Disable All Video Addons', 'togglecache', 'false', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

    set_view()

#########################################NET TOOLS#############################################


def net_tools(view=None):
    add_dir('Speed Tester', 'speedtestM', icon=CONFIG.ICONSPEED, themeit=CONFIG.THEME1)
    if CONFIG.HIDESPACERS == 'No':
        add_separator()
    add_dir('View IP Address & MAC Address', 'viewIP', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)

    set_view()


def view_ip():
    from resources.libs import speedtest

    mac, inter_ip, ip, city, state, country, isp = speedtest.net_info()
    add_file('[COLOR {0}]MAC:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, mac), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Internal IP: [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, inter_ip), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]External IP:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, ip), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]City:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, city), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]State:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, state), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Country:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, country), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]ISP:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, isp), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)

    set_view()


def speed_test():
    import datetime

    add_file('Run Speed Test', 'runspeedtest', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    if os.path.exists(CONFIG.SPEEDTESTFOLD):
        speedimg = glob.glob(os.path.join(CONFIG.SPEEDTESTFOLD, '*.png'))
        speedimg.sort(key=lambda f: os.path.getmtime(f), reverse=True)
        if len(speedimg) > 0:
            add_file('Clear Results', 'clearspeedtest', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            add_separator('Previous Runs', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            for item in speedimg:
                created = datetime.fromtimestamp(os.path.getmtime(item)).strftime('%m/%d/%Y %H:%M:%S')
                img = item.replace(os.path.join(CONFIG.SPEEDTESTFOLD, ''), '')
                add_file('[B]{0}[/B]: [I]Ran {1}[/I]'.format(img, created), 'viewspeedtest', img, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)


def clear_speed_test():
    from resources.libs import tools

    speedimg = glob.glob(os.path.join(CONFIG.SPEEDTESTFOLD, '*.png'))
    for file in speedimg:
        tools.remove_file(file)


def view_speed_test(img=None):
    from resources.libs import gui

    img = os.path.join(CONFIG.SPEEDTESTFOLD, img)
    gui.show_speed_test(img)


def run_speed_test():
    from resources.libs import logging
    from resources.libs import speedtest

    try:
        found = speedtest.speedtest()
        if not os.path.exists(CONFIG.SPEEDTESTFOLD):
            os.makedirs(CONFIG.SPEEDTESTFOLD)
        urlsplits = found[0].split('/')
        dest = os.path.join(CONFIG.SPEEDTESTFOLD, urlsplits[-1])
        urlretrieve(found[0], dest)
        view_speed_test(urlsplits[-1])
    except:
        logging.log("[Speed Test] Error Running Speed Test")
        pass


def system_info():
    from resources.libs import logging
    from resources.libs import tools
    from resources.libs import speedtest

    infoLabel = ['System.FriendlyName', 'System.BuildVersion', 'System.CpuUsage', 'System.ScreenMode',
                 'Network.IPAddress', 'Network.MacAddress', 'System.Uptime', 'System.TotalUptime', 'System.FreeSpace',
                 'System.UsedSpace', 'System.TotalSpace', 'System.Memory(free)', 'System.Memory(used)',
                 'System.Memory(total)']
    data = []
    x = 0
    for info in infoLabel:
        temp = tools.get_info_label(info)
        y = 0
        while temp == "Busy" and y < 10:
            temp = tools.get_info_label(info)
            y += 1
            logging.log("{0} sleep {1}".format(info, str(y)))
            xbmc.sleep(200)
        data.append(temp)
        x += 1
    storage_free = data[8] if 'Una' in data[8] else tools.convert_size(int(float(data[8][:-8]))*1024*1024)
    storage_used = data[9] if 'Una' in data[9] else tools.convert_size(int(float(data[9][:-8]))*1024*1024)
    storage_total = data[10] if 'Una' in data[10] else tools.convert_size(int(float(data[10][:-8]))*1024*1024)
    ram_free = tools.convert_size(int(float(data[11][:-2]))*1024*1024)
    ram_used = tools.convert_size(int(float(data[12][:-2]))*1024*1024)
    ram_total = tools.convert_size(int(float(data[13][:-2]))*1024*1024)

    picture = []
    music = []
    video = []
    programs = []
    repos = []
    scripts = []
    skins = []

    fold = glob.glob(os.path.join(CONFIG.ADDONS, '*/'))
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername == 'packages': continue
        xml = os.path.join(folder, 'addon.xml')
        if os.path.exists(xml):
            prov = re.compile("<provides>(.+?)</provides>").findall(tools.read_from_file(xml))
            if len(prov) == 0:
                if foldername.startswith('skin'):
                    skins.append(foldername)
                elif foldername.startswith('repo'):
                    repos.append(foldername)
                else:
                    scripts.append(foldername)
            elif not (prov[0]).find('executable') == -1:
                programs.append(foldername)
            elif not (prov[0]).find('video') == -1:
                video.append(foldername)
            elif not (prov[0]).find('audio') == -1:
                music.append(foldername)
            elif not (prov[0]).find('image') == -1:
                picture.append(foldername)

    add_file('[B]Media Center Info:[/B]', '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Name:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, data[0]), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_file('[COLOR {0}]Version:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, data[1]), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_file('[COLOR {0}]Platform:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, tools.platform().title()), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_file('[COLOR {0}]CPU Usage:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, data[2]), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
    add_file('[COLOR {0}]Screen Mode:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, data[3]), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

    add_file('[B]Uptime:[/B]', '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Current Uptime:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, data[6]), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Total Uptime:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, data[7]), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)

    add_file('[B]Local Storage:[/B]', '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Used Storage:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, storage_used), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Free Storage:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, storage_free), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Total Storage:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, storage_total), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)

    add_file('[B]Ram Usage:[/B]', '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Used Memory:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, ram_free), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Free Memory:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, ram_used), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Total Memory:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, ram_total), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)

    mac, inter_ip, ip, city, state, country, isp = speedtest.net_info()
    add_file('[B]Network:[/B]', '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Mac:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, mac), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Internal IP: [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, inter_ip), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]External IP:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, ip), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]City:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, city), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]State:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, state), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Country:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, country), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]ISP:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, isp), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)

    totalcount = len(picture) + len(music) + len(video) + len(programs) + len(scripts) + len(skins) + len(repos)
    add_file('[B]Addons([COLOR {0}]{1}[/COLOR]):[/B]'.format(CONFIG.COLOR1, totalcount), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Video Addons:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, str(len(video))), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Program Addons:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, str(len(programs))), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Music Addons:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, str(len(music))), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Picture Addons:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, str(len(picture))), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Repositories:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, str(len(repos))), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Skins:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, str(len(skins))), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)
    add_file('[COLOR {0}]Scripts/Modules:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, str(len(scripts))), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME2)


def save_menu():
    on = '[COLOR springgreen]ON[/COLOR]'
    off = '[COLOR red]OFF[/COLOR]'

    trakt = 'true' if CONFIG.KEEPTRAKT == 'true' else 'false'
    debrid = 'true' if CONFIG.KEEPDEBRID == 'true' else 'false'
    login = 'true' if CONFIG.KEEPLOGIN == 'true' else 'false'
    sources = 'true' if CONFIG.KEEPSOURCES == 'true' else 'false'
    advanced = 'true' if CONFIG.KEEPADVANCED == 'true' else 'false'
    profiles = 'true' if CONFIG.KEEPPROFILES == 'true' else 'false'
    playercore = 'true' if CONFIG.KEEPPLAYERCORE == 'true' else 'false'
    favourites = 'true' if CONFIG.KEEPFAVS == 'true' else 'false'
    repos = 'true' if CONFIG.KEEPREPOS == 'true' else 'false'
    super = 'true' if CONFIG.KEEPSUPER == 'true' else 'false'
    whitelist = 'true' if CONFIG.KEEPWHITELIST == 'true' else 'false'

    add_dir('Keep Trakt Data', 'trakt', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME1)
    add_dir('Keep Debrid', 'realdebrid', icon=CONFIG.ICONDEBRID, themeit=CONFIG.THEME1)
    add_dir('Keep Login Info', 'login', icon=CONFIG.ICONLOGIN, themeit=CONFIG.THEME1)
    add_file('Import Save Data', 'managedata', 'import', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Export Save Data', 'managedata', 'export', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('- Click to toggle settings -', '', themeit=CONFIG.THEME3)
    add_file('Save Trakt: {0}'.format(trakt.replace('true', on).replace('false', off)),'togglesetting', 'keeptrakt', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME1)
    add_file('Save Debrid: {0}'.format(debrid.replace('true', on).replace('false', off)),'togglesetting', 'keepdebrid', icon=CONFIG.ICONDEBRID, themeit=CONFIG.THEME1)
    add_file('Save Login Info: {0}'.format(login.replace('true', on).replace('false', off)),'togglesetting', 'keeplogin', icon=CONFIG.ICONLOGIN, themeit=CONFIG.THEME1)
    add_file('Keep \'Sources.xml\': {0}'.format(sources.replace('true', on).replace('false', off)),'togglesetting', 'keepsources', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Keep \'Profiles.xml\': {0}'.format(profiles.replace('true', on).replace('false', off)),'togglesetting', 'keepprofiles', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Keep \'playercorefactory.xml\': {0}'.format(playercore.replace('true', on).replace('false', off)), 'togglesetting', 'keepplayercore', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Keep \'Advancedsettings.xml\': {0}'.format(advanced.replace('true', on).replace('false', off)),'togglesetting', 'keepadvanced', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Keep \'Favourites.xml\': {0}'.format(favourites.replace('true', on).replace('false', off)),'togglesetting', 'keepfavourites', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Keep Super Favourites: {0}'.format(super.replace('true', on).replace('false', off)),'togglesetting', 'keepsuper', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Keep Installed Repo\'s: {0}'.format(repos.replace('true', on).replace('false', off)),'togglesetting', 'keeprepos', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    add_file('Keep My \'WhiteList\': {0}'.format(whitelist.replace('true', on).replace('false', off)),'togglesetting', 'keepwhitelist', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
    if whitelist == 'true':
        add_file('Edit My Whitelist', 'whitelist', 'edit', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
        add_file('View My Whitelist', 'whitelist', 'view', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
        add_file('Clear My Whitelist', 'whitelist', 'clear', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
        add_file('Import My Whitelist', 'whitelist', 'import', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
        add_file('Export My Whitelist', 'whitelist', 'export', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)

    set_view()


def trakt_menu():
    from resources.libs import traktit

    trakt = '[COLOR springgreen]ON[/COLOR]' if CONFIG.KEEPTRAKT == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(CONFIG.TRAKTSAVE) if not CONFIG.TRAKTSAVE == '' else 'Trakt hasn\'t been saved yet.'
    add_file('[I]Register FREE Account at https://www.trakt.tv/[/I]', '', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    add_file('Save Trakt Data: {0}'.format(trakt), 'togglesetting', 'keeptrakt', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    if CONFIG.KEEPTRAKT == 'true':
        add_file('Last Save: {0}'.format(str(last)), '', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    add_separator(icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)

    for trakt in traktit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(traktit.TRAKTID[trakt]['plugin'])):
            name = traktit.TRAKTID[trakt]['name']
            path = traktit.TRAKTID[trakt]['path']
            saved = traktit.TRAKTID[trakt]['saved']
            file = traktit.TRAKTID[trakt]['file']
            user = CONFIG.get_setting(saved)
            auser = traktit.traktUser(trakt)
            icon = traktit.TRAKTID[trakt]['icon'] if os.path.exists(path) else CONFIG.ICONTRAKT
            fanart = traktit.TRAKTID[trakt]['fanart'] if os.path.exists(path) else CONFIG.FANART
            menu = create_addon_data_menu('Trakt', trakt)
            menu2 = create_save_data_menu('Trakt', trakt)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=trakt)'.format(CONFIG.ADDON_ID, trakt)))

            add_file('[+]-> {0}'.format(name), '', icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
            if not os.path.exists(path):
                add_file('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:
                add_file('[COLOR red]Addon Data: Not Registered[/COLOR]', 'authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
            else:
                add_file('[COLOR springgreen]Addon Data: {0}[/COLOR]'.format(auser), 'authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file):
                    add_file('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]', 'importtrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
                else:
                    add_file('[COLOR red]Saved Data: Not Saved[/COLOR]', 'savetrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
            else:
                add_file('[COLOR springgreen]Saved Data: {0|[/COLOR]'.format(user), '', icon=icon, fanart=fanart, menu=menu2)

    add_separator()
    add_file('Save All Trakt Data', 'savetrakt', 'all', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    add_file('Recover All Saved Trakt Data', 'restoretrakt', 'all', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    add_file('Import Trakt Data', 'importtrakt', 'all', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    add_file('Clear All Addon Trakt Data', 'addontrakt', 'all', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)
    add_file('Clear All Saved Trakt Data', 'cleartrakt', 'all', icon=CONFIG.ICONTRAKT, themeit=CONFIG.THEME3)

    set_view()

# MIGRATION: move to menu
def realMenu():
    real = '[COLOR springgreen]ON[/COLOR]' if KEEPREAL == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(REALSAVE) if not REALSAVE == '' else 'Real Debrid hasnt been saved yet.'
    addFile('[I]http://real-debrid.com is a PAID service.[/I]', '', icon=ICONREAL, themeit=THEME3)
    addFile('Save Real Debrid Data: %s' % real, 'togglesetting', 'keepdebrid', icon=ICONREAL, themeit=THEME3)
    if KEEPREAL == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONREAL, themeit=THEME3)
    add_separator(icon=CONFIG.ICONREAL)

    for debrid in debridit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % DEBRIDID[debrid]['plugin']):
            name   = DEBRIDID[debrid]['name']
            path   = DEBRIDID[debrid]['path']
            saved  = DEBRIDID[debrid]['saved']
            file   = DEBRIDID[debrid]['file']
            user   = wiz.getS(saved)
            auser  = debridit.debridUser(debrid)
            icon   = DEBRIDID[debrid]['icon']   if os.path.exists(path) else ICONREAL
            fanart = DEBRIDID[debrid]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Debrid', debrid)
            menu2 = createMenu('save', 'Debrid', debrid)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=debrid)' %   (ADDON_ID, debrid)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importdebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savedebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Debrid Data',          'savedebrid',    'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Recover All Saved Debrid Data', 'restoredebrid', 'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Import Debrid Data',            'importdebrid',  'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Clear All Addon Debrid Data',               'addondebrid',   'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Clear All Saved Debrid Data',   'cleardebrid',   'all', icon=ICONREAL,  themeit=THEME3)
    setView('files', 'viewType')

# MIGRATION: move to menu
def loginMenu():
    login = '[COLOR springgreen]ON[/COLOR]' if KEEPLOGIN == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(LOGINSAVE) if not LOGINSAVE == '' else 'Login data hasnt been saved yet.'
    addFile('[I]Several of these addons are PAID services.[/I]', '', icon=ICONLOGIN, themeit=THEME3)
    addFile('Save API Keys: %s' % login, 'togglesetting', 'keeplogin', icon=ICONLOGIN, themeit=THEME3)
    if KEEPLOGIN == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONLOGIN, themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONLOGIN, themeit=THEME3)

    for login in loginit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % LOGINID[login]['plugin']):
            name   = LOGINID[login]['name']
            path   = LOGINID[login]['path']
            saved  = LOGINID[login]['saved']
            file   = LOGINID[login]['file']
            user   = wiz.getS(saved)
            auser  = loginit.loginUser(login)
            icon   = LOGINID[login]['icon']   if os.path.exists(path) else ICONLOGIN
            fanart = LOGINID[login]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Login', login)
            menu2 = createMenu('save', 'Login', login)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=login)' %   (ADDON_ID, login)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authlogin', login, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authlogin', login, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importlogin', login, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savelogin', login, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Login Info',          'savelogin',    'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Recover All Saved Login Info', 'restorelogin', 'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Import Login Info',            'importlogin',  'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Clear All Addon Login Info',         'addonlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Clear All Saved Login Info',   'clearlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
    setView('files', 'viewType')


def enable_addons():
    addFile("[I][B][COLOR red]!!Notice: Disabling Some Addons Can Cause Issues!![/COLOR][/B][/I]", '', icon=ICONMAINT)
    fold = glob.glob(os.path.join(ADDONS, '*/'))
    x = 0
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername in EXCLUDES: continue
        if foldername in DEFAULTPLUGINS: continue
        addonxml = os.path.join(folder, 'addon.xml')
        if os.path.exists(addonxml):
            x += 1
            fold   = folder.replace(ADDONS, '')[1:-1]
            f      = open(addonxml)
            a      = f.read().replace('\n','').replace('\r','').replace('\t','')
            match  = wiz.parseDOM(a, 'addon', ret='id')
            match2 = wiz.parseDOM(a, 'addon', ret='name')
            try:
                pluginid = match[0]
                name = match2[0]
            except:
                continue
            try:
                add    = xbmcaddon.Addon(id=pluginid)
                state  = "[COLOR springgreen][Enabled][/COLOR]"
                goto   = "false"
            except:
                state  = "[COLOR red][Disabled][/COLOR]"
                goto   = "true"
                pass
            icon   = os.path.join(folder, 'icon.png') if os.path.exists(os.path.join(folder, 'icon.png')) else ICON
            fanart = os.path.join(folder, 'fanart.jpg') if os.path.exists(os.path.join(folder, 'fanart.jpg')) else FANART
            addFile("%s %s" % (state, name), 'toggleaddon', fold, goto, icon=icon, fanart=fanart)
            f.close()
    if x == 0:
        addFile("No Addons Found to Enable or Disable.", '', icon=ICONMAINT)
    setView('files', 'viewType')


def advanced_window(url=None):
    from resources.libs import logging

    if not CONFIG.ADVANCEDFILE == 'http://':
        from resources.libs import clear
        from resources.libs import check

        if url is None:
            TEMPADVANCEDFILE = clear.text_cache(CONFIG.ADVANCEDFILE)
            if not TEMPADVANCEDFILE:
                ADVANCEDWORKING = check.check_url(CONFIG.ADVANCEDFILE)
        else:
            TEMPADVANCEDFILE = clear.text_cache(url)
            if not TEMPADVANCEDFILE:
                ADVANCEDWORKING = check.check_url(url)
        add_file('Quick Configure advancedsettings.xml', 'autoadvanced', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if os.path.exists(CONFIG.ADVANCED):
            add_file('View Current advancedsettings.xml', 'currentsettings', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            add_file('Remove Current advancedsettings.xml', 'removeadvanced',  icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if TEMPADVANCEDFILE:
            if CONFIG.HIDESPACERS == 'No':
                add_file(sep(), '', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            link = TEMPADVANCEDFILE.replace('\n', '').replace('\r', '').replace('\t', '')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                for name, section, url, icon, fanart, description in match:
                    if section.lower() == "yes":
                        add_dir("[B]{0}[/B]".format(name), 'advancedsetting', url, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
                    else:
                        add_file(name, 'writeadvanced', name, url, description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
            else:
                logging.log("[Advanced Settings] ERROR: Invalid Format.")
        else:
            logging.log("[Advanced Settings] URL not working: {0}".format(CONFIG.ADVANCEDFILE))
    else:
        logging.log("[Advanced Settings] not Enabled")

# MIGRATION: move to menu
def removeAddonMenu():
    fold = glob.glob(os.path.join(ADDONS, '*/'))
    addonnames = []; addonids = []
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername in EXCLUDES: continue
        elif foldername in DEFAULTPLUGINS: continue
        elif foldername == 'packages': continue
        xml = os.path.join(folder, 'addon.xml')
        if os.path.exists(xml):
            f      = open(xml)
            a      = f.read()
            match  = wiz.parseDOM(a, 'addon', ret='id')

            addid  = foldername if len(match) == 0 else match[0]
            try:
                add = xbmcaddon.Addon(id=addid)
                addonnames.append(add.getAddonInfo('name'))
                addonids.append(addid)
            except:
                pass
    if len(addonnames) == 0:
        wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Addons To Remove[/COLOR]" % COLOR2)
        return
    if KODIV > 16:
        selected = DIALOG.multiselect("%s: Select the addons you wish to remove." % ADDONTITLE, addonnames)
    else:
        selected = []; choice = 0
        tempaddonnames = ["-- Click here to Continue --"] + addonnames
        while not choice == -1:
            choice = DIALOG.select("%s: Select the addons you wish to remove." % ADDONTITLE, tempaddonnames)
            if choice == -1: break
            elif choice == 0: break
            else:
                choice2 = (choice-1)
                if choice2 in selected:
                    selected.remove(choice2)
                    tempaddonnames[choice] = addonnames[choice2]
                else:
                    selected.append(choice2)
                    tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
    if selected == None: return
    if len(selected) > 0:
        wiz.addonUpdates('set')
        for addon in selected:
            removeAddon(addonids[addon], addonnames[addon], True)

        xbmc.sleep(500)

        if INSTALLMETHOD == 1: todo = 1
        elif INSTALLMETHOD == 2: todo = 0
        else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR red]Force Close[/COLOR][/B]")
        if todo == 1: wiz.reloadFix('remove addon')
        else: wiz.addonUpdates('reset'); wiz.killxbmc(True)

# MIGRATION: move to menu
def removeAddonDataMenu():
    if os.path.exists(ADDOND):
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data', 'removedata', 'all', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data for Uninstalled Addons', 'removedata', 'uninstalled', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Empty Folders in Addon_Data', 'removedata', 'empty', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] %s Addon_Data' % ADDONTITLE, 'resetaddon', themeit=THEME2)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        fold = glob.glob(os.path.join(ADDOND, '*/'))
        for folder in sorted(fold, key = lambda x: x):
            foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
            icon = os.path.join(folder.replace(ADDOND, ADDONS), 'icon.png')
            fanart = os.path.join(folder.replace(ADDOND, ADDONS), 'fanart.png')
            folderdisplay = foldername
            replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR springgreen][SCRIPT] [/COLOR]', 'service.':'[COLOR springgreen][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
            for rep in replace:
                folderdisplay = folderdisplay.replace(rep, replace[rep])
            if foldername in EXCLUDES: folderdisplay = '[COLOR springgreen][B][PROTECTED][/B][/COLOR] %s' % folderdisplay
            else: folderdisplay = '[COLOR red][B][REMOVE][/B][/COLOR] %s' % folderdisplay
            addFile(' %s' % folderdisplay, 'removedata', foldername, icon=icon, fanart=fanart, themeit=THEME2)
    else:
        addFile('No Addon data folder found.', '', themeit=THEME3)
    setView('files', 'viewType')


def change_freq():
    from resources.libs import gui
    from resources.libs import logging

    change = gui.DIALOG.select("[COLOR {0}]How often would you list to Auto Clean on Startup?[/COLOR]".format(CONFIG.COLOR2), CONFIG.CLEANFREQ)
    if not change == -1:
        CONFIG.set_setting('autocleanfeq', str(change))
        logging.log_notify('[COLOR {0}]Auto Clean Up[/COLOR]'.format(CONFIG.COLOR1),
                           '[COLOR {0}]Frequency Now {1}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.CLEANFREQ[change]))


def developer():
    add_file('Create QR Code', 'createqr', themeit=CONFIG.THEME1)
    add_file('Test Notifications', 'testnotify', themeit=CONFIG.THEME1)
    add_file('Test Update', 'testupdate', themeit=CONFIG.THEME1)
    add_file('Test First Run', 'testfirst', themeit=CONFIG.THEME1)
    add_file('Test First Run Settings', 'testfirstrun', themeit=CONFIG.THEME1)
    set_view('files', 'viewType')

###########################
###### Build Install ######
###########################
# MIGRATION: move to menu
def buildWizard(name, type, theme=None, over=False):
    if over == False:
        testbuild = wiz.checkBuild(name, 'url')
        if testbuild == False:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Unabled to find build[/COLOR]" % COLOR2)
            return
        testworking = wiz.workingURL(testbuild)
        if testworking == False:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Build Zip Error: %s[/COLOR]" % (COLOR2, testworking))
            return
    if type == 'gui':
        if name == BUILDNAME:
            if over == True: yes = 1
            else: yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to apply the guifix for:' % COLOR2, '[COLOR %s]%s[/COLOR]?[/COLOR]' % (COLOR1, name), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Apply Fix[/COLOR][/B]')
        else:
            yes = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, "[COLOR %s][COLOR %s]%s[/COLOR] community build is not currently installed." % (COLOR2, COLOR1, name), "Would you like to apply the guiFix anyways?.[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Apply Fix[/COLOR][/B]')
        if yes:
            buildzip = wiz.checkBuild(name,'gui')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Invalid Zip Url![/COLOR]' % COLOR2); return
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading GuiFix:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s_guisettings.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(buildzip, lib, DP)
            xbmc.sleep(500)
            title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
            DP.update(0, title,'', 'Please Wait')
            extract.all(lib,USERDATA,DP, title=title)
            DP.close()
            wiz.defaultSkin()
            wiz.lookandFeelData('save')
            if KODIV >= 17:
                installed = grabAddons(lib)
                wiz.addonDatabase(installed, 1, True)
            if INSTALLMETHOD == 1: todo = 1
            elif INSTALLMETHOD == 2: todo = 0
            else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Gui fix has been installed.  Would you like to Reload the profile or Force Close Kodi?[/COLOR]" % COLOR2, yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
            if todo == 1: wiz.reloadFix()
            else: DIALOG.ok(ADDONTITLE, "[COLOR %s]To save changes you now need to force close Kodi, Press OK to force close Kodi[/COLOR]" % COLOR2); wiz.killxbmc('true')
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Cancelled![/COLOR]' % COLOR2)
    elif type == 'fresh':
        freshStart(name)
    elif type == 'normal':
        if url == 'normal':
            if KEEPTRAKT == 'true':
                traktit.autoUpdate('all')
                wiz.setS('traktlastsave', str(THREEDAYS))
            if KEEPREAL == 'true':
                debridit.autoUpdate('all')
                wiz.setS('debridlastsave', str(THREEDAYS))
            if KEEPLOGIN == 'true':
                loginit.autoUpdate('all')
                wiz.setS('loginlastsave', str(THREEDAYS))
        temp_kodiv = int(KODIV); buildv = int(float(wiz.checkBuild(name, 'kodi')))
        if not temp_kodiv == buildv:
            if temp_kodiv == 16 and buildv <= 15: warning = False
            else: warning = True
        else: warning = False
        if warning == True:
            yes_pressed = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, '[COLOR %s]There is a chance that the skin will not appear correctly' % COLOR2, 'When installing a %s build on a Kodi %s install' % (wiz.checkBuild(name, 'kodi'), KODIV), 'Would you still like to install: [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Yes, Install[/COLOR][/B]')
        else:
            if not over == False: yes_pressed = 1
            else: yes_pressed = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to Download and Install:' % COLOR2, '[COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Yes, Install[/COLOR][/B]')
        if yes_pressed:
            wiz.clearS('build')
            buildzip = wiz.checkBuild(name, 'url')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Build Install: Invalid Zip Url![/COLOR]' % COLOR2); return
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(buildzip, lib, DP)
            xbmc.sleep(500)
            title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version'))
            DP.update(0, title,'', 'Please Wait')
            percent, errors, error = extract.all(lib,HOME,DP, title=title)
            if int(float(percent)) > 0:
                wiz.fixmetas()
                wiz.lookandFeelData('save')
                wiz.defaultSkin()
                #wiz.addonUpdates('set')
                wiz.setS('buildname', name)
                wiz.setS('buildversion', wiz.checkBuild( name,'version'))
                wiz.setS('buildtheme', '')
                wiz.setS('latestversion', wiz.checkBuild( name,'version'))
                wiz.setS('lastbuildcheck', str(NEXTCHECK))
                wiz.setS('installed', 'true')
                wiz.setS('extract', str(percent))
                wiz.setS('errors', str(errors))
                wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
                try: os.remove(lib)
                except: pass
                if int(float(errors)) > 0:
                    yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B][COLOR red]No Thanks[/COLOR][/B]', yeslabel='[B][COLOR springgreen]View Errors[/COLOR][/B]')
                    if yes:
                        if isinstance(errors, unicode):
                            error = error.encode('utf-8')
                        wiz.TextBox(ADDONTITLE, error)
                DP.close()
                themefile = wiz.themeCount(name)
                if not themefile == False:
                    buildWizard(name, 'theme')
                if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
                if INSTALLMETHOD == 1: todo = 1
                elif INSTALLMETHOD == 2: todo = 0
                else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
                if todo == 1: wiz.reloadFix()
                else: wiz.killxbmc(True)
            else:
                if isinstance(errors, unicode):
                    error = error.encode('utf-8')
                wiz.TextBox("%s: Error Installing Build" % ADDONTITLE, error)
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Build Install: Cancelled![/COLOR]' % COLOR2)
    elif type == 'theme':
        if theme == None:
            themefile = wiz.checkBuild(name, 'theme')
            themelist = []
            if not themefile == 'http://' and wiz.workingURL(themefile) == True:
                themelist = wiz.themeCount(name, False)
                if len(themelist) > 0:
                    if DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Build [COLOR %s]%s[/COLOR] comes with [COLOR %s]%s[/COLOR] different themes" % (COLOR2, COLOR1, name, COLOR1, len(themelist)), "Would you like to install one now?[/COLOR]", yeslabel="[B][COLOR springgreen]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]"):
                        wiz.log("Theme List: %s " % str(themelist))
                        ret = DIALOG.select(ADDONTITLE, themelist)
                        wiz.log("Theme install selected: %s" % ret)
                        if not ret == -1: theme = themelist[ret]; installtheme = True
                        else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
                    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
            else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: None Found![/COLOR]' % COLOR2)
        else: installtheme = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to install the theme:' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, theme), 'for [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), yeslabel="[B][COLOR springgreen]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]")
        if installtheme:
            themezip = wiz.checkTheme(name, theme, 'url')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(themezip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Invalid Zip Url![/COLOR]' % COLOR2); return False
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(themezip, lib, DP)
            xbmc.sleep(500)
            DP.update(0,"", "Installing %s " % name)
            test = False
            if url not in ["fresh", "normal"]:
                test = testTheme(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
                test2 = testGui(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
                if test == True:
                    wiz.lookandFeelData('save')
                    swap = wiz.skinToDefault('Theme Install')
                    if swap == False: return False
                    xbmc.sleep(500)
            title = '[COLOR %s][B]Installing Theme:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme)
            DP.update(0, title,'', 'Please Wait')
            percent, errors, error = extract.all(lib,HOME,DP, title=title)
            wiz.setS('buildtheme', theme)
            wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
            DP.close()
            if url not in ["fresh", "normal"]:
                wiz.forceUpdate()
                if KODIV >= 17:
                    installed = grabAddons(lib)
                    wiz.addonDatabase(installed, 1, True)
                if test2 == True:
                    wiz.lookandFeelData('save')
                    wiz.defaultSkin()
                    gotoskin = wiz.getS('defaultskin')
                    wiz.swapSkins(gotoskin, "Theme Installer")
                    wiz.lookandFeelData('restore')
                elif test == True:
                    wiz.lookandFeelData('save')
                    wiz.defaultSkin()
                    gotoskin = wiz.getS('defaultskin')
                    wiz.swapSkins(gotoskin, "Theme Installer")
                    wiz.lookandFeelData('restore')
                else:
                    wiz.ebi("ReloadSkin()")
                    xbmc.sleep(1000)
                    wiz.ebi("Container.Refresh")
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2)

###########################
#      Misc Functions     #
###########################


def create_install_menu(name):
    menu_items = []

    name2 = quote_plus(name)
    menu_items.append(CONFIG.THEME2.format(name), 'RunAddon({0}, ?mode=viewbuild&name={1})'.format(CONFIG.ADDON_ID, name2))
    menu_items.append(CONFIG.THEME3.format('Fresh Install'), 'RunPlugin(plugin://{0}/?mode=install&name={1}&url=fresh)'.format(CONFIG.ADDON_ID, name2))
    menu_items.append(CONFIG.THEME3.format('Normal Install'), 'RunPlugin(plugin://{0}/?mode=install&name={1}&url=normal)'.format(CONFIG.ADDON_ID, name2))
    menu_items.append(CONFIG.THEME3.format('Apply guiFix'), 'RunPlugin(plugin://{0}/?mode=install&name={1}&url=gui)'.format(CONFIG.ADDON_ID, name2))
    menu_items.append(CONFIG.THEME3.format('Build Information'), 'RunPlugin(plugin://{0}/?mode=buildinfo&name={1})'.format(CONFIG.ADDON_ID, name2))
    menu_items.append(CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID))

    return menu_items


def create_addon_data_menu(add='', name=''):
    menu_items = []

    add2 = quote_plus(add.lower().replace(' ', ''))
    add3 = add.replace('Debrid', 'Real Debrid')
    name2 = quote_plus(name.lower().replace(' ', ''))
    name = name.replace('url', 'URL Resolver')
    menu_items.append(CONFIG.THEME2.format(name.title()), ' ')
    menu_items.append(CONFIG.THEME3.format('Save {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=save{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))
    menu_items.append(CONFIG.THEME3.format('Restore {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=restore{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))
    menu_items.append(CONFIG.THEME3.format('Clear {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=clear{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))

    menu_items.append(CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID))

    return menu_items


def create_save_data_menu(add='', name=''):
    menu_items = []

    add2 = quote_plus(add.lower().replace(' ', ''))
    add3 = add.replace('Debrid', 'Real Debrid')
    name2 = quote_plus(name.lower().replace(' ', ''))
    name = name.replace('url', 'URL Resolver')
    menu_items.append(CONFIG.THEME2.format(name.title()), ' ')
    menu_items.append(CONFIG.THEME3.format('Register {0}'.format(add3)), 'RunPlugin(plugin://{0}/?mode=auth{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))
    menu_items.append(CONFIG.THEME3.format('Save {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=save{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))
    menu_items.append(CONFIG.THEME3.format('Restore {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=restore{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))
    menu_items.append(CONFIG.THEME3.format('Import {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=import{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))
    menu_items.append(CONFIG.THEME3.format('Clear Addon {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=addon{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2))

    menu_items.append(CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID))

    return menu_items

# MIGRATION: move to check?
def buildInfo(name):
    if wiz.workingURL(BUILDFILE) == True:
        if wiz.checkBuild(name, 'url'):
            name, version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description = wiz.checkBuild(name, 'all')
            adult = 'Yes' if adult.lower() == 'yes' else 'No'
            extend = False
            if not info == "http://":
                try:
                    tname, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts = wiz.checkInfo(info)
                    extend = True
                except:
                    extend = False
            if extend == True:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] v[COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, version)
                msg += "[COLOR %s]Latest Update:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, created)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Extracted Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(extracted))))
                msg += "[COLOR %s]Zip Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(zipsize))))
                msg += "[COLOR %s]Skin Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, skin)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, description)
                msg += "[COLOR %s]Programs:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, programs)
                msg += "[COLOR %s]Video:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, video)
                msg += "[COLOR %s]Music:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, music)
                msg += "[COLOR %s]Pictures:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, picture)
                msg += "[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, repos)
                msg += "[COLOR %s]Scripts:[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, scripts)
            else:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, version)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, description)

            wiz.TextBox(ADDONTITLE, msg)
        else: wiz.log("Invalid Build Name!")
    else: wiz.log("Build text file not working: %s" % WORKINGURL)

###########################
#  Making the Directory   #
###########################


def add_separator(middle='', fanart=CONFIG.FANART, icon=CONFIG.ICON, themeit=CONFIG.THEME3):
    if CONFIG.HIDESPACERS == 'No':
        char = CONFIG.SPACER
        ret = char * 40
        if not middle == '':
            middle = '[ {0} ]'.format(middle)
            fluff = int((40 - len(middle))/2)
            ret = "{0}{1}{2}".format(ret[:fluff], middle, ret[:fluff+2])

            add_file(ret[:40], middle, fanart=fanart, icon=icon, themeit=themeit)


def add_file(display, mode=None, name=None, url=None, menu=None, description=CONFIG.ADDONTITLE, overwrite=True, fanart=CONFIG.FANART, icon=CONFIG.ICON, themeit=None, isFolder=False):
    add_menu_item(display, mode, name, url, menu, description, overwrite, fanart, icon, themeit, isFolder)


def add_dir(display, mode=None, name=None, url=None, menu=None, description=CONFIG.ADDONTITLE, overwrite=True, fanart=CONFIG.FANART, icon=CONFIG.ICON, themeit=None, isFolder=True):
    add_menu_item(display, mode, name, url, menu, description, overwrite, fanart, icon, themeit, isFolder)


def add_menu_item(display, mode, name, url, menu, description, overwrite, fanart, icon, themeit, isFolder):
    u = sys.argv[0]
    if mode is not None:
        u += "?mode={0}".format(quote_plus(mode))
    if name is not None:
        u += "&name={0}".format(quote_plus(name))
    if url is not None:
        u += "&url={0}".format(quote_plus(url))
    ok = True
    if themeit:
        display = themeit.format(display)
    liz = xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": display, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    if menu is not None:
        liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
    return ok


def set_view(viewtype='viewType'):
    if CONFIG.get_setting('auto-view') == 'true':
        views = CONFIG.get_setting(viewtype)
        if views == '50' and CONFIG.SKIN == 'skin.estuary':
            views = '55'
        if views == '500' and CONFIG.SKIN == 'skin.estuary':
            views = '50'
        xbmc.executebuiltin("Container.SetViewMode({0})".format(views))
