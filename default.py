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
import xbmcplugin

import sys

try:  # Python 3
    from urllib.parse import unquote_plus
except ImportError:  # Python 2
    from urllib import unquote_plus

from resources.libs.config import CONFIG
from resources.libs import logging


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params)-1] == '/':
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if len(splitparams) == 2:
                param[splitparams[0]] = splitparams[1]

        return param


params = get_params()
url = None
name = None
mode = None

try:
    mode = unquote_plus(params["mode"])
except:
    pass
try:
    name = unquote_plus(params["name"])
except:
    pass
try:
    url = unquote_plus(params["url"])
except:
    pass

logging.log('[ Version : \'{0}\' ] [ Mode : \'{1}\' ] [ Name : \'{2}\' ] [ Url : \'{3}\' ]'.format(CONFIG.ADDON_VERSION, mode if not mode == '' else None, name, url))

if not mode:
    from resources.libs import menu
    menu.main_menu()

elif mode == 'wizardupdate':
    from resources.libs import update
    update.wizard_update()
elif mode == 'builds':
    from resources.libs import menu
    menu.build_menu()
elif mode == 'viewbuild':
    from resources.libs import menu
    menu.view_build(name)
elif mode == 'buildinfo':
    from resources.libs import check
    check.build_info(name)
elif mode == 'buildpreview':
    from resources.libs import yt
    yt.build_video(name)
elif mode == 'install':
    from resources.libs import menu
    menu.wizard_menu(name, url)
elif mode == 'theme':
    from resources.libs import menu
    menu.wizard_menu(name, mode, url)
elif mode == 'maint':
    from resources.libs import menu
    menu.maint_menu(name)
elif mode == 'kodi17fix':
    from resources.libs import db
    db.kodi_17_fix()
elif mode == 'unknownsources':
    from resources.libs import skin
    skin.swap_us()
elif mode == 'advancedsetting':
    from resources.libs import menu
    menu.advanced_window(name)
elif mode == 'autoadvanced':
    from resources.libs import advanced
    advanced.autoConfig()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'removeadvanced':
    from resources.libs import advanced
    advanced.remove_advanced()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'asciicheck':
     from resources.libs import tools
     tools.ascii_check()
elif mode == 'backupbuild':
    from resources.libs import backup
    backup.backup('build')
elif mode == 'backupgui':
    from resources.libs import backup
    backup.backup('guifix')
elif mode == 'backuptheme':
    from resources.libs import backup
    backup.backup('theme')
elif mode == 'backupaddonpack':
    from resources.libs import backup
    backup.backup('addon pack')
elif mode == 'backupaddon':
    from resources.libs import backup
    backup.backup('addon_data')
elif mode == 'oldThumbs':
    from resources.libs import clear
    clear.old_thumbs()
elif mode == 'clearbackup':
    from resources.libs import backup
    backup.cleanup_backup()
elif mode == 'convertpath':
    from resources.libs import tools
    tools.convert_special(CONFIG.HOME)
elif mode == 'currentsettings':
    from resources.libs import advanced
    advanced.view_advanced()
elif mode == 'fullclean':
    from resources.libs import clear
    clear.total_clean()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'clearcache':
    from resources.libs import clear
    clear.clear_cache()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'clearfunctioncache':
    from resources.libs import clear
    clear.clear_function_cache()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'clearpackages':
    from resources.libs import clear
    clear.clear_packages()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'clearcrash':
    from resources.libs import clear
    clear.clear_crash()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'clearthumb':
    from resources.libs import clear
    clear.clear_thumbs()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'cleararchive':
    from resources.libs import clear
    clear.clear_archive()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'checksources':
    from resources.libs import check
    check.check_sources()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'checkrepos':
    from resources.libs import check
    check.check_repos()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'freshstart':
    from resources.libs import install
    install.fresh_start()
elif mode == 'forceupdate':
    from resources.libs import update
    update.force_update()
elif mode == 'forceprofile':
    from resources.libs import tools
    tools.reload_profile(tools.get_info_label('System.ProfileName'))
elif mode == 'forceclose':
    from resources.libs import tools
    tools.kill_kodi()
elif mode == 'forceskin':
    xbmc.executebuiltin("ReloadSkin()")
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'hidepassword':
    from resources.libs import db
    db.hide_password()
elif mode == 'unhidepassword':
    from resources.libs import db
    db.unhide_password()
elif mode == 'enableaddons':
    from resources.libs import menu
    menu.enable_addons()
elif mode == 'toggleaddon':
    from resources.libs import db
    db.toggle_addon(name, url)
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'togglecache':
    from resources.libs import clear
    clear.toggle_cache(name)
    xbmc.executebuiltin('Container.Refresh()')
# elif mode == 'toggleadult':
#     from resources.libs import db
#     db.toggle_adult()
#     xbmc.executebuiltin('Container.Refresh()')
elif mode == 'changefeq':
    from resources.libs import menu
    menu.change_freq()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'uploadlog':
    logging.upload_log()
elif mode == 'viewlog':
    from resources.libs import gui
    gui.show_log_viewer()
elif mode == 'viewwizlog':
    from resources.libs import gui
    gui.show_log_viewer(CONFIG.WIZLOG)
elif mode == 'viewerrorlog':
    logging.error_checking()
elif mode == 'viewerrorlast':
    logging.error_checking(last=True)
elif mode == 'clearwizlog':
    from resources.libs import tools
    tools.remove_file(CONFIG.WIZLOG)
    logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                       "[COLOR {0}]Wizard Log Cleared![/COLOR]".format(CONFIG.COLOR2))
elif mode == 'purgedb':
    from resources.libs import db
    db.purge_db()
elif mode == 'fixaddonupdate':
    from resources.libs import db
    db.fix_update()
elif mode == 'removeaddons':
    from resources.libs import clear
    clear.remove_addon_menu()
elif mode == 'removeaddon':
    from resources.libs import clear
    clear.remove_addon(name)
elif mode == 'removeaddondata':
    from resources.libs import menu
    menu.remove_addon_data_menu()
elif mode == 'removedata':
    from resources.libs import clear
    clear.remove_addon_data(name)
elif mode == 'resetaddon':
    from resources.libs import tools
    total = tools.clean_house(CONFIG.ADDON_DATA, ignore=True)
    logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                       "[COLOR {0}]Addon_Data reset[/COLOR]".format(CONFIG.COLOR2))
elif mode == 'systeminfo':
    from resources.libs import menu
    menu.system_info()
elif mode == 'restorezip':
    from resources.libs import backup
    backup.restore_it('build')
elif mode == 'restoregui':
    from resources.libs import backup
    backup.restore_it('gui')
elif mode == 'restoreaddon':
    from resources.libs import backup
    backup.restore_it('addondata')
elif mode == 'restoreextzip':
    from resources.libs import backup
    backup.restore_it_external('build')
elif mode == 'restoreextgui':
    from resources.libs import backup
    backup.restore_it_external('gui')
elif mode == 'restoreextaddon':
    from resources.libs import backup
    backup.restore_it_external('addondata')
elif mode == 'writeadvanced':
    from resources.libs import advanced
    advanced.write_advanced(name, url)
elif mode == 'speedtest':
    from resources.libs import menu
    menu.net_tools()
elif mode == 'runspeedtest':
    from resources.libs import menu
    menu.run_speed_test()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'clearspeedtest':
    from resources.libs import menu
    menu.clear_speed_test()
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'viewspeedtest':
    from resources.libs import menu
    menu.view_speed_test(name)
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'viewIP':
    from resources.libs import menu
    menu.view_ip()

elif mode == 'speedtestM':
    from resources.libs import menu
    menu.speed_test()

elif mode == 'apk':
    from resources.libs import menu
    menu.apk_menu(name, url)
elif mode == 'apkscrape':
    from resources.libs import menu
    menu.apk_scraper(name)
elif mode == 'apkinstall':
    from resources.libs import install
    install.install_apk(name, url)

elif mode == 'youtube':
    from resources.libs import menu
    menu.youtube_menu(name, url)
elif mode == 'viewVideo':
    from resources.libs import yt
    yt.play_video(url)

elif mode == 'addons':
    from resources.libs import menu
    menu.addon_menu(name, url)
elif mode == 'addonpack':
    from resources.libs import install
    install.install_addon_pack(name, url)
elif mode == 'skinpack':
    from resources.libs import install
    install.install_skin(name, url)
elif mode == 'addoninstall':
    from resources.libs import install
    install.install_addon(name, url)

elif mode == 'savedata':
    from resources.libs import menu
    menu.save_menu()
elif mode == 'togglesetting':
    CONFIG.set_setting(name, 'false' if CONFIG.get_setting(name) == 'true' else 'true')
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'whitelist':
    from resources.libs import whitelist
    whitelist.whitelist(name)

elif mode == 'trakt':
    from resources.libs import menu
    menu.trakt_menu()
elif mode == 'savetrakt':
    from resources.libs import traktit
    traktit.trakt_it('update', name)
elif mode == 'restoretrakt':
    from resources.libs import traktit
    traktit.trakt_it('restore', name)
elif mode == 'addontrakt':
    from resources.libs import traktit
    traktit.trakt_it('clearaddon', name)
elif mode == 'cleartrakt':
    from resources.libs import traktit
    traktit.clear_saved(name)
elif mode == 'authtrakt':
    from resources.libs import traktit
    traktit.activate_trakt(name)
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'updatetrakt':
    from resources.libs import traktit
    traktit.auto_update('all')
elif mode == 'importtrakt':
    from resources.libs import traktit
    traktit.import_list(name)
    xbmc.executebuiltin('Container.Refresh()')

elif mode == 'realdebrid':
    from resources.libs import menu
    menu.debrid_menu()
elif mode == 'savedebrid':
    from resources.libs import debridit
    debridit.debrid_it('update', name)
elif mode == 'restoredebrid':
    from resources.libs import debridit
    debridit.debrid_it('restore', name)
elif mode == 'addondebrid':
    from resources.libs import debridit
    debridit.debrid_it('clearaddon', name)
elif mode == 'cleardebrid':
    from resources.libs import debridit
    debridit.clear_saved(name)
elif mode == 'authdebrid':
    from resources.libs import debridit
    debridit.activate_debrid(name)
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'updatedebrid':
    from resources.libs import debridit
    debridit.auto_update('all')
elif mode == 'importdebrid':
    from resources.libs import debridit
    debridit.import_list(name)
    xbmc.executebuiltin('Container.Refresh()')

elif mode == 'login':
    from resources.libs import menu
    menu.login_menu()
elif mode == 'savelogin':
    from resources.libs import loginit
    loginit.login_it('update', name)
elif mode == 'restorelogin':
    from resources.libs import loginit
    loginit.login_it('restore', name)
elif mode == 'addonlogin':
    from resources.libs import loginit
    loginit.login_it('clearaddon', name)
elif mode == 'clearlogin':
    from resources.libs import loginit
    loginit.clear_saved(name)
elif mode == 'authlogin':
    from resources.libs import loginit
    loginit.activate_login(name)
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'updatelogin':
    from resources.libs import loginit
    loginit.auto_update('all')
elif mode == 'importlogin':
    from resources.libs import loginit
    loginit.import_list(name)
    xbmc.executebuiltin('Container.Refresh()')

elif mode == 'contact':
    from resources.libs import gui
    gui.show_contact(CONFIG.CONTACT)
elif mode == 'settings':
    CONFIG.open_settings(name)
    xbmc.executebuiltin('Container.Refresh()')
elif mode == 'forcetext':
    from resources.libs import clear
    clear.force_text()
elif mode == 'opensettings':
    id = eval(url.upper()+'ID')[name]['plugin']
    CONFIG.open_settings(id)
    xbmc.executebuiltin('Container.Refresh()')

elif mode == 'developer':
    from resources.libs import menu
    menu.developer()
elif mode == 'createqr':
    from resources.libs import qr
    qr.create_code()
elif mode == 'testnotify':
    from resources.libs import test
    test.test_notify()
elif mode == 'testupdate':
    from resources.libs import test
    test.test_update()
elif mode == 'testfirst':
    from resources.libs import test
    test.test_save_data_settings()
elif mode == 'testfirstrun':
    from resources.libs import test
    test.test_first_run()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
