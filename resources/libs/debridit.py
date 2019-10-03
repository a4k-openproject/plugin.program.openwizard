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
import re
import time

from resources.libs.config import CONFIG
from resources.libs import logging
from resources.libs import tools

ORDER = ['gaiard', 'gaiapm', 'pmzer', 'serenrd', 'serenpm', 'rurlrd', 'rurlpm', 'urlrd', 'urlpm']

DEBRIDID = {
    'gaiard': {
        'name'     : 'Gaia RD',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'gaiard',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'gaia_debrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.debrid.realdebrid.id',
        'data'     : ['accounts.debrid.realdebrid.auth', 'accounts.debrid.realdebrid.enabled', 'accounts.debrid.realdebrid.id', 'accounts.debrid.realdebrid.refresh', 'accounts.debrid.realdebrid.secret', 'accounts.debrid.realdebrid.token'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=realdebridAuthentication)'},
    'gaiapm': {
        'name'     : 'Gaia PM',
        'plugin'   : 'plugin.video.gaia',
        'saved'    : 'gaiapm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.gaia', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'gaia_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.gaia', 'settings.xml'),
        'default'  : 'accounts.debrid.premiumize.user',
        'data'     : [ 'accounts.debrid.premiumize.enabled', 'accounts.debrid.premiumize.user', 'accounts.debrid.premiumize.pin'],
        'activate' : 'RunPlugin(plugin://plugin.video.gaia/?action=premiumizeSettings)'},
    'serenrd': {
        'name'     : 'Seren RD',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'seren_rd'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'rd.username',
        'data'     : [ 'rd.auth', 'rd.client_id', 'rd.expiry', 'rd.refresh', 'rd.secret', 'rd.username', 'realdebrid.enabled'],
        'activate' : 'RunPlugin(plugin://plugin.video.seren/?action=authRealDebrid)'},
    'serenpm': {
        'name'     : 'Seren PM',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren', 'temp-fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'seren_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'premiumize.pin',
        'data'     : ['premiumize.enabled', 'premiumize.pin'],
        'activate' : 'RunPlugin(plugin.video.seren/?action=openSettings)'},
    'urlrd': {
        'name'     : 'URLResolver RD',
        'plugin'   : 'script.module.urlresolver',
        'saved'    : 'urlrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'url_debrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.urlresolver', 'settings.xml'),
        'default'  : 'RealDebridResolver_client_id',
        'data'     : ['RealDebridResolver_autopick', 'RealDebridResolver_client_id', 'RealDebridResolver_client_secret', 'RealDebridResolver_enabled', 'RealDebridResolver_login', 'RealDebridResolver_priority', 'RealDebridResolver_refresh', 'RealDebridResolver_token', 'RealDebridResolver_torrents'],
        'activate' : 'RunPlugin(plugin://script.module.urlresolver/?mode=auth_rd)'},
    'rurlrd': {
        'name'     : 'ResolveURL RD',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlrd',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'resurl_debrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'RealDebridResolver_client_id',
        'data'     : ['RealDebridResolver_autopick', 'RealDebridResolver_client_id', 'RealDebridResolver_client_secret', 'RealDebridResolver_enabled', 'RealDebridResolver_login', 'RealDebridResolver_priority', 'RealDebridResolver_refresh', 'RealDebridResolver_token', 'RealDebridResolver_torrents', 'RealDebridResolver_cached_only'],
        'activate' : 'RunPlugin(plugin://script.module.resolveurl/?mode=auth_rd)'},
    'urlpm': {
        'name'     : 'URLResolver PM',
        'plugin'   : 'script.module.urlresolver',
        'saved'    : 'urlpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.urlresolver', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'pmurl_debrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.urlresolver', 'settings.xml'),
        'default'  : 'PremiumizeMeResolver_password',
        'data'     : ['PremiumizeMeResolver_enabled', 'PremiumizeMeResolver_login', 'PremiumizeMeResolver_password', 'PremiumizeMeResolver_priority', 'PremiumizeMeResolver_torrents'],
        'activate' : ''},
    'rurlpm': {
        'name'     : 'ResolveURL PM',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'pmrurl_debrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'PremiumizeMeResolver_token',
        'data'     : ['PremiumizeMeResolver_enabled', 'PremiumizeMeResolver_priority', 'PremiumizeMeResolver_token', 'PremiumizeMeResolver_torrents', 'PremiumizeMeResolver_cached_only'],
        'activate' : ''},
    'pmzer': {
        'name'     : 'Premiumizer',
        'plugin'   : 'plugin.video.premiumizer',
        'saved'    : 'pmzer',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizer', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'premiumizer_debrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizer', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
        'activate' : 'RunPlugin(plugin://plugin.video.premiumizer/?action=authPremiumize)'}
# need to save rdauth.json :(
#	'realizer': {
#		'name'     : 'Realizer',
#		'plugin'   : 'plugin.video.realizer',
#		'saved'    : 'realizer',
#		'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer'),
#		'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'icon.png'),
#		'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.realizer', 'fanart.jpg'),
#		'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'realizer_debrid'),
#		'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.realizer', 'settings.xml'),
#		'default'  : 'premiumize.token',
#		'data'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
#		'activate' : 'RunPlugin(plugin://plugin.video.realizer/?action=authRealdebrid)'}
}


def debrid_user(who):
    user = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user = add.getSetting(DEBRIDID[who]['default'])
            except:
                pass
    return user


def debrid_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.DEBRIDFOLD):
        os.makedirs(CONFIG.DEBRIDFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(DEBRIDID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(DEBRIDID[log]['plugin'])
                    default = DEBRIDID[log]['default']
                    user = addonid.getSetting(default)
                    if user == '' and do == 'update':
                        continue
                    update_debrid(do, log)
                except:
                    pass
            else:
                logging.log('[Debrid Info] {0}({1}) is not installed'.format(DEBRIDID[log]['name'], DEBRIDID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('debridlastsave', tools.get_date(days=3))
    else:
        if DEBRIDID[who]:
            if os.path.exists(DEBRIDID[who]['path']):
                update_debrid(do, who)
        else:
            logging.log('[Debrid Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)


def clear_saved(who, over=False):
    if who == 'all':
        for debrid in DEBRIDID:
            clear_saved(debrid,  True)
    elif DEBRIDID[who]:
        file = DEBRIDID[who]['file']
        if os.path.exists(file):
            os.remove(file)
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, DEBRIDID[who]['name']),
                               '[COLOR {0}]Debrid Info: Removed![/COLOR]'.format(CONFIG.COLOR2),
                               2000,
                               DEBRIDID[who]['icon'])
        CONFIG.set_setting(DEBRIDID[who]['saved'], '')
    if not over:
        xbmc.executebuiltin('Container.Refresh()')


def update_debrid(do, who):
    file = DEBRIDID[who]['file']
    settings = DEBRIDID[who]['settings']
    data = DEBRIDID[who]['data']
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    saved = DEBRIDID[who]['saved']
    default = DEBRIDID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = DEBRIDID[who]['name']
    icon = DEBRIDID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                with open(file, 'w') as f:
                    for debrid in data:
                        f.write('<debrid>\n\t<id>{0}</id>\n\t<value>{1}</value>\n</debrid>\n'.format(debrid, addonid.getSetting(debrid)))
                    f.close()
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Debrid Info: Saved![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else: logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                 '[COLOR {0}]Debrid Info: Not Registered![/COLOR]'.format(CONFIG.COLOR2),
                                 2000,
                                 icon)
    elif do == 'restore':
        if os.path.exists(file):
            f = open(file, mode='r')
            g = f.read().replace('\n', '').replace('\r', '').replace('\t', '')
            f.close()
            match = re.compile('<debrid><id>(.+?)</id><value>(.+?)</value></debrid>').findall(g)
            try:
                if len(match) > 0:
                    for debrid, value in match:
                        addonid.setSetting(debrid, value)
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Debrid Info: Restored![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log_notify(name, 'Real Debrid Info: [COLOR red]Not Found![/COLOR]', 2000, icon)
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        if os.path.exists(settings):
            try:
                f = open(settings, "r")
                lines = f.readlines()
                f.close()
                f = open(settings, "w")
                for line in lines:
                    match = tools.parse_dom(line, 'setting', ret='id')
                    if len(match) == 0:
                        f.write(line)
                    else:
                        if match[0] not in data:
                            f.write(line)
                        else:
                            logging.log('Removing Line: {0}'.format(line), level=xbmc.LOGNOTICE)
                f.close()
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Addon Data: Cleared![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    xbmc.executebuiltin('Container.Refresh()')


def auto_update(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['path']):
                auto_update(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            u = debrid_user(who)
            su = CONFIG.get_setting(DEBRIDID[who]['saved'])
            n = DEBRIDID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                debrid_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                                    "[COLOR {0}]Would you like to save the [COLOR {1}]Debrid Info[/COLOR] for [COLOR {2}]{3}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR {0}]Save Debrid[/COLOR][/B]".format(CONFIG.COLOR2),
                                    nolabel="[B][COLOR {0}]No, Cancel[/COLOR][/B]".format(CONFIG.COLOR1)):
                    debrid_it('update', who)
            else:
                debrid_it('update', who)


def import_list(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['file']):
                import_list(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['file']):
            d = DEBRIDID[who]['default']
            sa = DEBRIDID[who]['saved']
            su = CONFIG.get_setting(sa)
            n = DEBRIDID[who]['name']
            f = open(DEBRIDID[who]['file'], mode='r')
            g = f.read().replace('\n', '').replace('\r', '').replace('\t', '')
            f.close()
            m = re.compile('<debrid><id>{0}</id><value>(.+?)</value></debrid>'.format(d)).findall(g)
            if len(m) > 0:
                if not m[0] == su:
                    dialog = xbmcgui.Dialog()

                    if dialog.yesno("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                                        "[COLOR {0}]Would you like to import the [COLOR {1}]Debrid Info[/COLOR] for [COLOR {2}]{3}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1, n),
                                        "File: [COLOR springgreen][B]{0}[/B][/COLOR]".format(m[0]),
                                        "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                        yeslabel="[B][COLOR {0}]Import Debrid[/COLOR][/B]".format(CONFIG.COLOR2),
                                        nolabel="[B][COLOR {0}]No, Cancel[/COLOR][/B]".format(CONFIG.COLOR1)):
                        CONFIG.set_setting(sa, m[0])
                        logging.log('[Import Data] {0}: {1}'.format(who, str(m)), level=xbmc.LOGNOTICE)
                    else:
                        logging.log('[Import Data] Declined Import({0}): {1}'.format(who, str(m)), level=xbmc.LOGNOTICE)
                else:
                    logging.log('[Import Data] Duplicate Entry({0}): {1}'.format(who, str(m)), level=xbmc.LOGNOTICE)
            else:
                logging.log('[Import Data] No Match({0}): {1}'.format(who, str(m)), level=xbmc.LOGNOTICE)


def activate_debrid(who):
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            act = DEBRIDID[who]['activate']
            addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
            if act == '':
                addonid.openSettings()
            else:
                xbmc.executebuiltin(DEBRIDID[who]['activate'])
        else:
            dialog = xbmcgui.Dialog()

            dialog.ok("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                          '{0} is not currently installed.'.format(DEBRIDID[who]['name']))
    else:
        xbmc.executebuiltin('Container.Refresh()')
        return

    check = 0
    while not debrid_user(who):
        if check == 30:
            break
        check += 1
        time.sleep(10)
    xbmc.executebuiltin('Container.Refresh()')
