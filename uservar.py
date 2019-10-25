import xbmcaddon

import os

#########################################################
#         Global Variables - DON'T EDIT!!!              #
#########################################################
ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
#########################################################

#########################################################
#        User Edit Variables                            #
#########################################################
ADDONTITLE = '[B][COLOR grey]Soul TV[/COLOR][/B] Helper'
BUILDERNAME = 'Seoul'
EXCLUDES = [ADDON_ID, 'repository.soultv', 'pvr.iptvsimpleclient', 'inputstream.adaptive', 'inputstream.rtmp', 'service.coreelec.settings', 'service.libreelec.settings']
# Text File with build info in it.
BUILDFILE = 'https://raw.githubusercontent.com/SoulTV/soultv.github.io/master/Helper%20Files/text/builds.txt'
# How often you would like it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK = 0
# Text File with apk info in it.  Leave as 'http://' to ignore
APKFILE = 'http://'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE = ''
YOUTUBEFILE = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE = 'http://'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE = 'https://raw.githubusercontent.com/SoulTV/soultv.github.io/master/Helper%20Files/text/advanced.txt'
#########################################################

#########################################################
#        Theming Menu Items                             #
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS = os.path.join(ART, 'builds.png')
ICONMAINT = os.path.join(ART, 'maintenance.png')
ICONSPEED = os.path.join(ART, 'speed.png')
ICONAPK = os.path.join(ART, 'apkinstaller.png')
ICONADDONS = os.path.join(ART, 'addoninstaller.png')
ICONYOUTUBE = os.path.join(ART, 'youtube.png')
ICONSAVE = os.path.join(ART, 'savedata.png')
ICONTRAKT = os.path.join(ART, 'keeptrakt.png')
ICONREAL = os.path.join(ART, 'keepdebrid.png')
ICONLOGIN = os.path.join(ART, 'keeplogin.png')
ICONCONTACT = os.path.join(ART, 'information.png')
ICONSETTINGS = os.path.join(ART, 'settings.png')
# Hide the section separators 'Yes' or 'No'
HIDESPACERS = 'No'
# Character used in separator
SPACER = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1 = 'grey'
COLOR2 = 'grey'
# Primary menu items   / {0} is the menu item and is required
THEME1 = '[COLOR '+COLOR1+'][B][I]([COLOR '+COLOR2+']Soul TV[/COLOR])[/I][/B][/COLOR] [COLOR '+COLOR2+']{0}[/COLOR]'
# Build Names          / {0} is the menu item and is required
THEME2 = '[COLOR '+COLOR2+']{0}[/COLOR]'
# Alternate items      / {0} is the menu item and is required
THEME3 = '[COLOR '+COLOR1+']{0}[/COLOR]'
# Current Build Header / {0} is the menu item and is required
THEME4 = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']{0}[/COLOR]'
# Current Theme Header / {0} is the menu item and is required
THEME5 = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']{0}[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT = 'No'
# You can add \n to do line breaks
CONTACT = 'Thank you for choosing Soul TV.\n\nContact us at soultvstudio@gmail.com'
# Images used for the contact window.  http:// for default icon and fanart
CONTACTICON = os.path.join(ART, 'qricon.png')
CONTACTFANART = 'https://raw.githubusercontent.com/SoulTV/soultv.github.io/master/Helper%20Files/Images/fanart.jpg'
#########################################################

#########################################################
#        Auto Update For Those With No Repo             #
#########################################################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE = 'No'
# Url to wizard version
WIZARDFILE = BUILDFILE
#########################################################

#########################################################
#        Auto Install Repo If Not Installed             #
#########################################################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL = 'Yes'
# Addon ID for the repository
REPOID = 'repository.soultv'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML = 'https://raw.githubusercontent.com/SoulTV/soultv.github.io/master/zips/addons.xml'
# Url to folder zip is located in
REPOZIPURL = 'https://github.com/SoulTV/soultv.github.io/raw/master/zips/repository.soultv/'
#########################################################

#########################################################
#        Notification Window                            #
#########################################################
# Enable Notification screen Yes or No
ENABLE = 'Yes'
# Url to notification file
NOTIFICATION = 'http://'
# Use either 'Text' or 'Image'
HEADERTYPE = 'Text'
# Font size of header
FONTHEADER = 'Font14'
HEADERMESSAGE = '[B][COLOR grey]Soul TV[/COLOR][/B] Helper'
# url to image if using Image 424x180
HEADERIMAGE = 'http://'
# Font for Notification Window
FONTSETTINGS = 'Font13'
# Background for Notification Window
BACKGROUND = 'http://'
#########################################################
