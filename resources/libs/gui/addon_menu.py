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

import os

from resources.libs.common.config import CONFIG
from resources.libs.common import directory
from resources.libs.common import logging
from resources.libs.common import tools


def installed(addon):
    url = os.path.join(CONFIG.ADDONS, addon, 'addon.xml')
    if os.path.exists(url):
        try:
            name = tools.parse_dom(tools.read_from_file(url), 'addon', ret='name', attrs={'id': addon})
            icon = os.path.join(CONFIG.ADDONS, addon, 'icon.png')  # read from infolabel?
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, name[0]),
                               '[COLOR {0}]Add-on Enabled[/COLOR]'.format(CONFIG.COLOR2), '2000', icon)
        except:
            pass


def install_from_kodi(plugin):
    import time

    installed_cond = 'System.HasAddon({0})'.format(plugin)
    visible_cond = 'Window.IsTopMost(yesnodialog)'

    if xbmc.getCondVisibility(installed_cond):
        logging.log('Already installed ' + plugin, level=xbmc.LOGDEBUG)
        return True

    logging.log('Installing ' + plugin, level=xbmc.LOGDEBUG)
    xbmc.executebuiltin('InstallAddon({0})'.format(plugin))

    clicked = False
    start = time.time()
    timeout = 20
    while not xbmc.getCondVisibility(installed_cond):
        if time.time() >= start + timeout:
            logging.log('Timed out installing', level=xbmc.LOGDEBUG)
            return False

        xbmc.sleep(500)

        # Assuming we only want to answer the one known "install" dialog
        if xbmc.getCondVisibility(visible_cond) and not clicked:
            logging.log('Dialog to click open', level=xbmc.LOGDEBUG)
            xbmc.executebuiltin('SendClick(yesnodialog, 11)')
            clicked = True
        else:
            logging.log('...waiting', level=xbmc.LOGDEBUG)

    logging.log('Installed {0}!'.format(plugin), level=xbmc.LOGDEBUG)
    return True


class AddonMenu:
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
        self.progress_dialog = xbmcgui.DialogProgress()

    def show_menu(self, url=None):
        response = tools.open_url(CONFIG.ADDONFILE)
        url_response = tools.open_url(url)
        local_file = os.path.join(CONFIG.ADDON_PATH, 'resources', 'text', 'addons.json')

        if url_response:
            TEMPADDONFILE = url_response.text
        elif response:
            TEMPADDONFILE = response.text
        elif os.path.exists(local_file):
            TEMPADDONFILE = tools.read_from_file(local_file)
        else:
            TEMPADDONFILE = None
            logging.log("[Addon Menu] No Addon list added.")

        if TEMPADDONFILE:
            import json

            try:
                addons_json = json.loads(TEMPADDONFILE)
            except:
                addons_json = None
                logging.log("[Advanced Settings] ERROR: Invalid Format for {0}.".format(TEMPADDONFILE))

            if addons_json:
                addons = addons_json['addons']

                if addons and len(addons) > 0:
                    for addon in addons:
                        addonname = addon.get('name', '')
                        type = addon.get('type', 'addon')
                        section = addon.get('section', False)
                        plugin = addon.get('plugin', '')
                        addonurl = addon.get('url', '')
                        repository = addon.get('repository', '')
                        repositoryxml = addon.get('repositoryxml', '')
                        repositoryurl = addon.get('repositoryurl', '')
                        icon = addon.get('icon', CONFIG.ADDON_ICON)
                        fanart = addon.get('fanart', CONFIG.ADDON_FANART)
                        adult = addon.get('adult', False)
                        description = addon.get('description', '')

                        if not addonname:
                            logging.log('[Advanced Settings] Missing tag \'name\'', level=xbmc.LOGDEBUG)
                            continue

                        if not addonurl:
                            logging.log('[Advanced Settings] Missing tag \'url\'', level=xbmc.LOGDEBUG)
                            continue
                        else:
                            if '.zip' in addonurl:
                                pass
                            elif not section:
                                broken = False
                                if not repository:
                                    logging.log('[Advanced Settings] Missing tag \'repository\'', level=xbmc.LOGDEBUG)
                                    broken = True
                                if not repositoryxml:
                                    logging.log('[Advanced Settings] Missing tag \'repositoryxml\'',
                                                level=xbmc.LOGDEBUG)
                                    broken = True
                                if not repositoryurl:
                                    logging.log('[Advanced Settings] Missing tag \'repositoryurl\'',
                                                level=xbmc.LOGDEBUG)
                                    broken = True
                                if broken:
                                    continue

                        if section:
                            directory.add_dir(addonname, {'mode': 'addons', 'url': addonurl}, description=description,
                                              icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
                        else:
                            if not CONFIG.SHOWADULT == 'true' and adult:
                                continue

                            if type.lower() == 'skin':
                                directory.add_file(addonname,
                                                   {'mode': 'addons', 'action': 'skin', 'name': addonname,
                                                    'url': addonurl}, description=description, icon=icon, fanart=fanart,
                                                   themeit=CONFIG.THEME2)
                            elif type.lower() == 'addonpack':
                                directory.add_file(addonname, {'mode': 'addons', 'action': 'addonpack',
                                                               'name': addonname, 'url': addonurl},
                                                   description=description, icon=icon, fanart=fanart,
                                                   themeit=CONFIG.THEME2)
                            else:
                                try:
                                    add = tools.get_addon_info(plugin, 'path')
                                    if os.path.exists(add):
                                        addonname = "[COLOR springgreen][Installed][/COLOR] {0}".format(addonname)
                                except:
                                    pass

                                directory.add_file(addonname, {'mode': 'addons', 'action': 'addon', 'name': plugin,
                                                               'addonurl': addonurl, 'repository': repository, 'repositoryxml': repositoryxml,
                                                                        'repositoryurl': repositoryurl}, description=description,
                                                   icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
                else:
                    if not addons:
                        directory.add_file('Text File not formatted correctly!', themeit=CONFIG.THEME3)
                        logging.log("[Addon Menu] ERROR: Invalid Format.")
                    elif len(addons) == 0:
                        directory.add_file("No addons added to this menu yet!", themeit=CONFIG.THEME2)
        else:
            logging.log("[Addon Menu] ERROR: URL for Addon list not working.")
            directory.add_file('Url for txt file not valid', themeit=CONFIG.THEME3)
            directory.add_file('{0}'.format(CONFIG.ADDONFILE), themeit=CONFIG.THEME3)

    def install_dependency(self, plugin):
        from resources.libs import db

        dep = os.path.join(CONFIG.ADDONS, plugin, 'addon.xml')
        if os.path.exists(dep):
            match = tools.parse_dom(tools.read_from_file(dep), 'import', ret='addon')
            for depends in match:
                if 'xbmc.python' not in depends:
                    self.progress_dialog.update(0, '\n'+'[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, depends))

                    try:
                        add = tools.get_addon_by_id(id=depends)
                        name2 = tools.get_addon_info(add, 'name')
                    except:
                        db.create_temp(depends)
                        db.addon_database(depends, 1)

    def install_addon_from_url(self, plugin, url):
        from resources.libs.downloader import Downloader
        from resources.libs import db
        from resources.libs import extract
        from resources.libs import skin

        response = tools.open_url(url, check=True)

        if not response:
            logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                               '[COLOR {0}]{1}:[/COLOR] [COLOR {2}]Invalid Zip Url![/COLOR]'.format(CONFIG.COLOR1,
                                                                                                    plugin,
                                                                                                    CONFIG.COLOR2))
            return

        tools.ensure_folders(CONFIG.PACKAGES)

        self.progress_dialog.create(CONFIG.ADDONTITLE,
                               '[COLOR {0}][B]Downloading:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2,
                                                                                                      CONFIG.COLOR1,
                                                                                                      plugin)
                               +'\n'+''
                               +'\n'+'[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
        urlsplits = url.split('/')
        lib = os.path.join(CONFIG.PACKAGES, urlsplits[-1])

        try:
            os.remove(lib)
        except:
            pass
            
        Downloader().download(url, lib)
        title = '[COLOR {0}][B]Installing:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1,
                                                                                      plugin)
        self.progress_dialog.update(0, title
                                    +'\n'+''
                                    +'\n'+'[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
        percent, errors, error = extract.all(lib, CONFIG.ADDONS, title=title)
        self.progress_dialog.update(0, title
                                    +'\n'+''
                                    +'\n'+'[COLOR {0}]Installing Dependencies[/COLOR]'.format(CONFIG.COLOR2))
        installed(plugin)
        installlist = db.grab_addons(lib)
        logging.log(str(installlist))
        db.addon_database(installlist, 1, True)
        self.install_dependency(plugin)
        self.progress_dialog.close()

        xbmc.executebuiltin('UpdateAddonRepos()')
        xbmc.executebuiltin('UpdateLocalAddons()')
        xbmc.executebuiltin('Container.Refresh()')

        for item in installlist:
            if item.startswith('skin.') and not item == 'skin.shortcuts':
                if not CONFIG.BUILDNAME == '' and CONFIG.DEFAULTIGNORE == 'true':
                    CONFIG.set_setting('defaultskinignore', 'true')
                skin.switch_to_skin(item, 'Skin Installer')

    def install_addon(self, plugin, urls, over=False):
        from resources.libs import db

        install = None

        if not over:        
            if xbmc.getCondVisibility('System.HasAddon({0})'.format(plugin)):
                install = self.dialog.yesno(CONFIG.ADDONTITLE, '[COLOR {0}]{1}[/COLOR] already installed. Would you like to reinstall it?'.format(CONFIG.COLOR1, plugin))
            else:
                install = self.dialog.yesno(CONFIG.ADDONTITLE, 'Would you like to install [COLOR {0}]{1}[/COLOR]?'.format(CONFIG.COLOR1, plugin))
        else:
            install = True
            
        if not install:
            return
            
        url_response = tools.open_url(urls[0], check=True)
        repositoryurl_response = tools.open_url(urls[2], check=True)
        repositoryxml_response = tools.open_url(urls[3])
        
        if False not in [repositoryxml_response, repositoryurl_response]:
        
            repo_id = urls[1]
        
            if not xbmc.getCondVisibility('System.HasAddon({0})'.format(repo_id)):
                logging.log("Repository not installed, installing it")

                from xml.etree import ElementTree
                root = ElementTree.fromstring(repositoryxml_response.text.encode('ascii', 'backslashreplace'))
                entries = root.findall('addon')
                version = None

                for entry in entries:
                    if entry.attrib['id'] == repo_id:
                        version = entry.attrib['version']

                if version:
                    repozip = '{0}{1}-{2}.zip'.format(urls[2], repo_id, version)
                    logging.log(repozip)
                    db.addon_database(repo_id, 1)
                    self.install_addon(repo_id, repozip, over=True)
                    xbmc.executebuiltin('UpdateAddonRepos()')
                    install = install_from_kodi(plugin)
                    if install:
                        xbmc.executebuiltin('Container.Refresh()')
                        return True
                else:
                    logging.log(
                        "[Addon Installer] Repository not installed: Unable to grab url! ({0})".format(urls[1]))
            else:
                logging.log("Repository installed, installing addon")
                install = install_from_kodi(plugin)
                if install:
                    xbmc.executebuiltin('Container.Refresh()')
                    return True
        elif url_response:
            logging.log("No repository, installing addon")
            self.install_addon_from_url(plugin, urls[0])

            if os.path.exists(os.path.join(CONFIG.ADDONS, plugin)):
                return True

            from xml.etree import ElementTree
            root = ElementTree.parse(repositoryxml_response.text)
            entries = root.findall('addon')
            version = None

            for entry in entries:
                if entry.attrib['id'] == repo_id:
                    version = entry.attrib['version']

            if version > 0:
                url = "{0}{1}-{2}.zip".format(urls[0], plugin, version)
                logging.log(str(url))
                db.addon_database(plugin, 1)
                self.install_addon_from_url(plugin, url)
                xbmc.executebuiltin('Container.Refresh()')
            else:
                logging.log("no match")
                return False
    
    def install_addon_pack(self, name, url):
        from resources.libs.downloader import Downloader
        from resources.libs import db
        from resources.libs import extract
        from resources.libs.common import logging
        from resources.libs.common import tools

        progress_dialog = xbmcgui.DialogProgress()

        response = tools.open_url(url, check=True)

        if not response:
            logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                               '[COLOR {0}]{1}:[/COLOR] [COLOR {2}]Invalid Zip Url![/COLOR]'.format(CONFIG.COLOR1, name, CONFIG.COLOR2))
            return

        if not os.path.exists(CONFIG.PACKAGES):
            os.makedirs(CONFIG.PACKAGES)
        
        progress_dialog.create(CONFIG.ADDONTITLE,
                      '[COLOR {0}][B]Downloading:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name)
                      +'\n'+''
                      +'\n'+'[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
        urlsplits = url.split('/')
        lib = xbmc.makeLegalFilename(os.path.join(CONFIG.PACKAGES, urlsplits[-1]))
        try:
            os.remove(lib)
        except:
            pass
        Downloader().download(url, lib)
        title = '[COLOR {0}][B]Installing:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name)
        progress_dialog.update(0, title
                                +'\n'+''
                                +'\n'+'[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
        percent, errors, error = extract.all(lib, CONFIG.ADDONS, title=title)
        installed = db.grab_addons(lib)
        db.addon_database(installed, 1, True)
        progress_dialog.close()
        logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                           '[COLOR {0}]{1}: Installed![/COLOR]'.format(CONFIG.COLOR2, name))
        xbmc.executebuiltin('UpdateAddonRepos()')
        xbmc.executebuiltin('UpdateLocalAddons()')
        xbmc.executebuiltin('Container.Refresh()')


    def install_skin(self, name, url):
        from resources.libs.downloader import Downloader
        from resources.libs import db
        from resources.libs import extract
        from resources.libs.common import logging
        from resources.libs import skin
        from resources.libs.common import tools

        progress_dialog = xbmcgui.DialogProgress()

        response = tools.open_url(url, check=False)

        if not response:
            logging.log_notify("[COLOR {0}]Addon Installer[/COLOR]".format(CONFIG.COLOR1),
                               '[COLOR {0}]{1}:[/COLOR] [COLOR {2}]Invalid Zip Url![/COLOR]'.format(CONFIG.COLOR1, name, CONFIG.COLOR2))
            return

        if not os.path.exists(CONFIG.PACKAGES):
            os.makedirs(CONFIG.PACKAGES)
        
        progress_dialog.create(CONFIG.ADDONTITLE,
                      '[COLOR {0}][B]Downloading:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name)
                      +'\n'+''
                      +'\n'+'[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))

        urlsplits = url.split('/')
        lib = xbmc.makeLegalFilename(os.path.join(CONFIG.PACKAGES, urlsplits[-1]))
        try:
            os.remove(lib)
        except:
            pass
        Downloader().download(url, lib)
        title = '[COLOR {0}][B]Installing:[/B][/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, name)
        progress_dialog.update(0, title
                                    +'\n'+''
                                    +'\n'+'[COLOR {0}]Please Wait[/COLOR]'.format(CONFIG.COLOR2))
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
