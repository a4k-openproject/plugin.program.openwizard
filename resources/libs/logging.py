import xbmc

import os

import uservar
from resources.libs import gui
from resources.libs import tools
from resources.libs import vars


LOGFILES = ['log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log',
            'tvmc.log', 'tvmc.old.log', 'dmp', 'Thumbs.db', '.gitignore', '.DS_Store']
MAXWIZSIZE = [100, 200, 300, 400, 500, 1000]
MAXWIZLINES = [100, 200, 300, 400, 500]
MAXWIZDATES = [1, 2, 3, 7]


def log(msg, level=xbmc.LOGDEBUG):
    WIZDEBUGGING = tools.get_setting('addon_debug')
    DEBUGLEVEL = tools.get_setting('debuglevel')
    ENABLEWIZLOG = tools.get_setting('wizardlog')
    CLEANWIZLOG = tools.get_setting('autocleanwiz')
    NEXTCLEANDATE = tools.get_setting('nextcleandate')

    if not os.path.exists(vars.ADDONDATA):
        os.makedirs(vars.ADDONDATA)
    if not os.path.exists(vars.WIZLOG):
        f = open(vars.WIZLOG, 'w')
        f.close()
    if WIZDEBUGGING == 'false':
        return False
    if DEBUGLEVEL == '0':  # No Logging
        return False
    if DEBUGLEVEL == '1':  # Normal Logging
        if level not in [xbmc.LOGNOTICE, xbmc.LOGERROR, xbmc.LOGSEVERE, xbmc.LOGFATAL]:
            return False
    if DEBUGLEVEL == '2':  # Full Logging
        level = xbmc.LOGNOTICE
    try:
        xbmc.log('{0}: {1}'.format(uservar.ADDONTITLE, msg), level)
    except Exception as e:
        try:
            xbmc.log('Logging Failure: {0}'.format(e), level)
        except:
            pass
    if ENABLEWIZLOG == 'true':
        lastcheck = NEXTCLEANDATE if not NEXTCLEANDATE == '' else str(tools.get_date())
        if CLEANWIZLOG == 'true' and lastcheck <= str(tools.get_date()):
            check_log()
        with open(vars.WIZLOG, 'a') as f:
            line = "[{0} {1}] {2}".format(tools.get_date(now=True).date(),
                                          str(tools.get_date(now=True).time())[:8],
                                          msg)
            f.write(line.rstrip('\r\n') + '\n')


def check_log():
    CLEANWIZLOGBY = tools.get_setting('wizlogcleanby')
    CLEANDAYS = tools.get_setting('wizlogcleandays')
    CLEANSIZE = tools.get_setting('wizlogcleansize')
    CLEANLINES = tools.get_setting('wizlogcleanlines')

    next = tools.get_date(days=1)
    lines = tools.read_from_file(vars.WIZLOG).split('\n')

    if CLEANWIZLOGBY == '0':  # By Days
        keep = tools.get_date(days=-MAXWIZDATES[int(float(CLEANDAYS))])
        x = 0
        for line in lines:
            if str(line[1:11]) >= str(keep):
                break
            x += 1
        newfile = lines[x:]
        tools.write_to_file(vars.WIZLOG, '\n'.join(newfile))
    elif CLEANWIZLOGBY == '1':  # By Size
        maxsize = MAXWIZSIZE[int(float(CLEANSIZE))]*1024
        if os.path.getsize(vars.WIZLOG) >= maxsize:
            start = len(lines)/2
            newfile = lines[start:]
            tools.write_to_file(vars.WIZLOG, '\n'.join(newfile))
    elif CLEANWIZLOGBY == '2':  # By Lines
        maxlines = MAXWIZLINES[int(float(CLEANLINES))]
        if len(lines) > maxlines:
            start = len(lines) - int(maxlines/2)
            newfile = lines[start:]
            tools.write_to_file(vars.WIZLOG, '\n'.join(newfile))
    tools.set_setting('nextcleandate', str(next))


def log_notify(title, message, times=2000, icon=vars.ICON, sound=False):
    gui.DIALOG.notification(title, message, icon, int(times), sound)
