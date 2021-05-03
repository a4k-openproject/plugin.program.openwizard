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

import requests
import sys
import os
import time

from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common.config import CONFIG


class Downloader:
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
        self.progress_dialog = xbmcgui.DialogProgress()

    def download(self, url, dest):
        self.progress_dialog.create(CONFIG.ADDONTITLE, "Downloading Content", ' ', ' ')
        self.progress_dialog.update(0)
        
        path = os.path.split(dest)[0]
        if not os.path.exists(path):
            os.makedirs(path)
        with open(dest, 'wb') as f:
            response = tools.open_url(url, stream=True)
            
            if not response:
                logging.log_notify(CONFIG.ADDONTITLE,
                                   '[COLOR {0}]Build Install: Invalid Zip Url![/COLOR]'.format(CONFIG.COLOR2))
                return
            else:
                total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                start_time = time.time()
                mb = 1024*1024
                
                for chunk in response.iter_content(chunk_size=max(int(total/512), mb)):
                    downloaded += len(chunk)
                    f.write(chunk)
                    
                    done = int(100 * downloaded / total)
                    kbps_speed = downloaded / (time.time() - start_time)
                    
                    if kbps_speed > 0 and not done >= 100:
                        eta = (total - downloaded) / kbps_speed
                    else:
                        eta = 0
                    
                    kbps_speed = kbps_speed / 1024
                    type_speed = 'KB'
                    
                    if kbps_speed >= 1024:
                        kbps_speed = kbps_speed / 1024
                        type_speed = 'MB'
                        
                    currently_downloaded = '[COLOR %s][B]Size:[/B] [COLOR %s]%.02f[/COLOR] MB of [COLOR %s]%.02f[/COLOR] MB[/COLOR]' % (CONFIG.COLOR2, CONFIG.COLOR1, downloaded / mb, CONFIG.COLOR1, total / mb)
                    speed = '[COLOR %s][B]Speed:[/B] [COLOR %s]%.02f [/COLOR]%s/s ' % (CONFIG.COLOR2, CONFIG.COLOR1, kbps_speed, type_speed)
                    div = divmod(eta, 60)
                    speed += '[B]ETA:[/B] [COLOR %s]%02d:%02d[/COLOR][/COLOR]' % (CONFIG.COLOR1, div[0], div[1])
                    
                    self.progress_dialog.update(done, '', currently_downloaded, speed)
