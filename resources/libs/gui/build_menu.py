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

import re

try:  # Python 3
    from urllib.parse import quote_plus
except ImportError:  # Python 2
    from urllib import quote_plus

from resources.libs import check
from resources.libs.common import directory
from resources.libs.common import tools
from resources.libs.common.config import CONFIG


class BuildMenu:

    def _list_all(self, match, kodiv=None):
        from resources.libs import test

        for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
            if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                continue
            if not CONFIG.DEVELOPER == 'true' and test.str_test(name):
                continue

            if not kodiv or kodiv == int(float(kodi)):
                menu = self.create_install_menu(name)
                directory.add_dir('[{0}] {1} (v{2})'.format(float(kodi), name, version), {'mode': 'viewbuild', 'name': name}, description=description, fanart=fanart, icon=icon, menu=menu, themeit=CONFIG.THEME2)

    def theme_count(self, name, count=True):
        from resources.libs import check
        from resources.libs.common import tools

        themefile = check.check_build(name, 'theme')

        response = tools.open_url(themefile)

        if not response:
            return False

        themetext = response.text
        link = tools.clean_text(themetext)
        match = re.compile('name="(.+?)"').findall(link)

        if len(match) == 0:
            return False

        themes = []
        for item in match:
            themes.append(item)
            
        if len(themes) > 0:
            if count:
                return len(themes)
            else:
                return themes
        else:
            return False

    def get_listing(self):
        from resources.libs import test
        
        response = tools.open_url(CONFIG.BUILDFILE)
        
        if response:
            link = tools.clean_text(response.text)
        else:
            directory.add_file('Kodi Version: {0}'.format(CONFIG.KODIV), icon=CONFIG.ICONBUILDS,
                               themeit=CONFIG.THEME3)
            directory.add_dir('Save Data Menu', {'mode': 'savedata'}, icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME3)
            directory.add_separator()
            directory.add_file('URL for txt file not valid', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
            directory.add_file('{0}'.format(CONFIG.BUILDFILE), icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
            return

        total, count19, adultcount, hidden = check.build_count()

        match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
        
        if total == 1:
            for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                    continue
                if not CONFIG.DEVELOPER == 'true' and test.str_test(name):
                    continue

                self.view_build(match[0][0])
                return

        directory.add_file('Kodi Version: {0}'.format(CONFIG.KODIV), icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
        directory.add_dir('Save Data Menu', {'mode': 'savedata'}, icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME3)
        directory.add_separator()

        if len(match) >= 1:
            if CONFIG.SEPARATE == 'true':
                self._list_all(match)
            else:
                if count19 > 0:
                    state = '+' if CONFIG.SHOW19 == 'false' else '-'
                    directory.add_file('[B]{0} Matrix Builds ({1})[/B]'.format(state, count19), {'mode': 'togglesetting',
                                       'name': 'show19'}, themeit=CONFIG.THEME3)
                    if CONFIG.SHOW19 == 'true':
                        self._list_all(match, kodiv=19)

        elif hidden > 0:
            if adultcount > 0:
                directory.add_file('There is currently only Adult builds', icon=CONFIG.ICONBUILDS,
                                   themeit=CONFIG.THEME3)
                directory.add_file('Enable Show Adults in Addon Settings > Misc', icon=CONFIG.ICONBUILDS,
                                   themeit=CONFIG.THEME3)
            else:
                directory.add_file('Currently No Builds Offered from {0}'.format(CONFIG.ADDONTITLE),
                                   icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME3)
        else:
            directory.add_file('Text file for builds not formatted correctly.', icon=CONFIG.ICONBUILDS,
                               themeit=CONFIG.THEME3)

    def view_build(self, name):
    
        response = tools.open_url(CONFIG.BUILDFILE)
        
        if response:
            link = tools.clean_text(response.text)
        else:
            directory.add_file('URL for txt file not valid', themeit=CONFIG.THEME3)
            directory.add_file('{0}'.format(CONFIG.BUILDFILE), themeit=CONFIG.THEME3)
            return

        if not check.check_build(name, 'version'):
            directory.add_file('Error reading the txt file.', themeit=CONFIG.THEME3)
            directory.add_file('{0} was not found in the builds list.'.format(name), themeit=CONFIG.THEME3)
            return

        match = re.compile(
            'name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?nfo="(.+?)".+?escription="(.+?)"' % name).findall(
            link)
            
        for version, url, gui, kodi, themefile, icon, fanart, preview, adult, info, description in match:
            build = '{0} (v{1})'.format(name, version)
            
            updatecheck = CONFIG.BUILDNAME == name and version > CONFIG.BUILDVERSION
            versioncheck = True if float(CONFIG.KODIV) == float(kodi) else False
            previewcheck = tools.open_url(preview, check=True)
            guicheck = tools.open_url(gui, check=True)
            themecheck = tools.open_url(themefile, check=True)
            
            if updatecheck:
                build = '{0} [COLOR red][CURRENT v{1}][/COLOR]'.format(build, CONFIG.BUILDVERSION)
                
            directory.add_file(build, description=description, fanart=fanart, icon=icon, themeit=CONFIG.THEME4)
            directory.add_separator()
            directory.add_dir('Save Data Menu', {'mode': 'savedata'}, icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME3)
            directory.add_file('Build Information', {'mode': 'buildinfo', 'name': name}, description=description, fanart=fanart,
                               icon=icon, themeit=CONFIG.THEME3)
                               
            if previewcheck:
                directory.add_file('View Video Preview', {'mode': 'buildpreview', 'name': name}, description=description, fanart=fanart,
                                   icon=icon, themeit=CONFIG.THEME3)
            
            if versioncheck:
                directory.add_file(
                    '[I]Build designed for Kodi v{0} (installed: v{1})[/I]'.format(str(kodi), str(CONFIG.KODIV)),
                    fanart=fanart, icon=icon, themeit=CONFIG.THEME3)
                    
            directory.add_separator('INSTALL')
            directory.add_file('Install', {'mode': 'install', 'action': 'build', 'name': name}, description=description, fanart=fanart,
                               icon=icon, themeit=CONFIG.THEME1)
                               
            if guicheck:
                directory.add_file('Apply guiFix', {'mode': 'install', 'action': 'gui', 'name': name}, description=description, fanart=fanart,
                                   icon=icon, themeit=CONFIG.THEME1)
                                   
            if themecheck:
                directory.add_separator('THEMES', fanart=fanart, icon=icon)

                response = tools.open_url(themefile)
                theme = response.text
                themelink = tools.clean_text(theme)
                match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(themelink)
                for themename, themeurl, themeicon, themefanart, themeadult, description in match:
                    adultcheck = CONFIG.SHOWADULT != 'true' and themeadult.lower() == 'yes'
                    
                    if adultcheck:
                        continue
                        
                    themetitle = themename if not themename == CONFIG.BUILDTHEME else "[B]{0} (Installed)[/B]".format(themename)
                    themeicon = themeicon if tools.open_url(themeicon, check=True) else icon
                    themefanart = themefanart if tools.open_url(themefanart, check=True) else fanart
                    
                    directory.add_file(themetitle, {'mode': 'install', 'action': 'theme', 'name': name, 'url': themename}, description=description, fanart=themefanart,
                        icon=themeicon, themeit=CONFIG.THEME3)

    def build_info(self, name):
        from resources.libs import check
        from resources.libs.common import logging
        from resources.libs.common import tools
        from resources.libs.gui import window
        
        response = tools.open_url(CONFIG.BUILDFILE, check=True)
        
        if response:
            if check.check_build(name, 'url'):
                name, version, url, minor, gui_ignore, kodi, theme, icon, fanart, preview, adult, info, description = check.check_build(name, 'all')
                adult = 'Yes' if adult.lower() == 'yes' else 'No'

                info_response = tools.open_url(info)

                if info_response:
                    try:
                        tname, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts, binaries = check.check_info(info_response.text)
                        extend = True
                    except:
                        extend = False
                else:
                    extend = False

                themes = self.theme_count(name, count=False)

                msg = "[COLOR {0}]Build Name:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, name)
                msg += "[COLOR {0}]Build Version:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, version)
                if themes:
                    msg += "[COLOR {0}]Build Theme(s):[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, ', '.join(themes))
                msg += "[COLOR {0}]Kodi Version:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, kodi)
                msg += "[COLOR {0}]Adult Content:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, adult)
                msg += "[COLOR {0}]Description:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, description)

                if extend:
                    msg += "[COLOR {0}]Latest Update:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, created)
                    msg += "[COLOR {0}]Extracted Size:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, tools.convert_size(int(float(extracted))))
                    msg += "[COLOR {0}]Zip Size:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, tools.convert_size(int(float(zipsize))))
                    msg += "[COLOR {0}]Skin Name:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, skin)
                    msg += "[COLOR {0}]Programs:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, programs)
                    msg += "[COLOR {0}]Video:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, video)
                    msg += "[COLOR {0}]Music:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, music)
                    msg += "[COLOR {0}]Pictures:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, picture)
                    msg += "[COLOR {0}]Repositories:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, repos)
                    msg += "[COLOR {0}]Scripts:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, scripts)
                    msg += "[COLOR {0}]Binaries:[/COLOR] [COLOR {1}]{2}[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, binaries)

                window.show_text_box("Viewing Build Info: {0}".format(name), msg)
            else:
                logging.log("Invalid Build Name!")
        else:
            logging.log("Build text file not working: {0}".format(CONFIG.BUILDFILE))

    def build_video(self, name):
        from resources.libs import check
        from resources.libs import yt
        from resources.libs.common import logging
        from resources.libs.common import tools
        
        response = tools.open_url(CONFIG.BUILDFILE, check=True)
        
        if response:
            videofile = check.check_build(name, 'preview')
            if tools.open_url(videofile, check=True):
                yt.play_video(videofile)
            else:
                logging.log("[{0}]Unable to find url for video preview".format(name))
        else:
            logging.log("Build text file not working: {0}".format(CONFIG.BUILDFILE))

    def create_install_menu(self, name):
        menu_items = []

        buildname = quote_plus(name)
        menu_items.append((CONFIG.THEME2.format(name), 'RunAddon({0}, ?mode=viewbuild&name={1})'.format(CONFIG.ADDON_ID, buildname)))
        menu_items.append((CONFIG.THEME3.format('Fresh Install'), 'RunPlugin(plugin://{0}/?mode=install&name={1}&url=fresh)'.format(CONFIG.ADDON_ID, buildname)))
        menu_items.append((CONFIG.THEME3.format('Normal Install'), 'RunPlugin(plugin://{0}/?mode=install&name={1}&url=normal)'.format(CONFIG.ADDON_ID, buildname)))
        menu_items.append((CONFIG.THEME3.format('Apply guiFix'), 'RunPlugin(plugin://{0}/?mode=install&name={1}&url=gui)'.format(CONFIG.ADDON_ID, buildname)))
        menu_items.append((CONFIG.THEME3.format('Build Information'), 'RunPlugin(plugin://{0}/?mode=buildinfo&name={1})'.format(CONFIG.ADDON_ID, buildname)))
        menu_items.append((CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID)))

        return menu_items
