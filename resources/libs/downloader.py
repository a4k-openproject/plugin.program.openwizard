################################################################################
#      Copyright (C) 2019 drinfernoo                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc
import xbmcgui

import sys
import time

try:  # Python 3
    from urllib.request import urlretrieve
except ImportError:  # Python 2
    from urllib import urlretrieve

from resources.libs.common.config import CONFIG


def download(url, dest):
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(CONFIG.ADDONTITLE, "Downloading Content", ' ', ' ')
    progress_dialog.update(0)
    start_time = time.time()
    urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, progress_dialog, start_time))


def _pbhook(numblocks, blocksize, filesize, dp, start_time):
    from resources.libs.common import logging

    try:
        percent = min(numblocks * blocksize * 100 / filesize, 100)
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
        kbps_speed = numblocks * blocksize / (time.time() - start_time)
        if kbps_speed > 0 and not percent >= 100:
            eta = (filesize - numblocks * blocksize) / kbps_speed
        else:
            eta = 0
        kbps_speed = kbps_speed / 1024
        type_speed = 'KB'
        if kbps_speed >= 1024:
            kbps_speed = kbps_speed / 1024
            type_speed = 'MB'
        total = float(filesize) / (1024 * 1024)
        mbs = '[COLOR %s][B]Size:[/B] [COLOR %s]%.02f[/COLOR] MB of [COLOR %s]%.02f[/COLOR] MB[/COLOR]' % (CONFIG.COLOR2, CONFIG.COLOR1, currently_downloaded, CONFIG.COLOR1, total)
        speed = '[COLOR %s][B]Speed:[/B] [COLOR %s]%.02f [/COLOR]%s/s ' % (CONFIG.COLOR2, CONFIG.COLOR1, kbps_speed, type_speed)
        div = divmod(eta, 60)
        speed += '[B]ETA:[/B] [COLOR %s]%02d:%02d[/COLOR][/COLOR]' % (CONFIG.COLOR1, div[0], div[1])
        dp.update(int(percent), '', mbs, speed)
    except Exception as e:
        logging.log("ERROR Downloading: {0}".format(e), level=xbmc.LOGERROR)
        return e
    if dp.iscanceled():
        dp.close()
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]Download Cancelled[/COLOR]".format(CONFIG.COLOR2))
        sys.exit()
