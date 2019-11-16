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

import os

try:  # Python 3
    from urllib.parse import quote_plus
except ImportError:  # Python 2
    from urllib import quote_plus

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.gui import window


def writeAdvanced():
    if CONFIG.RAM > 1536:
        buffer = '209715200'
    else:
        buffer = '104857600'
    with open(CONFIG.ADVANCED, 'w+') as f:
        f.write('<advancedsettings>\n')
        f.write('	<network>\n')
        f.write('		<buffermode>2</buffermode>\n')
        f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % buffer)
        f.write('		<readbufferfactor>5</readbufferfactor>\n')
        f.write('		<curlclienttimeout>10</curlclienttimeout>\n')
        f.write('		<curllowspeedtime>10</curllowspeedtime>\n')
        f.write('	</network>\n')
        f.write('</advancedsettings>\n')
    f.close()


def autoConfig(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
    class MyWindow(xbmcgui.WindowDialog):
        scr = {}

        def __init__(self, msg='', L=0, T=0, W=1280, H=720, TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
            buttonfocus, buttonnofocus = window.get_artwork('button')
            radiobgfocus, radiobgnofocus, radiofocus, radionofocus = window.get_artwork('radio')
            slidernibfocus, slidernibnofocus, sliderfocus, slidernofocus = window.get_artwork('slider')
            image_path = os.path.join(CONFIG.ART, 'ContentPanel.png')
            boxbg = os.path.join(CONFIG.ART, 'bgg2.png')
            self.border = xbmcgui.ControlImage(L, T, W, H, image_path)
            self.addControl(self.border)
            self.BG = xbmcgui.ControlImage(L + BorderWidth, T + BorderWidth, W - (BorderWidth*2), H - (BorderWidth*2), CONFIG.ADDON_FANART, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
            self.addControl(self.BG)
            top = T + BorderWidth
            leftside = L + BorderWidth
            rightside = L + (W/2)-(BorderWidth*2)
            firstrow = top + 30
            secondrow = firstrow + 275 + (BorderWidth/2)
            currentwidth = ((W/2) - (BorderWidth*4))/2

            header = '[COLOR {0}]Advanced Settings Configurator[/COLOR]'.format(CONFIG.COLOR2)
            self.Header = xbmcgui.ControlLabel(L, top, W, 30, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header)
            top += 30+BorderWidth
            self.bgarea = xbmcgui.ControlImage(leftside, firstrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
            self.addControl(self.bgarea)
            self.bgarea2 = xbmcgui.ControlImage(rightside+BorderWidth+BorderWidth, firstrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
            self.addControl(self.bgarea2)
            self.bgarea3 = xbmcgui.ControlImage(leftside, secondrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
            self.addControl(self.bgarea3)
            self.bgarea4 = xbmcgui.ControlImage(rightside+BorderWidth+BorderWidth, secondrow, rightside-L, 275, boxbg, aspectRatio=0, colorDiffuse='0x5FFFFFFF')
            self.addControl(self.bgarea4)

            header = '[COLOR {0}]Video Cache Size[/COLOR]'.format(CONFIG.COLOR2)
            self.Header2 = xbmcgui.ControlLabel(leftside+BorderWidth, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header2)
            freeMemory = int(float(xbmc.getInfoLabel('System.Memory(free)')[:-2])*.33)
            recMemory = int(float(xbmc.getInfoLabel('System.Memory(free)')[:-2])*.23)
            msg3 = "[COLOR {0}]Number of bytes used for buffering streams in memory.  When set to [COLOR {1}]0[/COLOR] the cache will be written to disk instead of RAM.  Note: For the memory size set here, Kodi will require 3x the amount of RAM to be free. Setting this too high might cause Kodi to crash if it can't get enough RAM(1/3 of Free Memory: [COLOR {2}]{3}[/COLOR])[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, CONFIG.COLOR1, freeMemory)
            self.Support3 = xbmcgui.ControlTextBox(leftside + int(BorderWidth*1.5), firstrow + 30 + BorderWidth, (W/2) - (BorderWidth*4), 150, font='font12', textColor=TxtColor)
            self.addControl(self.Support3)
            self.Support3.setText(msg3)
            try:
                self.videoCacheSize = xbmcgui.ControlSlider(leftside + int(BorderWidth*1.5), firstrow+210, (W/2) - (BorderWidth*5), 20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL)
            except:
                self.videoCacheSize = xbmcgui.ControlSlider(leftside + int(BorderWidth*1.5), firstrow+210, (W/2) - (BorderWidth*5), 20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
            self.addControl(self.videoCacheSize)
            self.videomin = 0
            self.videomax = freeMemory if freeMemory < 2000 else 2000
            self.recommendedVideo = recMemory if recMemory < 500 else 500
            self.currentVideo = self.recommendedVideo
            videopos = tools.percentage(self.currentVideo, self.videomax)
            self.videoCacheSize.setPercent(videopos)
            current1 = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2} MB[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.currentVideo)
            recommended1 = '[COLOR {0}]Recommended:[/COLOR] [COLOR {1}]{2} MB[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.recommendedVideo)
            self.currentVideo1 = xbmcgui.ControlTextBox(leftside + BorderWidth, firstrow + 235, currentwidth, 20, font=Font, textColor=TxtColor)
            self.addControl(self.currentVideo1)
            self.currentVideo1.setText(current1)
            self.recommendedVideo1 = xbmcgui.ControlTextBox(leftside + BorderWidth + currentwidth, firstrow + 235, currentwidth, 20, font=Font, textColor=TxtColor)
            self.addControl(self.recommendedVideo1)
            self.recommendedVideo1.setText(recommended1)

            header = '[COLOR {0}]CURL Timeout/CURL Low Speed[/COLOR]'.format(CONFIG.COLOR2)
            self.Header3=xbmcgui.ControlLabel(rightside+BorderWidth, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header3)
            msg3 = "[COLOR {0}][B]curlclienttimeout[/B] is the time in seconds for how long it takes for libcurl connection will timeout and [B]curllowspeedtime[/B] is the time in seconds for libcurl to consider a connection lowspeed.  For slower connections set it to 20.[/COLOR]".format(CONFIG.COLOR2)
            self.Support3 = xbmcgui.ControlTextBox(rightside + int(BorderWidth*3.5), firstrow + 30 + BorderWidth, (W/2) - (BorderWidth*4), 150, font='font12', textColor=TxtColor)
            self.addControl(self.Support3)
            self.Support3.setText(msg3)
            try:
                self.CURLTimeout = xbmcgui.ControlSlider(rightside + int(BorderWidth*3.5), firstrow + 210, (W/2) - (BorderWidth*5), 20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL)
            except:
                self.CURLTimeout = xbmcgui.ControlSlider(rightside + int(BorderWidth*3.5), firstrow + 210, (W/2) - (BorderWidth*5), 20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
            self.addControl(self.CURLTimeout)
            self.curlmin = 0
            self.curlmax = 20
            self.recommendedCurl = 10
            self.currentCurl = self.recommendedCurl
            curlpos = tools.percentage(self.currentCurl, self.curlmax)
            self.CURLTimeout.setPercent(curlpos)
            current2 = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2}s[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.currentCurl)
            recommended2 = '[COLOR {0}]Recommended:[/COLOR] [COLOR {1}]{2}s[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.recommendedCurl)
            self.currentCurl2 = xbmcgui.ControlTextBox(rightside + (BorderWidth*3), firstrow + 235, currentwidth, 20,font=Font,textColor=TxtColor)
            self.addControl(self.currentCurl2)
            self.currentCurl2.setText(current2)
            self.recommendedCurl2 = xbmcgui.ControlTextBox(rightside + (BorderWidth*3) + currentwidth, firstrow + 235, currentwidth, 20,font=Font,textColor=TxtColor)
            self.addControl(self.recommendedCurl2)
            self.recommendedCurl2.setText(recommended2)

            header = '[COLOR {0}]Read Buffer Factor[/COLOR]'.format(CONFIG.COLOR2)
            self.Header4=xbmcgui.ControlLabel(leftside, secondrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header4)
            msg3 = "[COLOR {0}]The value of this setting is a multiplier of the default limit. If Kodi is loading a typical bluray raw file at 36 Mbit/s, then a value of 2 will need at least 72 Mbit/s of network bandwidth. However, unlike with the RAM setting, you can safely increase this value however high you want, and Kodi won't crash.[/COLOR]".format(CONFIG.COLOR2)
            self.Support3 = xbmcgui.ControlTextBox(leftside + int(BorderWidth*1.5), secondrow + 30 + BorderWidth, (W/2) - (BorderWidth*4), 150, font='font12', textColor=TxtColor)
            self.addControl(self.Support3)
            self.Support3.setText(msg3)
            try:
                self.readBufferFactor = xbmcgui.ControlSlider(leftside + int(BorderWidth*1.5), secondrow + 210, (W/2) - (BorderWidth*5), 20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL)
            except:
                self.readBufferFactor = xbmcgui.ControlSlider(leftside + int(BorderWidth*1.5), secondrow + 210, (W/2) - (BorderWidth*5), 20, textureback=sliderfocus, texture=slidernibnofocus, texturefocus=slidernibfocus)
            self.addControl(self.readBufferFactor)
            self.readmin = 0
            self.readmax = 10
            self.recommendedRead = 5
            self.currentRead = self.recommendedRead
            readpos = tools.percentage(self.currentRead, self.readmax)
            self.readBufferFactor.setPercent(readpos)
            current3 = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.currentRead)
            recommended3 = '[COLOR {0}]Recommended:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.recommendedRead)
            self.currentRead3 = xbmcgui.ControlTextBox(leftside + BorderWidth, secondrow + 235, currentwidth, 20, font=Font, textColor=TxtColor)
            self.addControl(self.currentRead3)
            self.currentRead3.setText(current3)
            self.recommendedRead3 = xbmcgui.ControlTextBox(leftside + BorderWidth + currentwidth, secondrow + 235, currentwidth, 20, font=Font, textColor=TxtColor)
            self.addControl(self.recommendedRead3)
            self.recommendedRead3.setText(recommended3)

            header = '[COLOR {0}]Buffer Mode[/COLOR]'.format(CONFIG.COLOR2)
            self.Header4 = xbmcgui.ControlLabel(rightside + BorderWidth, secondrow + 5, (W/2) - (BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header4)
            msg4 = "[COLOR {0}]This setting will force Kodi to use a cache for all video files, including local network, internet, and even the local hard drive. Default value is 0 and will only cache videos that use internet file paths/sources.[/COLOR]".format(CONFIG.COLOR2)
            self.Support4 = xbmcgui.ControlTextBox(rightside + int(BorderWidth*3.5), secondrow + 30 + BorderWidth, (W/2) - (BorderWidth*4), 110, font='font12', textColor=TxtColor)
            self.addControl(self.Support4)
            self.Support4.setText(msg4)
            B1 = secondrow + 130 + BorderWidth
            B2 = B1 + 30
            B3 = B2 + 30
            B4 = B3 + 30
            self.Button0 = xbmcgui.ControlRadioButton(rightside + (BorderWidth*3), B1, (W/2) - (BorderWidth*4), 30, '0: Buffer all internet filesystems', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
            self.Button1 = xbmcgui.ControlRadioButton(rightside + (BorderWidth*3), B2, (W/2) - (BorderWidth*4), 30, '1: Buffer all filesystems', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
            self.Button2 = xbmcgui.ControlRadioButton(rightside + (BorderWidth*3), B3, (W/2) - (BorderWidth*4), 30, '2: Only buffer true internet filesystems', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
            self.Button3 = xbmcgui.ControlRadioButton(rightside + (BorderWidth*3), B4, (W/2) - (BorderWidth*4), 30, '3: No Buffer', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
            self.addControl(self.Button0)
            self.addControl(self.Button1)
            self.addControl(self.Button2)
            self.addControl(self.Button3)
            self.Button0.setSelected(False)
            self.Button1.setSelected(False)
            self.Button2.setSelected(True)
            self.Button3.setSelected(False)

            self.buttonWrite = xbmcgui.ControlButton(leftside, T + H - 40 - BorderWidth, (W/2) - (BorderWidth*2), 35, "Write File", textColor="0xFF000000", focusedColor="0xFF000000", alignment=2, focusTexture=buttonfocus, noFocusTexture=buttonnofocus)
            self.buttonCancel=xbmcgui.ControlButton(rightside + BorderWidth*2, T + H - 40 - BorderWidth, (W/2) - (BorderWidth*2), 35, "Cancel", textColor="0xFF000000", focusedColor="0xFF000000", alignment=2, focusTexture=buttonfocus, noFocusTexture=buttonnofocus)
            self.addControl(self.buttonWrite)
            self.addControl(self.buttonCancel)

            self.buttonWrite.controlLeft(self.buttonCancel)
            self.buttonWrite.controlRight(self.buttonCancel)
            self.buttonWrite.controlUp(self.Button3)
            self.buttonWrite.controlDown(self.videoCacheSize)
            self.buttonCancel.controlLeft(self.buttonWrite)
            self.buttonCancel.controlRight(self.buttonWrite)
            self.buttonCancel.controlUp(self.Button3)
            self.buttonCancel.controlDown(self.videoCacheSize)
            self.videoCacheSize.controlUp(self.buttonWrite)
            self.videoCacheSize.controlDown(self.CURLTimeout)
            self.CURLTimeout.controlUp(self.videoCacheSize)
            self.CURLTimeout.controlDown(self.readBufferFactor)
            self.readBufferFactor.controlUp(self.CURLTimeout)
            self.readBufferFactor.controlDown(self.Button0)
            self.Button0.controlUp(self.CURLTimeout)
            self.Button0.controlDown(self.Button1)
            self.Button0.controlLeft(self.readBufferFactor)
            self.Button0.controlRight(self.readBufferFactor)
            self.Button1.controlUp(self.Button0)
            self.Button1.controlDown(self.Button2)
            self.Button1.controlLeft(self.readBufferFactor)
            self.Button1.controlRight(self.readBufferFactor)
            self.Button2.controlUp(self.Button1)
            self.Button2.controlDown(self.Button3)
            self.Button2.controlLeft(self.readBufferFactor)
            self.Button2.controlRight(self.readBufferFactor)
            self.Button3.controlUp(self.Button2)
            self.Button3.controlDown(self.buttonWrite)
            self.Button3.controlLeft(self.readBufferFactor)
            self.Button3.controlRight(self.readBufferFactor)
            self.setFocus(self.videoCacheSize)


        def updateCurrent(self, control):
            if control == self.videoCacheSize:
                self.currentVideo = (self.videomax)*self.videoCacheSize.getPercent()/100
                current = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2} MB[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, int(self.currentVideo))
                self.currentVideo1.setText(current)

            elif control == self.CURLTimeout:
                self.currentCurl = (self.curlmax)*self.CURLTimeout.getPercent()/100
                current = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2}s[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, int(self.currentCurl))
                self.currentCurl2.setText(current)

            elif control == self.readBufferFactor:
                self.currentRead = (self.readmax)*self.readBufferFactor.getPercent()/100
                current = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, int(self.currentRead))
                self.currentRead3.setText(current)

            elif control in [self.Button0, self.Button1, self.Button2, self.Button3]:
                self.Button0.setSelected(False)
                self.Button1.setSelected(False)
                self.Button2.setSelected(False)
                self.Button3.setSelected(False)
                control.setSelected(True)


        def doWrite(self):
            dialog = xbmcgui.Dialog()
            
            if self.Button0.isSelected():
                buffermode = 0
            elif self.Button1.isSelected():
                buffermode = 1
            elif self.Button2.isSelected():
                buffermode = 2
            elif self.Button3.isSelected():
                buffermode = 3
            if os.path.exists(CONFIG.ADVANCED):
                choice = dialog.yesno(CONFIG.ADDONTITLE,
                                          "[COLOR {0}]There is currently an active [COLOR {1}]advancedsettings.xml[/COLOR], would you like to remove it and continue?[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1),
                                          yeslabel="[B][COLOR springgreen]Remove Settings[/COLOR][/B]",
                                          nolabel="[B][COLOR red]Cancel Write[/COLOR][/B]")
                if choice == 0:
                    return
                try:
                    os.remove(CONFIG.ADVANCED)
                except:
                    f = open(CONFIG.ADVANCED, 'w');
                    f.close()
            if CONFIG.KODIV < 17:
                with open(CONFIG.ADVANCED, 'w+') as f:
                    f.write('<advancedsettings>\n')
                    f.write('	<network>\n')
                    f.write('		<buffermode>%s</buffermode>\n' % buffermode)
                    f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % int(self.currentVideo*1024*1024))
                    f.write('		<readbufferfactor>%s</readbufferfactor>\n' % self.currentRead)
                    f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
                    f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
                    f.write('	</network>\n')
                    f.write('</advancedsettings>\n')
                f.close()
            else:
                with open(CONFIG.ADVANCED, 'w+') as f:
                    f.write('<advancedsettings>\n')
                    f.write('	<cache>\n')
                    f.write('		<buffermode>%s</buffermode>\n' % buffermode)
                    f.write('		<memorysize>%s</memorysize>\n' % int(self.currentVideo*1024*1024))
                    f.write('		<readfactor>%s</readfactor>\n' % self.currentRead)
                    f.write('	</cache>\n')
                    f.write('	<network>\n')
                    f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
                    f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
                    f.write('	</network>\n')
                    f.write('</advancedsettings>\n')
                f.close()
            self.close()


        def onControl(self, control):
            if control == self.buttonWrite:
                self.doWrite()
            elif control == self.buttonCancel:
                self.close()


        def onAction(self, action):
            try:
                F = self.getFocus()
            except:
                F = False
            if F == self.videoCacheSize:
                self.updateCurrent(self.videoCacheSize)
            elif F == self.CURLTimeout:
                self.updateCurrent(self.CURLTimeout)
            elif F == self.readBufferFactor:
                self.updateCurrent(self.readBufferFactor)
            elif F in [self.Button0, self.Button1, self.Button2, self.Button3] and action in [window.ACTION_MOUSE_LEFT_CLICK, window.ACTION_SELECT_ITEM]:
                self.updateCurrent(F)
            elif action == window.ACTION_PREVIOUS_MENU:
                self.close()
            elif action == window.ACTION_NAV_BACK:
                self.close()

    maxW = 1280
    maxH = 720
    W = int(900)
    H = int(650)
    L = int((maxW-W)/2)
    T = int((maxH-H)/2);
    TempWindow = MyWindow(L=L, T=T, W=W, H=H, TxtColor=TxtColor, Font=Font, BorderWidth=BorderWidth)
    TempWindow.doModal()
    del TempWindow


def QautoConfig(msg='', TxtColor='0xFFFFFFFF', Font='font10', BorderWidth=10):
    class MyWindow(xbmcgui.WindowDialog):
        scr = {}

        def __init__(self, msg='', L=0, T=0, W=1280, H=720, TxtColor='0xFFFFFFFF', Font='font10', BorderWidth=10):
            buttonfocus, buttonnofocus = window.get_artwork('button')
            self.BG = xbmcgui.ControlImage(L+BorderWidth, T+BorderWidth, W-(BorderWidth*2), H-(BorderWidth*2), CONFIG.ADDON_FANART, aspectRatio=0)
            self.addControl(self.BG)
            top = T+BorderWidth
            leftside = L+BorderWidth
            rightside = L+(W/2)-(BorderWidth*2)
            header = '[COLOR {0}]Quick Advanced Settings Configurator[/COLOR]'.format(CONFIG.COLOR2)
            self.Header=xbmcgui.ControlLabel(L, top, W, 30, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header)
            top += 30+BorderWidth
            freeMemory = int(float(tools.get_info_label('System.Memory(free)')[:-2]) * .33)
            recMemory = int(float(tools.get_info_label('System.Memory(free)')[:-2]) * .23)
            self.videomin = 0
            self.videomax = freeMemory if freeMemory < 2000 else 2000
            self.recommendedVideo = recMemory if recMemory < 500 else 500
            self.currentVideo = self.recommendedVideo
            current1 = '[COLOR {0}]Video Cache Size[/COLOR]=[COLOR {1}]{2} MB[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.currentVideo)
            recommended1 = '[COLOR {0}]Video Cache Size:[/COLOR] [COLOR {1}]{2} MB[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.recommendedVideo)
            self.curlmin = 0
            self.curlmax = 20
            self.recommendedCurl = 10
            self.currentCurl = self.recommendedCurl
            curlpos = tools.percentage(self.currentCurl, self.curlmax)
            recommended2 = '[COLOR {0}]CURL Timeout/CURL Low Speed:[/COLOR] [COLOR {1}]{2}s[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.recommendedCurl)
            self.readmin = 0
            self.readmax = 10
            self.recommendedRead = 5
            self.currentRead = self.recommendedRead
            readpos = tools.percentage(self.currentRead, self.readmax)
            recommended3 = '[COLOR {0}]Read Buffer Factor:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, self.recommendedRead)
            recommended4 = '[COLOR {0}]Buffer Mode:[/COLOR] [COLOR {1}]2[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2)
            msgbox = '[COLOR {0}]These settings will be written to the advancedsettings.xml[/COLOR]\r\n\r\n{1}\r\n{2}\r\n{3}\r\n{4}'.format(CONFIG.COLOR1, recommended4, recommended1, recommended3, recommended2)
            self.box = xbmcgui.ControlTextBox(L+25, T+50, W, H, font='font14')
            self.addControl(self.box)
            self.box.setText(msgbox)
            self.buttonWrite = xbmcgui.ControlButton(leftside, T+H-40-BorderWidth, (W/2)-(BorderWidth*2), 35, "Write File", textColor="0xFF000000", focusedColor="0xFF000000", alignment=2, focusTexture=buttonfocus, noFocusTexture=buttonnofocus)
            self.buttonCancel = xbmcgui.ControlButton(rightside+BorderWidth*2, T+H-40-BorderWidth, (W/2)-(BorderWidth*2), 35, "Cancel", textColor="0xFF000000", focusedColor="0xFF000000", alignment=2, focusTexture=buttonfocus, noFocusTexture=buttonnofocus)
            self.addControl(self.buttonWrite)
            self.addControl(self.buttonCancel)
            self.setFocus(self.buttonCancel)
            self.buttonWrite.controlLeft(self.buttonCancel)
            self.buttonWrite.controlRight(self.buttonCancel)
            self.buttonCancel.controlLeft(self.buttonWrite)
            self.buttonCancel.controlRight(self.buttonWrite)

        def updateCurrent(self, control):
            if control == self.videoCacheSize:
                self.currentVideo = (self.videomax)*self.videoCacheSize.getPercent()/100
                current = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2} MB[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, int(self.currentVideo))
                self.currentVideo1.setText(current)

            elif control == self.CURLTimeout:
                self.currentCurl = (self.curlmax)*self.CURLTimeout.getPercent()/100
                current = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2}s[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, int(self.currentCurl))
                self.currentCurl2.setText(current)

            elif control == self.readBufferFactor:
                self.currentRead = (self.readmax)*self.readBufferFactor.getPercent()/100
                current = '[COLOR {0}]Current:[/COLOR] [COLOR {1}]{2}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.COLOR2, int(self.currentRead))
                self.currentRead3.setText(current)


        def doWrite(self):
            dialog = xbmcgui.Dialog()
            
            buffermode = 2
            if os.path.exists(CONFIG.ADVANCED):
                choice = dialog.yesno(CONFIG.ADDONTITLE,
                                          "[COLOR {0}]There is currently an active [COLOR {1}]advancedsettings.xml[/COLOR], would you like to remove it and continue?[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1),
                                          yeslabel="[B][COLOR green]Remove Settings[/COLOR][/B]",
                                          nolabel="[B][COLOR red]Cancel Write[/COLOR][/B]")
                if choice == 0:
                    return
                try:
                    os.remove(CONFIG.ADVANCED)
                except:
                    f = open(CONFIG.ADVANCED, 'w'); f.close()
            if CONFIG.KODIV < 17:
                with open(CONFIG.ADVANCED, 'w+') as f:
                    f.write('<advancedsettings>\n')
                    f.write('	<network>\n')
                    f.write('		<buffermode>%s</buffermode>\n' % buffermode)
                    f.write('		<cachemembuffersize>%s</cachemembuffersize>\n' % int(self.currentVideo*1024*1024))
                    f.write('		<readbufferfactor>%s</readbufferfactor>\n' % self.currentRead)
                    f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
                    f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
                    f.write('	</network>\n')
                    f.write('</advancedsettings>\n')
                f.close()
            else:
                with open(CONFIG.ADVANCED, 'w+') as f:
                    f.write('<advancedsettings>\n')
                    f.write('	<cache>\n')
                    f.write('		<buffermode>%s</buffermode>\n' % buffermode)
                    f.write('		<memorysize>%s</memorysize>\n' % int(self.currentVideo*1024*1024))
                    f.write('		<readfactor>%s</readfactor>\n' % self.currentRead)
                    f.write('	</cache>\n')
                    f.write('	<network>\n')
                    f.write('		<curlclienttimeout>%s</curlclienttimeout>\n' % self.currentCurl)
                    f.write('		<curllowspeedtime>%s</curllowspeedtime>\n' % self.currentCurl)
                    f.write('	</network>\n')
                    f.write('</advancedsettings>\n')
                f.close()
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                                   '[COLOR {0}]advancedsettings.xml has been written[/COLOR]'.format(CONFIG.COLOR2))
            self.close()


        def onControl(self, control):
            if control == self.buttonWrite:
                self.doWrite()
            elif control == self.buttonCancel:
                self.close()


        def onAction(self, action):
            try:
                F = self.getFocus()
            except:
                F = False
            if action == window.ACTION_PREVIOUS_MENU:
                self.close()
            elif action == window.ACTION_NAV_BACK:
                self.close()

    maxW = 1280
    maxH = 720
    W = int(700)
    H = int(350)
    L = int((maxW-W)/2)
    T = int((maxH-H)/2)
    TempWindow = MyWindow(L=L, T=T, W=W, H=H, TxtColor=TxtColor, Font=Font, BorderWidth=BorderWidth);
    TempWindow.doModal()
    del TempWindow


def write_advanced(name, url):
    from resources.libs.common import tools
    from resources.libs.common import logging
    
    dialog = xbmcgui.Dialog()

    response = tools.open_url(url)
    
    if response:
        if os.path.exists(CONFIG.ADVANCED):
            choice = dialog.yesno(CONFIG.ADDONTITLE,
                                      "[COLOR {0}]Would you like to overwrite your current Advanced Settings with [COLOR {1}]{}[/COLOR]?[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, name),
                                      yeslabel="[B][COLOR springgreen]Overwrite[/COLOR][/B]",
                                      nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
        else:
            choice = dialog.yesno(CONFIG.ADDONTITLE,
                                      "[COLOR {0}]Would you like to download and install [COLOR {1}]{2}[/COLOR]?[/COLOR]".format(CONFIG.COLOR2, CONFIG.COLOR1, name),
                                      yeslabel="[B][COLOR springgreen]Install[/COLOR][/B]",
                                      nolabel="[B][COLOR red]Cancel[/COLOR][/B]")

        if choice == 1:
            tools.write_to_file(CONFIG.ADVANCED, response.text)
            dialog.ok(CONFIG.ADDONTITLE,
                          '[COLOR {0}]AdvancedSettings.xml file has been successfully written. Once you click okay it will force close kodi.[/COLOR]'.format(CONFIG.COLOR2))
            tools.kill_kodi(over=True)
        else:
            logging.log("[Advanced Settings] install canceled")
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                               "[COLOR {0}]Write Cancelled![/COLOR]".format(CONFIG.COLOR2))
            return
    else:
        logging.log("[Advanced Settings] URL not working: {0}".format(url))
        logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]URL Not Working[/COLOR]".format(CONFIG.COLOR2))


def view_advanced():
    from resources.libs.common import tools
    from resources.libs.gui import window

    window.show_text_box(CONFIG.ADDONTITLE, tools.read_from_file(CONFIG.ADVANCED).replace('\t', '    '))


def remove_advanced():
    from resources.libs.common import tools
    from resources.libs.common import logging

    if os.path.exists(CONFIG.ADVANCED):
        tools.remove_file(CONFIG.ADVANCED)
    else:
        logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, CONFIG.ADDONTITLE),
                           "[COLOR {0}]AdvancedSettings.xml not found[/COLOR]".format(CONFIG.COLOR2))

