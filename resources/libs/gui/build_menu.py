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

from resources.libs.common.config import CONFIG
from resources.libs.gui import directory


class MainMenu:

    def __init(self):
        super(MainMenu, self)

    def get_listing(self):
        from resources.libs import check
        from resources.libs.common import logging
        from resources.libs.common import tools

        errors = int(logging.error_checking(count=True))
        errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'

        if CONFIG.AUTOUPDATE == 'Yes':
            wizfile = tools.open_url(CONFIG.BUILDFILE)
            if wizfile:
                ver = check.check_wizard('version')
                if ver:
                    if ver > CONFIG.ADDON_VERSION:
                        directory.add_file(
                            '{0} [v{1}] [COLOR red][B][UPDATE v{2}][/B][/COLOR]'.format(CONFIG.ADDONTITLE,
                                                                                        CONFIG.ADDON_VERSION, ver),
                            'wizardupdate', themeit=CONFIG.THEME2)
                    else:
                        directory.add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.ADDON_VERSION), '',
                                           themeit=CONFIG.THEME2)
            else:
                directory.add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.ADDON_VERSION), '',
                                   themeit=CONFIG.THEME2)
        else:
            directory.add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.ADDON_VERSION), '', themeit=CONFIG.THEME2)
        if len(CONFIG.BUILDNAME) > 0:
            version = check.check_build(CONFIG.BUILDNAME, 'version')
            build = '{0} (v{1})'.format(CONFIG.BUILDNAME, CONFIG.BUILDVERSION)
            if version > CONFIG.BUILDVERSION:
                build = '{0} [COLOR red][B][UPDATE v{1}][/B][/COLOR]'.format(build, version)
            directory.add_dir(build, 'viewbuild', CONFIG.BUILDNAME, themeit=CONFIG.THEME4)
            themefile = check.theme_count(CONFIG.BUILDNAME)
            if themefile:
                directory.add_file('None' if CONFIG.BUILDTHEME == "" else CONFIG.BUILDTHEME, 'theme', CONFIG.BUILDNAME,
                                   themeit=CONFIG.THEME5)
        else:
            directory.add_dir('None', 'builds', themeit=CONFIG.THEME4)
        directory.add_separator()
        directory.add_dir('Builds', 'builds', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME1)
        directory.add_dir('Maintenance', 'maint', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        if (tools.platform() == 'android' or CONFIG.DEVELOPER == 'true') and CONFIG.KODIV < 18:
            directory.add_dir('APK Installer', 'apk', icon=CONFIG.ICONAPK, themeit=CONFIG.THEME1)
        if not CONFIG.ADDONFILE == 'http://':
            directory.add_dir('Addon Installer', 'addons', icon=CONFIG.ICONADDONS, themeit=CONFIG.THEME1)
        if not CONFIG.YOUTUBEFILE == 'http://' and not CONFIG.YOUTUBETITLE == '':
            directory.add_dir(CONFIG.YOUTUBETITLE, 'youtube', icon=CONFIG.ICONYOUTUBE, themeit=CONFIG.THEME1)
        directory.add_dir('Save Data', 'savedata', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
        if CONFIG.HIDECONTACT == 'No':
            directory.add_file('Contact', 'contact', icon=CONFIG.ICONCONTACT, themeit=CONFIG.THEME1)
        directory.add_separator()
        directory.add_file('Upload Log File', 'uploadlog', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_file('View Errors in Log: {0}'.format(errorsfound), 'viewerrorlog', icon=CONFIG.ICONMAINT,
                           themeit=CONFIG.THEME1)
        if errors > 0:
            directory.add_file('View Last Error In Log', 'viewerrorlast', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_separator()
        directory.add_file('Settings', 'settings', CONFIG.ADDON_ID, icon=CONFIG.ICONSETTINGS, themeit=CONFIG.THEME1)
        if CONFIG.DEVELOPER == 'true':
            directory.add_dir('Developer Menu', 'developer', icon=CONFIG.ADDON_ICON, themeit=CONFIG.THEME1)
