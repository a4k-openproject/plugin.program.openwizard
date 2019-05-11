################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
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
except ImportError:  # Python 3
    from urllib import quote_plus

from resources.libs.config import CONFIG
from resources.libs import gui
from resources.libs import logging
from resources.libs import tools
from resources.libs import whitelist


def autoConfig(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
    class MyWindow(xbmcgui.WindowDialog):
        scr = {}

        def __init__(self, msg='', L=0, T=0, W=1280, H=720, TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
            buttonfocus, buttonnofocus = gui.get_artwork('button')
            radiobgfocus, radiobgnofocus, radiofocus, radionofocus = gui.get_artwork('radio')
            slidernibfocus, slidernibnofocus, sliderfocus, slidernofocus = gui.get_artwork('slider')
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


        def doExit(self):
            self.CloseWindow()


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
            if self.Button0.isSelected():
                buffermode = 0
            elif self.Button1.isSelected():
                buffermode = 1
            elif self.Button2.isSelected():
                buffermode = 2
            elif self.Button3.isSelected():
                buffermode = 3
            if os.path.exists(CONFIG.ADVANCED):
                choice = gui.DIALOG.yesno(CONFIG.ADDONTITLE,
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
            self.CloseWindow()


        def onControl(self, control):
            if control == self.buttonWrite:
                self.doWrite()
            elif control == self.buttonCancel:
                self.doExit()


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
            elif F in [self.Button0, self.Button1, self.Button2, self.Button3] and action in [gui.ACTION_MOUSE_LEFT_CLICK, gui.ACTION_SELECT_ITEM]:
                self.updateCurrent(F)
            elif action == gui.ACTION_PREVIOUS_MENU:
                self.doExit()
            elif action == gui.ACTION_NAV_BACK:
                self.doExit()


        def CloseWindow(self):
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
            buttonfocus, buttonnofocus = gui.get_artwork('button')
            self.BG = xbmcgui.ControlImage(L+BorderWidth, T+BorderWidth, W-(BorderWidth*2), H-(BorderWidth*2), CONFIG.ADDON_FANART, aspectRatio=0)
            self.addControl(self.BG)
            top = T+BorderWidth
            leftside = L+BorderWidth
            rightside = L+(W/2)-(BorderWidth*2)
            header = '[COLOR {0}]Quick Advanced Settings Configurator[/COLOR]'.format(CONFIG.COLOR2)
            self.Header=xbmcgui.ControlLabel(L, top, W, 30, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header)
            top += 30+BorderWidth
            freeMemory = int(float(tools.get_info_label('System.Memory(free)')[:-2])*.33)
            recMemory = int(float(tools.get_info_label('System.Memory(free)')[:-2])*.23)
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


        def doExit(self):
            self.CloseWindow()


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
            buffermode = 2
            if os.path.exists(CONFIG.ADVANCED):
                choice = gui.DIALOG.yesno(CONFIG.ADDONTITLE,
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
            self.CloseWindow()


        def onControl(self, control):
            if control == self.buttonWrite:
                self.doWrite()
            elif control == self.buttonCancel:
                self.doExit()


        def onAction(self, action):
            try:
                F = self.getFocus()
            except:
                F = False
            if action == gui.ACTION_PREVIOUS_MENU:
                self.doExit()
            elif action == gui.ACTION_NAV_BACK:
                self.doExit()


        def CloseWindow(self):
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

##########################
### Converted to XML
##########################


def apkInstaller(apk):
    class APKInstaller(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.shut = kwargs['close_time']
            xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
            xbmc.executebuiltin("Skin.SetBool(AnimeWindowXMLDialogClose)")


        def onClick(self, controlID):
            self.CloseWindow()


        def onAction(self, action):
            if action in [gui.ACTION_PREVIOUS_MENU, gui.ACTION_BACKSPACE, gui.ACTION_NAV_BACK, gui.ACTION_SELECT_ITEM,
                          gui.ACTION_MOUSE_LEFT_CLICK, gui.ACTION_MOUSE_LONG_CLICK]:
                self.CloseWindow()


        def CloseWindow(self):
            xbmc.executebuiltin("Skin.Reset(AnimeWindowXMLDialogClose)")
            xbmc.sleep(400)
            self.close()

    xbmc.executebuiltin('Skin.SetString(apkinstaller, Now that {0} has been downloaded[CR]Click install on the next window!)'.format(apk))
    popup = APKInstaller('APK.xml', CONFIG.ADDON_PATH, 'DefaultSkin', close_time=34)
    popup.doModal()
    del popup


def speedTest(img):
    class speedTest(xbmcgui.WindowXMLDialog):

        def __init__(self, *args, **kwargs):
            self.imgfile = kwargs['img']


        def onInit(self):
            self.imagespeed = 101
            self.button = 201
            self.showdialog()


        def showdialog(self):
            self.setFocus(self.getControl(self.button))
            self.getControl(self.imagespeed).setImage(self.imgfile)


        def onClick(self, controlID):
            self.CloseWindow()

        def onAction(self, action):
            if action in [gui.ACTION_PREVIOUS_MENU, gui.ACTION_BACKSPACE, gui.ACTION_NAV_BACK, gui.ACTION_SELECT_ITEM,
                          gui.ACTION_MOUSE_LEFT_CLICK, gui.ACTION_MOUSE_LONG_CLICK]:
                self.CloseWindow()


        def CloseWindow(self):
            self.close()

    popup = speedTest('SpeedTest.xml', CONFIG.ADDON_PATH, 'DefaultSkin', img=img)
    popup.doModal()
    del popup


def firstRunSettings():
    class firstRun(xbmcgui.WindowXMLDialog):

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
            self.showdialog()
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


        def showdialog(self):
            self.getControl(self.title).setLabel(CONFIG.ADDONTITLE)
            self.setFocus(self.getControl(self.okbutton))


        def onClick(self, controlId):
            if controlId == self.okbutton:
                self.close()

                for item in self.controllist:
                    at = self.controllist.index(item)
                    if self.getControl(item).isSelected():
                        CONFIG.set_setting(self.controlsettings[at], 'true')
                    else:
                        CONFIG.set_setting(self.controlsettings[at], 'false')

                if self.getControl(self.whitelist).isSelected() and not self.whitelistcurrent == 'true':
                    whitelist.whitelist('edit')

    fr = firstRun("FirstRunSaveData.xml", CONFIG.ADDON_PATH, 'DefaultSkin', current=CONFIG.KEEPWHITELIST)
    fr.doModal()
    del fr


def firstRun():
    class MyWindow(xbmcgui.WindowXMLDialog):

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
            self.showdialog()


        def showdialog(self):
            self.getControl(self.image).setImage(CONFIG.ADDON_FANART)
            self.getControl(self.image).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setText(self.msg)
            self.getControl(self.titlebox).setLabel(self.title)
            self.setFocusId(self.buildmenu)


        def doBuildMenu(self):
            logging.log("[Check Updates] [User Selected: Open Build Menu] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))
            self.close()
            url = 'plugin://{0}/?mode=builds'.format(CONFIG.ADDON_ID)
            xbmc.executebuiltin('ActivateWindow(10025, "{0}", return)'.format(url))


        def doIgnore(self):
            self.close()
            logging.log("[First Run] [User Selected: Ignore Build Menu] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))


        def onAction(self, action):
            if action == gui.ACTION_PREVIOUS_MENU:
                self.doIgnore()
            elif action == gui.ACTION_NAV_BACK:
                self.doIgnore()


        def onClick(self, controlId):
            if controlId == self.buildmenu:
                self.doBuildMenu()
            else:
                self.doIgnore()

    fr = MyWindow("FirstRunBuild.xml", CONFIG.ADDON_PATH, 'DefaultSkin')
    fr.doModal()
    del fr


def split_notify(notify):
    link = tools.open_url(notify).replace('\r', '').replace('\t', '').replace('\n', '[CR]')
    if link.find('|||') == -1:
        return False, False
    id, msg = link.split('|||')
    if msg.startswith('[CR]'):
        msg = msg[4:]
    return id.replace('[CR]', ''), msg


def notification(msg='', test=False):
    class MyWindow(xbmcgui.WindowXMLDialog):

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
            self.showdialog()


        def showdialog(self):
            self.testimage = os.path.join(CONFIG.ART, 'text.png')
            self.getControl(self.image).setImage(CONFIG.BACKGROUND)
            self.getControl(self.image).setColorDiffuse('9FFFFFFF')
            self.getControl(self.textbox).setText(self.message)
            self.setFocusId(self.remindme)
            if CONFIG.HEADERTYPE == 'Text':
                self.getControl(self.titlebox).setLabel(CONFIG.THEME3 % CONFIG.HEADERMESSAGE)
            else:
                self.getControl(self.titleimage).setImage(CONFIG.HEADERIMAGE)


        def doRemindMeLater(self):
            if not test:
                CONFIG.set_setting("notedismiss", "false")
            logging.log("[Notification] NotifyID {0} Remind Me Later".format(CONFIG.get_setting('noteid')), level=xbmc.LOGNOTICE)
            self.close()


        def doDismiss(self):
            if not test:
                CONFIG.set_setting("notedismiss", "true")
            logging.log("[Notification] NotifyID {0} Dismissed".format(CONFIG.get_setting('noteid')), level=xbmc.LOGNOTICE)
            self.close()


        def onAction(self, action):
            if action == gui.ACTION_PREVIOUS_MENU:
                self.doRemindMeLater()
            elif action == gui.ACTION_NAV_BACK:
                self.doRemindMeLater()


        def onClick(self, controlId):
            if controlId == self.dismiss:
                self.doDismiss()
            else:
                self.doRemindMeLater()

    xbmc.executebuiltin('Skin.SetString(headertexttype, {0})'.format('true' if CONFIG.HEADERTYPE == 'Text' else 'false'))
    xbmc.executebuiltin('Skin.SetString(headerimagetype, {0})'.format('true' if CONFIG.HEADERTYPE == 'Image' else 'false'))
    notify = MyWindow("Notifications.xml", CONFIG.ADDON_PATH, 'DefaultSkin', msg=msg, test=test)
    notify.doModal()
    del notify


def updateWindow(name='Testing Window', current='1.0', new='1.1', icon=CONFIG.ADDON_ICON, fanart=CONFIG.ADDON_FANART):
    class MyWindow(xbmcgui.WindowXMLDialog):

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
            self.showdialog()


        def showdialog(self):
            self.getControl(self.header).setLabel(self.name)
            self.getControl(self.textbox).setText(CONFIG.THEME2 % self.msgupdate if current < new else self.msgcurrent)
            self.getControl(self.imagefanart).setImage(self.fanart)
            self.getControl(self.imagefanart).setColorDiffuse('2FFFFFFF')
            self.getControl(self.imageicon).setImage(self.icon)
            self.setFocusId(self.fresh)


        def doFreshInstall(self):
            logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] [User Selected: Fresh Install build]".format(CONFIG.BUILDVERSION, CONFIG.LATESTVERSION), level=xbmc.LOGNOTICE)
            logging.log("[Check Updates] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))
            self.close()
            url = 'plugin://{0}/?mode=install&name={1}&url=fresh'.format(CONFIG.ADDON_ID, quote_plus(CONFIG.BUILDNAME))
            xbmc.executebuiltin('RunPlugin({0})'.format(url))


        def doNormalInstall(self):
            logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] [User Selected: Normal Install build]".format(CONFIG.BUILDVERSION, CONFIG.LATESTVERSION), level=xbmc.LOGNOTICE)
            logging.log("[Check Updates] [Next Check: {0}]".format(str(CONFIG.NEXTCHECK)), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(CONFIG.NEXTCHECK))
            self.close()
            url = 'plugin://{0}/?mode=install&name={1}&url=normal'.format(CONFIG.ADDON_ID, quote_plus(CONFIG.BUILDNAME))
            xbmc.executebuiltin('RunPlugin({0})'.format(url))


        def doIgnore(self):
            logging.log("[Check Updates] [Installed Version: {0}] [Current Version: {1}] [User Selected: Ignore 3 Days]".format(CONFIG.BUILDVERSION, CONFIG.LATESTVERSION), level=xbmc.LOGNOTICE)
            logging.log("[Check Updates] [Next Check: {0}]".format(str(tools.get_date(days=3))), level=xbmc.LOGNOTICE)
            CONFIG.set_setting('lastbuildcheck', str(tools.get_date(days=3)))
            self.close()


        def onAction(self, action):
            if action == gui.ACTION_PREVIOUS_MENU:
                self.doIgnore()
            elif action == gui.ACTION_NAV_BACK:
                self.doIgnore()


        def onClick(self, controlId):
            if controlId == self.fresh:
                self.doFreshInstall()
            elif controlId == self.normal:
                self.doNormalInstall()
            else:
                self.doIgnore()

    update = MyWindow("BuildUpdate.xml", CONFIG.ADDON_PATH, 'DefaultSkin', name=name, current=current, new=new, icon=icon, fanart=fanart)
    update.doModal()
    del update
