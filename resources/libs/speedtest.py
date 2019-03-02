#!/usr/bin/env python
############################################################################
#                             /T /I                                        #
#                              / |/ | .-~/                                 #
#                          T\ Y  I  |/  /  _                               #
#         /T               | \I  |  I  Y.-~/                               #
#        I l   /I       T\ |  |  l  |  T  /                                #
#     T\ |  \ Y l  /T   | \I  l   \ `  l Y                                 #
# __  | \l   \l  \I l __l  l   \   `  _. |                                 #
# \ ~-l  `\   `\  \  \ ~\  \   `. .-~   |                                  #
#  \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |                                 #
#.--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./                                 #
# >--.  ~-.   ._  ~>-"    "\   7   7   ]                                   #
#^.___~"--._    ~-{  .-~ .  `\ Y . /    |                                  #
# <__ ~"-.  ~       /_/   \   \I  Y   : |                                  #
#   ^-.__           ~(_/   \   >._:   | l______                            #
#       ^--.,___.-~"  /_/   !  `-.~"--l_ /     ~"-.                        #
#              (_/ .  ~(   /'     "~"--,Y   -=b-. _)                       #
#               (_/ .  \  Fire TV Guru/ l      c"~o \                      #
#                \ /    `.    .     .^   \_.-~"~--.  )                     #
#                 (_/ .   `  /     /       !       )/                      #
#                  / / _.   '.   .':      /        '                       #
#                  ~(_/ .   /    _  `  .-<_                                #
#                    /_/ . ' .-~" `.  / \  \          ,z=.                 #
#                    ~( /   '  :   | K   "-.~-.______//                    #
#                      "-,.    l   I/ \_    __{--->._(==.                  #
#                       //(     \  <    ~"~"     //                        #
#                      /' /\     \  \     ,v=.  ((                         #
#                    .^. / /\     "  }__ //===-  `                         #
#                   / / ' '  "-.,__ {---(==-                               #
#                 .^ '       :  T  ~"   ll                                 #
#                / .  .  . : | :!        \                                 #
#               (_/  /   | | j-"          ~^                               #
#                 ~-<_(_.^-~"                                              #
#                                                                          #
#   Copyright (C) 2014-2016 Matt Martz                                     #
#                                                                          #
#                      original speedtest-cli DEV                          #
#            Matt Martz (https://github.com/sivel/speedtest-cli)           #
#                                                                          #
#             Credits to : Josh.5 for the original kodi layout             #
#                                                                          #
#     Updated layout, fixed errors and cleaned up code: Fire TV Guru       #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License"); you may  #
# not use this file except in compliance with the License. You may obtain  #
# a copy of the License at                                                 #
#                                                                          #
#      http://www.apache.org/licenses/LICENSE-2.0                          #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,WITHOUT #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the #
# License for the specific language governing permissions and limitations  #
# under the License.                                                       #
############################################################################
if 64 - 64: FGGFTFFTFF
if 65 - 65: tg / FTFFGTGGTGTTG % tffffffftt - FGTTF
if 73 - 73: TTGGGFFFF
import xbmc
import xbmcgui
import xbmcaddon
import os
import re
import sys
import math
import signal
import socket
import timeit
import platform
import threading
import time
import uuid
import uservar
if 22 - 22: TGTFFT * tfgtff / tftgtgg . tftfttgg . fgfttfgtgtff / TGFFGGFTFGGF
if 48 - 48: ftgf / ttffttf / TGGF / TFGT
try :
 import xml . etree . cElementTree as ET
 from xml . dom import minidom as DOM
except ImportError :
 try :
  import xml . etree . ElementTree as ET
 except ImportError :
  from xml . dom import minidom as DOM
  if 48 - 48: FTTGGGF % TFTT + TGTFGGG / fftftgf * TFGT
  ET = None
  if 46 - 46: fftftgf * TGGF - tffffffftt
TTGFTTGF = uservar . ADDON_ID
ftgfTTTT = xbmcaddon . Addon ( TTGFTTGF )
tfgftgffgftgg = xbmc . translatePath ( 'special://home/' )
FGGGT = os . path . join ( tfgftgffgftgg , 'userdata' )
TTGTFGFTGF = os . path . join ( FGGGT , 'addon_data' , TTGFTTGF )
FFTGFTFT = os . path . join ( TTGTFGFTGF , 'SpeedTest' )
if 91 - 91: tftgtgg . FGGFTFFTFF / ftgf % TGGF / tftgtgg - FGGFTFFTFF
if 8 - 8: fgfttfgtgtff * TGFFGGFTFGGF * FTFFGTGGTGTTG . TFTT / TFTT % TFTT
if 22 - 22: TFGT . TFTT
__version__ = '0.3.2'
TGG = None
tfgfggggfgfg = None
ftfgffffggf = socket . socket
ftgfgfgfftgft = ( 'Mozilla/5.0' , '(%s; U; %s; en-us)'
 % ( platform . system ( ) , platform . architecture ( ) [ 0 ] ) ,
 'Python/%s' % platform . python_version ( ) ,
 '(KHTML, like Gecko)' , 'speedtest-cli/%s' % __version__ )
ffgfgtgg = ' ' . join ( ftgfgfgfftgft )
if 68 - 68: ttffttf . TGTFFT / FTTGGGF
try :
 import xml . etree . cElementTree as ET
 from xml . dom import minidom as DOM
except ImportError :
 try :
  import xml . etree . ElementTree as ET
 except ImportError :
  from xml . dom import minidom as DOM
  if 72 - 72: tftgtgg / tftgtgg
  ET = None
  if 30 - 30: tftgtgg
try :
 from urllib2 import urlopen , Request , HTTPError , URLError
except ImportError :
 from urllib . request import urlopen , Request , HTTPError , URLError
 if 95 - 95: ftgf * fgfttfgtgtff / TTGGGFFFF . TGFFGGFTFGGF + ttffttf
 if 47 - 47: tftfttgg / TFGT * tffffffftt
try :
 from httplib import HTTPConnection , HTTPSConnection
except ImportError :
 from http . client import HTTPConnection , HTTPSConnection
 if 9 - 9: TGTFFT - TFGT % FGTTF % tffffffftt
 if 3 - 3: FTTGGGF + tg
try :
 from Queue import Queue
except ImportError :
 from queue import Queue
 if 42 - 42: ttffttf / FGTTF + FGGFTFFTFF - TFGT
try :
 from urlparse import urlparse
except ImportError :
 from urllib . parse import urlparse
 if 78 - 78: tftgtgg
 if 18 - 18: tg - FTTGGGF / FTTGGGF + fftftgf % fftftgf - TFTT
try :
 from urlparse import parse_qs
except ImportError :
 try :
  from urllib . parse import parse_qs
 except ImportError :
  from cgi import parse_qs
  if 62 - 62: FTTGGGF - TFTT - tftfttgg % FGTTF / ftgf
  if 77 - 77: TTGGGFFFF - TTGGGFFFF . TGTFFT / fgfttfgtgtff
try :
 from hashlib import md5
except ImportError :
 from md5 import md5
 if 14 - 14: TGGF % tg
 if 41 - 41: FGTTF + TGTFGGG + ttffttf - TFTT
try :
 from argparse import ArgumentParser as ArgParser
except ImportError :
 from optparse import OptionParser as ArgParser
 if 77 - 77: tfgtff . TFTT % fftftgf
try :
 import builtins
except ImportError :
 def TTFFTFTG ( * args , ** kwargs ) :
  FFTFTTF = kwargs . pop ( 'file' , sys . stdout )
  if FFTFTTF is None :
   return
   if 65 - 65: tftfttgg
  def FFGT ( data ) :
   if not isinstance ( data , basestring ) :
    data = str ( data )
   FFTFTTF . write ( data )
   if 76 - 76: tg / fgfttfgtgtff . TGTFFT * TFGT - ttffttf
  tfff = False
  tggf = kwargs . pop ( 'sep' , None )
  if tggf is not None :
   if isinstance ( tggf , unicode ) :
    tfff = True
   elif not isinstance ( tggf , str ) :
    raise TypeError ( 'sep must be None or a string' )
  tgg = kwargs . pop ( 'end' , None )
  if tgg is not None :
   if isinstance ( tgg , unicode ) :
    tfff = True
   elif not isinstance ( tgg , str ) :
    raise TypeError ( 'end must be None or a string' )
  if kwargs :
   raise TypeError ( 'invalid keyword arguments to print()' )
  if not tfff :
   for FGGTG in args :
    if isinstance ( FGGTG , unicode ) :
     tfff = True
     break
  if tfff :
   TFGGTFGGT = unicode ( '\n' )
   FTGGFGTG = unicode ( ' ' )
  else :
   TFGGTFGGT = '\n'
   FTGGFGTG = ' '
  if tggf is None :
   tggf = FTGGFGTG
  if tgg is None :
   tgg = TFGGTFGGT
  for ( fgfgtttgfg , FGGTG ) in enumerate ( args ) :
   if fgfgtttgfg :
    FFGT ( tggf )
   FFGT ( FGGTG )
  FFGT ( tgg )
else :
 TTFFTFTG = getattr ( builtins , 'print' )
 del builtins
 if 84 - 84: TFTT
 if 25 - 25: tfgtff - TFTT . tffffffftt
 if 22 - 22: TFTT + TTGGGFFFF % TGTFGGG . TGGF . tftfttgg
class ttgffgftt ( Exception ) :
 if 54 - 54: TGTFFT % TTGGGFFFF % TTGGGFFFF
 if 13 - 13: fgfttfgtgtff . TFGT
 if 19 - 19: TGGF + fftftgf
 if 53 - 53: tffffffftt . FGTTF
 if 18 - 18: fgfttfgtgtff
def TGFGTGTT ( * args , ** kwargs ) :
 if 45 - 45: TGTFGGG . tftfttgg
 global TGG
 ft = ftfgffffggf ( * args , ** kwargs )
 ft . bind ( ( TGG , 0 ) )
 return ft
 if 6 - 6: TGFFGGFTFGGF
 if 31 - 31: TFGT . TFGT - fgfttfgtgtff / tftgtgg + fftftgf * TGTFFT
 if 63 - 63: TGTFGGG % FGTTF / tffffffftt - tffffffftt
def FTFFGGT ( origin , destination ) :
 ( tttgtttggff , TFFGGGTT ) = origin
 ( FFFFGGT , tffgttgftt ) = destination
 FFGGFG = 6371
 if 29 - 29: TGFFGGFTFGGF % TGTFFT + fftftgf / fgfttfgtgtff + ttffttf * fgfttfgtgtff
 FGTGFT = math . radians ( FFFFGGT - tttgtttggff )
 ffgtffttfg = math . radians ( tffgttgftt - TFFGGGTT )
 fgt = math . sin ( FGTGFT / 2 ) * math . sin ( FGTGFT / 2 ) + math . cos ( math . radians ( tttgtttggff ) ) * math . cos ( math . radians ( FFFFGGT ) ) * math . sin ( ffgtffttfg / 2 ) * math . sin ( ffgtffttfg / 2 )
 if 72 - 72: FTTGGGF / FGTTF * tfgtff - TGTFGGG
 if 51 - 51: TTGGGFFFF * tftgtgg % fgfttfgtgtff * TTGGGFFFF % TGFFGGFTFGGF / fftftgf
 FTTTTFFG = 2 * math . atan2 ( math . sqrt ( fgt ) , math . sqrt ( 1 - fgt ) )
 ffgggttggtf = FFGGFG * FTTTTFFG
 if 51 - 51: TFTT * fgfttfgtgtff + TGGF + tftgtgg
 return ffgggttggtf
 if 66 - 66: tftfttgg
 if 97 - 97: ftgf % TFTT * TFTT
 if 39 - 39: TFGT % TFTT
def FGGGTFTGT ( url , data = None , headers = { } ) :
 if url [ 0 ] == ':' :
  tgFTT = '%s%s' % ( scheme , url )
 else :
  tgFTT = url
 headers [ 'User-Agent' ] = ffgfgtgg
 return Request ( tgFTT , data = data , headers = headers )
 if 80 - 80: TFTT . ftgf
def TTF ( request ) :
 try :
  FGGFTTTTTFG = urlopen ( request )
  return FGGFTTTTTFG
 except ( HTTPError , URLError , socket . error ) :
  FFTTGFG = sys . exc_info ( ) [ 1 ]
  return ( None , FFTTGFG )
  if 66 - 66: ttffttf - TGGF
  if 5 - 5: TGTFGGG + TFGT / tfgtff - ftgf
  if 63 - 63: ttffttf % ftgf * ftgf * tftgtgg / TGFFGGFTFGGF
class fgfft ( threading . Thread ) :
 if 98 - 98: FTTGGGF * FTTGGGF / FTTGGGF + TGGF
 def __init__ ( self , url , start ) :
  self . url = url
  self . result = None
  self . starttime = start
  threading . Thread . __init__ ( self )
  if 34 - 34: fftftgf
 def run ( self ) :
  self . result = [ 0 ]
  try :
   if timeit . default_timer ( ) - self . starttime <= 10 :
    TGGGGTGFTTGG = FGGGTFTGT ( self . url )
    tfffgtgffggft = urlopen ( TGGGGTGFTTGG )
    while 1 and not tfgfggggfgfg . isSet ( ) :
     self . result . append ( len ( tfffgtgffggft . read ( 10240 ) ) )
     if self . result [ - 1 ] == 0 :
      break
    tfffgtgffggft . close ( )
  except IOError :
   pass
   if 14 - 14: tftfttgg / TFTT . tftfttgg . TGGF % tftgtgg * TGGF
   if 16 - 16: tftfttgg . fftftgf + FGGFTFFTFF
   if 38 - 38: TFTT * ttffttf . fgfttfgtgtff
class fffgtt ( threading . Thread ) :
 if 65 - 65: TFGT . FTFFGTGGTGTTG / tg - TFGT
 def __init__ (
 self ,
 url ,
 start ,
 size ,
 ) :
  self . url = url
  FFFGFGFFFFTF = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  TFFF = FFFGFGFFFFTF * int ( round ( int ( size ) / 36.0 ) )
  self . data = ( 'content1=%s' % TFFF [ 0 : int ( size ) - 9 ] ) . encode ( )
  del TFFF
  self . result = None
  self . starttime = start
  threading . Thread . __init__ ( self )
  if 75 - 75: tftfttgg % fgfttfgtgtff % fgfttfgtgtff . TGTFGGG
 def run ( self ) :
  try :
   if timeit . default_timer ( ) - self . starttime <= 10 and not tfgfggggfgfg . isSet ( ) :
    if 5 - 5: fgfttfgtgtff * fftftgf + tftfttgg . ttffttf + tftfttgg
    TGGGGTGFTTGG = FGGGTFTGT ( self . url , data = self . data )
    tfffgtgffggft = urlopen ( TGGGGTGFTTGG )
    tfffgtgffggft . read ( 11 )
    tfffgtgffggft . close ( )
    self . result = len ( self . data )
   else :
    self . result = 0
  except IOError :
   self . result = 0
   if 91 - 91: tg
   if 61 - 61: TTGGGFFFF
def tgttt ( dom , tagName ) :
 TTGGFTFTTTFT = dom . getElementsByTagName ( tagName ) [ 0 ]
 return dict ( list ( TTGGFTFTTTFT . attributes . items ( ) ) )
 if 67 - 67: TGTFGGG . FTTGGGF . tg
 if 10 - 10: TGFFGGFTFGGF % TGFFGGFTFGGF - FTFFGTGGTGTTG / ttffttf + TFGT
def ttttftffgtgtg ( ) :
 TGGGGTGFTTGG = FGGGTFTGT ( 'http://www.speedtest.net/speedtest-config.php' )
 if 85 - 85: ftgf % FGGFTFFTFF - FTTGGGF * tffffffftt / TGTFFT % TGTFFT
 FGGFTTTTTFG = TTF ( TGGGGTGFTTGG )
 if FGGFTTTTTFG is False :
  TTFFTFTG ( 'Could not retrieve speedtest.net configuration: %s' % e )
  sys . exit ( 1 )
 TTFTFGFT = [ ]
 while 1 :
  TTFTFGFT . append ( FGGFTTTTTFG . read ( 10240 ) )
  if len ( TTFTFGFT [ - 1 ] ) == 0 :
   break
 if int ( FGGFTTTTTFG . code ) != 200 :
  return None
 FGGFTTTTTFG . close ( )
 try :
  try :
   FGTFFFTGFT = ET . fromstring ( '' . encode ( ) . join ( TTFTFGFT ) )
   FGFTF = {
 'client' : FGTFFFTGFT . find ( 'client' ) . attrib ,
 'times' : FGTFFFTGFT . find ( 'times' ) . attrib ,
 'download' : FGTFFFTGFT . find ( 'download' ) . attrib ,
 'upload' : FGTFFFTGFT . find ( 'upload' ) . attrib ,
 }
  except Exception :
   if 68 - 68: FGGFTFFTFF % TGFFGGFTFGGF + FGGFTFFTFF
   if 31 - 31: TTGGGFFFF . TGTFFT
   if 1 - 1: tfgtff / fgfttfgtgtff % FTTGGGF * TFTT . FGGFTFFTFF
   FGTFFFTGFT = DOM . parseString ( '' . join ( TTFTFGFT ) )
   FGFTF = {
 'client' : tgttt ( FGTFFFTGFT , 'client' ) ,
 'times' : tgttt ( FGTFFFTGFT , 'times' ) ,
 'download' : tgttt ( FGTFFFTGFT , 'download' ) ,
 'upload' : tgttt ( FGTFFFTGFT , 'upload' ) ,
 }
 except SyntaxError :
  TTFFTFTG ( 'Failed to parse speedtest.net configuration' )
  sys . exit ( 1 )
 del FGTFFFTGFT
 del TTFTFGFT
 return FGFTF
 if 2 - 2: TGFFGGFTFGGF * TGGF - FTFFGTGGTGTTG + TGTFFT . ftgf % FTTGGGF
 if 92 - 92: FTTGGGF
def TTFTFFTF ( client , all = False ) :
 if 51 - 51: TGGF + FTTGGGF % FTFFGTGGTGTTG / ftgf / ttffttf % tffffffftt
 fgtgtttgtff = [
 'https://www.speedtest.net/speedtest-servers-static.php' ,
 'http://c.speedtest.net/speedtest-servers-static.php' ,
 ]
 FFTFT = [ ]
 TG = { }
 for tttggtgt in fgtgtttgtff :
  try :
   TGGGGTGFTTGG = FGGGTFTGT ( tttggtgt )
   FGGFTTTTTFG = TTF ( TGGGGTGFTTGG )
   if FGGFTTTTTFG is False :
    FFTFT . append ( '%s' % e )
    raise ttgffgftt
   FFF = [ ]
   while 1 :
    FFF . append ( FGGFTTTTTFG . read ( 10240 ) )
    if len ( FFF [ - 1 ] ) == 0 :
     break
   if int ( FGGFTTTTTFG . code ) != 200 :
    FGGFTTTTTFG . close ( )
    raise ttgffgftt
   FGGFTTTTTFG . close ( )
   try :
    try :
     FGTFFFTGFT = ET . fromstring ( '' . encode ( ) . join ( FFF ) )
     ftfftttftf = FGTFFFTGFT . getiterator ( 'server' )
    except Exception :
     if 41 - 41: TFGT - tg - tg
     if 68 - 68: ttffttf % TGTFGGG
     if 88 - 88: FTFFGTGGTGTTG - fftftgf + ttffttf
     FGTFFFTGFT = DOM . parseString ( '' . join ( FFF ) )
     ftfftttftf = FGTFFFTGFT . getElementsByTagName ( 'server' )
   except SyntaxError :
    raise ttgffgftt
   for TFTGGGGGGTTTT in ftfftttftf :
    try :
     FGTF = TFTGGGGGGTTTT . attrib
    except AttributeError :
     FGTF = dict ( list ( TFTGGGGGGTTTT . attributes . items ( ) ) )
    ffgggttggtf = FTFFGGT ( [ float ( client [ 'lat' ] ) , float ( client [ 'lon'
 ] ) ] , [ float ( FGTF . get ( 'lat' ) ) ,
 float ( FGTF . get ( 'lon' ) ) ] )
    FGTF [ 'd' ] = ffgggttggtf
    if ffgggttggtf not in TG :
     TG [ ffgggttggtf ] = [ FGTF ]
    else :
     TG [ ffgggttggtf ] . append ( FGTF )
   del FGTFFFTGFT
   del FFF
   del ftfftttftf
  except ttgffgftt :
   continue
  if TG :
   break
 if not TG :
  TTFFTFTG ( '''Failed to retrieve list of speedtest.net servers:
%s'''
 % '\n' . join ( FFTFT ) )
  sys . exit ( 1 )
 FFGGGFTGFTFG = [ ]
 for ffgggttggtf in sorted ( TG . keys ( ) ) :
  for ttt in TG [ ffgggttggtf ] :
   FFGGGFTGFTFG . append ( ttt )
   if len ( FFGGGFTGFTFG ) == 5 and not all :
    break
  else :
   continue
  break
 del TG
 return FFGGGFTGFTFG
 if 68 - 68: TTGGGFFFF + TGGF
 if 45 - 45: FTTGGGF / FTTGGGF + TGTFGGG + fftftgf
def FTGGGF ( servers ) :
 TTFGGFGFGFTG = { }
 for TFTGGGGGGTTTT in servers :
  FFFTFG = [ ]
  tttggtgt = '%s/latency.txt' % os . path . dirname ( TFTGGGGGGTTTT [ 'url' ] )
  FGTGFFGGFGTFF = urlparse ( tttggtgt )
  for fgfgtttgfg in range ( 0 , 3 ) :
   try :
    if FGTGFFGGFGTFF [ 0 ] == 'https' :
     TGTFFFFT = HTTPSConnection ( FGTGFFGGFGTFF [ 1 ] )
    else :
     TGTFFFFT = HTTPConnection ( FGTGFFGGFGTFF [ 1 ] )
    fgtTFTT = { 'User-Agent' : ffgfgtgg }
    FFGFTTGTT = timeit . default_timer ( )
    TGTFFFFT . request ( 'GET' , FGTGFFGGFGTFF [ 2 ] , headers = fgtTFTT )
    TFFGTGTGGFFTG = TGTFFFFT . getresponse ( )
    TGTGFGT = timeit . default_timer ( ) - FFGFTTGTT
   except ( HTTPError , URLError , socket . error ) :
    FFFTFG . append ( 3600 )
    continue
   FFGTtgftg = TFFGTGTGGFFTG . read ( 9 )
   if int ( TFFGTGTGGFFTG . status ) == 200 and FFGTtgftg == 'test=test' . encode ( ) :
    FFFTFG . append ( TGTGFGT )
   else :
    FFFTFG . append ( 3600 )
   TGTFFFFT . close ( )
  ftg = round ( sum ( FFFTFG ) / 6 * 1000 , 3 )
  TTFGGFGFGFTG [ ftg ] = TFTGGGGGGTTTT
 tgttgt = sorted ( TTFGGFGFGFTG . keys ( ) ) [ 0 ]
 tt = TTFGGFGFGFTG [ tgttgt ]
 tt [ 'latency' ] = tgttgt
 return tt
 if 83 - 83: tg / TGTFFT - tftgtgg - ttffttf
 if 36 - 36: TFTT
 if 36 - 36: fftftgf / tg * tfgtff - ttffttf % FTFFGTGGTGTTG * ftgf
 if 79 - 79: tg
class fttggt ( xbmcgui . WindowXMLDialog ) :
 def __init__ ( self , * args , ** kwargs ) :
  xbmcgui . WindowXMLDialog . __init__ ( self , * args , ** kwargs )
  self . doModal ( )
  if 77 - 77: tfgtff - FGTTF - TGGF . tftfttgg
 def onInit ( self ) :
  self . testRun = False
  self . screenx = 1920
  self . screeny = 1080
  self . image_dir = xbmc . translatePath ( os . path . join ( ftgfTTTT . getAddonInfo ( 'path' ) , 'resources' , 'skins' , 'Defaultskin' , 'media' ) )
  self . image_background = self . image_dir + '/bg_screen.jpg'
  self . image_shadow = self . image_dir + '/shadowframe.png'
  self . image_progress = self . image_dir + '/ajax-loader-bar.gif'
  self . image_ping = self . image_dir + '/ping_progress_bg.png'
  self . image_ping_glow = self . image_dir + '/ping_progress_glow.png'
  self . image_gauge = self . image_dir + '/gauge_bg.png'
  self . image_gauge_arrow = self . image_dir + '/gauge_ic_arrow.png'
  self . image_button_run = self . image_dir + '/btn_start_bg.png'
  self . image_button_run_glow = self . image_dir + '/btn_start_glow_active.png'
  self . image_speedtestresults = self . image_dir + '/speedtest_results_wtext.png'
  self . image_centertext_testingping = self . image_dir + '/testing_ping.png'
  self . rec_speedpic = self . image_dir + '/recspeed.png'
  self . image_result = self . image_speedtestresults
  if 39 - 39: TTGGGFFFF / fftftgf + TGTFGGG / tftfttgg
  self . textbox = xbmcgui . ControlTextBox ( 50 , 50 , 1500 , 800 , textColor = '0xFFFFFFFF' )
  self . addControl ( self . textbox )
  self . displayButtonRun ( )
  self . displayButtonClose ( )
  self . setFocus ( self . button_run )
  if 13 - 13: TFTT + tg + FTTGGGF % TGTFFT / fgfttfgtgtff . TFTT
 def onAction ( self , action ) :
  if action == 10 or action == 92 :
   self . saveClose ( )
   if 86 - 86: ftgf * fgfttfgtgtff % FGTTF . TFGT . FGGFTFFTFF
 def displayButtonRun ( self , function = "true" ) :
  if ( function == "true" ) :
   if 56 - 56: TGFFGGFTFGGF % tg - TGTFFT
   if 100 - 100: TFGT - tg % ftgf * ttffttf + TGTFFT
   if 88 - 88: tffffffftt - tftgtgg * tg * tffffffftt . tffffffftt
   self . button_run_glow = xbmcgui . ControlImage ( 800 , 500 , 360 , 182 , '' , aspectRatio = 0 )
   self . addControl ( self . button_run_glow )
   self . button_run_glow . setVisible ( False )
   self . button_run_glow . setImage ( self . image_button_run_glow )
   self . button_run_glow . setAnimations ( [
 ( 'conditional' , 'effect=fade start=0 time=1000 condition=true pulse=true' )
 ] )
   if 33 - 33: TGTFGGG + FTTGGGF * ftgf / FTFFGTGGTGTTG - TGTFFT
   self . button_run = xbmcgui . ControlButton ( 800 , 500 , 360 , 182 , "[B]Run Speedtest[/B]" ,
 focusTexture = self . image_button_run ,
 noFocusTexture = self . image_button_run , alignment = 2 | 4 ,
 textColor = '0xFF000000' , focusedColor = '0xFF000000' ,
 shadowColor = '0xFFCCCCCC' , disabledColor = '0xFF000000' )
   self . addControl ( self . button_run )
   self . setFocus ( self . button_run )
   self . button_run . setVisible ( False )
   self . button_run . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=100 end=0 time=300 condition=!Control.IsEnabled(%d)' % self . button_run . getId ( ) )
 ] )
   self . button_run_ID = self . button_run . getId ( )
   if 54 - 54: TGTFGGG / ttffttf . ftgf % FTTGGGF
   self . button_run . setEnabled ( True )
   self . button_run . setVisible ( True )
   self . button_run_glow . setEnabled ( True )
   self . button_run_glow . setVisible ( True )
  else :
   self . button_run . setEnabled ( False )
   self . button_run . setVisible ( False )
   self . button_run_glow . setEnabled ( False )
   self . button_run_glow . setVisible ( False )
   if 57 - 57: FGGFTFFTFF . TGFFGGFTFGGF - TFGT - ftgf + tftfttgg
 def displayButtonClose ( self , function = "true" ) :
  if ( function == "true" ) :
   if 63 - 63: tftfttgg * FTTGGGF
   self . button_close_glow = xbmcgui . ControlImage ( 1355 , 589 , 360 , 182 , '' , aspectRatio = 0 )
   self . addControl ( self . button_close_glow )
   self . button_close_glow . setVisible ( False )
   self . button_close_glow . setImage ( self . image_button_run_glow )
   self . button_close_glow . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 time=1000 delay=2000 pulse=true condition=Control.IsVisible(%d)' % self . button_close_glow . getId ( ) )
 ] )
   if 69 - 69: tg . tftgtgg
   self . button_close = xbmcgui . ControlButton ( 99999 , 99999 , 360 , 182 , "[B]Close[/B]" ,
 focusTexture = self . image_button_run ,
 noFocusTexture = self . image_button_run , alignment = 2 | 4 ,
 textColor = '0xFF000000' , focusedColor = '0xFF000000' ,
 shadowColor = '0xFFCCCCCC' )
   self . addControl ( self . button_close )
   self . button_close . setVisible ( False )
   self . button_close . setPosition ( 1355 , 589 )
   self . button_close_ID = self . button_close . getId ( )
   self . button_close . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 end=100 delay=1000 time=1000 condition=Control.IsVisible(%d)' % self . button_close . getId ( ) )
 ] )
  elif ( function == "visible" ) :
   self . button_close . setVisible ( True )
   self . button_close_glow . setVisible ( True )
   self . setFocus ( self . button_close )
  else :
   self . button_close . setVisible ( False )
   self . button_close_glow . setVisible ( False )
   if 49 - 49: TGTFFT - TGGF
 def displayPingTest ( self , function = "true" ) :
  if ( function == "true" ) :
   tfttftffffttf = ( self . screenx / 2 ) - ( 340 / 2 )
   ftfgt = ( self . screeny / 2 ) - ( 150 / 2 ) + 50
   self . imgCentertext = xbmcgui . ControlImage ( tfttftffffttf , ftfgt , 340 , 150 , ' ' , aspectRatio = 0 )
   self . addControl ( self . imgCentertext )
   ffgtg = ( self . screenx / 2 ) - ( 800 / 2 )
   FT = ( self . screeny / 2 ) - ( 500 / 2 )
   self . imgPing = xbmcgui . ControlImage ( ffgtg , FT , 800 , 500 , '' , aspectRatio = 1 )
   self . imgPing_glow = xbmcgui . ControlImage ( ffgtg , FT , 800 , 500 , '' , aspectRatio = 1 )
   self . addControl ( self . imgPing )
   self . addControl ( self . imgPing_glow )
   self . imgPing . setVisible ( False )
   self . imgPing_glow . setVisible ( False )
   self . imgPing . setImage ( self . image_ping )
   self . imgPing_glow . setImage ( self . image_ping_glow )
   self . imgPing . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 end=100 delay=1000 time=1000 condition=Control.IsVisible(%d)' % self . imgPing . getId ( ) ) ,
 ( 'conditional' ,
 'effect=fade start=100 end=0 time=300 condition=!Control.IsEnabled(%d)' % self . imgPing . getId ( ) )
 ] )
   self . imgPing_glow . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 time=1000 pulse=true condition=Control.IsEnabled(%d)' % self . imgPing_glow . getId ( ) ) ,
 ( 'conditional' ,
 'effect=fade start=0 end=100 delay=1000 time=1000 condition=Control.IsVisible(%d)' % self . imgPing_glow . getId ( ) ) ,
 ( 'conditional' ,
 'effect=fade start=100 end=0 time=300 condition=!Control.IsEnabled(%d)' % self . imgPing_glow . getId ( ) )
 ] )
   self . imgCentertext . setAnimations ( [
 ( 'conditional' , 'effect=fade start=70 time=1000 condition=true pulse=true' )
 ] )
  elif ( function == "visible" ) :
   self . imgPing . setVisible ( True )
   self . imgPing_glow . setVisible ( True )
  else :
   self . imgPing . setVisible ( False )
   self . imgPing_glow . setVisible ( False )
   if 89 - 89: fgfttfgtgtff + tftgtgg * TGGF * TFGT
   self . imgCentertext . setVisible ( False )
   if 37 - 37: tffffffftt - tg - fgfttfgtgtff
 def displayGaugeTest ( self , function = "true" ) :
  if ( function == "true" ) :
   if 77 - 77: ttffttf * FTFFGTGGTGTTG
   ftggfttffft = ( self . screenx / 2 ) - ( 800 / 2 ) - 5
   TFTFGGFT = ( self . screeny / 2 ) - ( 500 / 2 )
   if 83 - 83: TTGGGFFFF % tfgtff % fftftgf % TGFFGGFTFGGF
   tftgggtgtf = ( self . screenx / 2 ) - ( 80 / 2 ) - 5
   tfgfgffffgtg = ( self . screeny / 2 ) - ( 275 / 2 ) - 60
   self . imgGauge = xbmcgui . ControlImage ( ftggfttffft , TFTFGGFT , 800 , 500 , '' , aspectRatio = 0 )
   self . imgGauge_arrow = xbmcgui . ControlImage ( tftgggtgtf , tfgfgffffgtg , 80 , 275 , '' , aspectRatio = 0 )
   self . addControl ( self . imgGauge )
   self . addControl ( self . imgGauge_arrow )
   self . imgGauge . setVisible ( False )
   self . imgGauge_arrow . setVisible ( False )
   self . imgGauge . setImage ( self . image_gauge )
   self . imgGauge_arrow . setImage ( self . image_gauge_arrow )
   self . imgGauge . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 end=100 delay=1000 time=1000 condition=Control.IsVisible(%d)' % self . imgGauge . getId ( ) ) ,
 ( 'conditional' ,
 'effect=fade start=100 end=0 time=300 condition=!Control.IsEnabled(%d)' % self . imgGauge . getId ( ) )
 ] )
   self . imgGauge_arrow . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 end=100 time=1000 condition=Control.IsVisible(%d)' % self . imgGauge_arrow . getId ( ) ) ,
 ( 'conditional' ,
 'effect=fade start=100 end=0 time=300 condition=!Control.IsEnabled(%d)' % self . imgGauge_arrow . getId ( ) )
 ] )
   if 93 - 93: tg % FGTTF . ttffttf / TGTFFT - TGTFGGG / TGTFFT
   TTGTFFTFGF = ( self . screenx / 2 ) - ( 300 / 2 )
   FFTGGFFGTG = ( self . screeny / 2 ) - ( 100 / 2 ) + 200
   self . dlul_prog_textbox = xbmcgui . ControlLabel ( TTGTFFTFGF , FFTGGFFGTG , 300 , 100 , label = '' ,
 textColor = '0xFFFFFFFF' , font = 'font30' , alignment = 2 | 4 )
   self . addControl ( self . dlul_prog_textbox )
  elif ( function == "visible" ) :
   self . imgGauge . setEnabled ( True )
   self . imgGauge . setVisible ( True )
   self . imgGauge_arrow . setEnabled ( True )
   self . imgGauge_arrow . setVisible ( True )
  else :
   self . imgGauge . setEnabled ( False )
   self . imgGauge . setVisible ( False )
   self . imgGauge_arrow . setEnabled ( False )
   self . imgGauge_arrow . setVisible ( False )
   self . dlul_prog_textbox . setLabel ( '' )
   if 82 - 82: TTGGGFFFF % TGGF / tftgtgg + tftfttgg / fgfttfgtgtff / TGTFGGG
 def displayProgressBar ( self , function = "true" ) :
  if ( function == "true" ) :
   self . imgProgress = xbmcgui . ControlImage ( 500 , 875 , 900 , 30 , '' , aspectRatio = 0 , colorDiffuse = "0xFF00AACC" )
   self . addControl ( self . imgProgress )
   self . imgProgress . setVisible ( False )
   self . imgProgress . setImage ( self . image_progress )
   self . imgProgress . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 end=100 time=500 condition=Control.IsVisible(%d)' % self . imgProgress . getId ( ) ) ,
 ( 'conditional' ,
 'effect=fade start=100 end=0 time=300 condition=!Control.IsEnabled(%d)' % self . imgProgress . getId ( ) )
 ] )
   self . imgProgress . setVisible ( True )
   ftfgttftg = ( self . screenx / 2 ) - ( 250 / 2 )
   TT = ( self . screeny / 2 ) - ( 100 / 2 ) + 300
   self . please_wait_textbox = xbmcgui . ControlLabel ( ftfgttftg , TT , 250 , 100 ,
 label = 'Please wait...' , textColor = '0xFFFFFFFF' ,
 alignment = 2 | 4 )
   self . addControl ( self . please_wait_textbox )
  elif ( function == "visible" ) :
   self . please_wait_textbox . setVisible ( True )
   self . imgProgress . setEnabled ( True )
   self . imgProgress . setVisible ( True )
  else :
   self . please_wait_textbox . setVisible ( False )
   self . imgProgress . setEnabled ( False )
   self . imgProgress . setVisible ( False )
   if 93 - 93: TFTT * tffffffftt + fftftgf
 def displayResults ( self , function = "true" ) :
  if ( function == "true" ) :
   self . imgResults = xbmcgui . ControlImage ( 1375 , 40 , 475 , 225 , '' , aspectRatio = 0 )
   self . addControl ( self . imgResults )
   self . imgResults . setVisible ( False )
   self . imgResults . setImage ( self . image_speedtestresults )
   self . imgResults . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=100 end=0 time=300 delay=1000 condition=!Control.IsEnabled(%d)' % self . imgResults . getId ( ) )
 ] )
   self . imgResults . setVisible ( True )
   if 33 - 33: tg * fgfttfgtgtff - TGTFGGG % TGTFGGG
   self . ping_textbox = xbmcgui . ControlLabel ( 1408 , 190 , 120 , 75 , label = '' , textColor = '0xFFFFFFFF' )
   self . addControl ( self . ping_textbox )
   if 18 - 18: TGTFGGG / tfgtff * TGTFGGG + TGTFGGG * FGGFTFFTFF * TGFFGGFTFGGF
   self . dl_textbox = xbmcgui . ControlLabel ( 1520 , 190 , 120 , 75 , label = '' , textColor = '0xFFFFFFFF' )
   self . addControl ( self . dl_textbox )
   if 11 - 11: fftftgf / tftfttgg - TFTT * tffffffftt + tffffffftt . tftfttgg
   self . ul_textbox = xbmcgui . ControlLabel ( 1700 , 190 , 120 , 75 , label = '' , textColor = '0xFFFFFFFF' )
   self . addControl ( self . ul_textbox )
   if 26 - 26: TFGT % TGFFGGFTFGGF
  elif ( function == "visible" ) :
   self . imgResults . setEnabled ( True )
   self . imgResults . setVisible ( True )
  else :
   self . imgResults . setEnabled ( False )
   self . dl_textbox . setLabel ( '' )
   self . ul_textbox . setLabel ( '' )
   self . ping_textbox . setLabel ( '' )
   if 76 - 76: TFTT * FTTGGGF
 def showEndResult ( self ) :
  self . imgFinalResults = xbmcgui . ControlImage ( 1375 , 55 , 475 , 225 , '' , aspectRatio = 0 )
  self . addControl ( self . imgFinalResults )
  self . imgFinalResults . setVisible ( False )
  self . imgFinalResults . setEnabled ( False )
  if 52 - 52: ttffttf
  self . imgFinalResults . setImage ( image_result )
  self . imgFinalResults . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 end=100 time=1000 delay=100 condition=Control.IsVisible(%d)' % self . imgFinalResults . getId ( ) ) ,
 ( 'conditional' ,
 'effect=zoom end=175 start=100 center=%s time=2000 delay=3000 condition=Control.IsVisible(%d)' % (
 "auto" , self . imgFinalResults . getId ( ) ) ) ,
 ( 'conditional' ,
 'effect=slide end=-100,25 time=2000 delay=3000 tween=linear easing=in condition=Control.IsVisible(%d)' % self . imgFinalResults . getId ( ) )
 ] )
  self . imgFinalResults . setVisible ( True )
  self . imgFinalResults . setEnabled ( True )
  if 19 - 19: TGTFFT
 def showEndResultSP ( self ) :
  self . rec_speed = xbmcgui . ControlTextBox ( 525 , 750 , 950 , 550 , textColor = '0xFFFFFFFF' )
  self . addControl ( self . rec_speed )
  self . rec_speed . setVisible ( False )
  self . rec_speed . setEnabled ( False )
  self . rec_speed . setText ( "" . join ( "[B]Recomenended Speeds for Streaming! \n3 to 5 Mb/s for viewing standard definition 480p video \n5 to 10 Mb/s for viewing high-def 720p video \n10+ Mb/s or more for the best  1080p experience \n10+ Mb/s for the best Live TV Streaming experience \n25 to 50+ Mb/s 4K streaming \nAll Speeds are based on the device not what speed you pay for![/B]" ) )
  self . rec_speed . setAnimations ( [
 ( 'conditional' ,
 'effect=fade start=0 end=100 time=1000 delay=100 condition=Control.IsVisible(%d)' % self . rec_speed . getId ( ) ) ,
 ] )
  self . rec_speed . setVisible ( True )
  self . rec_speed . setEnabled ( True )
  if 25 - 25: TFGT / fftftgf
 def onAction ( self , action ) :
  if action == 10 or action == 92 :
   self . saveClose ( )
   if 31 - 31: ttffttf . tg % TGTFFT . fgfttfgtgtff + TFTT
 def onClick ( self , control ) :
  if control == self . button_run_ID :
   self . testRun = True
   if 71 - 71: TGTFGGG . TTGGGFFFF
   self . displayButtonRun ( False )
   self . displayResults ( )
   self . displayProgressBar ( )
   self . displayPingTest ( )
   self . displayGaugeTest ( )
   if 62 - 62: tffffffftt . TGGF
   self . speedtest ( share = True , simple = True )
   if 61 - 61: tftfttgg - ttffttf - FGTTF
   self . displayProgressBar ( False )
   self . displayPingTest ( False )
   self . displayGaugeTest ( False )
   self . displayResults ( False )
   self . showEndResult ( )
   self . showEndResultSP ( )
   self . displayButtonClose ( "visible" )
  if control == self . button_close_ID :
   self . close ( )
   if 25 - 25: tg * TGGF + TGFFGGFTFGGF . fgfttfgtgtff . fgfttfgtgtff
 def saveClose ( self ) :
  self . close ( )
  if 58 - 58: TGTFFT
 def update_textbox ( self , text ) :
  self . textbox . setText ( "\n" . join ( text ) )
  if 53 - 53: FGTTF
 def error ( self , message ) :
  if 59 - 59: fgfttfgtgtff
  self . imgProgress . setImage ( ' ' )
  self . button_close . setVisible ( True )
  self . setFocus ( self . button_close )
  if 81 - 81: tftfttgg - tftfttgg . FTTGGGF
 def configGauge ( self , speed , last_speed = 0 , time = 1000 ) :
  if last_speed == 0 :
   last_speed = 122
  fgtftfggfgf = 0
  if speed <= 1 :
   fgtftfggfgf = 122 - float ( ( float ( speed ) - float ( 0 ) ) ) * float (
 ( float ( 31 ) / float ( 1 ) ) )
  elif speed <= 2 :
   fgtftfggfgf = 90 - float ( ( float ( speed ) - float ( 1 ) ) ) * float (
 ( float ( 31 ) / float ( 1 ) ) )
  elif speed <= 3 :
   fgtftfggfgf = 58 - float ( ( float ( speed ) - float ( 2 ) ) ) * float (
 ( float ( 29 ) / float ( 1 ) ) )
  elif speed <= 5 :
   fgtftfggfgf = 28 - float ( ( float ( speed ) - float ( 3 ) ) ) * float (
 ( float ( 28 ) / float ( 2 ) ) )
  elif speed <= 10 :
   fgtftfggfgf = float ( ( float ( speed ) - float ( 5 ) ) ) * float (
 ( float ( 28 ) / float ( 5 ) ) )
  elif speed <= 20 :
   fgtftfggfgf = 29 + float ( ( float ( speed ) - float ( 10 ) ) ) * float (
 ( float ( 29 ) / float ( 10 ) ) )
  elif speed <= 30 :
   fgtftfggfgf = 59 + float ( ( float ( speed ) - float ( 20 ) ) ) * float (
 ( float ( 31 ) / float ( 10 ) ) )
  elif speed <= 50 :
   fgtftfggfgf = 91 + float ( ( float ( speed ) - float ( 30 ) ) ) * float (
 ( float ( 31 ) / float ( 20 ) ) )
  elif speed > 50 :
   fgtftfggfgf = 122
  TGTTGTGGTGT = "%.0f" % float ( fgtftfggfgf )
  if speed > 5 :
   TGTTGTGGTGT = '-' + str ( TGTTGTGGTGT )
   if 54 - 54: tffffffftt + fgfttfgtgtff - FGTTF % FGGFTFFTFF
  tftgggtgtf = ( self . screenx / 2 ) - ( 80 / 2 ) + 29
  tfgfgffffgtg = ( self . screeny / 2 ) + ( 275 / 2 ) - 89
  self . imgGauge_arrow . setAnimations ( [
 ( 'conditional' , 'effect=rotate start=%d end=%d center=%d,%d condition=Control.IsVisible(%d) time=%d' % (
 int ( last_speed ) , int ( TGTTGTGGTGT ) , tftgggtgtf , tfgfgffffgtg , self . imgGauge . getId ( ) , time ) )
 ] )
  return TGTTGTGGTGT
  if 3 - 3: fgfttfgtgtff % fgfttfgtgtff
  if 83 - 83: TTGGGFFFF + TGTFGGG
 def downloadSpeed ( self , files , quiet = False ) :
  FFGFTTGTT = timeit . default_timer ( )
  def ftggfffftgf ( q , files ) :
   for file in files :
    ffgf = fgfft ( file , FFGFTTGTT )
    ffgf . start ( )
    q . put ( ffgf , True )
    if 51 - 51: TGGF % TGTFFT
    if not quiet and not tfgfggggfgfg . isSet ( ) :
     sys . stdout . write ( '.' )
     sys . stdout . flush ( )
  tfftf = [ ]
  def FGGTTTGGGGFTF ( q , total_files ) :
   TGFGGGT = 0
   while len ( tfftf ) < total_files :
    ffgf = q . get ( True )
    while ffgf . isAlive ( ) :
     ffgf . join ( timeout = 0.1 )
    tfftf . append ( sum ( ffgf . result ) )
    tff = ( ( sum ( tfftf ) / ( timeit . default_timer ( ) - FFGFTTGTT ) ) / 1000 / 1000 ) * 8
    TGFGGGT = self . configGauge ( tff , TGFGGGT )
    self . dlul_prog_textbox . setLabel ( '%.02f Mbps ' % tff )
    del ffgf
    if 65 - 65: tg * tffffffftt % ttffttf / TFTT - TFGT / TGGF
    if 56 - 56: TGTFFT * FGGFTFFTFF * TGTFGGG
  ftftfgtgtttft = Queue ( 6 )
  FTGGTTTFFFGTT = threading . Thread ( target = ftggfffftgf , args = ( ftftfgtgtttft , files ) )
  FGTTGF = threading . Thread ( target = FGGTTTGGGGFTF , args = ( ftftfgtgtttft ,
 len ( files ) ) )
  FFGFTTGTT = timeit . default_timer ( )
  FTGGTTTFFFGTT . start ( )
  FGTTGF . start ( )
  while FTGGTTTFFFGTT . isAlive ( ) :
   FTGGTTTFFFGTT . join ( timeout = 0.1 )
  while FGTTGF . isAlive ( ) :
   FGTTGF . join ( timeout = 0.1 )
  return sum ( tfftf ) / ( timeit . default_timer ( ) - FFGFTTGTT )
  if 83 - 83: tftfttgg - TFGT / TGGF / TGTFGGG + ftgf - tg
 def uploadSpeed ( self , url , sizes , quiet = False ) :
  if 4 - 4: ttffttf * tftgtgg % FGTTF * FGGFTFFTFF % tfgtff - ftgf
  FFGFTTGTT = timeit . default_timer ( )
  if 67 - 67: tftfttgg + TGFFGGFTFGGF . fgfttfgtgtff . TTGGGFFFF
  if 98 - 98: FTTGGGF
  def ftggfffftgf ( q , sizes ) :
   for tfffftgftttt in sizes :
    ffgf = fffgtt ( url , FFGFTTGTT , tfffftgftttt )
    ffgf . start ( )
    q . put ( ffgf , True )
    if not quiet and not tfgfggggfgfg . isSet ( ) :
     sys . stdout . write ( '.' )
     sys . stdout . flush ( )
  tfftf = [ ]
  def FGGTTTGGGGFTF ( q , total_sizes ) :
   TGFGGGT = 0
   while len ( tfftf ) < total_sizes :
    ffgf = q . get ( True )
    while ffgf . isAlive ( ) :
     ffgf . join ( timeout = 0.1 )
    tfftf . append ( ffgf . result )
    tff = ( ( sum ( tfftf ) / ( timeit . default_timer ( ) - FFGFTTGTT ) ) / 1000 / 1000 ) * 8
    TGFGGGT = self . configGauge ( tff , TGFGGGT )
    self . dlul_prog_textbox . setLabel ( '%.02f Mbps ' % tff )
    del ffgf
    if 100 - 100: FTTGGGF % ttffttf
    if 86 - 86: tfgtff . tg - tffffffftt . tftgtgg + TFGT
  ftftfgtgtttft = Queue ( 6 )
  FTGGTTTFFFGTT = threading . Thread ( target = ftggfffftgf , args = ( ftftfgtgtttft , sizes ) )
  FGTTGF = threading . Thread ( target = FGGTTTGGGGFTF , args = ( ftftfgtgtttft ,
 len ( sizes ) ) )
  FFGFTTGTT = timeit . default_timer ( )
  FTGGTTTFFFGTT . start ( )
  FGTTGF . start ( )
  while FTGGTTTFFFGTT . isAlive ( ) :
   FTGGTTTFFFGTT . join ( timeout = 0.1 )
  while FGTTGF . isAlive ( ) :
   FGTTGF . join ( timeout = 0.1 )
  return sum ( tfftf ) / ( timeit . default_timer ( ) - FFGFTTGTT )
  if 57 - 57: fgfttfgtgtff . FGTTF . TFTT * FGGFTFFTFF + TGTFGGG . TFTT
  if 57 - 57: TGTFGGG
 def speedtest ( self , list = False , mini = None , server = None , share = False , simple = False , src = None , timeout = 10 ,

 units = ( 'bit' , 8 ) , version = False ) :
  self . imgPing . setVisible ( True )
  self . imgPing_glow . setVisible ( True )
  TGGTFFFGT = [ 'Speed Test Script Executed' ]
  if 90 - 90: FTFFGTGGTGTTG % fftftgf
  global tfgfggggfgfg , TGG
  tfgfggggfgfg = threading . Event ( )
  if 73 - 73: tg * FTTGGGF + TFGT + fftftgf
  socket . setdefaulttimeout ( timeout )
  if 40 - 40: TTGGGFFFF . tftfttgg * TGTFGGG + ttffttf + ttffttf
  if src :
   TGG = src
   socket . socket = TGFGTGTT
   if 9 - 9: TGGF % tffffffftt . ftgf % TGGF
  TGGTFFFGT . append ( 'Retrieving speedtest.net configuration' )
  self . update_textbox ( TGGTFFFGT )
  if not simple :
   TTFFTFTG ( 'Retrieving speedtest.net configuration' )
  try :
   FGFTF = ttttftffgtgtg ( )
  except URLError :
   TTFFTFTG ( 'Cannot retrieve speedtest configuration' )
   return False
   if 32 - 32: FGGFTFFTFF
  TGGTFFFGT . append ( 'Retrieving speedtest.net server list' )
  self . update_textbox ( TGGTFFFGT )
  self . imgCentertext . setImage ( self . image_centertext_testingping )
  TTFFTFTG ( 'Retrieving speedtest.net server list...' )
  if 31 - 31: FTFFGTGGTGTTG / tftgtgg / TGFFGGFTFGGF
  TG = TTFTFFTF ( FGFTF [ 'client' ] )
  if 41 - 41: tfgtff
  TGGTFFFGT . append ( 'Testing from %(isp)s (%(ip)s)' % FGFTF [ 'client' ] )
  self . update_textbox ( TGGTFFFGT )
  TTFFTFTG ( 'Testing from %(isp)s (%(ip)s)...' % FGFTF [ 'client' ] )
  if 10 - 10: tfgtff / tfgtff / TGTFGGG . TGTFGGG
  tt = FTGGGF ( TG )
  if 98 - 98: tfgtff / TGTFFT . tg + tftgtgg
  try :
   TGGTFFFGT . append ( 'Selecting best server based on latency' )
   self . update_textbox ( TGGTFFFGT )
   TTFFTFTG ( 'Selecting best server based on latency' )
  except : pass
  try :
   TGGTFFFGT . append ( 'Hosted by: %(sponsor)s' % tt )
   self . update_textbox ( TGGTFFFGT )
   TTFFTFTG ( 'Hosted by %(sponsor)s' % tt )
  except : pass
  try :
   TGGTFFFGT . append ( 'Host Server: %(host)s' % tt )
   self . update_textbox ( TGGTFFFGT )
   TTFFTFTG ( 'Host Server: %(host)s' % tt )
  except : pass
  try :
   TGGTFFFGT . append ( 'Country: %(country)s' % tt )
   self . update_textbox ( TGGTFFFGT )
   TTFFTFTG ( 'Location: %(country)s' % tt )
  except : pass
  try :
   TGGTFFFGT . append ( 'City , State: %(name)s' % tt )
   self . update_textbox ( TGGTFFFGT )
   TTFFTFTG ( 'City , State: %(name)s' % tt )
  except : pass
  try :
   FF = 0.62
   TFFFGFTGF = '%(d)0.2f ' % tt
   TGFFGFFGGFGT = float ( TFFFGFTGF )
   fgtftt = TGFFGFFGGFGT * FF
   TGGTFFFGT . append ( 'Distance: %s mi' % fgtftt )
   self . update_textbox ( TGGTFFFGT )
   TTFFTFTG ( 'Distance: %s' % fgtftt )
  except : pass
  try :
   TGGTFFFGT . append ( 'Ping: %(latency)s ms' % tt )
   self . update_textbox ( TGGTFFFGT )
   self . ping_textbox . setLabel ( "%.0f" % float ( tt [ 'latency' ] ) )
   TTFFTFTG ( 'Ping: %(latency)s ms' % tt )
  except : pass
  self . imgCentertext . setImage ( ' ' )
  self . imgPing . setEnabled ( False )
  self . imgPing_glow . setEnabled ( False )
  if 55 - 55: fftftgf - TGGF + TTGGGFFFF + FTTGGGF % TFGT
  FFTGGFGTT = [ 350 , 500 , 750 , 1000 , 1500 , 2000 , 2500 , 3000 , 3500 , 4000 ]
  fgtgtttgtff = [ ]
  for ttgtgttfgt in FFTGGFGTT :
   for fgfgtttgfg in range ( 0 , 4 ) :
    fgtgtttgtff . append ( '%s/random%sx%s.jpg' %
 ( os . path . dirname ( tt [ 'url' ] ) , ttgtgttfgt , ttgtgttfgt ) )
  self . imgGauge . setVisible ( True )
  time . sleep ( 1 )
  self . configGauge ( 0 )
  self . imgGauge_arrow . setVisible ( True )
  if 36 - 36: fftftgf . tfgtff % fftftgf % tftgtgg
  TGGTFFFGT . append ( 'Testing download speed' )
  self . update_textbox ( TGGTFFFGT )
  if not simple :
   TTFFTFTG ( 'Testing download speed' , end = '' )
  FTTTTTGT = self . downloadSpeed ( fgtgtttgtff , simple )
  if not simple :
   TTFFTFTG ( )
  TGGTFFFGT . append ( 'Download: %0.2f M%s/s' % ( ( FTTTTTGT / 1000 / 1000 ) * units [ 1 ] , units [ 0 ] ) )
  self . update_textbox ( TGGTFFFGT )
  self . dl_textbox . setLabel ( "%.2f" % float ( ( FTTTTTGT / 1000 / 1000 ) * units [ 1 ] ) )
  TTFFTFTG ( 'Download: %0.2f M%s/s' %
 ( ( FTTTTTGT / 1000 / 1000 ) * units [ 1 ] , units [ 0 ] ) )
  self . configGauge ( 0 , ( FTTTTTGT / 1000 / 1000 ) * 8 , time = 3000 )
  time . sleep ( 2 )
  if 51 - 51: FTFFGTGGTGTTG . fftftgf + FTFFGTGGTGTTG
  ftftt = [ int ( .25 * 1000 * 1000 ) , int ( .5 * 1000 * 1000 ) ]
  FFTGGFGTT = [ ]
  for ttgtgttfgt in ftftt :
   for fgfgtttgfg in range ( 0 , 25 ) :
    FFTGGFGTT . append ( ttgtgttfgt )
    if 44 - 44: TGTFFT / FTFFGTGGTGTTG % ftgf * tffffffftt % fftftgf
  TGGTFFFGT . append ( 'Testing upload speed' )
  self . update_textbox ( TGGTFFFGT )
  if not simple :
   TTFFTFTG ( 'Testing upload speed' , end = '' )
  FTG = self . uploadSpeed ( tt [ 'url' ] , FFTGGFGTT , simple )
  if not simple :
   TTFFTFTG ( )
  TGGTFFFGT . append ( 'Upload: %0.2f M%s/s' % ( ( FTG / 1000 / 1000 ) * units [ 1 ] , units [ 0 ] ) )
  self . update_textbox ( TGGTFFFGT )
  self . ul_textbox . setLabel ( "%.2f" % float ( ( FTG / 1000 / 1000 ) * units [ 1 ] ) )
  TTFFTFTG ( 'Upload: %0.2f M%s/s' %
 ( ( FTG / 1000 / 1000 ) * units [ 1 ] , units [ 0 ] ) )
  self . configGauge ( 0 , ( FTG / 1000 / 1000 ) * 8 , time = 3000 )
  time . sleep ( 2 )
  if 24 - 24: ftgf / FGGFTFFTFF + ftgf
  if share :
   TGFGGF = int ( round ( ( FTTTTTGT / 1000 ) * 8 , 0 ) )
   TFTF = int ( round ( tt [ 'latency' ] , 0 ) )
   tttttgtgg = int ( round ( ( FTG / 1000 ) * 8 , 0 ) )
   if 30 - 30: FTFFGTGGTGTTG . TGTFFT . ttffttf / fgfttfgtgtff
   FFTGTG = [
 'download=%s' % TGFGGF ,
 'ping=%s' % TFTF ,
 'upload=%s' % tttttgtgg ,
 'promo=' ,
 'startmode=%s' % 'pingselect' ,
 'recommendedserverid=%s' % tt [ 'id' ] ,
 'accuracy=%s' % 1 ,
 'serverid=%s' % tt [ 'id' ] ,
 'hash=%s' % md5 ( ( '%s-%s-%s-%s' %
 ( TFTF , tttttgtgg , TGFGGF , '297aae72' ) )
 . encode ( ) ) . hexdigest ( ) ]
   if 56 - 56: TGTFFT . tg + tfgtff
   fgtTFTT = { 'Referer' : 'https://c.speedtest.net/flash/speedtest.swf' }
   TGGGGTGFTTGG = FGGGTFTGT ( 'https://www.speedtest.net/api/api.php' ,
 data = '&' . join ( FFTGTG ) . encode ( ) ,
 headers = fgtTFTT )
   tfffgtgffggft = TTF ( TGGGGTGFTTGG )
   if tfffgtgffggft is False :
    TTFFTFTG ( 'Could not submit results to speedtest.net' )
    return False
   FGTTGTGTFFG = tfffgtgffggft . read ( )
   FFTGGTFF = tfffgtgffggft . code
   tfffgtgffggft . close ( )
   if int ( FFTGGTFF ) != 200 :
    TTFFTFTG ( 'Could not submit results to speedtest.net' )
    return False
   tgfgtg = parse_qs ( FGTTGTGTFFG . decode ( ) )
   TFGTTGTGGFG = tgfgtg . get ( 'resultid' )
   if not TFGTTGTGGFG or len ( TFGTTGTGGFG ) != 1 :
    TTFFTFTG ( 'Could not submit results to speedtest.net' )
    return False
   TTFFTFTG ( 'Share results: https://www.speedtest.net/result/%s.png' % TFGTTGTGGFG [ 0 ] )
   global image_result
   image_result = 'https://www.speedtest.net/result/%s.png' % TFGTTGTGGFG [ 0 ]
   if 59 - 59: ftgf % FTFFGTGGTGTTG . FGTTF
   import urllib
   if not os . path . exists ( FFTGFTFT ) : os . makedirs ( FFTGFTFT )
   FFTFGF = xbmc . translatePath ( 'special://home/userdata/addon_data/' + TTGFTTGF + '/SpeedTest/' )
   TGFGGGGGFGFGG = 'https://www.speedtest.net/result/%s.png' % TFGTTGTGGFG [ 0 ]
   urllib . urlretrieve ( TGFGGGGGFGFGG , FFTFGF + '%s.png' % TFGTTGTGGFG [ 0 ] )
   if 77 - 77: TGFFGGFTFGGF + tftgtgg / ftgf + tg * fgfttfgtgtff
   if 28 - 28: fftftgf + FGGFTFFTFF / TGGF % tftfttgg % tfgtff - tg
def speedtest ( ) :
 FFFGTFGTFG = fttggt ( "main.xml" , ftgfTTTT . getAddonInfo ( 'path' ) , "Defaultskin" )
 del FFFGTFGTFG
 if 21 - 21: ftgf . TGTFGGG . ttffttf / tfgtff / TGTFGGG
 if 17 - 17: ttffttf / ttffttf / TGGF
# fd678faae9ac167tc83abf78e5cb2f3f0688d3ag
