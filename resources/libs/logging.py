import xbmc

import os

from resources.libs.config import CONFIG


def log(msg, level=xbmc.LOGDEBUG):
    from resources.libs import tools

    if not os.path.exists(CONFIG.ADDONDATA):
        os.makedirs(CONFIG.ADDONDATA)
    if not os.path.exists(CONFIG.WIZLOG):
        f = tools.write_to_file(CONFIG.WIZLOG, "")

    if CONFIG.WIZDEBUGGING == 'false':
        return False
    if CONFIG.DEBUGLEVEL == '0':  # No Logging
        return False
    if CONFIG.DEBUGLEVEL == '1':  # Normal Logging
        if level not in [xbmc.LOGNOTICE, xbmc.LOGERROR, xbmc.LOGSEVERE, xbmc.LOGFATAL]:
            return False
    if CONFIG.DEBUGLEVEL == '2':  # Full Logging
        level = xbmc.LOGNOTICE
    try:
        xbmc.log('{0}: {1}'.format(CONFIG.ADDONTITLE, msg), level)
    except Exception as e:
        try:
            xbmc.log('Logging Failure: {0}'.format(e), level)
        except:
            pass
    if CONFIG.ENABLEWIZLOG == 'true':
        lastcheck = CONFIG.NEXTCLEANDATE if not CONFIG.NEXTCLEANDATE == '' else str(tools.get_date())
        if CONFIG.CLEANWIZLOG == 'true' and lastcheck <= str(tools.get_date()):
            check_log()

        line = "[{0} {1}] {2}".format(tools.get_date(now=True).date(),
                                      str(tools.get_date(now=True).time())[:8],
                                      msg)
        line = line.rstrip('\r\n') + '\n'
        tools.write_to_file(CONFIG.WIZLOG, line, mode='a')


def check_log():
    from resources.libs import tools

    next = tools.get_date(days=1)
    lines = tools.read_from_file(CONFIG.WIZLOG).split('\n')

    if CONFIG.CLEANWIZLOGBY == '0':  # By Days
        keep = tools.get_date(days=-CONFIG.MAXWIZDATES[int(float(CONFIG.CLEANDAYS))])
        x = 0
        for line in lines:
            if str(line[1:11]) >= str(keep):
                break
            x += 1
        newfile = lines[x:]
        tools.write_to_file(CONFIG.WIZLOG, '\n'.join(newfile))
    elif CONFIG.CLEANWIZLOGBY == '1':  # By Size
        maxsize = CONFIG.MAXWIZSIZE[int(float(CONFIG.CLEANSIZE))]*1024
        if os.path.getsize(CONFIG.WIZLOG) >= maxsize:
            start = len(lines)/2
            newfile = lines[start:]
            tools.write_to_file(CONFIG.WIZLOG, '\n'.join(newfile))
    elif CONFIG.CLEANWIZLOGBY == '2':  # By Lines
        maxlines = CONFIG.MAXWIZLINES[int(float(CONFIG.CLEANLINES))]
        if len(lines) > maxlines:
            start = len(lines) - int(maxlines/2)
            newfile = lines[start:]
            tools.write_to_file(CONFIG.WIZLOG, '\n'.join(newfile))
    CONFIG.set_setting('nextcleandate', str(next))


def log_notify(title, message, times=2000, icon=CONFIG.ICON, sound=False):
    from resources.libs import gui
    gui.DIALOG.notification(title, message, icon, int(times), sound)
