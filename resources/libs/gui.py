import xbmcgui

import os

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


def TextBox(title, msg):
    class TextBoxes(xbmcgui.WindowXMLDialog):
        def onInit(self):
            self.title = 101
            self.msg = 102
            self.scrollbar = 103
            self.okbutton = 201
            self.showdialog()

        def showdialog(self):
            self.getControl(self.title).setLabel(title)
            self.getControl(self.msg).setText(msg)
            self.setFocusId(self.scrollbar)

        def onClick(self, controlid):
            if controlid == self.okbutton:
                self.close()

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU:
                self.close()
            elif action == ACTION_NAV_BACK:
                self.close()

    tb = TextBoxes("Textbox.xml", CONFIG.PATH, 'DefaultSkin', title=title, msg=msg)
    tb.doModal()
    del tb


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


def contact(msg=""):
    class MyWindow(xbmcgui.WindowXMLDialog):
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
            self.showdialog()

        def showdialog(self):
            self.getControl(self.imagecontrol).setImage(self.image)
            self.getControl(self.fanartimage).setImage(self.fanart)
            self.getControl(self.fanartimage).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setText(self.msg)
            self.getControl(self.titlebox).setLabel(self.title)
            self.setFocusId(self.scrollcontrol)

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU:
                self.close()
            elif action == ACTION_NAV_BACK:
                self.close()

    cw = MyWindow("Contact.xml", CONFIG.PATH, 'DefaultSkin', title=CONFIG.ADDONTITLE, fanart=CONFIG.CONTACTFANART,
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
            self.showdialog()

        def showdialog(self):
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
