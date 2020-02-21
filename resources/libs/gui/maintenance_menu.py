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

import os

from resources.libs.common import directory
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common.config import CONFIG


class MaintenanceMenu:

    def get_listing(self):
        directory.add_dir('[B]Cleaning Tools[/B]', {'mode': 'maint', 'name': 'clean'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]Addon Tools[/B]', {'mode': 'maint', 'name': 'addon'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]Logging Tools[/B]', {'mode': 'maint', 'name': 'logging'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]Misc Maintenance[/B]', {'mode': 'maint', 'name': 'misc'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]Back up/Restore[/B]', {'mode': 'maint', 'name': 'backup'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_dir('[B]System Tweaks/Fixes[/B]', {'mode': 'maint', 'name': 'tweaks'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)

    def clean_menu(self):
        from resources.libs import clear
        from resources.libs.common import tools

        on = '[B][COLOR springgreen]ON[/COLOR][/B]'
        off = '[B][COLOR red]OFF[/COLOR][/B]'

        autoclean = 'true' if CONFIG.AUTOCLEANUP == 'true' else 'false'
        cache = 'true' if CONFIG.AUTOCACHE == 'true' else 'false'
        packages = 'true' if CONFIG.AUTOPACKAGES == 'true' else 'false'
        thumbs = 'true' if CONFIG.AUTOTHUMBS == 'true' else 'false'
        includevid = 'true' if CONFIG.INCLUDEVIDEO == 'true' else 'false'
        includeall = 'true' if CONFIG.INCLUDEALL == 'true' else 'false'

        sizepack = tools.get_size(CONFIG.PACKAGES)
        sizethumb = tools.get_size(CONFIG.THUMBNAILS)
        archive = tools.get_size(CONFIG.ARCHIVE_CACHE)
        sizecache = (clear.get_cache_size()) - archive
        totalsize = sizepack + sizethumb + sizecache

        directory.add_file(
            'Total Clean Up: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(totalsize)), {'mode': 'fullclean'},
            icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Clear Cache: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizecache)),
                           {'mode': 'clearcache'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)') or xbmc.getCondVisibility(
                'System.HasAddon(script.module.resolveurl)'):
            directory.add_file('Clear Resolver Function Caches', {'mode': 'clearfunctioncache'}, icon=CONFIG.ICONMAINT,
                               themeit=CONFIG.THEME3)
        directory.add_file('Clear Packages: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizepack)),
                           {'mode': 'clearpackages'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file(
            'Clear Thumbnails: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(tools.convert_size(sizethumb)),
            {'mode': 'clearthumb'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if os.path.exists(CONFIG.ARCHIVE_CACHE):
            directory.add_file('Clear Archive_Cache: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(
                tools.convert_size(archive)), {'mode': 'cleararchive'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Clear Old Thumbnails', {'mode': 'oldThumbs'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Clear Crash Logs', {'mode': 'clearcrash'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Purge Databases', {'mode': 'purgedb'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Fresh Start', {'mode': 'freshstart'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

        directory.add_file('Auto Clean', fanart=CONFIG.ADDON_FANART, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_file('Auto Clean Up On Startup: {0}'.format(autoclean.replace('true', on).replace('false', off)),
                           {'mode': 'togglesetting', 'name': 'autoclean'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if autoclean == 'true':
            directory.add_file(
                '--- Auto Clean Frequency: [B][COLOR springgreen]{0}[/COLOR][/B]'.format(
                    CONFIG.CLEANFREQ[CONFIG.AUTOFREQ]),
                {'mode': 'changefreq'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file(
                '--- Clear Cache on Startup: {0}'.format(cache.replace('true', on).replace('false', off)),
                {'mode': 'togglesetting', 'name': 'clearcache'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file(
                '--- Clear Packages on Startup: {0}'.format(packages.replace('true', on).replace('false', off)),
                {'mode': 'togglesetting', 'name': 'clearpackages'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file(
                '--- Clear Old Thumbs on Startup: {0}'.format(thumbs.replace('true', on).replace('false', off)),
                {'mode': 'togglesetting', 'name': 'clearthumbs'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Clear Video Cache', fanart=CONFIG.ADDON_FANART, icon=CONFIG.ICONMAINT,
                           themeit=CONFIG.THEME1)
        directory.add_file(
            'Include Video Cache in Clear Cache: {0}'.format(includevid.replace('true', on).replace('false', off)),
            {'mode': 'togglecache', 'name': 'includevideo'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

        if includeall == 'true':
            includegaia = 'true'
            includeexodusredux = 'true'
            includethecrew = 'true'
            includeyoda = 'true'
            includevenom = 'true'
            includenumbers = 'true'
            includescrubs = 'true'
            includeseren = 'true'
        else:
            includeexodusredux = 'true' if CONFIG.INCLUDEEXODUSREDUX == 'true' else 'false'
            includegaia = 'true' if CONFIG.INCLUDEGAIA == 'true' else 'false'
            includethecrew = 'true' if CONFIG.INCLUDETHECREW == 'true' else 'false'
            includeyoda = 'true' if CONFIG.INCLUDEYODA == 'true' else 'false'
            includevenom = 'true' if CONFIG.INCLUDEVENOM == 'true' else 'false'
            includenumbers = 'true' if CONFIG.INCLUDENUMBERS == 'true' else 'false'
            includescrubs = 'true' if CONFIG.INCLUDESCRUBS == 'true' else 'false'
            includeseren = 'true' if CONFIG.INCLUDESEREN == 'true' else 'false'

        if includevid == 'true':
            directory.add_file(
                '--- Include All Video Addons: {0}'.format(includeall.replace('true', on).replace('false', off)),
                {'mode': 'togglecache', 'name': 'includeall'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.exodusredux)'):
                directory.add_file(
                    '--- Include Exodus Redux: {0}'.format(
                        includeexodusredux.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includeexodusredux'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.gaia)'):
                directory.add_file(
                    '--- Include Gaia: {0}'.format(includegaia.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includegaia'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.numbersbynumbers)'):
                directory.add_file(
                    '--- Include NuMb3r5: {0}'.format(includenumbers.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includenumbers'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.scrubsv2)'):
                directory.add_file(
                    '--- Include Scrubs v2: {0}'.format(includescrubs.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includescrubs'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.seren)'):
                directory.add_file(
                    '--- Include Seren: {0}'.format(includeseren.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includeseren'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.thecrew)'):
                directory.add_file(
                    '--- Include THE CREW: {0}'.format(includethecrew.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includethecrew'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.venom)'):
                directory.add_file(
                    '--- Include Venom: {0}'.format(includevenom.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includevenom'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            if xbmc.getCondVisibility('System.HasAddon(plugin.video.yoda)'):
                directory.add_file(
                    '--- Include Yoda: {0}'.format(includeyoda.replace('true', on).replace('false', off)),
                    {'mode': 'togglecache', 'name': 'includeyoda'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
            directory.add_file('--- Enable All Video Addons', {'mode': 'togglecache', 'name': 'true'}, icon=CONFIG.ICONMAINT,
                               themeit=CONFIG.THEME3)
            directory.add_file('--- Disable All Video Addons', {'mode': 'togglecache', 'name': 'false'}, icon=CONFIG.ICONMAINT,
                               themeit=CONFIG.THEME3)

    def addon_menu(self):
        directory.add_file('Remove Addons', {'mode': 'removeaddons'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('Remove Addon Data', {'mode': 'removeaddondata'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('Enable/Disable Addons', {'mode': 'enableaddons'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        # directory.add_file('Enable/Disable Adult Addons', 'toggleadult', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Force Refresh all Repositories', {'mode': 'forceupdate'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Force Update all Addons', {'mode': 'forceupdate', 'action': 'auto'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

   
    def logging_menu(self):
        errors = int(logging.error_checking(count=True))
        errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'
        wizlogsize = ': [COLOR red]Not Found[/COLOR]' if not os.path.exists(
            CONFIG.WIZLOG) else ": [COLOR springgreen]{0}[/COLOR]".format(
            tools.convert_size(os.path.getsize(CONFIG.WIZLOG)))
            
        directory.add_file('Toggle Debug Logging', {'mode': 'enabledebug'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Upload Log File', {'mode': 'uploadlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('View Errors in Log: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(errorsfound), {'mode': 'viewerrorlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        if errors > 0:
            directory.add_file('View Last Error In Log', {'mode': 'viewerrorlast'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('View Log File', {'mode': 'viewlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('View Wizard Log File', {'mode': 'viewwizlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Clear Wizard Log File: [COLOR springgreen][B]{0}[/B][/COLOR]'.format(wizlogsize), {'mode': 'clearwizlog'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
   
        
    def misc_menu(self):
        directory.add_file('Kodi 17 Fix', {'mode': 'kodi17fix'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('Network Tools', {'mode': 'nettools'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Toggle Unknown Sources', {'mode': 'unknownsources'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Toggle Addon Updates', {'mode': 'toggleupdates'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Reload Skin', {'mode': 'forceskin'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Reload Profile', {'mode': 'forceprofile'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Force Close Kodi', {'mode': 'forceclose'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

    def backup_menu(self):
        directory.add_file('Clean Up Back Up Folder', {'mode': 'clearbackup'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Back Up Location: [COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.MYBUILDS), {'mode': 'settings', 'name': 'Maintenance'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Back Up]: Build', {'mode': 'backup', 'action': 'build'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Back Up]: GuiFix', {'mode': 'backup', 'action': 'gui'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Back Up]: Theme', {'mode': 'backup', 'action': 'theme'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Back Up]: Addon Pack', {'mode': 'backup', 'action': 'addonpack'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Back Up]: Addon_data', {'mode': 'backup', 'action': 'addondata'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: Local Build', {'mode': 'restore', 'action': 'build'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: Local GuiFix', {'mode': 'restore', 'action': 'gui'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: Local Theme', {'mode': 'restore', 'action': 'theme'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: Local Addon Pack', {'mode': 'restore', 'action': 'addonpack'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: Local Addon_data', {'mode': 'restore', 'action': 'addondata'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: External Build', {'mode': 'restore', 'action': 'build', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: External GuiFix', {'mode': 'restore', 'action': 'gui', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: External Theme', {'mode': 'restore', 'action': 'theme', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: External Addon Pack', {'mode': 'restore', 'action': 'addonpack', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('[Restore]: External Addon_data', {'mode': 'restore', 'action': 'addondata', 'name': 'external'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)

    def tweaks_menu(self):
        directory.add_dir('Advanced Settings', {'mode': 'advanced_settings'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Scan Sources for broken links', {'mode': 'checksources'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Scan For Broken Repositories', {'mode': 'checkrepos'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Remove Non-Ascii filenames', {'mode': 'asciicheck'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        # directory.add_file('Toggle Passwords On Keyboard Entry', {'mode': 'togglepasswords'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_file('Convert Paths to special', {'mode': 'convertpath'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
        directory.add_dir('System Information', {'mode': 'systeminfo'}, icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME3)
