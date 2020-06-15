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

import time
from datetime import datetime
from datetime import timedelta

import os
import sys

try:  # Python 3
    from urllib.parse import quote_plus
except ImportError:  # Python 2
    from urllib import quote_plus

from resources.libs.common.config import CONFIG
from resources.libs import clear
from resources.libs import check
from resources.libs import db
from resources.libs.gui import window
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs import skin
from resources.libs import update


def auto_install_repo():
    if not os.path.exists(os.path.join(CONFIG.ADDONS, CONFIG.REPOID)):
        response = tools.open_url(CONFIG.REPOADDONXML)

        if response:
            from xml.etree import ElementTree
            
            root = ElementTree.fromstring(response.text)
            repoaddon = root.findall('addon')
            repoversion = [tag.get('version') for tag in repoaddon if tag.get('id') == CONFIG.REPOID]
            
            if repoversion:
                installzip = '{0}-{1}.zip'.format(CONFIG.REPOID, repoversion[0])
                url = CONFIG.REPOZIPURL + installzip
                repo_response = tools.open_url(url, check=True)

                if repo_response:
                    progress_dialog = xbmcgui.DialogProgress()
                    
                    progress_dialog.create(CONFIG.ADDONTITLE, 'Downloading Repo...', '', 'Please Wait')
                    tools.ensure_folders(CONFIG.PACKAGES)
                    lib = os.path.join(CONFIG.PACKAGES, installzip)

                    # Remove the old zip if there is one
                    tools.remove_file(lib)

                    from resources.libs.downloader import Downloader
                    from resources.libs import extract
                    Downloader().download(url, lib)
                    extract.all(lib, CONFIG.ADDONS)

                    try:
                        repoxml = os.path.join(CONFIG.ADDONS, CONFIG.REPOID, 'addon.xml')
                        root = ElementTree.parse(repoxml).getroot()
                        reponame = root.get('name')
                        
                        logging.log_notify("{1}".format(CONFIG.COLOR1, reponame),
                                           "[COLOR {0}]Add-on updated[/COLOR]".format(CONFIG.COLOR2),
                                           icon=os.path.join(CONFIG.ADDONS, CONFIG.REPOID, 'icon.png'))
                                           
                    except Exception as e:
                        logging.log(str(e), level=xbmc.LOGERROR)

                    # Add wizard to add-on database
                    db.addon_database(CONFIG.REPOID, 1)

                    progress_dialog.close()
                    xbmc.sleep(500)

                    logging.log("[Auto Install Repo] Successfully Installed", level=xbmc.LOGNOTICE)
                else:
                    logging.log_notify("[COLOR {0}]Repo Install Error[/COLOR]".format(CONFIG.COLOR1),
                                       "[COLOR {0}]Invalid URL for zip![/COLOR]".format(CONFIG.COLOR2))
                    logging.log("[Auto Install Repo] Was unable to create a working URL for repository. {0}".format(
                        url), level=xbmc.LOGERROR)
            else:
                logging.log("Invalid URL for Repo zip", level=xbmc.LOGERROR)
        else:
            logging.log_notify("[COLOR {0}]Repo Install Error[/COLOR]".format(CONFIG.COLOR1),
                               "[COLOR {0}]Invalid addon.xml file![/COLOR]".format(CONFIG.COLOR2))
            logging.log("[Auto Install Repo] Unable to read the addon.xml file.", level=xbmc.LOGERROR)
    elif not CONFIG.AUTOINSTALL == 'Yes':
        logging.log("[Auto Install Repo] Not Enabled", level=xbmc.LOGNOTICE)
    elif os.path.exists(os.path.join(CONFIG.ADDONS, CONFIG.REPOID)):
        logging.log("[Auto Install Repo] Repository already installed")


def show_notification():
    note_id, msg = window.split_notify(CONFIG.NOTIFICATION)
    
    if note_id:
        if note_id == CONFIG.NOTEID:
            if CONFIG.NOTEDISMISS == 'false':
                window.show_notification(msg)
            else:
                logging.log('[Notifications] No new notifications.', level=xbmc.LOGNOTICE)
        elif note_id > CONFIG.NOTEID:
            logging.log('[Notifications] Showing notification {0}'
                        .format(note_id))
            CONFIG.set_setting('noteid', note_id)
            CONFIG.set_setting('notedismiss', 'false')
            window.show_notification(msg)
    else:
        logging.log('[Notifications] Notifications file at {0} not formatted correctly.'
                    .format(CONFIG.NOTIFICATION),
                    level=xbmc.LOGNOTICE)


def installed_build_check():
    dialog = xbmcgui.Dialog()

    if not CONFIG.EXTRACT == '100' and CONFIG.EXTERROR > 0:
        logging.log("[Build Installed Check] Build was extracted {0}/100 with [ERRORS: {1}]".format(CONFIG.EXTRACT,
                                                                                                    CONFIG.EXTERROR),
                    level=xbmc.LOGNOTICE)
        yes = dialog.yesno(CONFIG.ADDONTITLE,
                           '[COLOR {0}]{2}[/COLOR] [COLOR {1}]was not installed correctly![/COLOR]'.format(CONFIG.COLOR1,
                                                                                                   CONFIG.COLOR2,
                                                                                                   CONFIG.BUILDNAME),
                           ('Installed: [COLOR {0}]{1}[/COLOR] / '
                            'Error Count: [COLOR {2}]{3}[/COLOR]').format(CONFIG.COLOR1, CONFIG.EXTRACT, CONFIG.COLOR1,
                                                                          CONFIG.EXTERROR),
                           'Would you like to try again?[/COLOR]', nolabel='[B]No Thanks![/B]',
                           yeslabel='[B]Retry Install[/B]')
        CONFIG.clear_setting('build')
        if yes:
            xbmc.executebuiltin("PlayMedia(plugin://{0}/?mode=install&name={1}&url=fresh)".format(CONFIG.ADDON_ID,
                                                                                                  quote_plus(CONFIG.BUILDNAME)))
            logging.log("[Build Installed Check] Fresh Install Re-activated", level=xbmc.LOGNOTICE)
        else:
            logging.log("[Build Installed Check] Reinstall Ignored")
    elif CONFIG.SKIN in ['skin.confluence', 'skin.estuary', 'skin.estouchy']:
        logging.log("[Build Installed Check] Incorrect skin: {0}".format(CONFIG.SKIN), level=xbmc.LOGNOTICE)
        defaults = CONFIG.get_setting('defaultskin')
        if not defaults == '':
            if os.path.exists(os.path.join(CONFIG.ADDONS, defaults)):
                if skin.skin_to_default(defaults):
                    skin.look_and_feel_data('restore')
        if not CONFIG.SKIN == defaults and not CONFIG.BUILDNAME == "":
            gui_xml = check.check_build(CONFIG.BUILDNAME, 'gui')

            response = tools.open_url(gui_xml, check=True)
            if not response:
                logging.log("[Build Installed Check] Guifix was set to http://", level=xbmc.LOGNOTICE)
                dialog.ok(CONFIG.ADDONTITLE,
                          "[COLOR {0}]It looks like the skin settings was not applied to the build.".format(CONFIG.COLOR2),
                          "Sadly no gui fix was attached to the build",
                          "You will need to reinstall the build and make sure to do a force close[/COLOR]")
            else:
                yes = dialog.yesno(CONFIG.ADDONTITLE,
                                       '{0} was not installed correctly!'.format(CONFIG.BUILDNAME),
                                       'It looks like the skin settings was not applied to the build.',
                                       'Would you like to apply the GuiFix?',
                                       nolabel='[B]No, Cancel[/B]', yeslabel='[B]Apply Fix[/B]')
                if yes:
                    xbmc.executebuiltin("PlayMedia(plugin://{0}/?mode=install&name={1}&url=gui)".format(CONFIG.ADDON_ID,
                                                                                                        quote_plus(CONFIG.BUILDNAME)))
                    logging.log("[Build Installed Check] Guifix attempting to install")
                else:
                    logging.log('[Build Installed Check] Guifix url working but cancelled: {0}'.format(gui_xml),
                                level=xbmc.LOGNOTICE)
    else:
        logging.log('[Build Installed Check] Install seems to be completed correctly', level=xbmc.LOGNOTICE)
        
    if CONFIG.get_setting('installed') == 'true':
        if CONFIG.get_setting('keeptrakt') == 'true':
            from resources.libs import traktit
            logging.log('[Build Installed Check] Restoring Trakt Data', level=xbmc.LOGNOTICE)
            traktit.trakt_it('restore', 'all')
        if CONFIG.get_setting('keepdebrid') == 'true':
            from resources.libs import debridit
            logging.log('[Build Installed Check] Restoring Real Debrid Data', level=xbmc.LOGNOTICE)
            debridit.debrid_it('restore', 'all')
        if CONFIG.get_setting('keeplogin') == 'true':
            from resources.libs import loginit
            logging.log('[Build Installed Check] Restoring Login Data', level=xbmc.LOGNOTICE)
            loginit.login_it('restore', 'all')

        CONFIG.clear_setting('install')


def build_update_check():
    response = tools.open_url(CONFIG.BUILDFILE, check=True)

    if not response:
        logging.log("[Build Check] Not a valid URL for Build File: {0}".format(CONFIG.BUILDFILE), level=xbmc.LOGNOTICE)
    elif not CONFIG.BUILDNAME == '':
        if CONFIG.SKIN in ['skin.confluence', 'skin.estuary', 'skin.estouchy'] and not CONFIG.DEFAULTIGNORE == 'true':
            check.check_skin()

        logging.log("[Build Check] Build Installed: Checking Updates", level=xbmc.LOGNOTICE)
        check.check_build_update()

    CONFIG.set_setting('nextbuildcheck', tools.get_date(days=CONFIG.UPDATECHECK, formatted=True))


def save_trakt():
    current_time = time.mktime(time.strptime(tools.get_date(formatted=True), "%Y-%m-%d %H:%M:%S"))
    next_save = time.mktime(time.strptime(CONFIG.get_setting('traktnextsave'), "%Y-%m-%d %H:%M:%S"))
    
    if next_save <= current_time:
        from resources.libs import traktit
        logging.log("[Trakt Data] Saving all Data", level=xbmc.LOGNOTICE)
        traktit.auto_update('all')
        CONFIG.set_setting('traktnextsave', tools.get_date(days=3, formatted=True))
    else:
        logging.log("[Trakt Data] Next Auto Save isn't until: {0} / TODAY is: {1}".format(CONFIG.get_setting('traktnextsave'),
                                                                                          tools.get_date(formatted=True)),
                    level=xbmc.LOGNOTICE)


def save_debrid():
    current_time = time.mktime(time.strptime(tools.get_date(formatted=True), "%Y-%m-%d %H:%M:%S"))
    next_save = time.mktime(time.strptime(CONFIG.get_setting('debridnextsave'), "%Y-%m-%d %H:%M:%S"))
    
    if next_save <= current_time:
        from resources.libs import debridit
        logging.log("[Debrid Data] Saving all Data", level=xbmc.LOGNOTICE)
        debridit.auto_update('all')
        CONFIG.set_setting('debridnextsave', tools.get_date(days=3, formatted=True))
    else:
        logging.log("[Debrid Data] Next Auto Save isn't until: {0} / TODAY is: {1}".format(CONFIG.get_setting('debridnextsave'),
                                                                                           tools.get_date(formatted=True)),
                    level=xbmc.LOGNOTICE)


def save_login():
    current_time = time.mktime(time.strptime(tools.get_date(formatted=True), "%Y-%m-%d %H:%M:%S"))
    next_save = time.mktime(time.strptime(CONFIG.get_setting('loginnextsave'), "%Y-%m-%d %H:%M:%S"))
    
    if next_save <= current_time:
        from resources.libs import loginit
        logging.log("[Login Info] Saving all Data", level=xbmc.LOGNOTICE)
        loginit.auto_update('all')
        CONFIG.set_setting('loginnextsave', tools.get_date(days=3, formatted=True))
    else:
        logging.log("[Login Info] Next Auto Save isn't until: {0} / TODAY is: {1}".format(CONFIG.get_setting('loginnextsave'),
                                                                                          tools.get_date(formatted=True)),
                    level=xbmc.LOGNOTICE)


def auto_clean():
    service = False
    days = [tools.get_date(formatted=True), tools.get_date(days=1, formatted=True), tools.get_date(days=3, formatted=True), tools.get_date(days=7, formatted=True),
            tools.get_date(days=30, formatted=True)]

    freq = int(CONFIG.AUTOFREQ)
    next_cleanup = time.mktime(time.strptime(CONFIG.NEXTCLEANDATE, "%Y-%m-%d %H:%M:%S"))

    if next_cleanup <= tools.get_date() or freq == 0:
        service = True
        next_run = days[freq]
        CONFIG.set_setting('nextautocleanup', next_run)
    else:
        logging.log("[Auto Clean Up] Next Clean Up {0}".format(CONFIG.NEXTCLEANDATE),
                    level=xbmc.LOGNOTICE)
    if service:
        if CONFIG.AUTOCACHE == 'true':
            logging.log('[Auto Clean Up] Cache: On', level=xbmc.LOGNOTICE)
            clear.clear_cache(True)
        else:
            logging.log('[Auto Clean Up] Cache: Off', level=xbmc.LOGNOTICE)
        if CONFIG.AUTOTHUMBS == 'true':
            logging.log('[Auto Clean Up] Old Thumbs: On', level=xbmc.LOGNOTICE)
            clear.old_thumbs()
        else:
            logging.log('[Auto Clean Up] Old Thumbs: Off', level=xbmc.LOGNOTICE)
        if CONFIG.AUTOPACKAGES == 'true':
            logging.log('[Auto Clean Up] Packages: On', level=xbmc.LOGNOTICE)
            clear.clear_packages_startup()
        else:
            logging.log('[Auto Clean Up] Packages: Off', level=xbmc.LOGNOTICE)


def stop_if_duplicate():
    NOW = time.time()
    temp = CONFIG.get_setting('time_started')
    
    if temp:
        if temp > NOW - (60 * 2):
            logging.log('Killing Start Up Script')
            sys.exit()
            
    logging.log("{0}".format(NOW))
    CONFIG.set_setting('time_started', NOW)
    xbmc.sleep(1000)
    
    if not CONFIG.get_setting('time_started') == NOW:
        logging.log('Killing Start Up Script')
        sys.exit()
    else:
        logging.log('Continuing Start Up Script')


def check_for_video():
    while xbmc.Player().isPlayingVideo():
        xbmc.sleep(1000)


# Don't run the script while video is playing :)
check_for_video()
# Ensure that any needed folders are created
tools.ensure_folders()
# Stop this script if it's been run more than once
# if CONFIG.KODIV < 18:
    # stop_if_duplicate()
# Ensure that the wizard's name matches its folder
check.check_paths()


# FIRST RUN SETTINGS
if CONFIG.get_setting('first_install') == 'true':
    logging.log("[First Run] Showing Save Data Settings", level=xbmc.LOGNOTICE)
    window.show_save_data_settings()
else:
    logging.log("[First Run] Skipping Save Data Settings", level=xbmc.LOGNOTICE)

# BUILD INSTALL PROMPT
if tools.open_url(CONFIG.BUILDFILE, check=True) and CONFIG.get_setting('installed') == 'false':
    logging.log("[Current Build Check] Build Not Installed", level=xbmc.LOGNOTICE)
    window.show_build_prompt()
else:
    logging.log("[Current Build Check] Build Installed: {0}".format(CONFIG.BUILDNAME), level=xbmc.LOGNOTICE)
    
# BUILD UPDATE CHECK
buildcheck = CONFIG.get_setting('nextbuildcheck')
if CONFIG.get_setting('buildname'):
    current_time = time.time()
    epoch_check = time.mktime(time.strptime(buildcheck, "%Y-%m-%d %H:%M:%S"))
    
    if current_time >= epoch_check:
        logging.log("[Build Update Check] Started", level=xbmc.LOGNOTICE)
        build_update_check()
else:
    logging.log("[Build Update Check] Next Check: {0}".format(buildcheck), level=xbmc.LOGNOTICE)

# AUTO INSTALL REPO
if CONFIG.AUTOINSTALL == 'Yes':
    logging.log("[Auto Install Repo] Started", level=xbmc.LOGNOTICE)
    auto_install_repo()
else:
    logging.log("[Auto Install Repo] Not Enabled", level=xbmc.LOGNOTICE)

# REINSTALL ELIGIBLE BINARIES
binarytxt = os.path.join(CONFIG.USERDATA, 'build_binaries.txt')
if os.path.exists(binarytxt):
    logging.log("[Binary Detection] Reinstalling Eligible Binary Addons", level=xbmc.LOGNOTICE)
    from resources.libs import restore
    restore.restore('binaries')
else:
    logging.log("[Binary Detection] Eligible Binary Addons to Reinstall", level=xbmc.LOGNOTICE)
    
# AUTO UPDATE WIZARD
if CONFIG.AUTOUPDATE == 'Yes':
    logging.log("[Auto Update Wizard] Started", level=xbmc.LOGNOTICE)
    update.wizard_update()
else:
    logging.log("[Auto Update Wizard] Not Enabled", level=xbmc.LOGNOTICE)

# SHOW NOTIFICATIONS
if CONFIG.ENABLE_NOTIFICATION == 'Yes':
    show_notification()
else:
    logging.log('[Notifications] Not Enabled', level=xbmc.LOGNOTICE)

# INSTALLED BUILD CHECK
if CONFIG.get_setting('installed') == 'true':
    logging.log("[Build Installed Check] Started", level=xbmc.LOGNOTICE)
    installed_build_check()
else:
    logging.log("[Build Installed Check] Not Enabled", level=xbmc.LOGNOTICE)

# SAVE TRAKT
if CONFIG.get_setting('keeptrakt') == 'true':
    logging.log("[Trakt Data] Started", level=xbmc.LOGNOTICE)
    save_trakt()
else:
    logging.log("[Trakt Data] Not Enabled", level=xbmc.LOGNOTICE)

# SAVE DEBRID
if CONFIG.get_setting('keepdebrid') == 'true':
    logging.log("[Debrid Data] Started", level=xbmc.LOGNOTICE)
    save_debrid()
else:
    logging.log("[Debrid Data] Not Enabled", level=xbmc.LOGNOTICE)

# SAVE LOGIN
if CONFIG.get_setting('keeplogin') == 'true':
    logging.log("[Login Info] Started", level=xbmc.LOGNOTICE)
    save_login()
else:
    logging.log("[Login Info] Not Enabled", level=xbmc.LOGNOTICE)

# AUTO CLEAN
if CONFIG.get_setting('autoclean') == 'true':
    logging.log("[Auto Clean Up] Started", level=xbmc.LOGNOTICE)
    auto_clean()
else:
    logging.log('[Auto Clean Up] Not Enabled', level=xbmc.LOGNOTICE)

