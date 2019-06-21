import xbmc

import glob
import os
import re
import sys

try:
    from urllib.request import urlopen
    from urllib.request import Request
except ImportError:
    from urllib2 import urlopen
    from urllib2 import Request

from resources.libs.config import CONFIG


def check_url(url):
    from resources.libs import tools

    if url in ['http://', 'https://', '']:
        return False
    check = 0
    status = ''
    while check < 3:
        check += 1
        try:
            status = tools.open_url(url)
            break
        except Exception as e:
            status = str(e)
            from resources.libs import logging
            logging.log("Working Url Error: %s [%s]" % (e, url))
            xbmc.sleep(500)
    return status


def check_build(name, ret):
    from resources.libs import tools

    if not check_url(CONFIG.BUILDFILE):
        return False
    link = tools.open_url(CONFIG.BUILDFILE).replace('\n', '').replace('\r', '').replace('\t', '')\
        .replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
    match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?inor="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?nfo="(.+?)".+?escription="(.+?)"' % name).findall(link)
    if len(match) > 0:
        for version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description in match:
            if ret == 'version':
                return version
            elif ret == 'url':
                return url
            elif ret == 'minor':
                return minor
            elif ret == 'gui':
                return gui
            elif ret == 'kodi':
                return kodi
            elif ret == 'theme':
                return theme
            elif ret == 'icon':
                return icon
            elif ret == 'fanart':
                return fanart
            elif ret == 'preview':
                return preview
            elif ret == 'adult':
                return adult
            elif ret == 'description':
                return description
            elif ret == 'info':
                return info
            elif ret == 'all':
                return name, version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description
    else:
        return False


def check_info(name):
    from resources.libs import tools

    if not check_url(name):
        return False
    link = tools.open_url(name).replace('\n', '').replace('\r', '').replace('\t', '')
    match = re.compile('.+?ame="(.+?)".+?xtracted="(.+?)".+?ipsize="(.+?)".+?kin="(.+?)".+?reated="(.+?)".+?rograms="(.+?)".+?ideo="(.+?)".+?usic="(.+?)".+?icture="(.+?)".+?epos="(.+?)".+?cripts="(.+?)"').findall(link)
    if len(match) > 0:
        for name, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts in match:
            return name, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts
    else:
        return False


def build_info(name):
    from resources.libs import logging
    from resources.libs import tools

    if check_url(CONFIG.BUILDFILE):
        if check_build(name, 'url'):
            name, version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description = check_build(name, 'all')
            adult = 'Yes' if adult.lower() == 'yes' else 'No'
            extend = False
            if not info == "http://":
                try:
                    tname, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts = check_info(info)
                    extend = True
                except:
                    extend = False
            if extend:
                msg = "[COLOR {0}]Build Name:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, name)
                msg += "[COLOR {0}]Build Version:[/COLOR] v[COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, version)
                msg += "[COLOR {0}]Latest Update:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, created)
                if not theme == "http://":
                    themecount = theme_count(name, False)
                    msg += "[COLOR {0}]Build Theme(s):[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, ', '.join(themecount))
                msg += "[COLOR {0}]Kodi Version:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, kodi)
                msg += "[COLOR {0}]Extracted Size:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, tools.convert_size(int(float(extracted))))
                msg += "[COLOR {0}]Zip Size:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, tools.convert_size(int(float(zipsize))))
                msg += "[COLOR {0}]Skin Name:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, skin)
                msg += "[COLOR {0}]Adult Content:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, adult)
                msg += "[COLOR {0}]Description:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, description)
                msg += "[COLOR {0}]Programs:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, programs)
                msg += "[COLOR {0}]Video:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, video)
                msg += "[COLOR {0}]Music:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, music)
                msg += "[COLOR {0}]Pictures:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, picture)
                msg += "[COLOR {0}]Repositories:[/COLOR] [COLOR {1}]{2}[/COLOR][CR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, repos)
                msg += "[COLOR {0}]Scripts:[/COLOR] [COLOR {1}]{}[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, scripts)
            else:
                msg  = "[COLOR {0}]Build Name:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, name)
                msg += "[COLOR {0}]Build Version:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, version)
                if not theme == "http://":
                    themecount = theme_count(name, False)
                    msg += "[COLOR {0}]Build Theme(s):[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, ', '.join(themecount))
                msg += "[COLOR {0}]Kodi Version:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, kodi)
                msg += "[COLOR {0}]Adult Content:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, adult)
                msg += "[COLOR {0}]Description:[/COLOR] [COLOR {1}]{2}[/COLOR][CR]".format(CONFIG.COLOR2, CONFIG.COLOR1, description)

            gui.show_text_box(CONFIG.ADDONTITLE, msg)
        else:
            logging.log("Invalid Build Name!")
    else:
        logging.log("Build text file not working: {0}".format(CONFIG.BUILDFILE))


def check_theme(name, theme, ret):
    from resources.libs import tools

    themeurl = check_build(name, 'theme')
    if not check_url(themeurl):
        return False
    link = tools.open_url(themeurl).replace('\n', '').replace('\r', '').replace('\t', '')
    match = re.compile('name="{0}".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult=(.+?).+?escription="(.+?)"'.format(theme)).findall(link)
    if len(match) > 0:
        for url, icon, fanart, adult, description in match:
            if ret == 'url':
                return url
            elif ret == 'icon':
                return icon
            elif ret == 'fanart':
                return fanart
            elif ret == 'adult':
                return adult
            elif ret == 'description':
                return description
            elif ret == 'all':
                return name, theme, url, icon, fanart, adult, description


def check_wizard(ret):
    from resources.libs import tools

    if not check_url(CONFIG.BUILDFILE):
        return False
    link = tools.open_url(CONFIG.BUILDFILE).replace('\n', '').replace('\r', '').replace('\t', '')
    match = re.compile('id="{0}".+?ersion="(.+?)".+?ip="(.+?)"'.format(CONFIG.ADDON_ID)).findall(link)
    if len(match) > 0:
        for version, zip in match:
            if ret == 'version':
                return version
            elif ret == 'zip':
                return zip
            elif ret == 'all':
                return CONFIG.ADDON_ID, version, zip
    else:
        return False


def check_sources():
    from resources.libs import gui
    from resources.libs import logging
    from resources.libs import tools

    if not os.path.exists(CONFIG.SOURCES):
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]No sources.xml File Found![/COLOR]".format(CONFIG.COLOR2))
        return False
    x = 0
    bad = []
    remove = []
    a = tools.read_from_file(CONFIG.SOURCES)
    temp = a.replace('\r', '').replace('\n', '').replace('\t', '')
    match = re.compile('<files>.+?</files>').findall(temp)

    if len(match) > 0:
        match2 = re.compile('<source>.+?<name>(.+?)</name>.+?<path pathversion="1">(.+?)</path>.+?<allowsharing>(.+?)</allowsharing>.+?</source>').findall(match[0])
        gui.DP.create(CONFIG.ADDONTITLE, "[COLOR {0}]Scanning Sources for Broken links[/COLOR]".format(CONFIG.COLOR2))
        for name, path, sharing in match2:
            x += 1
            perc = int(tools.percentage(x, len(match2)))
            gui.DP.update(perc,
                          '',
                          "[COLOR {0}]Checking [COLOR {1}]{2}[/COLOR]:[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, name),
                          "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, path))
            if 'http' in path:
                working = check_url(path)
                if not working:
                    bad.append([name, path, sharing, working])

        logging.log("Bad Sources: {0}".format(len(bad)), level=xbmc.LOGNOTICE)
        if len(bad) > 0:
            choice = gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                                      "[COLOR {0}]{1}[/COLOR][COLOR {2}] Source(s) have been found Broken".format(CONFIG.COLOR1, len(bad), CONFIG.COLOR2),
                                      "Would you like to Remove all or choose one by one?[/COLOR]",
                                      yeslabel="[B][COLOR springgreen]Remove All[/COLOR][/B]",
                                      nolabel="[B][COLOR red]Choose to Delete[/COLOR][/B]")
            if choice == 1:
                remove = bad
            else:
                for name, path, sharing, working in bad:
                    logging.log("{0} sources: {1}, {2}".format(name, path, working), level=xbmc.LOGNOTICE)
                    if gui.DIALOG.yesno(CONFIG.ADDONTITLE,
                                        "[COLOR {0}]{1}[/COLOR][COLOR {2}] was reported as non working".format(CONFIG.COLOR1, name, CONFIG.COLOR2),
                                        "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, path),
                                        "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, working),
                                        yeslabel="[B][COLOR springgreen]Remove Source[/COLOR][/B]",
                                        nolabel="[B][COLOR red]Keep Source[/COLOR][/B]"):
                        remove.append([name, path, sharing, working])
                        logging.log("Removing Source {0}".format(name), level=xbmc.LOGNOTICE)
                    else:
                        logging.log("Source {0} was not removed".format(name), level=xbmc.LOGNOTICE)
            if len(remove) > 0:
                for name, path, sharing, working in remove:
                    a = a.replace('\n<source>\n<name>{0}</name>\n<path pathversion="1">{1}</path>\n<allowsharing>{2}</allowsharing>\n</source>'.format(name, path, sharing), '')
                    logging.log("Removing Source {0}".format(name), level=xbmc.LOGNOTICE)

                tools.write_to_file(CONFIG.SOURCES, str(a))
                alive = len(match) - len(bad)
                kept = len(bad) - len(remove)
                removed = len(remove)
                gui.DIALOG.ok(CONFIG.ADDONTITLE,
                              "[COLOR {0}]Checking sources for broken paths has been completed".format(CONFIG.COLOR2),
                              "Working: [COLOR {0}]{1}[/COLOR] | Kept: [COLOR {2}]{3}[/COLOR] | Removed: [COLOR {4}]{5}[/COLOR][/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, alive, CONFIG.COLOR1, kept, CONFIG.COLOR1, removed))
            else:
                logging.log("No Bad Sources to be removed.", level=xbmc.LOGNOTICE)
        else:
            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]All Sources Are Working[/COLOR]".format(CONFIG.COLOR2))
    else:
        logging.log("No Sources Found", level=xbmc.LOGNOTICE)


def check_repos():
    from resources.libs import gui
    from resources.libs import logging
    from resources.libs import tools

    gui.DP.create(CONFIG.ADDONTITLE, '[COLOR {0}]Checking Repositories...[/COLOR]'.format(CONFIG.COLOR2))
    badrepos = []
    xbmc.executebuiltin('UpdateAddonRepos')
    repolist = glob.glob(os.path.join(CONFIG.ADDONS, 'repo*'))
    if len(repolist) == 0:
        gui.DP.close()
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]No Repositories Found![/COLOR]".format(CONFIG.COLOR2))
        return
    sleeptime = len(repolist)
    start = 0
    while start < sleeptime:
        start += 1
        if gui.DP.iscanceled():
            break
        perc = int(tools.percentage(start, sleeptime))
        gui.DP.update(perc,
                      '',
                      '[COLOR {0}]Checking: [/COLOR][COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR2, CONFIG.COLOR1, repolist[start-1].replace(CONFIG.ADDONS, '')[1:]))
        xbmc.sleep(1000)
    if gui.DP.iscanceled():
        gui.DP.close()
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]Enabling Addons Cancelled[/COLOR]".format(CONFIG.COLOR2))
        sys.exit()
    gui.DP.close()
    logfile = logging.grab_log(False)
    fails = re.compile('CRepositoryUpdateJob(.+?)failed').findall(logfile)
    for item in fails:
        logging.log("Bad Repository: {0} ".format(item), level=xbmc.LOGNOTICE)
        brokenrepo = item.replace('[', '').replace(']', '').replace(' ', '').replace('/', '').replace('\\', '')
        if brokenrepo not in badrepos:
            badrepos.append(brokenrepo)
    if len(badrepos) > 0:
        msg = "[COLOR {0}]Below is a list of Repositories that did not resolve.  This does not mean that they are Depreciated, sometimes hosts go down for a short period of time.  Please do serveral scans of your repository list before removing a repository just to make sure it is broken.[/COLOR][CR][CR][COLOR {1}]".format(CONFIG.COLOR2, CONFIG.COLOR1)
        msg += '[CR]'.join(badrepos)
        msg += '[/COLOR]'
        gui.show_text_box("{0}: Bad Repositories".format(CONFIG.ADDONTITLE), msg)
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]All Repositories Working![/COLOR]".format(CONFIG.COLOR2))


def build_count():
    from resources.libs import test
    from resources.libs import tools

    link = tools.open_url(CONFIG.BUILDFILE).replace('\n', '').replace('\r', '').replace('\t', '')
    match = re.compile('name="(.+?)".+?odi="(.+?)".+?dult="(.+?)"').findall(link)
    total = 0
    count17 = 0
    count18 = 0
    hidden = 0
    adultcount = 0
    if len(match) > 0:
        for name, kodi, adult in match:
            if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
                hidden += 1
                adultcount += 1
                continue
            if not CONFIG.DEVELOPER == 'true' and test.str_test(name):
                hidden += 1
                continue
            kodi = int(float(kodi))
            total += 1
            if kodi == 18:
                count18 += 1
            elif kodi == 17:
                count17 += 1
    return total, count17, count18, adultcount, hidden


def theme_count(name, count=True):
    from resources.libs import tools

    themefile = check_build(name, 'theme')
    if themefile == 'http://' or not themefile:
        return False
    link = tools.open_url(themefile).replace('\n', '').replace('\r', '').replace('\t', '')
    match = re.compile('name="(.+?)".+?dult="(.+?)"').findall(link)
    if len(match) == 0:
        return False
    themes = []
    for item, adult in match:
        if not CONFIG.SHOWADULT == 'true' and adult.lower() == 'yes':
            continue
        themes.append(item)
    if len(themes) > 0:
        if count:
            return len(themes)
        else:
            return themes
    else:
        return False

