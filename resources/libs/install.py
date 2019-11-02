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
import re
import shutil

from resources.libs.common.config import CONFIG

###########################
#      Fresh Install      #
###########################


def wipe():
    from resources.libs import db
    from resources.libs.common import logging
    from resources.libs import skin
    from resources.libs.common import tools
    from resources.libs import update

    exclude_dirs = CONFIG.EXCLUDES
    exclude_dirs.append('My_Builds')
    
    progress_dialog = xbmcgui.DialogProgress()
    
    skin.skin_to_default('Fresh Install')
    
    update.addon_updates('set')
    xbmcPath = os.path.abspath(CONFIG.HOME)
    progress_dialog.create(CONFIG.ADDONTITLE,
                  "[COLOR {0}]Calculating files and folders".format(CONFIG.COLOR2), '', 'Please Wait![/COLOR]')
    total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)])
    del_file = 0
    progress_dialog.update(0, "[COLOR {0}]Gathering Excludes list.[/COLOR]".format(CONFIG.COLOR2))
    if CONFIG.KEEPREPOS == 'true':
        repos = glob.glob(os.path.join(CONFIG.ADDONS, 'repo*/'))
        for item in repos:
            repofolder = os.path.split(item[:-1])[1]
            if not repofolder == exclude_dirs:
                exclude_dirs.append(repofolder)
    if CONFIG.KEEPSUPER == 'true':
        exclude_dirs.append('plugin.program.super.favourites')
    if CONFIG.KEEPWHITELIST == 'true':
        from resources.libs import whitelist
        
        whitelist = whitelist.whitelist('read')
        if len(whitelist) > 0:
            for item in whitelist:
                try:
                    name, id, fold = item
                except:
                    pass

                depends = db.depends_list(fold)
                for plug in depends:
                    if plug not in exclude_dirs:
                        exclude_dirs.append(plug)
                    depends2 = db.depends_list(plug)
                    for plug2 in depends2:
                        if plug2 not in exclude_dirs:
                            exclude_dirs.append(plug2)
                if fold not in exclude_dirs:
                    exclude_dirs.append(fold)

    for item in CONFIG.DEPENDENCIES:
        exclude_dirs.append(item)

    progress_dialog.update(0, "[COLOR {0}]Clearing out files and folders:".format(CONFIG.COLOR2))
    latestAddonDB = db.latest_db('Addons')
    for root, dirs, files in os.walk(xbmcPath, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for name in files:
            del_file += 1
            fold = root.replace('/', '\\').split('\\')
            x = len(fold)-1
            if name == 'sources.xml' and fold[-1] == 'userdata' and CONFIG.KEEPSOURCES == 'true':
                logging.log("Keep sources.xml: {0}".format(os.path.join(root, name)), level=xbmc.LOGNOTICE)
            elif name == 'favourites.xml' and fold[-1] == 'userdata' and CONFIG.KEEPFAVS == 'true':
                logging.log("Keep favourites.xml: {0}".format(os.path.join(root, name)), level=xbmc.LOGNOTICE)
            elif name == 'profiles.xml' and fold[-1] == 'userdata' and CONFIG.KEEPPROFILES == 'true':
                logging.log("Keep profiles.xml: {0}".format(os.path.join(root, name)), level=xbmc.LOGNOTICE)
            elif name == 'playercorefactory.xml' and fold[-1] == 'userdata' and CONFIG.KEEPPLAYERCORE == 'true':
                logging.log("Keep playercorefactory.xml: {0}".format(os.path.join(root, name)), level=xbmc.LOGNOTICE)
            elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and CONFIG.KEEPADVANCED == 'true':
                logging.log("Keep advancedsettings.xml: {0}".format(os.path.join(root, name)), level=xbmc.LOGNOTICE)
            elif name in CONFIG.LOGFILES:
                logging.log("Keep Log File: {0}".format(name), level=xbmc.LOGNOTICE)
            elif name.endswith('.db'):
                try:
                    if name == latestAddonDB:
                        logging.log("Ignoring {0} on Kodi {1}".format(name, tools.kodi_version()), level=xbmc.LOGNOTICE)
                    else:
                        os.remove(os.path.join(root, name))
                except Exception as e:
                    if not name.startswith('Textures13'):
                        logging.log('Failed to delete, Purging DB', level=xbmc.LOGNOTICE)
                        logging.log("-> {0}".format(str(e)), level=xbmc.LOGNOTICE)
                        db.purge_db_file(os.path.join(root, name))
            else:
                progress_dialog.update(int(tools.percentage(del_file, total_files)), '',
                              '[COLOR {0}]File: [/COLOR][COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name), '')
                try:
                    os.remove(os.path.join(root, name))
                except Exception as e:
                    logging.log("Error removing {0}".format(os.path.join(root, name)), level=xbmc.LOGNOTICE)
                    logging.log("-> / {0}".format(str(e)), level=xbmc.LOGNOTICE)
        if progress_dialog.iscanceled():
            progress_dialog.close()
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]Fresh Start Cancelled[/COLOR]".format(CONFIG.COLOR2))
            return False
    for root, dirs, files in os.walk(xbmcPath, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for name in dirs:
            progress_dialog.update(100, '',
                          'Cleaning Up Empty Folder: [COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, name), '')
            if name not in ["Database", "userdata", "temp", "addons", "addon_data"]:
                shutil.rmtree(os.path.join(root, name), ignore_errors=True, onerror=None)
        if progress_dialog.iscanceled():
            progress_dialog.close()
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]Fresh Start Cancelled[/COLOR]".format(CONFIG.COLOR2))
            return False
            
    progress_dialog.close()
    CONFIG.clear_setting('build')


def fresh_start(install=None, over=False):
    from resources.libs.common import logging
    from resources.libs.common import tools

    dialog = xbmcgui.Dialog()
    
    if CONFIG.KEEPTRAKT == 'true':
        from resources.libs import traktit

        traktit.auto_update('all')
        CONFIG.set_setting('traktlastsave', str(tools.get_date(days=3)))
    if CONFIG.KEEPDEBRID == 'true':
        from resources.libs import debridit

        debridit.auto_update('all')
        CONFIG.set_setting('debridlastsave', str(tools.get_date(days=3)))
    if CONFIG.KEEPLOGIN == 'true':
        from resources.libs import loginit

        loginit.auto_update('all')
        CONFIG.set_setting('loginlastsave', str(tools.get_date(days=3)))

    if over:
        yes_pressed = 1

    elif install == 'restore':
        yes_pressed = dialog.yesno(CONFIG.ADDONTITLE,
                                       "[COLOR {0}]Do you wish to restore your".format(CONFIG.COLOR2),
                                       "Kodi configuration to default settings",
                                       "Before installing the local backup?[/COLOR]",
                                       nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                                       yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    elif install:
        yes_pressed = dialog.yesno(CONFIG.ADDONTITLE, "[COLOR {0}]Do you wish to restore your".format(CONFIG.COLOR2),
                                       "Kodi configuration to default settings",
                                       "Before installing [COLOR {0}]{1}[/COLOR]?".format(CONFIG.COLOR1, install),
                                       nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                                       yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    else:
        yes_pressed = dialog.yesno(CONFIG.ADDONTITLE,
                                       "[COLOR {0}]Do you wish to restore your".format(CONFIG.COLOR2),
                                       "Kodi configuration to default settings?[/COLOR]",
                                       nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',
                                       yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    if yes_pressed:
        wipe()
        
        if over:
            return True
        elif install == 'restore':
            return True
        elif install:
            from resources.libs.wizard import Wizard

            Wizard().build('normal', install, over=True)
        else:
            dialog.ok(CONFIG.ADDONTITLE, "[COLOR {0}]To save changes you now need to force close Kodi, Press OK to force close Kodi[/COLOR]".format(CONFIG.COLOR2))
            from resources.libs import update
            update.addon_updates('reset')
            tools.kill_kodi(True)
    else:
        if not install == 'restore':
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               '[COLOR {0}]Fresh Install: Cancelled![/COLOR]'.format(CONFIG.COLOR2))
            xbmc.executebuiltin('Container.Refresh()')


def install_addon_pack(name, url):
    from resources.libs import downloader
    from resources.libs import db
    from resources.libs import extract
    from resources.libs.common import logging
    from resources.libs.common import tools

    progress_dialog = xbmcgui.DialogProgress()
    
    if not tools.check_url(url):
        logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                           '[COLOR {0}]{1}:[/COLOR] [COLOR {2}]Invalid Zip Url![/COLOR]'.format(CONFIG.COLOR1, name, CONFIG.COLOR2))
        return
    if not os.path.exists(CONFIG.PACKAGES):
        os.makedirs(CONFIG.PACKAGES)
    
    progress_dialog.create(CONFIG.ADDONTITLE,
                  '[COLOR {0}][B]Downloading:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name),
                  '', '[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
    urlsplits = url.split('/')
    lib = xbmc.makeLegalFilename(os.path.join(CONFIG.PACKAGES, urlsplits[-1]))
    try:
        os.remove(lib)
    except:
        pass
    downloader.download(url, lib)
    title = '[COLOR {0}][B]Installing:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name)
    progress_dialog.update(0, title, '', '[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
    percent, errors, error = extract.all(lib, CONFIG.ADDONS, title=title)
    installed = db.grab_addons(lib)
    db.addon_database(installed, 1, True)
    progress_dialog.close()
    logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                       '[COLOR {0}]{1}: Installed![/COLOR]'.format(CONFIG.COLOR2, name))
    xbmc.executebuiltin('UpdateAddonRepos()')
    xbmc.executebuiltin('UpdateLocalAddons()')
    xbmc.executebuiltin('Container.Refresh()')


def install_skin(name, url):
    from resources.libs import downloader
    from resources.libs import db
    from resources.libs import extract
    from resources.libs.common import logging
    from resources.libs import skin
    from resources.libs.common import tools

    progress_dialog = xbmcgui.DialogProgress()
    
    if not tools.check_url(url):
        logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                           '[COLOR {0}]{1}:[/COLOR] [COLOR {2}]Invalid Zip Url![/COLOR]'.format(CONFIG.COLOR1, name, CONFIG.COLOR2))
        return
    if not os.path.exists(CONFIG.PACKAGES):
        os.makedirs(CONFIG.PACKAGES)
    
    progress_dialog.create(CONFIG.ADDONTITLE,
                  '[COLOR {0}][B]Downloading:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name),
                  '', '[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
    urlsplits = url.split('/')
    lib = xbmc.makeLegalFilename(os.path.join(CONFIG.PACKAGES, urlsplits[-1]))
    try:
        os.remove(lib)
    except:
        pass
    downloader.download(url, lib)
    title = '[COLOR {0}][B]Installing:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name)
    progress_dialog.update(0, title, '', '[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
    percent, errors, error = extract.all(lib, CONFIG.HOME, title=title)
    installed = db.grab_addons(lib)
    db.addon_database(installed, 1, True)
    progress_dialog.close()
    logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                       '[COLOR {0}]{1}: Installed![/COLOR]'.format(CONFIG.COLOR2, name))
    xbmc.executebuiltin('UpdateAddonRepos()')
    xbmc.executebuiltin('UpdateLocalAddons()')
    for item in installed:
        if item.startswith('skin.') and not item == 'skin.shortcuts':
            if not CONFIG.BUILDNAME == '' and CONFIG.DEFAULTIGNORE == 'true':
                CONFIG.set_setting('defaultskinignore', 'true')
            skin.switch_to_skin(item, 'Skin Installer')
    xbmc.executebuiltin('Container.Refresh()')


def install_addon_from_url(name, url):
    from resources.libs import downloader
    from resources.libs import db
    from resources.libs import extract
    from resources.libs.common import logging
    from resources.libs import skin
    from resources.libs.common import tools

    progress_dialog = xbmcgui.DialogProgress()
    
    if not tools.check_url(url):
        logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                           '[COLOR {0}]{1}:[/COLOR] [COLOR {2}]Invalid Zip Url![/COLOR]'.format(CONFIG.COLOR1, name, CONFIG.COLOR2))
        return
    if not os.path.exists(CONFIG.PACKAGES):
        os.makedirs(CONFIG.PACKAGES)
    
    progress_dialog.create(CONFIG.ADDONTITLE,
                  '[COLOR {0}][B]Downloading:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name),
                  '', '[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
    urlsplits = url.split('/')
    lib = os.path.join(CONFIG.PACKAGES, urlsplits[-1])
    try:
        os.remove(lib)
    except:
        pass
    downloader.download(url, lib)
    title = '[COLOR {0}][B]Installing:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name)
    progress_dialog.update(0, title, '', '[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
    percent, errors, error = extract.all(lib, CONFIG.ADDONS, title=title)
    progress_dialog.update(0, title, '', '[COLOR {0}]Installing Dependencies[/COLOR]'.format(CONFIG.COLOR2))
    installed(name)
    installlist = db.grab_addons(lib)
    logging.log(str(installlist))
    db.addon_database(installlist, 1, True)
    install_dependency(name, progress_dialog)
    progress_dialog.close()

    xbmc.executebuiltin('UpdateAddonRepos()')
    xbmc.executebuiltin('UpdateLocalAddons()')
    xbmc.executebuiltin('Container.Refresh()')

    for item in installlist:
        if item.startswith('skin.') and not item == 'skin.shortcuts':
            if not CONFIG.BUILDNAME == '' and CONFIG.DEFAULTIGNORE == 'true':
                CONFIG.set_setting('defaultskinignore', 'true')
            skin.switch_to_skin(item, 'Skin Installer')


def install_addon(plugin, url):
    from resources.libs.common import logging
    from resources.libs.common import tools

    if tools.check_url(CONFIG.ADDONFILE):
        from resources.libs import clear
        from resources.libs import downloader
        from resources.libs import db
        from resources.libs import extract
        from resources.libs import skin

        dialog = xbmcgui.Dialog()
        
        if url is None:
            url = CONFIG.ADDONFILE
            
        if tools.check_url(url):
            link = tools.open_url(url).replace('\n', '').replace('\r', '').replace('\t', '').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
            match = re.compile('name="(.+?)".+?lugin="%s".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % plugin).findall(link)
            if len(match) > 0:
                for name, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
                    if os.path.exists(os.path.join(CONFIG.ADDONS, plugin)):
                        do = ['Launch Addon', 'Remove Addon']
                        selected = dialog.select("[COLOR {0}]Addon already installed what would you like to do?[/COLOR]".format(CONFIG.COLOR2), do)
                        if selected == 0:
                            xbmc.executebuiltin('RunAddon({0})'.format(plugin))
                            xbmc.sleep(500)
                            return True
                        elif selected == 1:
                            tools.clean_house(os.path.join(CONFIG.ADDONS, plugin))
                            try:
                                tools.remove_folder(os.path.join(CONFIG.ADDONS, plugin))
                            except:
                                pass
                            if dialog.yesno(CONFIG.ADDONTITLE,
                                                "[COLOR {0}]Would you like to remove the addon_data for:".format(CONFIG.COLOR2),
                                                "[COLOR {0}]{1}[/COLOR]?[/COLOR]".format(CONFIG.COLOR1, plugin),
                                                yeslabel="[B][COLOR springgreen]Yes Remove[/COLOR][/B]",
                                                nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
                                clear.remove_addon_data(plugin)
                            xbmc.executebuiltin('Container.Refresh()')
                            return True
                        else:
                            return False
                    repo = os.path.join(CONFIG.ADDONS, repository)
                    if repository.lower() != 'none' and not os.path.exists(repo):
                        logging.log("Repository not installed, installing it")
                        if dialog.yesno(CONFIG.ADDONTITLE,
                                            "[COLOR {0}]Would you like to install the repository for [COLOR {1}]{2}[/COLOR]: ".format(CONFIG.COLOR2, CONFIG.COLOR1, plugin),
                                            "[COLOR {0}]{1}[/COLOR]?[/COLOR]".format(CONFIG.COLOR1, repository),
                                            yeslabel="[B][COLOR springgreen]Yes Install[/COLOR][/B]",
                                            nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
                            ver = tools.parse_dom(tools.open_url(repositoryxml), 'addon', ret='version', attrs={'id': repository})
                            if len(ver) > 0:
                                repozip = '{0}{1}-{2}.zip'.format(repositoryurl, repository, ver[0])
                                logging.log(repozip)
                                db.addon_database(repository, 1)
                                install_addon(repository, repozip)
                                xbmc.executebuiltin('UpdateAddonRepos()')
                                logging.log("Installing Addon from Kodi")
                                install = install_from_kodi(plugin)
                                logging.log("Install from Kodi: {0}".format(install))
                                if install:
                                    xbmc.executebuiltin('Container.Refresh()')
                                    return True
                            else:
                                logging.log("[Addon Installer] Repository not installed: Unable to grab url! ({0})".format(repository))
                        else:
                            logging.log("[Addon Installer] Repository for {0} not installed: {1}".format(plugin, repository))
                    elif repository.lower() == 'none':
                        logging.log("No repository, installing addon")
                        pluginid = plugin
                        zipurl = url
                        install_addon_from_url(plugin, url)
                        xbmc.executebuiltin('Container.Refresh()')
                        return True
                    else:
                        logging.log("Repository installed, installing addon")
                        install = install_from_kodi(plugin)
                        if install:
                            xbmc.executebuiltin('Container.Refresh()')
                            return True
                    if os.path.exists(os.path.join(CONFIG.ADDONS, plugin)):
                        return True
                    ver2 = tools.parse_dom(tools.open_url(repositoryxml), 'addon', ret='version', attrs={'id': plugin})
                    if len(ver2) > 0:
                        url = "{0}{1}-{2}.zip".format(url, plugin, ver2[0])
                        logging.log(str(url))
                        db.addon_database(plugin, 1)
                        install_addon_from_url(plugin, url)
                        xbmc.executebuiltin('Container.Refresh()')
                    else:
                        logging.log("no match")
                        return False
            else:
                logging.log("[Addon Installer] Invalid Format")
        else:
            logging.log("[Addon Installer] Text File: {0}".format(CONFIG.ADDONFILE))
    else:
        logging.log("[Addon Installer] Not Enabled.")


def install_from_kodi(plugin):
    import threading
    from resources.libs.gui import window

    xbmc.executebuiltin('RunPlugin(plugin://{0})'.format(plugin))
    
    threading.Thread(target=_dialog_watch, kwargs={'window': 'yesnodialog', 'action': 11, 'count': 200}).start()
    
    if os.path.exists(os.path.join(CONFIG.ADDONS, plugin)):
        return True
    else:
        return False


def install_dependency(name):
    from resources.libs import db
    from resources.libs.common import tools

    progress_dialog = xbmcgui.DialogProgress()
    
    dep = os.path.join(CONFIG.ADDONS, name, 'addon.xml')
    if os.path.exists(dep):
        match = tools.parse_dom(tools.read_from_file(dep), 'import', ret='addon')
        for depends in match:
            if 'xbmc.python' not in depends:
                progress_dialog.update(0, '', '[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, depends))
                
                try:
                    add = tools.get_addon_by_id(id=depends)
                    name2 = tools.get_addon_info(add, 'name')
                except:
                    db.create_temp(depends)
                    db.addon_database(depends, 1)


def installed(addon):
    url = os.path.join(CONFIG.ADDONS, addon, 'addon.xml')
    if os.path.exists(url):
        try:
            from resources.libs.common import logging
            from resources.libs.common import tools

            name = tools.parse_dom(tools.read_from_file(url), 'addon', ret='name', attrs={'id': addon})
            icon = os.path.join(CONFIG.ADDONS, addon, 'icon.png')  # read from infolabel?
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, name[0]),
                               '[COLOR {0}]Add-on Enabled[/COLOR]'.format(CONFIG.COLOR2), '2000', icon)
        except:
            pass


def install_apk(apk, url):
    from resources.libs import downloader
    from resources.libs.common import logging
    from resources.libs.common import tools
    from resources.libs.gui import window

    dialog = xbmcgui.Dialog()
    progress_dialog = xbmcgui.DialogProgress()
    
    logging.log(apk)
    logging.log(url)
    if tools.platform() == 'android':
        yes = dialog.yesno(CONFIG.ADDONTITLE,
                               "[COLOR {0}]Would you like to download and install: ".format(CONFIG.COLOR2),
                               "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, apk),
                               yeslabel="[B][COLOR springgreen]Download[/COLOR][/B]",
                               nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
        if not yes:
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               '[COLOR {0}]ERROR: Install Cancelled[/COLOR]'.format(CONFIG.COLOR2))
            return
        display = apk
        if not os.path.exists(CONFIG.PACKAGES):
            os.makedirs(CONFIG.PACKAGES)
        if not tools.check_url(url):
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               '[COLOR {0}]APK Installer: Invalid Apk Url![/COLOR]'.format(CONFIG.COLOR2))
            return
        progress_dialog.create(CONFIG.ADDONTITLE,
                      '[COLOR {0}][B]Downloading:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, display),
                      '', 'Please Wait')
        lib = os.path.join(CONFIG.PACKAGES, "{0}.apk".format(apk.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')))
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib)
        xbmc.sleep(100)
        progress_dialog.close()
        window.show_apk_warning(apk)
        xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:{0}")'.format(lib))
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           '[COLOR {0}]ERROR: None Android Device[/COLOR]'.format(CONFIG.COLOR2))
                           

def _dialog_watch(window='yesnodialog', action=11, count=100):
    x = 0
    while not xbmc.getCondVisibility("Window.isVisible({0})".format(window)) and x < count:
        x += 1
        xbmc.sleep(100)

    if xbmc.getCondVisibility("Window.isVisible({0})".format(window)):
        xbmc.executebuiltin('SendClick({0}, {1})'.format(window, action))
        return True
    else:
        return False
