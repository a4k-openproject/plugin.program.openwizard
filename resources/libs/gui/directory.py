import xbmc
import xbmcgui
import xbmcplugin

import sys

try:  # Python 3
    from urllib.parse import quote_plus
except ImportError:  # Python 2
    from urllib import quote_plus

from resources.libs.config import CONFIG


def set_view():
    if CONFIG.get_setting('auto-view') == 'true':
        view_type = CONFIG.get_setting('viewType')

        xbmc.executebuiltin("Container.SetViewMode({0})".format(view_type))


def add_separator(middle='', fanart=CONFIG.ADDON_FANART, icon=CONFIG.ADDON_ICON, themeit=CONFIG.THEME3):
    if CONFIG.HIDESPACERS == 'No':
        char = CONFIG.SPACER
        ret = char * 40

        if not middle == '':
            middle = '[ {0} ]'.format(middle)
            fluff = int((40 - len(middle)) / 2)
            ret = "{0}{1}{2}".format(ret[:fluff], middle, ret[:fluff + 2])

        add_file(ret[:40], fanart=fanart, icon=icon, themeit=themeit)


def add_file(display, mode=None, name=None, url=None, menu=None, description=CONFIG.ADDONTITLE, overwrite=True,
             fanart=CONFIG.ADDON_FANART, icon=CONFIG.ADDON_ICON, themeit=None, isFolder=False):
    _add_menu_item(display, mode, name, url, menu, description, overwrite, fanart, icon, themeit, isFolder)


def add_dir(display, mode=None, name=None, url=None, menu=None, description=CONFIG.ADDONTITLE, overwrite=True,
            fanart=CONFIG.ADDON_FANART, icon=CONFIG.ADDON_ICON, themeit=None, isFolder=True):
    _add_menu_item(display, mode, name, url, menu, description, overwrite, fanart, icon, themeit, isFolder)


def _add_menu_item(display, mode, name, url, menu, description, overwrite, fanart, icon, themeit, isFolder):
    u = sys.argv[0]

    if mode is not None:
        u += "?mode={0}".format(quote_plus(mode))
    if name is not None:
        u += "&name={0}".format(quote_plus(name))
    if url is not None:
        u += "&url={0}".format(quote_plus(url))
    ok = True
    if themeit:
        display = themeit.format(display)
    liz = xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo(type="Video", infoLabels={"Title": display, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    if menu is not None:
        liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
    return ok
