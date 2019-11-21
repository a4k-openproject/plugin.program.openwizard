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
import xbmcgui
import xbmcvfs

import os

try:  # Python 3
    from urllib.parse import quote_plus
    import zipfile
except ImportError:  # Python 2
    from urllib import quote_plus
    from resources.libs import zipfile

from resources.libs.common.config import CONFIG


class Restore:
    def __init__(self):
        from resources.libs.common import tools
        tools.ensure_folders()

        self.external = False
        self.location = 'Local'
        
    def _prompt_for_wipe(self):
        dialog = xbmcgui.Dialog()

        # Should we wipe first?
        wipe = dialog.yesno(CONFIG.ADDONTITLE,
                                           "[COLOR {0}]Do you wish to restore your".format(CONFIG.COLOR2),
                                           "Kodi configuration to default settings",
                                           "Before installing the {0} backup?[/COLOR]".format(self.location),
                                           nolabel='[B][COLOR red]No[/COLOR][/B]',
                                           yeslabel='[B][COLOR springgreen]Yes[/COLOR][/B]')
        if wipe:
            from resources.libs import install
            install.wipe()
        
    def binaries(self):
        from resources.libs import db
        from resources.libs import install
        from resources.libs.common import logging
        from resources.libs.common import tools
        
        dialog = xbmcgui.Dialog()
        binarytxt = os.path.join(CONFIG.USERDATA, 'build_binaries.txt')
        
        restore = False
        binaryids = []
        
        if os.path.exists(binarytxt):
            binaryids = tools.read_from_file(binarytxt).split(',')
            
            # dialog.ok(CONFIG.ADDONTITLE, '[COLOR {0}]The restored backup may depend on the following platform-specific addons, which were not included:[/COLOR]'.format(CONFIG.COLOR2), '[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, ', '.join([tools.get_addon_info(id, 'name') for id in binaryids])), '[COLOR {0}]For best results, consider installing them manually after Kodi restarts.[/COLOR]'.format(CONFIG.COLOR2))
            
            logging.log("[Binary Detection] Reinstalling Eligible Binary Addons")            
            dialog.ok(CONFIG.ADDONTITLE, '[COLOR {0}]The restored build contains platform-specific addons, which will now be automatically installed. A number of dialogs may pop up during this process. Cancelling them may cause the restored build to function incorrectly.[/COLOR]'.format(CONFIG.COLOR2))
            restore = True
        else:
            logging.log("[Binary Detection] No Eligible Binary Addons to Reinstall")
            return True
        
        if restore:       
            success = []
            fail = []
            
            if len(binaryids) == 0:
                logging.log('No addons selected for installation.')
                return
            
            # clear out the addons for sure
            # for id in binaryids:
                # if clear.remove_addon(id, tools.get_addon_info(id, 'name'), over=True, data=False):
                    # continue
                
            # finally, reinstall addons
            for id in binaryids:
                if install.install_from_kodi(id):
                    logging.log('{0} install succeeded.'.format(id))
                    success.append(id)
                else:
                    logging.log('{0} install failed.'.format(id))
                    fail.append(id)
                    
            if not fail:
                dialog.ok(CONFIG.ADDONTITLE, 'The selected addons were all installed successfully.')
                os.remove(binarytxt)
                return True
            else:
                dialog.ok(CONFIG.ADDONTITLE, 'The following addons failed to install:\n{0}'.format(', '.join(fail)))
                return False
        
    def _local(self, file, loc):
        display = os.path.split(file)
        filename = display[1]
        
        progress_dialog = xbmcgui.DialogProgress()

        try:
            zipfile.ZipFile(file, 'r')
        except:
            progress_dialog.update(0, '[COLOR {0}]Unable to read zipfile from current location.'.format(CONFIG.COLOR2),
                          'Copying file to packages')
            pack = os.path.join(CONFIG.PACKAGES, filename)
            xbmcvfs.copy(file, pack)
            file = xbmc.translatePath(pack)
            progress_dialog.update(0, '', 'Copying file to packages: Complete')
            zipfile.ZipFile(file, 'r')

        self._finish(file, loc, filename)

    def _external(self, source, loc):
        from resources.libs.downloader import Downloader
        
        progress_dialog = xbmcgui.DialogProgress()

        display = os.path.split(source)
        filename = display[1]

        file = os.path.join(CONFIG.PACKAGES, filename)
        Downloader().download(source, file)
        progress_dialog.update(0, 'Installing External Backup', '', 'Please Wait')

        self._finish(file, loc, filename)

    def _finish(self, file, loc, zname):
        from resources.libs import extract
        from resources.libs import db
        from resources.libs.common import tools

        dialog = xbmcgui.Dialog()
        progress_dialog = xbmcgui.DialogProgress()

        self._prompt_for_wipe()
        
        percent, errors, error = extract.all(file, loc)

        if int(errors) >= 1:
            if dialog.yesno(CONFIG.ADDONTITLE,
                                '[COLOR {0}][COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, zname),
                                'Completed: [COLOR {0}]{1}{2}[/COLOR] [Errors: [COLOR {3}]{4}[/COLOR]]'.format(CONFIG.COLOR1,
                                                                                                              percent, '%',
                                                                                                              CONFIG.COLOR1,
                                                                                                              errors),
                                'Would you like to view the errors?[/COLOR]',
                                nolabel='[B][COLOR red]No Thanks[/COLOR][/B]',
                                yeslabel='[B][COLOR springgreen]View Errors[/COLOR][/B]'):

                from resources.libs.gui import window
                window.show_text_box("Viewing Errors", error.replace('\t', ''))
        CONFIG.set_setting('installed', 'true')
        CONFIG.set_setting('extract', str(percent))
        CONFIG.set_setting('errors', str(errors))
        
        if self.external:
            try:
                os.remove(file)
            except:
                pass
                          
        # binaries_done = self._binaries()
        db.force_check_updates(over=True)
        
        # if not binaries_done:
            # dialog.ok(CONFIG.ADDONTITLE, '[COLOR {0}]There was an error while restoring. The build may not function correctly.[/COLOR]'.format(CONFIG.COLOR2))
            
        tools.kill_kodi(msg='[COLOR {0}]To save changes, Kodi needs to be force closed. Would you like to continue?[/COLOR]'.format(CONFIG.COLOR2))

    def _choose(self, loc):
        from resources.libs.common import logging
        from resources.libs import skin

        dialog = xbmcgui.Dialog()
        progress_dialog = xbmcgui.DialogProgress()
        
        skin.look_and_feel_data()

        if not self.external:
            file = dialog.browseSingle(1,
                                     '[COLOR {0}]Select the backup file you want to restore[/COLOR]'.format(
                                         CONFIG.COLOR2),
                                     'files', mask='.zip', useThumbs=True, defaultt=CONFIG.MYBUILDS)
            if not file.endswith('.zip'):
                logging.log_notify(CONFIG.ADDONTITLE,
                                   "[COLOR {0}]Local Restore: Cancelled[/COLOR]".format(CONFIG.COLOR2))
                return

            skin.skin_to_default("Restore")

            progress_dialog.create(CONFIG.ADDONTITLE, '[COLOR {0}]Installing Local Backup'.format(CONFIG.COLOR2), '',
                          'Please Wait[/COLOR]')

            self._local(file, loc)
        elif self.external:
            from resources.libs.common import tools

            source = dialog.browseSingle(1,
                                       '[COLOR {0}]Select the backup file you want to restore[/COLOR]'.format(
                                           CONFIG.COLOR2),
                                       '', mask='.zip', useThumbs=True)
            if not source.endswith('.zip'):
                logging.log_notify(CONFIG.ADDONTITLE,
                                   "[COLOR {0}]External Restore: Cancelled[/COLOR]".format(CONFIG.COLOR2))
                return

            response = tools.open_url(source, check=True)
            if not response:
                logging.log_notify(CONFIG.ADDONTITLE,
                                   "[COLOR {0}]External Restore: Invalid URL[/COLOR]".format(CONFIG.COLOR2))
                return

            skin.skin_to_default("Restore")

            self._external(source, loc)

    def _build(self):
        self._choose(CONFIG.HOME)

    def _guifix(self):
        self._choose(CONFIG.USERDATA)

    def _theme(self):
        self._choose(CONFIG.USERDATA)

    def _addonpack(self):
        self._choose(CONFIG.USERDATA)

    def _addondata(self):
        self._choose(CONFIG.ADDON_DATA)

    def restore(self, param, external=False):
        self.external = external
        self.location = 'Local' if not external else 'External'

        if param == 'build':
            self._build()
        elif param == 'guifix':
            self._guifix()
        elif param == 'theme':
            self._theme()
        elif param == 'addonpack':
            self._addonpack()
        elif param == 'addondata':
            self._addondata()
