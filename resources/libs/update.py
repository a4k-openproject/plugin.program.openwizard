import xbmc

import os
import re

import uservar
from resources.libs import tools


def force_update(silent=False):
    xbmc.executebuiltin('UpdateAddonRepos()')
    xbmc.executebuiltin('UpdateLocalAddons()')
    if not silent:
        from resources.libs import logging
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                           '[COLOR {0}]Forcing Addon Updates[/COLOR]'.format(uservar.COLOR2))


def wizard_update(startup=None):
    from resources.libs import check
    from resources.libs import gui
    from resources.libs import logging

    if check.check_url(uservar.WIZARDFILE):
        try:
            wid, ver, zip = check.check_wizard('all')
        except:
            return
        if ver > vars.VERSION:
            yes = gui.DIALOG.yesno(uservar.ADDONTITLE,
                                   '[COLOR {0}]There is a new version of the [COLOR {1}]{2}[/COLOR]!'.format(uservar.COLOR2, uservar.COLOR1, uservar.ADDONTITLE),
                                   'Would you like to download [COLOR {0}]v{1}[/COLOR]?[/COLOR]'.format(uservar.COLOR1, ver),
                                   nolabel='[B][COLOR red]Remind Me Later[/COLOR][/B]',
                                   yeslabel="[B][COLOR springgreen]Update Wizard[/COLOR][/B]")
            if yes:
                logging.log("[Auto Update Wizard] Installing wizard v{0}".format(ver), level=xbmc.LOGNOTICE)
                gui.DP.create(uservar.ADDONTITLE, '[COLOR {0}]Downloading Update...'.format(uservar.COLOR2), '',
                              'Please Wait[/COLOR]')
                lib = os.path.join(vars.PACKAGES, '{0}-{1}.zip'.format(uservar.ADDON_ID, ver))
                try:
                    os.remove(lib)
                except:
                    pass
                from resources.libs import downloader
                from resources.libs import extract
                downloader.download(zip, lib, DP)
                xbmc.sleep(2000)
                gui.DP.update(0, "", "Installing {0} update".format(uservar.ADDONTITLE))
                percent, errors, error = extract.all(lib, vars.ADDONS, gui.DP, True)
                gui.DP.close()
                xbmc.sleep(1000)
                force_update()
                xbmc.sleep(1000)
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                                   '[COLOR {0}]Add-on updated[/COLOR]'.format(uservar.COLOR2))
                logging.log("[Auto Update Wizard] Wizard updated to v{0}".format(ver), level=xbmc.LOGNOTICE)
                tools.remove_file(os.path.join(uservar.ADDONDATA, 'settings.xml'))
                from resources.libs import notify
                notify.firstRunSettings()
                if startup:
                    xbmc.executebuiltin('RunScript({0}/startup.py)'.format(vars.PLUGIN))
                return
            else:
                logging.log("[Auto Update Wizard] Install New Wizard Ignored: {0}".format(ver), level=xbmc.LOGNOTICE)
        else:
            if not startup:
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(uservar.COLOR1, uservar.ADDONTITLE),
                                   "[COLOR {0}]No New Version of Wizard[/COLOR]".format(uservar.COLOR2))
            logging.log("[Auto Update Wizard] No New Version v{0}".format(ver), level=xbmc.LOGNOTICE)
    else:
        logging.log("[Auto Update Wizard] Url for wizard file not valid: {0}".format(uservar.WIZARDFILE), level=xbmc.LOGNOTICE)


def addon_updates(do=None):
    setting = '"general.addonupdates"'
    if do == 'set':
        query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % setting
        response = xbmc.executeJSONRPC(query)
        match = re.compile('{"value":(.+?)}').findall(response)
        if len(match) > 0:
            default = match[0]
        else:
            default = 0
        tools.set_setting('default.addonupdate', str(default))
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, '2')
        response = xbmc.executeJSONRPC(query)
    elif do == 'reset':
        try:
            value = int(float(tools.get_setting('default.addonupdate')))
        except:
            value = 0
        if value not in [0, 1, 2]:
            value = 0
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
        response = xbmc.executeJSONRPC(query)
