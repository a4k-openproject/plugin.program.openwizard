import xbmcgui

from resources.libs import vars


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

        def onClick(self, controlId):
            if controlId == self.okbutton:
                self.close()

        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU:
                self.close()
            elif action == ACTION_NAV_BACK:
                self.close()

    tb = TextBoxes("Textbox.xml", vars.PATH, 'DefaultSkin', title=title, msg=msg)
    tb.doModal()
    del tb
