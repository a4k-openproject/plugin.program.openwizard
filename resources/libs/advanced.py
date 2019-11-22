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
from resources.libs.gui import window


class Advanced:
    def __init__(self):
        self.dialog = xbmcgui.Dialog()

        self.categories = ['cache', 'network']
        self.tags = {}

    def show_menu(self, url=None):
        response = tools.open_url(CONFIG.ADVANCEDFILE)
        url_response = tools.open_url(url)

        if response:
            TEMPADVANCEDFILE = tools.read_from_file(os.path.join(CONFIG.ADDON_PATH, 'resources', 'text',
                                                                 'advanced.json'))  # url_response.text if url else response.text

            directory.add_file('Quick Configure advancedsettings.xml',
                               {'mode': 'advanced_settings', 'action': 'quick_configure'}, icon=CONFIG.ICONMAINT,
                               themeit=CONFIG.THEME3)

            if os.path.exists(CONFIG.ADVANCED):
                directory.add_file('View Current advancedsettings.xml',
                                   {'mode': 'advanced_settings', 'action': 'view_current'}, icon=CONFIG.ICONMAINT,
                                   themeit=CONFIG.THEME3)
                directory.add_file('Remove Current advancedsettings.xml',
                                   {'mode': 'advanced_settings', 'action': 'remove_current'}, icon=CONFIG.ICONMAINT,
                                   themeit=CONFIG.THEME3)

            if TEMPADVANCEDFILE:
                import json

                directory.add_separator(icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
                advanced_json = json.loads(TEMPADVANCEDFILE)

                presets = advanced_json['presets']
                if presets and len(presets) > 0:
                    for preset in presets:
                        name = preset.get('name', '')
                        section = preset.get('section', '')
                        preseturl = preset.get('url', '')
                        icon = preset.get('icon', '')
                        fanart = preset.get('fanart', '')
                        description = preset.get('description', '')

                        if section:
                            directory.add_dir(name, {'mode': 'advanced_settings', 'name': preseturl},
                                              description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
                        else:
                            directory.add_file(name,
                                               {'mode': 'advanced_settings', 'action': 'write_advanced', 'name': name,
                                                'url': preseturl},
                                               description=description, icon=icon, fanart=fanart, themeit=CONFIG.THEME2)
                else:
                    logging.log("[Advanced Settings] ERROR: Invalid Format for {0}.".format(CONFIG.ADVANCEDFILE))
            else:
                logging.log("[Advanced Settings] URL not working: {0}".format(CONFIG.ADVANCEDFILE))
        else:
            logging.log("[Advanced Settings] No Presets Available")

    def default_advanced(self):
        if CONFIG.RAM > 1536:
            buffer = '209715200'
        else:
            buffer = '104857600'
        with open(CONFIG.ADVANCED, 'w+') as f:
            f.write('<advancedsettings>\n')
            f.write('	<network>\n')
            f.write('		<buffermode>2</buffermode>\n')
            f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % buffer)
            f.write('		<readbufferfactor>5</readbufferfactor>\n')
            f.write('		<curlclienttimeout>10</curlclienttimeout>\n')
            f.write('		<curllowspeedtime>10</curllowspeedtime>\n')
            f.write('	</network>\n')
            f.write('</advancedsettings>\n')
        f.close()

    def quick_configure(self):
        from xml.etree import ElementTree

        exists = os.path.exists(CONFIG.ADVANCED)

        if exists:
            root = ElementTree.parse(CONFIG.ADVANCED).getroot()

            for category in root.findall('*'):
                name = category.tag
                values = {}

                for element in category.findall('*'):
                    values[element.tag] = element.text

                self.tags[name] = values

        for category in self.tags:
            directory.add_separator(middle=category.upper())

    def write_advanced(self, name, url):
        response = tools.open_url(url)

        if response:
            if os.path.exists(CONFIG.ADVANCED):
                choice = self.dialog.yesno(CONFIG.ADDONTITLE,
                                           "[COLOR {0}]Would you like to overwrite your current Advanced Settings with [COLOR {1}]{2}[/COLOR]?[/COLOR]".format(
                                               CONFIG.COLOR2, CONFIG.COLOR1, name),
                                           yeslabel="[B][COLOR springgreen]Overwrite[/COLOR][/B]",
                                           nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
            else:
                choice = self.dialog.yesno(CONFIG.ADDONTITLE,
                                           "[COLOR {0}]Would you like to download and install [COLOR {1}]{2}[/COLOR]?[/COLOR]".format(
                                               CONFIG.COLOR2, CONFIG.COLOR1, name),
                                           yeslabel="[B][COLOR springgreen]Install[/COLOR][/B]",
                                           nolabel="[B][COLOR red]Cancel[/COLOR][/B]")

            if choice == 1:
                tools.write_to_file(CONFIG.ADVANCED, response.text)
                self.dialog.ok(CONFIG.ADDONTITLE,
                               '[COLOR {0}]AdvancedSettings.xml file has been successfully written. Once you click okay it will force close kodi.[/COLOR]'.format(
                                   CONFIG.COLOR2))
                tools.kill_kodi(over=True)
            else:
                logging.log("[Advanced Settings] install canceled")
                logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                                   "[COLOR {0}]Write Cancelled![/COLOR]".format(CONFIG.COLOR2))
                return
        else:
            logging.log("[Advanced Settings] URL not working: {0}".format(url))
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]URL Not Working[/COLOR]".format(CONFIG.COLOR2))

    def view_current(self):
        window.show_text_box(CONFIG.ADDONTITLE, tools.read_from_file(CONFIG.ADVANCED).replace('\t', '    '))

    def remove_current(self):
        if os.path.exists(CONFIG.ADVANCED):
            tools.remove_file(CONFIG.ADVANCED)
        else:
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]AdvancedSettings.xml not found[/COLOR]".format(CONFIG.COLOR2))

