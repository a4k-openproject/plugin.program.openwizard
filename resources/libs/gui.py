import xbmc
import xbmcgui

import os
import re

try:  # Python 3
    from urllib.parse import quote_plus
except ImportError:  # Python 3
    from urllib import quote_plus

from resources.libs.config import CONFIG


DIALOG = xbmcgui.Dialog()
DP = xbmcgui.DialogProgress()

ACTION_PREVIOUS_MENU = 10  # ESC action
ACTION_NAV_BACK = 92  # Backspace action
ACTION_MOVE_LEFT = 1  # Left arrow key
ACTION_MOVE_RIGHT = 2  # Right arrow key
ACTION_MOVE_UP = 3  # Up arrow key
ACTION_MOVE_DOWN = 4  # Down arrow key
ACTION_MOUSE_WHEEL_UP = 104	 # Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105  # Mouse wheel down
ACTION_MOVE_MOUSE = 107  # Down arrow key
ACTION_SELECT_ITEM = 7  # Number Pad Enter
ACTION_BACKSPACE = 110  # ?
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_LONG_CLICK = 108


def sep(middle=''):
    char = CONFIG.SPACER
    ret = char * 40
    if not middle == '':
        middle = '[ {0} ]'.format(middle)
        fluff = int((40 - len(middle))/2)
        ret = "{0}{1}{2}".format(ret[:fluff], middle, ret[:fluff+2])
    return ret[:40]


def highlight_text(msg):
    msg = msg.replace('\n', '[NL]')
    matches = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(msg)
    for item in matches:
        string = '-->Python callback/script returned the following error<--{0}-->End of Python script error report<--'.format(item)
        msg = msg.replace(string, '[COLOR red]{0}[/COLOR]'.format(string))
    msg = msg.replace('WARNING', '[COLOR yellow]WARNING[/COLOR]').replace('ERROR', '[COLOR red]ERROR[/COLOR]').replace('[NL]', '\n').replace(': EXCEPTION Thrown (PythonToCppException) :', '[COLOR red]: EXCEPTION Thrown (PythonToCppException) :[/COLOR]')
    msg = msg.replace('\\\\', '\\').replace(CONFIG.HOME, '')
    return msg


def get_artwork(file):
    if file == 'button':
        return os.path.join(CONFIG.SKIN, 'Button', 'button-focus_lightblue.png'),\
               os.path.join(CONFIG.SKIN, 'Button', 'button-focus_grey.png')
    elif file == 'radio' :
        return os.path.join(CONFIG.SKIN, 'RadioButton', 'MenuItemFO.png'),\
               os.path.join(CONFIG.SKIN, 'RadioButton', 'MenuItemNF.png'),\
               os.path.join(CONFIG.SKIN, 'RadioButton', 'radiobutton-focus.png'),\
               os.path.join(CONFIG.SKIN, 'RadioButton', 'radiobutton-nofocus.png')
    elif file == 'slider':
        return os.path.join(CONFIG.SKIN, 'Slider', 'osd_slider_nib.png'),\
               os.path.join(CONFIG.SKIN, 'Slider', 'osd_slider_nibNF.png'),\
               os.path.join(CONFIG.SKIN, 'Slider', 'slider1.png'),\
               os.path.join(CONFIG.SKIN, 'Slider', 'slider1.png')


def while_window(window, active=False, count=0, counter=15):
    from resources.libs import logging

    windowopen = xbmc.getCondVisibility('Window.IsActive({0})'.format(window))
    logging.log("{0} is {1}".format(window, windowopen))
    while not windowopen and count < counter:
        logging.log("{0} is {1}({2})".format(window, windowopen, count))
        windowopen = xbmc.getCondVisibility('Window.IsActive({0})'.format(window))
        count += 1
        xbmc.sleep(500)

    while windowopen:
        active = True
        logging.log("{0} is {1}".format(window, windowopen))
        windowopen = xbmc.getCondVisibility('Window.IsActive({0})'.format(window))
        xbmc.sleep(250)
    return active


def show_text_box(title, msg):
    class TextBox(xbmcgui.WindowXMLDialog):
        def onInit(self):
            self.title = 101
            self.msg = 102
            self.scrollbar = 103
            self.okbutton = 201
            self.show_dialog()

        def show_dialog(self):
            self.getControl(self.title).setLabel(title)
            self.getControl(self.msg).setText(msg)
            self.setFocusId(self.scrollbar)

        def onClick(self, controlid):
            if controlid == self.okbutton:
                self.close()

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU or action == ACTION_NAV_BACK:
                self.close()

    tb = TextBox("Textbox.xml", CONFIG.PATH, 'DefaultSkin', title=title, msg=msg)
    tb.doModal()
    del tb


def show_contact(msg=""):
    class ContactWindow(xbmcgui.WindowXMLDialog):
        def __init__(self, *args, **kwargs):
            self.title = CONFIG.THEME3 % kwargs["title"]
            self.image = kwargs["image"]
            self.fanart = kwargs["fanart"]
            self.msg = CONFIG.THEME2 % kwargs["msg"]

        def onInit(self):
            self.fanartimage = 101
            self.titlebox = 102
            self.imagecontrol = 103
            self.textbox = 104
            self.scrollcontrol = 105
            self.show_dialog()

        def show_dialog(self):
            self.getControl(self.imagecontrol).setImage(self.image)
            self.getControl(self.fanartimage).setImage(self.fanart)
            self.getControl(self.fanartimage).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setText(self.msg)
            self.getControl(self.titlebox).setLabel(self.title)
            self.setFocusId(self.scrollcontrol)

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU or action == ACTION_NAV_BACK:
                self.close()

    cw = ContactWindow("Contact.xml", CONFIG.PATH, 'DefaultSkin', title=CONFIG.ADDONTITLE, fanart=CONFIG.CONTACTFANART,
                  image=CONFIG.CONTACTICON, msg=msg)
    cw.doModal()
    del cw


def show_qr_code(layout, imagefile, message):
    class QRCode(xbmcgui.WindowXMLDialog):
        def __init__(self, *args, **kwargs):
            self.image = kwargs["image"]
            self.text = kwargs["text"]

        def onInit(self):
            self.imagecontrol = 501
            self.textbox = 502
            self.okbutton = 503
            self.title = 504
            self.show_dialog()

        def show_dialog(self):
            self.getControl(self.imagecontrol).setImage(self.image)
            self.getControl(self.textbox).setText(self.text)
            self.getControl(self.title).setLabel(CONFIG.ADDONTITLE)
            self.setFocus(self.getControl(self.okbutton))

        def onClick(self, controlid):
            if controlid == self.okbutton:
                self.close()

    qr = QRCode(layout, CONFIG.ADDON_PATH, 'DefaultSkin', image=imagefile, text=message)
    qr.doModal()
    del qr


def show_apk_warning(apk):
    class APKInstaller(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.shut = kwargs['close_time']
            xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
            xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")

        def onClick(self, controlid):
            self.close_window()

        def onAction(self, action):
            if action in [ACTION_PREVIOUS_MENU, ACTION_BACKSPACE, ACTION_NAV_BACK, ACTION_SELECT_ITEM,
                          ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_LONG_CLICK]:
                self.close_window()

        def close_window(self):
            xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
            xbmc.sleep(400)
            self.close()

    xbmc.executebuiltin('Skin.SetString(apkinstaller, Now that {0} has been downloaded[CR]Click install on the next window!)'.format(apk))
    popup = APKInstaller('APK.xml', CONFIG.ADDON_PATH, 'DefaultSkin', close_time=34)
    popup.doModal()
    del popup


def show_speed_test(img):
    class SpeedTest(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.imgfile = kwargs['img']

        def onInit(self):
            self.imagespeed = 101
            self.button = 201
            self.show_dialog()

        def show_dialog(self):
            self.setFocus(self.getControl(self.button))
            self.getControl(self.imagespeed).setImage(self.imgfile)

        def onClick(self, controlid):
            self.close_window()

        def onAction(self, action):
            if action in [ACTION_PREVIOUS_MENU, ACTION_BACKSPACE, ACTION_NAV_BACK, ACTION_SELECT_ITEM,
                          ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_LONG_CLICK]:
                self.close_window()

        def close_window(self):
            self.close()

    popup = SpeedTest('SpeedTest.xml', CONFIG.ADDON_PATH, 'DefaultSkin', img=img)
    popup.doModal()
    del popup


def show_save_data_settings():
    class FirstRun(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.whitelistcurrent = kwargs['current']

        def onInit(self):
            self.title = 101
            self.okbutton = 201
            self.trakt = 301
            self.debrid = 302
            self.login = 303
            self.sources = 304
            self.profiles = 305
            self.playercore = 314
            self.advanced = 306
            self.favourites = 307
            self.superfav = 308
            self.repo = 309
            self.whitelist = 310
            self.cache = 311
            self.packages = 312
            self.thumbs = 313
            self.show_dialog()
            self.controllist = [self.trakt, self.debrid, self.login,
                                    self.sources, self.profiles, self.playercore, self.advanced,
                                    self.favourites, self.superfav, self.repo,
                                    self.whitelist, self.cache, self.packages,
                                    self.thumbs]
            self.controlsettings = ['keeptrakt', 'keepdebrid', 'keeplogin',
                                    'keepsources', 'keepprofiles', 'keepplayercore', 'keepadvanced',
                                    'keepfavourites', 'keeprepos', 'keepsuper',
                                    'keepwhitelist', 'clearcache', 'clearpackages',
                                    'clearthumbs']
            for item in self.controllist:
                if CONFIG.get_setting(self.controlsettings[self.controllist.index(item)]) == 'true':
                    self.getControl(item).setSelected(True)

        def show_dialog(self):
            self.getControl(self.title).setLabel(CONFIG.ADDONTITLE)
            self.setFocus(self.getControl(self.okbutton))

        def onClick(self, controlid):
            if controlid == self.okbutton:

                for item in self.controllist:
                    at = self.controllist.index(item)
                    if self.getControl(item).isSelected():
                        CONFIG.set_setting(self.controlsettings[at], 'true')
                    else:
                        CONFIG.set_setting(self.controlsettings[at], 'false')

                if self.getControl(self.whitelist).isSelected() and not self.whitelistcurrent == 'true':
                    from resources.libs import whitelist
                    whitelist.whitelist('edit')

                self.close()

    fr = FirstRun("FirstRunSaveData.xml", CONFIG.ADDON_PATH, 'DefaultSkin', current=CONFIG.KEEPWHITELIST)
    fr.doModal()
    del fr


def show_build_prompt():
    class BuildPrompt(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.title = CONFIG.THEME3 % CONFIG.ADDONTITLE
            self.msg = "Currently no build installed from {0}.\n\nSelect 'Build Menu' to install a Community Build from us or 'Ignore' to never see this message again.\n\nThank you for choosing {1}.".format(CONFIG.ADDONTITLE, CONFIG.ADDONTITLE)
            self.msg = CONFIG.THEME2 % self.msg

        def onInit(self):
            self.image = 101
            self.titlebox = 102
            self.textbox = 103
            self.buildmenu = 201
            self.ignore = 202
            self.show_dialog()


        def show_dialog(self):
            self.getControl(self.image).setImage(CONFIG.ADDON_FANART)
            self.getControl(self.image).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setText(self.msg)
            self.getControl(self.titlebox).setLabel(self.title)
            self.setFocusId(self.buildmenu)

        def do_build_menu(self):
            from resources.libs import logging
            logging.log("[Check Updates] [User Selected: Open Build Menu] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)),
                        level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))
            url = 'plugin://{0}/?mode=builds'.format(CONFIG.ADDON_ID)
            xbmc.executebuiltin('ActivateWindow(10025, "{0}", return)'.format(url))
            self.close()

        def do_ignore(self):
            from resources.libs import logging
            logging.log("[First Run] [User Selected: Ignore Build Menu] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)),
                        level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))
            self.close()

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU or action == ACTION_NAV_BACK:
                self.do_ignore()

        def onClick(self, controlid):
            if controlid == self.buildmenu:
                self.do_build_menu()
            else:
                self.do_ignore()

    fr = BuildPrompt("FirstRunBuild.xml", CONFIG.ADDON_PATH, 'DefaultSkin')
    fr.doModal()
    del fr


def show_update_window(name='Testing Window', current='1.0', new='1.1', icon=CONFIG.ADDON_ICON, fanart=CONFIG.ADDON_FANART):
    class UpdateWindow(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.name = CONFIG.THEME3 % kwargs['name']
            self.current = kwargs['current']
            self.new = kwargs['new']
            self.icon = kwargs['icon']
            self.fanart = kwargs['fanart']
            self.msgupdate = "Update avaliable for installed build:\n[COLOR {0}]{1}[/COLOR]\n\nCurrent Version: v[COLOR {2}]{3}[/COLOR]\nLatest Version: v[COLOR {4}]{5}[/COLOR]\n\n[COLOR {6}]*Recommened: Fresh install[/COLOR]".format(CONFIG.COLOR1, self.name, CONFIG.COLOR1, self.current, CONFIG.COLOR1, self.new, CONFIG.COLOR1)
            self.msgcurrent = "Running latest version of installed build:\n[COLOR {0}]{1}[/COLOR]\n\nCurrent Version: v[COLOR {2}]{3}[/COLOR]\nLatest Version: v[COLOR {4}]{5}[/COLOR]\n\n[COLOR {6}]*Recommended: Fresh install[/COLOR]".format(CONFIG.COLOR1, self.name, CONFIG.COLOR1, self.current, CONFIG.COLOR1, self.new, CONFIG.COLOR1)

        def onInit(self):
            self.imagefanart = 101
            self.header = 102
            self.textbox = 103
            self.imageicon = 104
            self.fresh = 201
            self.normal = 202
            self.ignore = 203
            self.show_dialog()

        def show_dialog(self):
            self.getControl(self.header).setLabel(self.name)
            self.getControl(self.textbox).setText(CONFIG.THEME2 % self.msgupdate if current < new else self.msgcurrent)
            self.getControl(self.imagefanart).setImage(self.fanart)
            self.getControl(self.imagefanart).setColorDiffuse('2FFFFFFF')
            self.getControl(self.imageicon).setImage(self.icon)
            self.setFocusId(self.fresh)

        def do_fresh_install(self):
            from resources.libs import logging
            logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] [User Selected: Fresh Install build]".format(CONFIG.BUILDVERSION, CONFIG.LATESTVERSION), level=xbmc.LOGNOTICE)
            logging.log("[Check Updates] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))
            url = 'plugin://{0}/?mode=install&name={1}&url=fresh'.format(CONFIG.ADDON_ID, quote_plus(CONFIG.BUILDNAME))
            xbmc.executebuiltin('RunPlugin({0})'.format(url))
            self.close()


        def do_normal_install(self):
            from resources.libs import logging
            logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] [User Selected: Normal Install build]".format(CONFIG.BUILDVERSION, CONFIG.LATESTVERSION), level=xbmc.LOGNOTICE)
            logging.log("[Check Updates] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))
            url = 'plugin://{0}/?mode=install&name={1}&url=normal'.format(CONFIG.ADDON_ID, quote_plus(CONFIG.BUILDNAME))
            xbmc.executebuiltin('RunPlugin({0})'.format(url))
            self.close()

        def do_ignore(self):
            from resources.libs import logging
            from resources.libs import tools
            logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] [User Selected: Ignore 3 Days]".format(CONFIG.BUILDVERSION, CONFIG.LATESTVERSION), level=xbmc.LOGNOTICE)
            logging.log("[Check Updates] [Next Check: {0}]".format(str(tools.get_date(days=3))), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(tools.get_date(days=3)))
            self.close()

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU or action == ACTION_NAV_BACK:
                self.do_ignore()

        def onClick(self, controlid):
            if controlid == self.fresh:
                self.do_fresh_install()
            elif controlid == self.normal:
                self.do_normal_install()
            else:
                self.do_ignore()

    update = UpdateWindow("BuildUpdate.xml", CONFIG.ADDON_PATH, 'DefaultSkin', name=name, current=current, new=new, icon=icon, fanart=fanart)
    update.doModal()
    del update


def split_notify(notify):
    from resources.libs import tools
    link = tools.open_url(notify).replace('\r', '').replace('\t', '').replace('\n', '[CR]')
    if link.find('|||') == -1:
        return False, False
    id, msg = link.split('|||')
    if msg.startswith('[CR]'):
        msg = msg[4:]
    return id.replace('[CR]', ''), msg


def show_notification(msg='', test=False):
    class Notification(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.test = kwargs['test']
            self.message = CONFIG.THEME2 % kwargs['msg']

        def onInit(self):
            self.image = 101
            self.titlebox = 102
            self.titleimage = 103
            self.textbox = 104
            self.scroller = 105
            self.dismiss = 201
            self.remindme = 202
            self.show_dialog()

        def show_dialog(self):
            self.testimage = os.path.join(CONFIG.ART, 'text.png')
            self.getControl(self.image).setImage(CONFIG.BACKGROUND)
            self.getControl(self.image).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setText(self.message)
            self.setFocusId(self.remindme)
            if CONFIG.HEADERTYPE == 'Text':
                self.getControl(self.titlebox).setLabel(CONFIG.THEME3 % CONFIG.HEADERMESSAGE)
            else:
                self.getControl(self.titleimage).setImage(CONFIG.HEADERIMAGE)

        def do_remind(self):
            from resources.libs import logging
            if not test:
                CONFIG.set_setting("notedismiss", "false")
            logging.log("[Notification] NotifyID {0} Remind Me Later".format(CONFIG.get_setting('noteid')),
                        level=xbmc.LOGNOTICE)
            self.close()

        def do_dismiss(self):
            from resources.libs import logging
            if not test:
                CONFIG.set_setting("notedismiss", "true")
            logging.log("[Notification] NotifyID {0} Dismissed".format(CONFIG.get_setting('noteid')),
                        level=xbmc.LOGNOTICE)
            self.close()

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU or action == ACTION_NAV_BACK:
                self.do_remind()

        def onClick(self, controlid):
            if controlid == self.dismiss:
                self.do_dismiss()
            else:
                self.do_remind()

    xbmc.executebuiltin('Skin.SetString(headertexttype, {0})'.format('true' if CONFIG.HEADERTYPE == 'Text' else 'false'))
    xbmc.executebuiltin('Skin.SetString(headerimagetype, {0})'.format('true' if CONFIG.HEADERTYPE == 'Image' else 'false'))
    notify = Notification("Notifications.xml", CONFIG.ADDON_PATH, 'DefaultSkin', msg=msg, test=test)
    notify.doModal()
    del notify
