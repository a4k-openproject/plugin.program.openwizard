import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import sys

try:  # Python 3
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    from urlparse import parse_qsl

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.gui import menu

advanced_settings_mode = 'advanced_settings'
addon_installer_mode = 'addons'


class Router:
    def __init__(self):
        self.route = None
        self.params = {}
        tools.ensure_folders()

    def _log_params(self, paramstring):
        _url = sys.argv[0]

        self.params = dict(parse_qsl(paramstring))

        logstring = '{0}: '.format(_url)
        for param in self.params:
            logstring += '[ {0}: {1} ] '.format(param, self.params[param])

        logging.log(logstring, level=xbmc.LOGDEBUG)

        return self.params

    def dispatch(self, handle, paramstring):
        self._log_params(paramstring)

        mode = self.params['mode'] if 'mode' in self.params else None
        url = self.params['url'] if 'url' in self.params else None
        name = self.params['name'] if 'name' in self.params else None
        action = self.params['action'] if 'action' in self.params else None

        # MAIN MENU
        if mode is None:
            from resources.libs.gui.main_menu import MainMenu
            MainMenu().get_listing()
            self._finish(handle)

        # SETTINGS
        elif mode == 'settings':  # OpenWizard settings
            CONFIG.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'opensettings':  # Open other addons' settings
            settings_id = eval(url.upper() + 'ID')[name]['plugin']
            CONFIG.open_settings(settings_id)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'togglesetting':  # Toggle a setting
            CONFIG.set_setting(name, 'false' if CONFIG.get_setting(name) == 'true' else 'true')
            xbmc.executebuiltin('Container.Refresh()')

        # MENU SECTIONS
        elif mode == 'builds':  # Builds
            from resources.libs.gui.build_menu import BuildMenu
            BuildMenu().get_listing()
            self._finish(handle)
        elif mode == 'viewbuild':  # Builds -> "Your Build"
            from resources.libs.gui.build_menu import BuildMenu
            BuildMenu().view_build(name)
            self._finish(handle)
        elif mode == 'buildinfo':  # Builds -> Build Info
            from resources.libs.gui.build_menu import BuildMenu
            BuildMenu().build_info(name)
        elif mode == 'buildpreview':  # Builds -> Build Preview
            from resources.libs.gui.build_menu import BuildMenu
            BuildMenu().build_video(name)
        elif mode == 'install':  # Builds -> Fresh Install/Standard Install/Apply guifix
            from resources.libs.wizard import Wizard

            if action == 'build':
                Wizard().build(name)
            elif action == 'gui':
                Wizard().gui(name)
            elif action == 'theme':  # Builds -> "Your Build" -> "Your Theme"
                Wizard().theme(name, url)

        elif mode == 'maint':  # Maintenance + Maintenance -> any "Tools" section
            from resources.libs.gui.maintenance_menu import MaintenanceMenu

            if name == 'clean':
                MaintenanceMenu().clean_menu()
            elif name == 'addon':
                MaintenanceMenu().addon_menu()
            elif name == 'misc':
                MaintenanceMenu().misc_menu()
            elif name == 'backup':
                MaintenanceMenu().backup_menu()
            elif name == 'tweaks':
                MaintenanceMenu().tweaks_menu()
            elif name == 'logging':
                MaintenanceMenu().logging_menu()
            elif name is None:
                MaintenanceMenu().get_listing()
                
            self._finish(handle)

        elif mode == 'enableaddons':  # Maintenance - > Addon Tools -> Enable/Disable Addons
            menu.enable_addons()
            self._finish(handle)
        elif mode == 'enableall':
            menu.enable_addons(all=True)
        elif mode == 'toggleaddon':
            from resources.libs import db
            db.toggle_addon(name, url)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'forceupdate':
            from resources.libs import db
            db.force_check_updates(auto=action)
        elif mode == 'togglecache':
            from resources.libs import clear
            clear.toggle_cache(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'changefreq':  # Maintenance - Auto Clean Frequency
            menu.change_freq()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'systeminfo':  # Maintenance -> System Tweaks/Fixes -> System Information
            menu.system_info()
            self._finish(handle)
        elif mode == 'nettools':  # Maintenance -> Misc Maintenance -> Network Tools
            menu.net_tools()
            self._finish(handle)
        elif mode == 'runspeedtest':  # Maintenance -> Misc Maintenance -> Network Tools -> Speed Test -> Run Speed Test
            menu.run_speed_test()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'clearspeedtest':  # Maintenance -> Misc Maintenance -> Network Tools -> Speed Test -> Clear Results
            menu.clear_speed_test()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'viewspeedtest':  # Maintenance -> Misc Maintenance -> Network Tools -> Speed Test -> any previous test
            menu.view_speed_test(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'viewIP':  # Maintenance -> Misc Maintenance -> Network Tools -> View IP Address & MAC Address
            menu.view_ip()
            self._finish(handle)
        elif mode == 'speedtest': 
            xbmc.executebuiltin('InstallAddon("script.speedtester")')
            xbmc.executebuiltin('RunAddon("script.speedtester")')
        elif mode == 'apk':  # APK Installer
            menu.apk_menu(url)
            self._finish(handle)
        elif mode == 'kodiapk':  # APK Installer -> Official Kodi APK's
            xbmc.executebuiltin('RunScript(script.kodi.android.update)')
        elif mode == 'fmchoose':
            from resources.libs import install
            install.choose_file_manager()
        elif mode == 'apkinstall':
            from resources.libs import install
            install.install_apk(name, url)
        elif mode == 'removeaddondata':  # Maintenance - > Addon Tools -> Remove Addon Data
            menu.remove_addon_data_menu()
            self._finish(handle)
        elif mode == 'savedata':  # Save Data + Builds -> Save Data Menu
            menu.save_menu()
            self._finish(handle)
        elif mode == 'youtube':  # "YouTube Section"
            menu.youtube_menu(url)
            self._finish(handle)
        elif mode == 'viewVideo':  # View  Video
            from resources.libs import yt
            yt.play_video(url)
        elif mode == 'trakt':  # Save Data -> Keep Trakt Data
            menu.trakt_menu()
            self._finish(handle)
        elif mode == 'realdebrid':  # Save Data -> Keep Debrid
            menu.debrid_menu()
            self._finish(handle)
        elif mode == 'login':  # Save Data -> Keep Login Info
            menu.login_menu()
            self._finish(handle)
        elif mode == 'developer':  # Developer  Menu
            menu.developer()
            self._finish(handle)

        # MAINTENANCE FUNCTIONS
        elif mode == 'kodi17fix':  # Misc Maintenance -> Kodi 17 Fix
            from resources.libs import db
            db.kodi_17_fix()
        elif mode == 'unknownsources':  # Misc Maintenance -> Enable Unknown Sources
            from resources.libs import skin
            skin.swap_us()
        elif mode == 'enabledebug':  # Misc Maintenance -> Enable Debug Logging
            logging.swap_debug()
        elif mode == 'toggleupdates':  # Misc Maintenance -> Toggle Addon Updates
            from resources.libs import update
            update.toggle_addon_updates()
        elif mode == 'asciicheck':  # System Tweaks -> Scan for Non-Ascii Files
            from resources.libs.common import tools
            tools.ascii_check()
        elif mode == 'convertpath':  # System Tweaks -> Convert Special Paths
            from resources.libs.common import tools
            tools.convert_special(CONFIG.HOME)
        elif mode == 'forceprofile':  # Misc Maintenance -> Reload Profile
            from resources.libs.common import tools
            tools.reload_profile(tools.get_info_label('System.ProfileName'))
        elif mode == 'forceclose':  # Misc Maintenance -> Force Close Kodi
            from resources.libs.common import tools
            tools.kill_kodi()
        elif mode == 'forceskin':  # Misc Maintenance -> Reload Skin
            xbmc.executebuiltin("ReloadSkin()")
            xbmc.executebuiltin('Container.Refresh()')
        # elif mode == 'hidepassword':  # Addon Tools -> Hide Passwords on Keyboard Entry
        #     from resources.libs import db
        #     db.hide_password()
        # elif mode == 'unhidepassword':  # Addon Tools -> Unhide Passwords on Keyboard Entry
        #     from resources.libs import db
        #     db.unhide_password()
        elif mode == 'checksources':  # System Tweaks -> Scan source for broken links
            from resources.libs import check
            check.check_sources()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'checkrepos':  # System Tweaks -> Scan for broken repositories
            from resources.libs import check
            check.check_repos()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'whitelist':  # Whitelist Functions
            from resources.libs import whitelist
            whitelist.whitelist(name)

        #  CLEANING
        elif mode == 'oldThumbs':  # Cleaning Tools -> Clear Old Thumbnails
            from resources.libs import clear
            clear.old_thumbs()
        elif mode == 'clearbackup':  # Backup/Restore -> Clean Up Back Up Folder
            from resources.libs import backup
            backup.cleanup_backup()
        elif mode == 'fullclean':  # Cleaning Tools -> Total Cleanup
            from resources.libs import clear
            clear.total_clean()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'clearcache':  # Cleaning Tools -> Clear Cache
            from resources.libs import clear
            clear.clear_cache()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'clearfunctioncache':  # Cleaning Tools -> Clear Function Caches
            from resources.libs import clear
            clear.clear_function_cache()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'clearpackages':  # Cleaning Tools -> Clear Packages
            from resources.libs import clear
            clear.clear_packages()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'clearcrash':  # Cleaning Tools -> Clear Crash Logs
            from resources.libs import clear
            clear.clear_crash()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'clearthumb':  # Cleaning Tools -> Clear Thumbnails
            from resources.libs import clear
            clear.clear_thumbs()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'cleararchive':  # Cleaning Tools -> Clear Archive Cache
            from resources.libs import clear
            clear.clear_archive()
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'freshstart':  # Cleaning Tools -> Fresh Start
            from resources.libs import install
            install.fresh_start()
        elif mode == 'purgedb':  # Cleaning Tools -> Purge Databases
            from resources.libs import db
            db.purge_db()
        elif mode == 'removeaddons':  # Addon Tools -> Remove Addons
            from resources.libs import clear
            clear.remove_addon_menu()
        elif mode == 'removedata':  # Addon Tools -> Remove Addon Data
            from resources.libs import clear
            clear.remove_addon_data(name)
        elif mode == 'resetaddon':  # Addon Tools -> Remove Addon Data -> Remove  Wizard Addon Data
            from resources.libs.common import tools

            tools.clean_house(CONFIG.ADDON_DATA, ignore=True)
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]Addon_Data reset[/COLOR]".format(CONFIG.COLOR2))
        # BACKUP / RESTORE
        elif mode == 'backup' and action:
            from resources.libs import backup
            backup.backup(action)
        elif mode == 'restore' and action:
            from resources.libs import restore
            restore.restore(action, external=name == 'external')

        elif mode == 'wizardupdate':  # Wizard Update
            from resources.libs import update
            update.wizard_update()

        # LOGGING
        elif mode == 'uploadlog':  # Upload Log File
            logging.upload_log()
        elif mode == 'viewlog':  # View kodi.log
            logging.view_log_file()
        elif mode == 'viewwizlog':  # View wizard.log
            from resources.libs.gui import window
            window.show_log_viewer(log_file=CONFIG.WIZLOG)
        elif mode == 'viewerrorlog':  # View errors in log
            logging.error_checking()
        elif mode == 'viewerrorlast':  # View last error in log
            logging.error_checking(last=True)
        elif mode == 'clearwizlog':  # Clear wizard.log
            from resources.libs.common import tools
            tools.remove_file(CONFIG.WIZLOG)
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]Wizard Log Cleared![/COLOR]".format(CONFIG.COLOR2))

        # ADVANCED SETTINGS
        elif mode == advanced_settings_mode:
            from resources.libs import advanced

            self.route = advanced.AdvancedMenu()
            advanced_settings_actions = ['quick_configure', 'view_current', 'remove_current', 'write_advanced', 'set_setting', 'show_section']

            category = self.params['category'] if 'category' in self.params else None
            tag = self.params['tag'] if 'tag' in self.params else None
            value = self.params['value'] if 'value' in self.params else None
            tags = self.params['tags'] if 'tags' in self.params else None

            if not action:
                self.route.show_menu(url=url)
                self._finish(handle)
            elif action == advanced_settings_actions[0]:  # Advanced Settings Quick Configure
                self.route.quick_configure()
                self._finish(handle)
            elif action == advanced_settings_actions[1]:  # View Current Advanced Settings
                advanced.view_current()
            elif action == advanced_settings_actions[2]:  # Remove Current Advanced Settings
                advanced.remove_current()
            elif action == advanced_settings_actions[3] and url:  # Write New Advanced Settings
                self.route.write_advanced(name, url)
            elif action == advanced_settings_actions[4]:  # Set a Setting
                self.route.set_setting(category, tag, value)
            elif action == advanced_settings_actions[5]:  # Open a Section
                self.route.show_section(tags)
                self._finish(handle)
                
        # ADDON INSTALLER
        elif mode == addon_installer_mode:
            from resources.libs.gui import addon_menu
            
            self.route = addon_menu.AddonMenu()
            addon_installer_actions = ['addon', 'skin', 'addonpack']

            addonurl = self.params['addonurl'] if 'addonurl' in self.params else None
            repository = self.params['repository'] if 'repository' in self.params else None
            repositoryurl = self.params['repositoryurl'] if 'repositoryurl' in self.params else None
            repositoryxml = self.params['repositoryxml'] if 'repositoryxml' in self.params else None
            urls = [addonurl, repository, repositoryurl, repositoryxml]
            
            if not action:
                self.route.show_menu(url=url)
                self._finish(handle)
            elif action == addon_installer_actions[0]:
                self.route.install_addon(name, urls)
            elif action == addon_installer_actions[1]:
                pass
                # self.route.install_skin(name, url)
            elif action == addon_installer_actions[2]:
                pass
                # self.route.install_addon_pack(name, url)
            
        # SAVE DATA
        elif mode == 'managedata':
            from resources.libs import save

            if name == 'import':
                save.import_save_data()
            elif name == 'export':
                save.export_save_data()

        # TRAKT
        elif mode == 'savetrakt':  # Save Trakt Data
            from resources.libs import traktit
            traktit.trakt_it('update', name)
        elif mode == 'restoretrakt':  # Recover All Saved Trakt Data
            from resources.libs import traktit
            traktit.trakt_it('restore', name)
        elif mode == 'addontrakt':  # Clear All Addon Trakt Data
            from resources.libs import traktit
            traktit.trakt_it('clearaddon', name)
        elif mode == 'cleartrakt':  # Clear All Saved Trakt Data
            from resources.libs import traktit
            traktit.clear_saved(name)
        elif mode == 'authtrakt':  # Authorize Trakt
            from resources.libs import traktit
            traktit.activate_trakt(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatetrakt':  # Update Saved Trakt Data
            from resources.libs import traktit
            traktit.auto_update('all')
        elif mode == 'importtrakt':  # Import Saved Trakt Data
            from resources.libs import traktit
            traktit.import_list(name)
            xbmc.executebuiltin('Container.Refresh()')

        # DEBRID
        elif mode == 'savedebrid':  # Save Debrid Data
            from resources.libs import debridit
            debridit.debrid_it('update', name)
        elif mode == 'restoredebrid':  # Recover All Saved Debrid Data
            from resources.libs import debridit
            debridit.debrid_it('restore', name)
        elif mode == 'addondebrid':  # Clear All Addon Debrid Data
            from resources.libs import debridit
            debridit.debrid_it('clearaddon', name)
        elif mode == 'cleardebrid':  # Clear All Saved Debrid Data
            from resources.libs import debridit
            debridit.clear_saved(name)
        elif mode == 'authdebrid':  # Authorize Debrid
            from resources.libs import debridit
            debridit.activate_debrid(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatedebrid':  # Update Saved Debrid Data
            from resources.libs import debridit
            debridit.auto_update('all')
        elif mode == 'importdebrid':  # Import Saved Debrid Data
            from resources.libs import debridit
            debridit.import_list(name)
            xbmc.executebuiltin('Container.Refresh()')

        # LOGIN
        elif mode == 'savelogin':  # Save Login Data
            from resources.libs import loginit
            loginit.login_it('update', name)
        elif mode == 'restorelogin':  # Recover All Saved Login Data
            from resources.libs import loginit
            loginit.login_it('restore', name)
        elif mode == 'addonlogin':  # Clear All Addon Login Data
            from resources.libs import loginit
            loginit.login_it('clearaddon', name)
        elif mode == 'clearlogin':  # Clear All Saved Login Data
            from resources.libs import loginit
            loginit.clear_saved(name)
        elif mode == 'authlogin':  # "Authorize" Login
            from resources.libs import loginit
            loginit.activate_login(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatelogin':  # Update Saved Login Data
            from resources.libs import loginit
            loginit.auto_update('all')
        elif mode == 'importlogin':  # Import Saved Login Data
            from resources.libs import loginit
            loginit.import_list(name)
            xbmc.executebuiltin('Container.Refresh()')

        # DEVELOPER MENU
        elif mode == 'createqr':  # Developer Menu -> Create QR Code
            from resources.libs import qr
            qr.create_code()
        elif mode == 'testnotify':  # Developer Menu -> Test Notify
            from resources.libs import test
            test.test_notify()
        elif mode == 'testupdate':  # Developer Menu -> Test Update
            from resources.libs import test
            test.test_update()
        elif mode == 'testsavedata':  # Developer Menu -> Test Save Data Settings
            from resources.libs import test
            test.test_save_data_settings()
        elif mode == 'testbuildprompt':  # Developer Menu -> Test Build Prompt
            from resources.libs import test
            test.test_first_run()
        elif mode == 'binarycheck':
            from resources.libs import db
            db.find_binary_addons()
        elif mode == 'contact':  # Contact
            from resources.libs.gui import window
            window.show_contact(CONFIG.CONTACT)
        
    def _finish(self, handle):
        from resources.libs.common import directory
        
        directory.set_view()
        
        xbmcplugin.setContent(handle, 'files')
        xbmcplugin.endOfDirectory(handle)                       
