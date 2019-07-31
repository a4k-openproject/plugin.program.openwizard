try:  # Python 3
    import zipfile
except ImportError:  # Python 2
    from resources.libs import zipfile

from resources.libs.config import CONFIG


def str_test(teststr):
    a = (teststr.lower()).split(' ')
    if 'test' in a:
        return True
    else:
        return False


def test_theme(path):
    from resources.libs import logging

    zfile = zipfile.ZipFile(path)
    for item in zfile.infolist():
        logging.log(str(item.filename))
        if '/settings.xml' in item.filename:
            return True
    return False


def test_gui(path):
    zfile = zipfile.ZipFile(path)
    for item in zfile.infolist():
        if '/guisettings.xml' in item.filename:
            return True
    return False


def test_notify():
    from resources.libs import gui
    from resources.libs import logging
    from resources.libs import tools

    if tools.check_url(CONFIG.NOTIFICATION):
        try:
            id, msg = gui.split_notify(CONFIG.NOTIFICATION)
            if not id:
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                                   "[COLOR {0}]Notification: Not Formatted Correctly[/COLOR]".format(CONFIG.COLOR2))
                return
            gui.show_notification(msg, True)
        except Exception as e:
            logging.log("Error on Notifications Window: {0}".format(str(e)), level=xbmc.LOGERROR)
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]Invalid URL for Notification[/COLOR]".format(CONFIG.COLOR2))


def test_update():
    from resources.libs import check
    from resources.libs import gui

    if CONFIG.BUILDNAME == "":
        gui.show_update_window()
    else:
        gui.show_update_window(CONFIG.BUILDNAME, CONFIG.BUILDVERSION, CONFIG.BUILDLATEST, check.check_build(CONFIG.BUILDNAME, 'icon'), check.check_build(CONFIG.BUILDNAME, 'fanart'))


def test_first_run():
    from resources.libs import gui

    gui.show_build_prompt()


def test_save_data_settings():
    from resources.libs import gui

    gui.show_save_data_settings()
