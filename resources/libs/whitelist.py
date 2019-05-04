import xbmc
import xbmcvfs

import glob
import os
import re

import uservar
from resources.libs import gui
from resources.libs import logging
from resources.libs import tools
from resources.libs import vars


BACKUPLOCATION = tools.get_setting('path') if tools.get_setting('path') else vars.HOME
MYBUILDS = os.path.join(BACKUPLOCATION, 'My_Builds')


def parse(file, foldername):
    getid = tools.parse_dom(file, 'addon', ret='id')
    getname = tools.parse_dom(file, 'addon', ret='name')
    addid = foldername if len(getid) == 0 else getid[0]
    title = foldername if len(getname) == 0 else getname[0]
    temp = title.replace('[', '<').replace(']', '>')
    temp = re.sub('<[^<]+?>', '', temp)

    return temp, addid


def whitelist(do):
    addonnames = []
    addonids = []
    addonfolds = []

    if do == 'edit':
        fold = glob.glob(os.path.join(vars.ADDONS, '*/'))
        for folder in sorted(fold, key=lambda x: x):
            foldername = os.path.split(folder[:-1])[1]
            if foldername in uservar.EXCLUDES:
                continue
            elif foldername in vars.DEFAULTPLUGINS:
                continue
            elif foldername == 'packages':
                continue
            xml = os.path.join(folder, 'addon.xml')
            if os.path.exists(xml):
                a = tools.read_from_file(xml)
                temp, addid = parse(a, foldername)
                addonnames.append(temp)
                addonids.append(addid)
                addonfolds.append(foldername)
        fold2 = glob.glob(os.path.join(vars.ADDOND, '*/'))
        for folder in sorted(fold2, key=lambda x: x):
            foldername = os.path.split(folder[:-1])[1]
            if foldername in addonfolds:
                continue
            if foldername in uservar.EXCLUDES:
                continue
            xml = os.path.join(vars.ADDONS, foldername, 'addon.xml')
            xml2 = os.path.join(vars.XBMC, 'addons', foldername, 'addon.xml')
            if os.path.exists(xml):
                a = tools.read_from_file(xml)
            elif os.path.exists(xml2):
                a = tools.read_from_file(xml2)
            else:
                continue
            temp, addid = parse(a, foldername)
            addonnames.append(temp)
            addonids.append(addid)
            addonfolds.append(foldername)
        selected = []
        tempaddonnames = ["-- Click here to Continue --"] + addonnames
        currentWhite = whitelist(do='read')
        for item in currentWhite:
            logging.log(str(item), xbmc.LOGDEBUG)
            try:
                name, id, fold = item
            except Exception as e:
                logging.log(str(e))
            if id in addonids:
                pos = addonids.index(id)+1
                selected.append(pos-1)
                tempaddonnames[pos] = "[B][COLOR %s]%s[/COLOR][/B]" % (uservar.COLOR1, name)
            else:
                addonids.append(id)
                addonnames.append(name)
                tempaddonnames.append("[B][COLOR %s]%s[/COLOR][/B]" % (uservar.COLOR1, name))
        choice = 1
        while choice not in [-1, 0]:
            choice = gui.DIALOG.select("%s: Select the addons you wish to White List." % uservar.ADDONTITLE, tempaddonnames)
            if choice == -1:
                break
            elif choice == 0:
                break
            else:
                choice2 = (choice-1)
                if choice2 in selected:
                    selected.remove(choice2)
                    tempaddonnames[choice] = addonnames[choice2]
                else:
                    selected.append(choice2)
                    tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (uservar.COLOR1, addonnames[choice2])
        white_list = []
        if len(selected) > 0:
            for addon in selected:
                white_list.append("['%s', '%s', '%s']" % (addonnames[addon], addonids[addon], addonfolds[addon]))
            writing = '\n'.join(white_list)
            tools.write_to_file(vars.WHITELIST, writing)
        else:
            try:
                os.remove(vars.WHITELIST)
            except:
                pass
        logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]%s Addons in White List[/COLOR]" % (uservar.COLOR2, len(selected)))
    elif do == 'read':
        white_list = []
        if os.path.exists(vars.WHITELIST):
            lines = tools.read_from_file(vars.WHITELIST).split('\n')
            for item in lines:
                try:
                    name, id, fold = eval(item)
                    white_list.append(eval(item))
                except:
                    pass
        return white_list
    elif do == 'view':
        list = whitelist(do='read')
        if len(list) > 0:
            msg = "Here is a list of your whitelist items, these items(along with dependencies) will not be removed when preforming a fresh start or the userdata overwritten in a build install.[CR][CR]"
            for item in list:
                try:
                    name, id, fold = item
                except Exception as e:
                    logging.log(str(e))
                msg += "[COLOR %s]%s[/COLOR] [COLOR %s]\"%s\"[/COLOR][CR]" % (uservar.COLOR1, name, uservar.COLOR2, id)
            gui.TextBox("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), msg)
        else:
            logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]No items in White List[/COLOR]" % uservar.COLOR2)
    elif do == 'import':
        source = gui.DIALOG.browse(1, '[COLOR %s]Select the whitelist file to import[/COLOR]' % uservar.COLOR2, 'files', '.txt', False, False, vars.HOME)
        logging.log(str(source))
        if not source.endswith('.txt'):
            logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]Import Cancelled![/COLOR]" % uservar.COLOR2)
            return
        current = whitelist(do='read')
        idList = []
        count = 0
        for item in current:
            name, id, fold = item
            idList.append(id)
        lines = tools.read_from_file(xbmcvfs.File(source)).split('\n')
        with open(vars.WHITELIST, 'a') as f:
            for item in lines:
                try:
                    name, id, folder = eval(item)
                except Exception as e:
                    logging.log("Error Adding: '%s' / %s" % (item, str(e)), xbmc.LOGERROR)
                    continue
                logging.log("%s / %s / %s" % (name, id, folder), xbmc.LOGDEBUG)
                if id not in idList:
                    count += 1
                    writing = "['%s', '%s', '%s']" % (name, id, folder)
                    if len(idList) + count > 1:
                        writing = "\n%s" % writing
                    f.write(writing)
            logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]%s Item(s) Added[/COLOR]" % (uservar.COLOR2, count))
    elif do == 'export':
        source = gui.DIALOG.browse(3, '[COLOR %s]Select where you wish to export the whitelist file[/COLOR]' % uservar.COLOR2, 'files', '.txt', False, False, vars.HOME)
        logging.log(str(source), xbmc.LOGDEBUG)
        try:
            xbmcvfs.copy(vars.WHITELIST, os.path.join(source, 'whitelist.txt'))
            gui.DIALOG.ok(uservar.ADDONTITLE, "[COLOR %s]Whitelist has been exported to:[/COLOR]" % (uservar.COLOR2), "[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, os.path.join(source, 'whitelist.txt')))
            logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]Whitelist Exported[/COLOR]" % (uservar.COLOR2))
        except Exception as e:
            logging.log("Export Error: %s" % str(e), xbmc.LOGERROR)
            if not gui.DIALOG.yesno(uservar.ADDONTITLE, "[COLOR %s]The location you selected isnt writable would you like to select another one?[/COLOR]" % uservar.COLOR2, yeslabel="[B][COLOR springgreen]Change Location[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
                logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]Whitelist Export Cancelled[/COLOR]" % (uservar.COLOR2, e))
            else:
                whitelist(do='export')
    elif do == 'clear':
        if not gui.DIALOG.yesno(uservar.ADDONTITLE, "[COLOR %s]Are you sure you want to clear your whitelist?" % uservar.COLOR2, "This process can't be undone.[/COLOR]", yeslabel="[B][COLOR springgreen]Yes Remove[/COLOR][/B]", nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
            logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]Clear Whitelist Cancelled[/COLOR]" % (uservar.COLOR2))
            return
        try:
            os.remove(vars.WHITELIST)
            logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]Whitelist Cleared[/COLOR]" % (uservar.COLOR2))
        except:
            logging.log_notify("[COLOR %s]%s[/COLOR]" % (uservar.COLOR1, uservar.ADDONTITLE), "[COLOR %s]Error Clearing Whitelist![/COLOR]" % (uservar.COLOR2))
