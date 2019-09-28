import xbmc
import xbmcgui
import xbmcvfs

import os
import re

from resources.libs.config import CONFIG

try:  # Python 3
    from urllib.parse import urlencode
    from urllib.request import FancyURLopener
except ImportError:  # Python 2
    from urllib import urlencode
    from urllib import FancyURLopener


URL = 'https://paste.ubuntu.com/'
EXPIRATION = 2592000
REPLACES = (('//.+?:.+?@', '//USER:PASSWORD@'), ('<user>.+?</user>', '<user>USER</user>'), ('<pass>.+?</pass>',
                                                                                            '<pass>PASSWORD</pass>'),)


def log(msg, level=xbmc.LOGDEBUG):
    from resources.libs import tools

    if not os.path.exists(CONFIG.PLUGIN_DATA):
        os.makedirs(CONFIG.PLUGIN_DATA)
    if not os.path.exists(CONFIG.WIZLOG):
        f = open(CONFIG.WIZLOG, 'w+')
        f.close()
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


def log_notify(title, message, times=2000, icon=CONFIG.ADDON_ICON, sound=False):
    dialog = xbmcgui.Dialog()
    dialog.notification(title, message, icon, int(times), sound)


def grab_log(file=False, old=False, wizard=False):
    from resources.libs import tools
    if wizard:
        if not os.path.exists(CONFIG.WIZLOG):
            return False
        else:
            if file:
                return CONFIG.WIZLOG
            else:
                return tools.read_from_file(CONFIG.WIZLOG)
    finalfile = 0
    logfilepath = os.listdir(CONFIG.LOGPATH)
    logsfound = []

    for item in logfilepath:
        if old and item.endswith('.old.log'):
            logsfound.append(os.path.join(CONFIG.LOGPATH, item))
        elif not old and item.endswith('.log') and not item.endswith('.old.log'):
            logsfound.append(os.path.join(CONFIG.LOGPATH, item))

    if len(logsfound) > 0:
        logsfound.sort(key=lambda f: os.path.getmtime(f))
        if file:
            return logsfound[-1]
        else:
            return tools.read_from_file(logsfound[-1])
    else:
        return False


def upload_log():
    files = get_files()
    for item in files:
        filetype = item[0]
        if filetype == 'log':
            log = os.path.basename(grab_log(file=True))
            name = log if log else "kodi.log"
            error = "Error posting the {0} file".format(name)
        elif filetype == 'oldlog':
            log = os.path.basename(grab_log(file=True, old=True))
            name = log if log else "kodi.old.log"
            error = "Error posting the {0} file".format(name)
        elif filetype == 'wizlog':
            name = "wizard.log"
            error = "Error posting the {0} file".format(name)
        elif filetype == 'crashlog':
            name = "crash log"
            error = "Error posting the crashlog file"
        succes, data = read_log(item[1])
        if succes:
            content = clean_log(data)
            succes, result = post_log(content, name)
            if succes:
                msg = "Post this url or scan QRcode for your [COLOR {0}]{1}[/COLOR]," \
                      "together with a description of the problem:[CR][COLOR {2}]{3}[/COLOR]".format(
                    CONFIG.COLOR1, name, CONFIG.COLOR1, result)

                # if len(self.email) > 5:
                # em_result, em_msg = self.email_Log(self.email, result, name)
                # if em_result == 'message':
                # msg += "[CR]%s" % em_msg
                # else:
                # msg += "[CR]Email ERROR: %s" % em_msg

                show_result(msg, result)
            else:
                show_result('{0}[CR]{1}'.format(error, result))
        else:
            show_result('{0}[CR]{1}'.format(error, result))


def get_files():
    logfiles = []
    log = grab_log(file=True)
    old = grab_log(file=True, old=True)
    wizard = False if not os.path.exists(CONFIG.WIZLOG) else CONFIG.WIZLOG
    if log:
        if os.path.exists(log):
            logfiles.append(['log', log])
        else:
            show_result("No log file found")
    else:
        show_result("No log file found")
    if CONFIG.KEEPOLDLOG:
        if old:
            if os.path.exists(old):
                logfiles.append(['oldlog', old])
            else:
                show_result("No old log file found")
        else:
            show_result("No old log file found")
    if CONFIG.KEEPWIZLOG:
        if wizard:
            logfiles.append(['wizlog', wizard])
        else:
            show_result("No wizard log file found")
    if CONFIG.KEEPCRASHLOG:
        from resources.libs import tools
        crashlog_path = ''
        items = []
        if xbmc.getCondVisibility('system.platform.osx'):
            crashlog_path = os.path.join(os.path.expanduser('~'), 'Library/Logs/DiagnosticReports/')
            filematch = 'Kodi'
        elif xbmc.getCondVisibility('system.platform.ios'):
            crashlog_path = '/var/mobile/Library/Logs/CrashReporter/'
            filematch = 'Kodi'
        elif tools.platform() == 'linux':
            # not 100% accurate (crashlogs can be created in the dir kodi was started from as well)
            crashlog_path = os.path.expanduser('~')
            filematch = 'kodi_crashlog'
        elif tools.platform() == 'windows':
            log("Windows crashlogs are not supported, please disable this option in the addon settings", level=xbmc.LOGNOTICE)
        elif tools.platform() == 'android':
            log("Android crashlogs are not supported, please disable this option in the addon settings", level=xbmc.LOGNOTICE)
        if crashlog_path and os.path.isdir(crashlog_path):
            dirs, files = xbmcvfs.listdir(crashlog_path)
            for item in files:
                if filematch in item and os.path.isfile(os.path.join(crashlog_path, item)):
                    items.append(os.path.join(crashlog_path, item))
                    items.sort(key=lambda f: os.path.getmtime(f))
                    lastcrash = items[-1]
                    logfiles.append(['crashlog', lastcrash])
        if len(items) == 0:
            log("No crashlog file found", level=xbmc.LOGNOTICE)
    return logfiles


def read_log(path):
    try:
        lf = xbmcvfs.File(path)
        content = lf.read()
        if content:
            return True, content
        else:
            log('file is empty', level=xbmc.LOGNOTICE)
            return False, "File is Empty"
    except Exception as e:
        log('unable to read file: {0}'.format(e), level=xbmc.LOGNOTICE)
        return False, "Unable to Read File"


def clean_log(content):
    for pattern, repl in REPLACES:
        content = re.sub(pattern, repl, content)
        return content


def post_log(data, name):
    params = {'poster': CONFIG.BUILDERNAME, 'content': data, 'syntax': 'text', 'expiration': 'week'}
    params = urlencode(params)

    try:
        page = LogURLopener().open(URL, params)
    except Exception as e:
        a = 'failed to connect to the server'
        log("{0}: {1}".format(a, str(e)), level=xbmc.LOGERROR)
        return False, a

    try:
        page_url = page.url.strip()
        # copy_to_clipboard(page_url)
        log("URL for {0}: {1}".format(name, page_url), level=xbmc.LOGNOTICE)
        return True, page_url
    except Exception as e:
        a = 'unable to retrieve the paste url'
        log("{0}: {1}".format(a, str(e)), level=xbmc.LOGERROR)
        return False, a


# CURRENTLY NOT IN USE
def copy_to_clipboard(txt):
    from resources.libs import tools
    import subprocess

    platform = tools.platform()
    if platform == 'windows':
        try:
            cmd = 'echo ' + txt.strip() + '|clip'
            return subprocess.check_call(cmd, shell=True)
            pass
        except:
            pass
    elif platform == 'linux':
        try:
            from subprocess import Popen, PIPE

            p = Popen(['xsel', '-pi'], stdin=PIPE)
            p.communicate(input=txt)
        except:
            pass
    else:
        pass


# CURRENTLY NOT IN USE
def email_log(email, results, file):
    URL = 'http://aftermathwizard.net/mail_logs.php'
    data = {'email': email, 'results': results, 'file': file, 'wizard': CONFIG.ADDONTITLE}
    params = urlencode(data)

    try:
        result = LogURLopener().open(URL, params)
        returninfo = result.read()
        log(str(returninfo), level=xbmc.LOGNOTICE)
    except Exception as e:
        a = 'failed to connect to the server'
        log("{0}: {1}".format(a, str(e)), level=xbmc.LOGERROR)
        return False, a

    try:
        return True, "Emailing logs is currently disabled."
        # js_data = json.loads(returninfo)

        # if 'type' in js_data:
            # return js_data['type'], str(js_data['text'])
        # else:
            # return str(js_data)
    except Exception as e:
        log("ERROR: {0}".format(str(e)), level=xbmc.LOGERROR)
        return False, "Error Sending Email."


class LogURLopener(FancyURLopener):
    version = '{0}: {1}'.format(CONFIG.ADDON_ID, CONFIG.ADDON_VERSION)


def show_result(message, url=None):
    from resources.libs import gui

    if url:
        try:
            from resources.libs import qr
            
            fn = url.split('/')[-2]
            imagefile = qr.generate_code(url, fn)
            gui.show_qr_code("loguploader.xml", imagefile, message)
            try:
                os.remove(imagefile)
            except:
                pass
        except Exception as e:
            log(str(e), xbmc.LOGNOTICE)
            confirm = dialog.ok(CONFIG.ADDONTITLE, "[COLOR %s]%s[/COLOR]" % (CONFIG.COLOR2, message))
    else:
        confirm = dialog.ok(CONFIG.ADDONTITLE, "[COLOR %s]%s[/COLOR]" % (CONFIG.COLOR2, message))


def view_log_file():
    from resources.libs import gui

    mainlog = grab_log(file=True)
    oldlog = grab_log(file=True, old=True)
    which = 0

    if oldlog and mainlog:

        which = dialog.select(CONFIG.ADDONTITLE,
                                  ["View {0}".format(mainlog.replace(CONFIG.LOG, "")), "View {0}".format(oldlog.replace(CONFIG.LOG, ""))])
        if which == -1:
            log_notify('[COLOR {0}]View Log[/COLOR]'.format(CONFIG.COLOR1),
                       '[COLOR {0}]View Log Cancelled![/COLOR]'.format(CONFIG.COLOR2))
            return
    elif not mainlog and not oldlog:
        log_notify('[COLOR {0}]View Log[/COLOR]'.format(CONFIG.COLOR1),
                   '[COLOR {0}]No Log File Found![/COLOR]'.format(CONFIG.COLOR2))
        return
    elif mainlog:
        which = 0
    elif oldlog:
        which = 1

    logtype = mainlog if which == 0 else oldlog
    msg = grab_log() if which == 0 else grab_log(old=True)

    gui.show_log_viewer("Viewing Log File: {0}".format(logtype), msg, ext_buttons=True)


def error_list(file):
    from resources.libs import tools

    errors = []
    b = tools.read_from_file(file).replace('\n', '[CR]').replace('\r', '')

    match = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(b)
    for item in match:
        errors.append(item)
    return errors


def error_checking(log=None, count=None, last=None):
    errors = []
    error1 = []
    error2 = []
    if log is None:
        curr = grab_log(file=True)
        old = grab_log(file=True, old=True)
        if not old  and not curr:
            if count is None:
                log_notify('[COLOR {0}]View Error Log[/COLOR]'.format(CONFIG.COLOR1),
                           '[COLOR {0}]No Log File Found![/COLOR]'.format(CONFIG.COLOR2))
                return
            else:
                return 0
        if curr:
            error1 = error_list(curr)
        if old:
            error2 = error_list(old)
        if len(error2) > 0:
            for item in error2:
                errors = [item] + errors
        if len(error1) > 0:
            for item in error1:
                errors = [item] + errors
    else:
        error1 = error_list(log)
        if len(error1) > 0:
            for item in error1:
                errors = [item] + errors

    if count is not None:
        return len(errors)
    elif len(errors) > 0:
        from resources.libs import gui
        
        if last is None:
            i = 0
            string = ''
            for item in errors:
                i += 1
                string += "[B][COLOR red]ERROR NUMBER {0}:[/B][/COLOR] {1}\n".format(str(i), item.replace(CONFIG.HOME, '/').replace('                                        ', ''))
            gui.show_log_viewer("Viewing Errors in Log", string)
        else:
            string = "[B][COLOR red]Last Error in Log:[/B][/COLOR] {0}\n".format(errors[0].replace(CONFIG.HOME, '/').replace('                                        ', ''))
            gui.show_log_viewer("Viewing Last Error in Log", string)

    else:
        log_notify('[COLOR {0}]View Error Log[/COLOR]'.format(CONFIG.COLOR1),
                   '[COLOR {0}]No Errors Found![/COLOR]'.format(CONFIG.COLOR2))

