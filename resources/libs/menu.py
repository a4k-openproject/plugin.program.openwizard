###########################
###### Menu Items   #######
###########################
#addDir (display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
#addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)

# MIGRATION: move to menu
def index():
    errors = int(errorChecking(count=True))
    errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'

    if AUTOUPDATE == 'Yes':
        wizfile = wiz.textCache(WIZARDFILE)
        if not wizfile == False:
            ver = wiz.checkWizard('version')
            if ver > VERSION: addFile('%s [v%s] [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (ADDONTITLE, VERSION, ver), 'wizardupdate', themeit=THEME2)
            else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
        else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
    else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
    if len(BUILDNAME) > 0:
        version = wiz.checkBuild(BUILDNAME, 'version')
        build = '%s (v%s)' % (BUILDNAME, BUILDVERSION)
        if version > BUILDVERSION: build = '%s [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (build, version)
        addDir(build,'viewbuild', BUILDNAME, themeit=THEME4)
        themefile = wiz.themeCount(BUILDNAME)
        if not themefile == False:
            addFile('None' if BUILDTHEME == "" else BUILDTHEME, 'theme', BUILDNAME, themeit=THEME5)
    else: addDir('None', 'builds', themeit=THEME4)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addDir ('Builds', 'builds',   icon=ICONBUILDS,   themeit=THEME1)
    addDir ('Maintenance', 'maint',    icon=ICONMAINT,    themeit=THEME1)
    if wiz.platform() == 'android' or DEVELOPER == 'true': addDir ('Apk Installer' ,'apk', icon=ICONAPK, themeit=THEME1)
    if not ADDONFILE == 'http://': addDir ('Addon Installer' ,'addons', icon=ICONADDONS, themeit=THEME1)
    if not YOUTUBEFILE == 'http://' and not YOUTUBETITLE == '': addDir (YOUTUBETITLE ,'youtube', icon=ICONYOUTUBE, themeit=THEME1)
    addDir ('Save Data', 'savedata', icon=ICONSAVE,     themeit=THEME1)
    if HIDECONTACT == 'No': addFile('Contact' ,'contact', icon=ICONCONTACT,  themeit=THEME1)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Upload Log File', 'uploadlog',       icon=ICONMAINT, themeit=THEME1)
    addFile('View Errors in Log: %s' % (errorsfound), 'viewerrorlog', icon=ICONMAINT, themeit=THEME1)
    if errors > 0: addFile('View Last Error In Log', 'viewerrorlast', icon=ICONMAINT, themeit=THEME1)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Settings', 'settings', icon=ICONSETTINGS, themeit=THEME1)
    addFile('Force Update Text Files', 'forcetext', icon=ICONMAINT, themeit=THEME1)
    if DEVELOPER == 'true': addDir('Developer Menu', 'developer', icon=ICON, themeit=THEME1)
    setView('files', 'viewType')


# MIGRATION: move to menu
def buildMenu():
    bf = wiz.textCache(BUILDFILE)
    if bf == False:
        WORKINGURL = wiz.workingURL(BUILDFILE)
        addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
        addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
        addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
        return
    total, count15, count16, count17, count18, adultcount, hidden = wiz.buildCount()
    third = False; addin = []
    if THIRDPARTY == 'true':
        if not THIRD1NAME == '' and not THIRD1URL == '': third = True; addin.append('1')
        if not THIRD2NAME == '' and not THIRD2URL == '': third = True; addin.append('2')
        if not THIRD3NAME == '' and not THIRD3URL == '': third = True; addin.append('3')
    link  = bf.replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"').replace('adult=""', 'adult="no"')
    match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
    if total == 1 and third == False:
        for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
            if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
            if not DEVELOPER == 'true' and wiz.strTest(name): continue
            viewBuild(match[0][0])
            return
    addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
    addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    if third == True:
        for item in addin:
            name = eval('THIRD%sNAME' % item)
            addDir ("[B]%s[/B]" % name, 'viewthirdparty', item, icon=ICONBUILDS, themeit=THEME3)
    if len(match) >= 1:
        if SEPERATE == 'true':
            for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                if not DEVELOPER == 'true' and wiz.strTest(name): continue
                menu = createMenu('install', '', name)
                addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
        else:
            if count18 > 0:
                state = '+' if SHOW18 == 'false' else '-'
                addFile('[B]%s Leia Builds(%s)[/B]' % (state, count18), 'togglesetting',  'show17', themeit=THEME3)
                if SHOW18 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv == 18:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
            if count17 > 0:
                state = '+' if SHOW17 == 'false' else '-'
                addFile('[B]%s Krypton Builds(%s)[/B]' % (state, count17), 'togglesetting',  'show17', themeit=THEME3)
                if SHOW17 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv == 17:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
            if count16 > 0:
                state = '+' if SHOW16 == 'false' else '-'
                addFile('[B]%s Jarvis Builds(%s)[/B]' % (state, count16), 'togglesetting',  'show16', themeit=THEME3)
                if SHOW16 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv == 16:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
            if count15 > 0:
                state = '+' if SHOW15 == 'false' else '-'
                addFile('[B]%s Isengard and Below Builds(%s)[/B]' % (state, count15), 'togglesetting',  'show15', themeit=THEME3)
                if SHOW15 == 'true':
                    for name, version, url, gui, kodi, theme, icon, fanart, adult, description in match:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        if not DEVELOPER == 'true' and wiz.strTest(name): continue
                        kodiv = int(float(kodi))
                        if kodiv <= 15:
                            menu = createMenu('install', '', name)
                            addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
    elif hidden > 0:
        if adultcount > 0:
            addFile('There is currently only Adult builds', '', icon=ICONBUILDS, themeit=THEME3)
            addFile('Enable Show Adults in Addon Settings > Misc', '', icon=ICONBUILDS, themeit=THEME3)
        else:
            addFile('Currently No Builds Offered from %s' % ADDONTITLE, '', icon=ICONBUILDS, themeit=THEME3)
    else: addFile('Text file for builds not formated correctly.', '', icon=ICONBUILDS, themeit=THEME3)
    setView('files', 'viewType')


# MIGRATION: move to menu
def viewBuild(name):
    bf = wiz.textCache(BUILDFILE)
    if bf == False:
        WORKINGURL = wiz.workingURL(BUILDFILE)
        addFile('Url for txt file not valid', '', themeit=THEME3)
        addFile('%s' % WORKINGURL, '', themeit=THEME3)
        return
    if wiz.checkBuild(name, 'version') == False:
        addFile('Error reading the txt file.', '', themeit=THEME3)
        addFile('%s was not found in the builds list.' % name, '', themeit=THEME3)
        return
    link = bf.replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
    match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?inor="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?nfo="(.+?)".+?escription="(.+?)"' % name).findall(link)
    for version, url, minor, gui, kodi, themefile, icon, fanart, preview, adult, info, description in match:
        icon        = icon
        fanart      = fanart
        build       = '%s (v%s)' % (name, version)
        if BUILDNAME == name and version > BUILDVERSION:
            build = '%s [COLOR red][CURRENT v%s][/COLOR]' % (build, BUILDVERSION)
        addFile(build, '', description=description, fanart=fanart, icon=icon, themeit=THEME4)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        addDir ('Save Data Menu',       'savedata', icon=ICONSAVE,     themeit=THEME3)
        addFile('Build Information',    'buildinfo', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
        if not preview == "http://": addFile('View Video Preview', 'buildpreview', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
        temp1 = int(float(KODIV)); temp2 = int(float(kodi))
        if not temp1 == temp2:
            if temp1 == 16 and temp2 <= 15: warning = False
            else: warning = True
        else: warning = False
        if warning == True:
            addFile('[I]Build designed for kodi version %s(installed: %s)[/I]' % (str(kodi), str(KODIV)), '', fanart=fanart, icon=icon, themeit=THEME3)
        addFile(wiz.sep('INSTALL'), '', fanart=fanart, icon=icon, themeit=THEME3)
        addFile('Fresh Install'   , 'install', name, 'fresh'  , description=description, fanart=fanart, icon=icon, themeit=THEME1)
        addFile('Standard Install', 'install', name, 'normal' , description=description, fanart=fanart, icon=icon, themeit=THEME1)
        if not gui == 'http://': addFile('Apply guiFix'    , 'install', name, 'gui'     , description=description, fanart=fanart, icon=icon, themeit=THEME1)
        if not themefile == 'http://':
            themecheck = wiz.textCache(themefile)
            if not themecheck == False:
                addFile(wiz.sep('THEMES'), '', fanart=fanart, icon=icon, themeit=THEME3)
                link  = themecheck.replace('\n','').replace('\r','').replace('\t','')
                match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
                for themename, themeurl, themeicon, themefanart, themeadult, description in match:
                    if not SHOWADULT == 'true' and themeadult.lower() == 'yes': continue
                    themeicon   = themeicon   if themeicon   == 'http://' else icon
                    themefanart = themefanart if themefanart == 'http://' else fanart
                    addFile(themename if not themename == BUILDTHEME else "[B]%s (Installed)[/B]" % themename, 'theme', name, themename, description=description, fanart=themefanart, icon=themeicon, themeit=THEME3)
    setView('files', 'viewType')



# MIGRATION: move to menu?
def apkScraper(name=""):
    if name == 'kodi':
        kodiurl1 = 'http://mirrors.kodi.tv/releases/android/arm/'
        kodiurl2 = 'http://mirrors.kodi.tv/releases/android/arm/old/'
        url1 = wiz.openURL(kodiurl1).replace('\n', '').replace('\r', '').replace('\t', '')
        url2 = wiz.openURL(kodiurl2).replace('\n', '').replace('\r', '').replace('\t', '')
        x = 0
        match1 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url1)
        match2 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url2)

        addFile("Official Kodi Apk\'s", themeit=THEME1)
        rc = False
        for url, name, size, date in match1:
            if url in ['../', 'old/']: continue
            if not url.endswith('.apk'): continue
            if not url.find('_') == -1 and rc == True: continue
            try:
                tempname = name.split('-')
                if not url.find('_') == -1:
                    rc = True
                    name2, v2 = tempname[2].split('_')
                else:
                    name2 = tempname[2]
                    v2 = ''
                title = "[COLOR %s]%s v%s%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], v2.upper(), name2, COLOR2, size.replace(' ', ''), COLOR1, date)
                download = urljoin(kodiurl1, url)
                addFile(title, 'apkinstall', "%s v%s%s %s" % (tempname[0].title(), tempname[1], v2.upper(), name2), download)
                x += 1
            except:
                wiz.log("Error on: %s" % name)

        for url, name, size, date in match2:
            if url in ['../', 'old/']: continue
            if not url.endswith('.apk'): continue
            if not url.find('_') == -1: continue
            try:
                tempname = name.split('-')
                title = "[COLOR %s]%s v%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], tempname[2], COLOR2, size.replace(' ', ''), COLOR1, date)
                download = urljoin(kodiurl2, url)
                addFile(title, 'apkinstall', "%s v%s %s" % (tempname[0].title(), tempname[1], tempname[2]), download)
                x += 1
            except:
                wiz.log("Error on: %s" % name)
        if x == 0: addFile("Error Kodi Scraper Is Currently Down.")

# MIGRATION: move to menu
def apkMenu(name=None, url=None):
    if url == None:
        addDir ('Official Kodi Apk\'s', 'apkscrape', 'kodi', icon=ICONAPK, themeit=THEME1)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    if not APKFILE == 'http://':
        if url == None:
            TEMPAPKFILE = wiz.textCache(uservar.APKFILE)
            if TEMPAPKFILE == False: APKWORKING  = wiz.workingURL(uservar.APKFILE)
        else:
            TEMPAPKFILE = wiz.textCache(url)
            if TEMPAPKFILE == False: APKWORKING  = wiz.workingURL(url)
        if not TEMPAPKFILE == False:
            link = TEMPAPKFILE.replace('\n','').replace('\r','').replace('\t','')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                x = 0
                for aname, section, url, icon, fanart, adult, description in match:
                    if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                    if section.lower() == 'yes':
                        x += 1
                        addDir ("[B]%s[/B]" % aname, 'apk', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    elif section.lower() == 'yes':
                        x += 1
                        # addFile(aname, 'rominstall', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    else:
                        x += 1
                        addFile(aname, 'apkinstall', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    if x == 0:
                        addFile("No addons adde0d to this menu yet!", '', themeit=THEME2)
            else: wiz.log("[APK Menu] ERROR: Invalid Format.", xbmc.LOGERROR)
        else:
            wiz.log("[APK Menu] ERROR: URL for apk list not working.", xbmc.LOGERROR)
            addFile('Url for txt file not valid', '', themeit=THEME3)
            addFile('%s' % APKWORKING, '', themeit=THEME3)
        return
    else: wiz.log("[APK Menu] No APK list added.")
    setView('files', 'viewType')

# MIGRATION: move to menu
def addonMenu(name=None, url=None):
    if not ADDONFILE == 'http://':
        if url == None:
            TEMPADDONFILE = wiz.textCache(uservar.ADDONFILE)
            if TEMPADDONFILE == False: ADDONWORKING  = wiz.workingURL(uservar.ADDONFILE)
        else:
            TEMPADDONFILE = wiz.textCache(url)
            if TEMPADDONFILE == False: ADDONWORKING  = wiz.workingURL(url)
        if not TEMPADDONFILE == False:
            link = TEMPADDONFILE.replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
            match = re.compile('name="(.+?)".+?lugin="(.+?)".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                x = 0
                for aname, plugin, aurl, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
                    if plugin.lower() == 'section':
                        x += 1
                        addDir ("[B]%s[/B]" % aname, 'addons', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    elif plugin.lower() == 'skin':
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        x += 1
                        addFile("[B]%s[/B]" % aname, 'skinpack', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    elif plugin.lower() == 'pack':
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        x += 1
                        addFile("[B]%s[/B]" % aname, 'addonpack', aname, aurl, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    else:
                        if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
                        try:
                            add    = xbmcaddon.Addon(id=plugin).getAddonInfo('path')
                            if os.path.exists(add):
                                aname   = "[COLOR springgreen][Installed][/COLOR] %s" % aname
                        except:
                            pass
                        x += 1
                        addFile(aname, 'addoninstall', plugin, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
                    if x < 1:
                        addFile("No addons added to this menu yet!", '', themeit=THEME2)
            else:
                addFile('Text File not formated correctly!', '', themeit=THEME3)
                wiz.log("[Addon Menu] ERROR: Invalid Format.")
        else:
            wiz.log("[Addon Menu] ERROR: URL for Addon list not working.")
            addFile('Url for txt file not valid', '', themeit=THEME3)
            addFile('%s' % ADDONWORKING, '', themeit=THEME3)
    else: wiz.log("[Addon Menu] No Addon list added.")
    setView('files', 'viewType')

# MIGRATION: move to menu
def youtubeMenu(name=None, url=None):
    if not YOUTUBEFILE == 'http://':
        if url == None:
            TEMPYOUTUBEFILE = wiz.textCache(uservar.YOUTUBEFILE)
            if TEMPYOUTUBEFILE == False: YOUTUBEWORKING  = wiz.workingURL(uservar.YOUTUBEFILE)
        else:
            TEMPYOUTUBEFILE = wiz.textCache(url)
            if TEMPYOUTUBEFILE == False: YOUTUBEWORKING  = wiz.workingURL(url)
        if not TEMPYOUTUBEFILE == False:
            link = TEMPYOUTUBEFILE.replace('\n','').replace('\r','').replace('\t','')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                for name, section, url, icon, fanart, description in match:
                    if section.lower() == "yes":
                        addDir ("[B]%s[/B]" % name, 'youtube', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    else:
                        addFile(name, 'viewVideo', url=url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
            else: wiz.log("[YouTube Menu] ERROR: Invalid Format.")
        else:
            wiz.log("[YouTube Menu] ERROR: URL for YouTube list not working.")
            addFile('Url for txt file not valid', '', themeit=THEME3)
            addFile('%s' % YOUTUBEWORKING, '', themeit=THEME3)
    else: wiz.log("[YouTube Menu] No YouTube list added.")
    setView('files', 'viewType')

# MIGRATION: move to menu
def maintMenu(view=None):
    on = '[B][COLOR springgreen]ON[/COLOR][/B]'; off = '[B][COLOR red]OFF[/COLOR][/B]'
    autoclean   = 'true' if AUTOCLEANUP    == 'true' else 'false'
    cache       = 'true' if AUTOCACHE      == 'true' else 'false'
    packages    = 'true' if AUTOPACKAGES   == 'true' else 'false'
    thumbs      = 'true' if AUTOTHUMBS     == 'true' else 'false'
    maint       = 'true' if SHOWMAINT      == 'true' else 'false'
    includevid  = 'true' if INCLUDEVIDEO   == 'true' else 'false'
    includeall  = 'true' if INCLUDEALL     == 'true' else 'false'
    thirdparty  = 'true' if THIRDPARTY     == 'true' else 'false'
    errors = int(errorChecking(count=True))
    errorsfound = str(errors) + ' Error(s) Found' if errors > 0 else 'None Found'
    wizlogsize = ': [COLOR red]Not Found[/COLOR]' if not os.path.exists(WIZLOG) else ": [COLOR springgreen]%s[/COLOR]" % wiz.convertSize(os.path.getsize(WIZLOG))
    if includeall == 'true':
        includeplacenta = 'true'
        includegaia = 'true'
        includeexodusredux = 'true'
        includeovereasy = 'true'
        includeyoda = 'true'
        includevenom = 'true'
        includescrubs = 'true'
        includeseren = 'true'
    else:
        includeexodusredux = 'true' if INCLUDEEXODUSREDUX     == 'true' else 'false'
        includeovereasy = 'true' if INCLUDEOVEREASY     == 'true' else 'false'
        includeplacenta = 'true' if INCLUDEPLACENTA == 'true' else 'false'
        includegaia = 'true' if INCLUDEGAIA   == 'true' else 'false'
        includeyoda = 'true' if INCLUDEYODA   == 'true' else 'false'
        includevenom = 'true' if INCLUDEVENOM == 'true' else 'false'
        includescrubs = 'true' if INCLUDESCRUBS == 'true' else 'false'
        includeseren = 'true' if INCLUDESEREN   == 'true' else 'false'
    sizepack   = wiz.getSize(PACKAGES)
    sizethumb  = wiz.getSize(THUMBS)
    archive    = wiz.getSize(ARCHIVE_CACHE)
    sizecache  = (wiz.getCacheSize())-archive
    totalsize  = sizepack+sizethumb+sizecache
    feq        = ['Always', 'Daily', '3 Days', 'Weekly']
    addDir ('[B]Cleaning Tools[/B]'       ,'maint', 'clean',  icon=ICONMAINT, themeit=THEME1)
    if view == "clean" or SHOWMAINT == 'true':
        addFile('Total Clean Up: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(totalsize),    'fullclean',       icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Cache: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizecache),       'clearcache',      icon=ICONMAINT, themeit=THEME3)
        if (xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)') or xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)')): addFile('Clear Resolver Function Caches',       'clearfunctioncache',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Packages: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizepack),     'clearpackages',   icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Thumbnails: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizethumb),  'clearthumb',      icon=ICONMAINT, themeit=THEME3)
        if os.path.exists(ARCHIVE_CACHE): addFile('Clear Archive_Cache: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(archive), 'cleararchive',    icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Old Thumbnails', 'oldThumbs',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Crash Logs',               'clearcrash',      icon=ICONMAINT, themeit=THEME3)
        addFile('Purge Databases',                'purgedb',         icon=ICONMAINT, themeit=THEME3)
        addFile('Fresh Start',                    'freshstart',      icon=ICONMAINT, themeit=THEME3)
    addDir ('[B]Addon Tools[/B]',       'maint', 'addon',  icon=ICONMAINT, themeit=THEME1)
    if view == "addon" or SHOWMAINT == 'true':
        addFile('Remove Addons',                  'removeaddons',    icon=ICONMAINT, themeit=THEME3)
        addDir ('Remove Addon Data',              'removeaddondata', icon=ICONMAINT, themeit=THEME3)
        addDir ('Enable/Disable Addons',          'enableaddons',    icon=ICONMAINT, themeit=THEME3)
        addFile('Enable/Disable Adult Addons',    'toggleadult',     icon=ICONMAINT, themeit=THEME3)
        addFile('Force Update Addons',            'forceupdate',     icon=ICONMAINT, themeit=THEME3)
        # addFile('Hide Passwords On Keyboard Entry',   'hidepassword',   icon=ICONMAINT, themeit=THEME3)
        # addFile('Unhide Passwords On Keyboard Entry', 'unhidepassword', icon=ICONMAINT, themeit=THEME3)
    addDir ('[B]Misc Maintenance[/B]'     ,'maint', 'misc',   icon=ICONMAINT, themeit=THEME1)
    if view == "misc" or SHOWMAINT == 'true':
        addFile('Kodi 17 Fix',                    'kodi17fix',       icon=ICONMAINT, themeit=THEME3)
        addDir ('Speed Test',                     'speedtest',       icon=ICONMAINT, themeit=THEME3)
        addFile('Enable Unknown Sources',         'unknownsources',  icon=ICONMAINT, themeit=THEME3)
        addFile('Reload Skin',                    'forceskin',       icon=ICONMAINT, themeit=THEME3)
        addFile('Reload Profile',                 'forceprofile',    icon=ICONMAINT, themeit=THEME3)
        addFile('Force Close Kodi',               'forceclose',      icon=ICONMAINT, themeit=THEME3)
        addFile('Upload Log File', 'uploadlog',       icon=ICONMAINT, themeit=THEME3)
        addFile('View Errors in Log: %s' % (errorsfound), 'viewerrorlog', icon=ICONMAINT, themeit=THEME3)
        if errors > 0: addFile('View Last Error In Log', 'viewerrorlast', icon=ICONMAINT, themeit=THEME3)
        addFile('View Log File',                  'viewlog',         icon=ICONMAINT, themeit=THEME3)
        addFile('View Wizard Log File',           'viewwizlog',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Wizard Log File%s' % wizlogsize,'clearwizlog',     icon=ICONMAINT, themeit=THEME3)
    addDir ('[B]Back up/Restore[/B]'     ,'maint', 'backup',   icon=ICONMAINT, themeit=THEME1)
    if view == "backup" or SHOWMAINT == 'true':
        addFile('Clean Up Back Up Folder',        'clearbackup',     icon=ICONMAINT,   themeit=THEME3)
        addFile('Back Up Location: [COLOR %s]%s[/COLOR]' % (COLOR2, MYBUILDS),'settings', 'Maintenance', icon=ICONMAINT, themeit=THEME3)
        #addFile('Extract a ZipFile',              'extractazip',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Build',               'backupbuild',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: GuiFix',              'backupgui',       icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Theme',               'backuptheme',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Addon Pack',          'backupaddonpack', icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Addon_data',          'backupaddon',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local Build',         'restorezip',      icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local GuiFix',        'restoregui',      icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local Addon_data',    'restoreaddon',    icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External Build',      'restoreextzip',   icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External GuiFix',     'restoreextgui',   icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External Addon_data', 'restoreextaddon', icon=ICONMAINT,   themeit=THEME3)
    addDir ('[B]System Tweaks/Fixes[/B]',       'maint', 'tweaks', icon=ICONMAINT, themeit=THEME1)
    if view == "tweaks" or SHOWMAINT == 'true':
        if not ADVANCEDFILE == 'http://' and not ADVANCEDFILE == '':
            addDir ('Advanced Settings',            'advancedsetting',  icon=ICONMAINT, themeit=THEME3)
        else:
            if os.path.exists(ADVANCED):
                addFile('View Current AdvancedSettings.xml',   'currentsettings', icon=ICONMAINT, themeit=THEME3)
                addFile('Remove Current AdvancedSettings.xml', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
            addFile('Quick Configure AdvancedSettings.xml',    'autoadvanced',    icon=ICONMAINT, themeit=THEME3)
        addFile('Scan Sources for broken links',  'checksources',    icon=ICONMAINT, themeit=THEME3)
        addFile('Scan For Broken Repositories',   'checkrepos',      icon=ICONMAINT, themeit=THEME3)
        addFile('Fix Addons Not Updating',        'fixaddonupdate',  icon=ICONMAINT, themeit=THEME3)
        addFile('Remove Non-Ascii filenames',     'asciicheck',      icon=ICONMAINT, themeit=THEME3)
        addFile('Convert Paths to special',       'convertpath',     icon=ICONMAINT, themeit=THEME3)
        addDir ('System Information',             'systeminfo',      icon=ICONMAINT, themeit=THEME3)
    addFile('Show All Maintenance: %s' % maint.replace('true',on).replace('false',off) ,'togglesetting', 'showmaint', icon=ICONMAINT, themeit=THEME2)
    addDir ('[I]<< Return to Main Menu[/I]', icon=ICONMAINT, themeit=THEME2)
    addFile('Third Party Wizards: %s' % thirdparty.replace('true',on).replace('false',off) ,'togglesetting', 'enable3rd', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
    if thirdparty == 'true':
        first = THIRD1NAME if not THIRD1NAME == '' else 'Not Set'
        secon = THIRD2NAME if not THIRD2NAME == '' else 'Not Set'
        third = THIRD3NAME if not THIRD3NAME == '' else 'Not Set'
        addFile('Edit Third Party Wizard 1: [COLOR %s]%s[/COLOR]' % (COLOR2, first), 'editthird', '1', icon=ICONMAINT, themeit=THEME3)
        addFile('Edit Third Party Wizard 2: [COLOR %s]%s[/COLOR]' % (COLOR2, secon), 'editthird', '2', icon=ICONMAINT, themeit=THEME3)
        addFile('Edit Third Party Wizard 3: [COLOR %s]%s[/COLOR]' % (COLOR2, third), 'editthird', '3', icon=ICONMAINT, themeit=THEME3)
    addFile('Auto Clean', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
    addFile('Auto Clean Up On Startup: %s' % autoclean.replace('true',on).replace('false',off) ,'togglesetting', 'autoclean',   icon=ICONMAINT, themeit=THEME3)
    if autoclean == 'true':
        addFile('--- Auto Clean Fequency: [B][COLOR springgreen]%s[/COLOR][/B]' % feq[AUTOFEQ], 'changefeq', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Clear Cache on Startup: %s' % cache.replace('true',on).replace('false',off), 'togglesetting', 'clearcache', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Clear Packages on Startup: %s' % packages.replace('true',on).replace('false',off), 'togglesetting', 'clearpackages', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Clear Old Thumbs on Startup: %s' % thumbs.replace('true',on).replace('false',off), 'togglesetting', 'clearthumbs', icon=ICONMAINT, themeit=THEME3)
    addFile('Clear Video Cache', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
    addFile('Include Video Cache in Clear Cache: %s' % includevid.replace('true',on).replace('false',off), 'togglecache', 'includevideo', icon=ICONMAINT, themeit=THEME3)
    if includevid == 'true':
        addFile('--- Include All Video Addons: %s' % includeall.replace('true',on).replace('false',off), 'togglecache', 'includeall', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.exodusredux)'): addFile('--- Include Exodus Redux: %s' % includeexodusredux.replace('true',on).replace('false',off), 'togglecache', 'includeexodusredux', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.gaia)'): addFile('--- Include Gaia: %s' % includegaia.replace('true',on).replace('false',off), 'togglecache', 'includegaia', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.overeasy)'): addFile('--- Include Overeasy: %s' % includeovereasy.replace('true',on).replace('false',off), 'togglecache', 'includeovereasy', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.placenta)'): addFile('--- Include Placenta: %s' % includeplacenta.replace('true',on).replace('false',off), 'togglecache', 'includeplacenta', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.scrubsv2)'): addFile( '--- Include Scrubs v2: %s' % includescrubs.replace('true', on).replace('false', off), 'togglecache', 'includescrubs', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.seren)'): addFile('--- Include Seren: %s' % includeseren.replace('true',on).replace('false',off), 'togglecache', 'includeseren', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.venom)'): addFile('--- Include Venom: %s' % includevenom.replace('true', on).replace('false', off), 'togglecache', 'includevenom', icon=ICONMAINT, themeit=THEME3)
        if xbmc.getCondVisibility('System.HasAddon(plugin.video.yoda)'): addFile('--- Include Yoda: %s' % includeyoda.replace('true',on).replace('false',off), 'togglecache', 'includeyoda', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Enable All Video Addons', 'togglecache', 'true', icon=ICONMAINT, themeit=THEME3)
        addFile('--- Disable All Video Addons', 'togglecache', 'false', icon=ICONMAINT, themeit=THEME3)
    setView('files', 'viewType')


#########################################NET TOOLS#############################################

# MIGRATION: move to menu
def net_tools(view=None):
    addDir ('Speed Tester' ,'speedtestM', icon=ICONAPK, themeit=THEME1)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addDir ('View IP Address & MAC Address',        'viewIP',    icon=ICONMAINT, themeit=THEME1)
    setView('files', 'viewType')

# MIGRATION: move to menu
def viewIP():
    mac,inter_ip,ip,city,state,country,isp = wiz.net_info()
    addFile('[COLOR %s]Mac:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, mac), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Internal IP: [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, inter_ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]External IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]City:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, city), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]State:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, state), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Country:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, country), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]ISP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, isp), '', icon=ICONMAINT, themeit=THEME2)
    setView('files', 'viewType')

# MIGRATION: move to menu
def speedTest():
    addFile('Run Speed Test',             'runspeedtest',      icon=ICONMAINT, themeit=THEME3)
    if os.path.exists(SPEEDTESTFOLD):
        speedimg = glob.glob(os.path.join(SPEEDTESTFOLD, '*.png'))
        speedimg.sort(key=lambda f: os.path.getmtime(f), reverse=True)
        if len(speedimg) > 0:
            addFile('Clear Results',          'clearspeedtest',    icon=ICONMAINT, themeit=THEME3)
            addFile(wiz.sep('Previous Runs'), '', icon=ICONMAINT, themeit=THEME3)
            for item in speedimg:
                created = datetime.fromtimestamp(os.path.getmtime(item)).strftime('%m/%d/%Y %H:%M:%S')
                img = item.replace(os.path.join(SPEEDTESTFOLD, ''), '')
                addFile('[B]%s[/B]: [I]Ran %s[/I]' % (img, created), 'viewspeedtest', img, icon=ICONMAINT, themeit=THEME3)

# MIGRATION: move to menu
def clearSpeedTest():
    speedimg = glob.glob(os.path.join(SPEEDTESTFOLD, '*.png'))
    for file in speedimg:
        wiz.removeFile(file)

# MIGRATION: move to menu
def viewSpeedTest(img=None):
    img = os.path.join(SPEEDTESTFOLD, img)
    notify.speedTest(img)

# MIGRATION: move to speedtest?
def runSpeedTest():
    try:
        found = speedtest.speedtest()
        if not os.path.exists(SPEEDTESTFOLD): os.makedirs(SPEEDTESTFOLD)
        urlsplits = found[0].split('/')
        dest = os.path.join(SPEEDTESTFOLD, urlsplits[-1])
        urllib.urlretrieve(found[0], dest)
        viewSpeedTest(urlsplits[-1])
    except:
        wiz.log("[Speed Test] Error Running Speed Test")
        pass

# MIGRATION: move to tools and/or menu
def systemInfo():
    infoLabel = ['System.FriendlyName',
                 'System.BuildVersion',
                 'System.CpuUsage',
                 'System.ScreenMode',
                 'Network.IPAddress',
                 'Network.MacAddress',
                 'System.Uptime',
                 'System.TotalUptime',
                 'System.FreeSpace',
                 'System.UsedSpace',
                 'System.TotalSpace',
                 'System.Memory(free)',
                 'System.Memory(used)',
                 'System.Memory(total)']
    data      = []; x = 0
    for info in infoLabel:
        temp = wiz.getInfo(info)
        y = 0
        while temp == "Busy" and y < 10:
            temp = wiz.getInfo(info); y += 1; wiz.log("%s sleep %s" % (info, str(y))); xbmc.sleep(200)
        data.append(temp)
        x += 1
    storage_free  = data[8] if 'Una' in data[8] else wiz.convertSize(int(float(data[8][:-8]))*1024*1024)
    storage_used  = data[9] if 'Una' in data[9] else wiz.convertSize(int(float(data[9][:-8]))*1024*1024)
    storage_total = data[10] if 'Una' in data[10] else wiz.convertSize(int(float(data[10][:-8]))*1024*1024)
    ram_free      = wiz.convertSize(int(float(data[11][:-2]))*1024*1024)
    ram_used      = wiz.convertSize(int(float(data[12][:-2]))*1024*1024)
    ram_total     = wiz.convertSize(int(float(data[13][:-2]))*1024*1024)

    picture = []; music = []; video = []; programs = []; repos = []; scripts = []; skins = []

    fold = glob.glob(os.path.join(ADDONS, '*/'))
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername == 'packages': continue
        xml = os.path.join(folder, 'addon.xml')
        if os.path.exists(xml):
            f      = open(xml)
            a      = f.read()
            prov   = re.compile("<provides>(.+?)</provides>").findall(a)
            if len(prov) == 0:
                if foldername.startswith('skin'): skins.append(foldername)
                elif foldername.startswith('repo'): repos.append(foldername)
                else: scripts.append(foldername)
            elif not (prov[0]).find('executable') == -1: programs.append(foldername)
            elif not (prov[0]).find('video') == -1: video.append(foldername)
            elif not (prov[0]).find('audio') == -1: music.append(foldername)
            elif not (prov[0]).find('image') == -1: picture.append(foldername)

    addFile('[B]Media Center Info:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Name:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[0]), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]Version:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[1]), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]Platform:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, wiz.platform().title()), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]CPU Usage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[2]), '', icon=ICONMAINT, themeit=THEME3)
    addFile('[COLOR %s]Screen Mode:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[3]), '', icon=ICONMAINT, themeit=THEME3)

    addFile('[B]Uptime:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Current Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[6]), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Total Uptime:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, data[7]), '', icon=ICONMAINT, themeit=THEME2)

    addFile('[B]Local Storage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Used Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_used), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Free Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_free), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Total Storage:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, storage_total), '', icon=ICONMAINT, themeit=THEME2)

    addFile('[B]Ram Usage:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Used Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_free), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Free Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_used), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Total Memory:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ram_total), '', icon=ICONMAINT, themeit=THEME2)

    addFile('[B]Network:[/B]', '', icon=ICONMAINT, themeit=THEME2)
    mac,inter_ip,ip,city,state,country,isp = wiz.net_info()
    addFile('[COLOR %s]Mac:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, mac), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Internal IP: [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, inter_ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]External IP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, ip), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]City:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, city), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]State:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, state), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Country:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, country), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]ISP:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, isp), '', icon=ICONMAINT, themeit=THEME2)

    totalcount = len(picture) + len(music) + len(video) + len(programs) + len(scripts) + len(skins) + len(repos)
    addFile('[B]Addons([COLOR %s]%s[/COLOR]):[/B]' % (COLOR1, totalcount), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Video Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(video))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Program Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(programs))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Music Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(music))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Picture Addons:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(picture))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(repos))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Skins:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(skins))), '', icon=ICONMAINT, themeit=THEME2)
    addFile('[COLOR %s]Scripts/Modules:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, str(len(scripts))), '', icon=ICONMAINT, themeit=THEME2)

# MIGRATION: move to menu
def saveMenu():
    on = '[COLOR springgreen]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
    trakt      = 'true' if KEEPTRAKT     == 'true' else 'false'
    real       = 'true' if KEEPREAL      == 'true' else 'false'
    login      = 'true' if KEEPLOGIN     == 'true' else 'false'
    sources    = 'true' if KEEPSOURCES   == 'true' else 'false'
    advanced   = 'true' if KEEPADVANCED  == 'true' else 'false'
    profiles   = 'true' if KEEPPROFILES  == 'true' else 'false'
    playercore = 'true' if KEEPPLAYERCORE == 'true' else 'false'
    favourites = 'true' if KEEPFAVS      == 'true' else 'false'
    repos      = 'true' if KEEPREPOS     == 'true' else 'false'
    super      = 'true' if KEEPSUPER     == 'true' else 'false'
    whitelist  = 'true' if KEEPWHITELIST == 'true' else 'false'

    addDir ('Keep Trakt Data',               'trakt',                icon=ICONTRAKT, themeit=THEME1)
    addDir ('Keep Debrid',              'realdebrid',           icon=ICONREAL,  themeit=THEME1)
    addDir ('Keep Login Info',               'login',                icon=ICONLOGIN, themeit=THEME1)
    addFile('Import Save Data',              'managedata', 'import', icon=ICONSAVE,  themeit=THEME1)
    addFile('Export Save Data',              'managedata', 'export', icon=ICONSAVE,  themeit=THEME1)
    addFile('- Click to toggle settings -', '', themeit=THEME3)
    addFile('Save Trakt: %s' % trakt.replace('true',on).replace('false',off)                       ,'togglesetting', 'keeptrakt',      icon=ICONTRAKT, themeit=THEME1)
    addFile('Save Debrid: %s' % real.replace('true',on).replace('false',off)                  ,'togglesetting', 'keepdebrid',     icon=ICONREAL,  themeit=THEME1)
    addFile('Save Login Info: %s' % login.replace('true',on).replace('false',off)                  ,'togglesetting', 'keeplogin',      icon=ICONLOGIN, themeit=THEME1)
    addFile('Keep \'Sources.xml\': %s' % sources.replace('true',on).replace('false',off)           ,'togglesetting', 'keepsources',    icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep \'Profiles.xml\': %s' % profiles.replace('true',on).replace('false',off)         ,'togglesetting', 'keepprofiles',   icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep \'playercorefactory.xml\': %s' % playercore.replace('true', on).replace('false', off), 'togglesetting', 'keepplayercore', icon=ICONSAVE, themeit=THEME1)
    addFile('Keep \'Advancedsettings.xml\': %s' % advanced.replace('true',on).replace('false',off) ,'togglesetting', 'keepadvanced',   icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep \'Favourites.xml\': %s' % favourites.replace('true',on).replace('false',off)     ,'togglesetting', 'keepfavourites', icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep Super Favourites: %s' % super.replace('true',on).replace('false',off)            ,'togglesetting', 'keepsuper',      icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep Installed Repo\'s: %s' % repos.replace('true',on).replace('false',off)           ,'togglesetting', 'keeprepos',      icon=ICONSAVE,  themeit=THEME1)
    addFile('Keep My \'WhiteList\': %s' % whitelist.replace('true',on).replace('false',off)        ,'togglesetting', 'keepwhitelist',  icon=ICONSAVE,  themeit=THEME1)
    if whitelist == 'true':
        addFile('Edit My Whitelist',        'whitelist', 'edit',   icon=ICONSAVE,  themeit=THEME1)
        addFile('View My Whitelist',        'whitelist', 'view',   icon=ICONSAVE,  themeit=THEME1)
        addFile('Clear My Whitelist',       'whitelist', 'clear',  icon=ICONSAVE,  themeit=THEME1)
        addFile('Import My Whitelist',      'whitelist', 'import', icon=ICONSAVE,  themeit=THEME1)
        addFile('Export My Whitelist',      'whitelist', 'export', icon=ICONSAVE,  themeit=THEME1)
    setView('files', 'viewType')

# MIGRATION: move to menu
def traktMenu():
    trakt = '[COLOR springgreen]ON[/COLOR]' if KEEPTRAKT == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(TRAKTSAVE) if not TRAKTSAVE == '' else 'Trakt hasnt been saved yet.'
    addFile('[I]Register FREE Account at http://trakt.tv[/I]', '', icon=ICONTRAKT, themeit=THEME3)
    addFile('Save Trakt Data: %s' % trakt, 'togglesetting', 'keeptrakt', icon=ICONTRAKT, themeit=THEME3)
    if KEEPTRAKT == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONTRAKT, themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONTRAKT, themeit=THEME3)

    for trakt in traktit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % TRAKTID[trakt]['plugin']):
            name   = TRAKTID[trakt]['name']
            path   = TRAKTID[trakt]['path']
            saved  = TRAKTID[trakt]['saved']
            file   = TRAKTID[trakt]['file']
            user   = wiz.getS(saved)
            auser  = traktit.traktUser(trakt)
            icon   = TRAKTID[trakt]['icon']   if os.path.exists(path) else ICONTRAKT
            fanart = TRAKTID[trakt]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Trakt', trakt)
            menu2 = createMenu('save', 'Trakt', trakt)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=trakt)' %   (ADDON_ID, trakt)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importtrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savetrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Trakt Data',          'savetrakt',    'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Recover All Saved Trakt Data', 'restoretrakt', 'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Import Trakt Data',            'importtrakt',  'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Clear All Addon Trakt Data',         'addontrakt',   'all', icon=ICONTRAKT,  themeit=THEME3)
    addFile('Clear All Saved Trakt Data',   'cleartrakt',   'all', icon=ICONTRAKT,  themeit=THEME3)
    setView('files', 'viewType')

# MIGRATION: move to menu
def realMenu():
    real = '[COLOR springgreen]ON[/COLOR]' if KEEPREAL == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(REALSAVE) if not REALSAVE == '' else 'Real Debrid hasnt been saved yet.'
    addFile('[I]http://real-debrid.com is a PAID service.[/I]', '', icon=ICONREAL, themeit=THEME3)
    addFile('Save Real Debrid Data: %s' % real, 'togglesetting', 'keepdebrid', icon=ICONREAL, themeit=THEME3)
    if KEEPREAL == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONREAL, themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONREAL, themeit=THEME3)

    for debrid in debridit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % DEBRIDID[debrid]['plugin']):
            name   = DEBRIDID[debrid]['name']
            path   = DEBRIDID[debrid]['path']
            saved  = DEBRIDID[debrid]['saved']
            file   = DEBRIDID[debrid]['file']
            user   = wiz.getS(saved)
            auser  = debridit.debridUser(debrid)
            icon   = DEBRIDID[debrid]['icon']   if os.path.exists(path) else ICONREAL
            fanart = DEBRIDID[debrid]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Debrid', debrid)
            menu2 = createMenu('save', 'Debrid', debrid)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=debrid)' %   (ADDON_ID, debrid)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importdebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savedebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Debrid Data',          'savedebrid',    'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Recover All Saved Debrid Data', 'restoredebrid', 'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Import Debrid Data',            'importdebrid',  'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Clear All Addon Debrid Data',               'addondebrid',   'all', icon=ICONREAL,  themeit=THEME3)
    addFile('Clear All Saved Debrid Data',   'cleardebrid',   'all', icon=ICONREAL,  themeit=THEME3)
    setView('files', 'viewType')

# MIGRATION: move to menu
def loginMenu():
    login = '[COLOR springgreen]ON[/COLOR]' if KEEPLOGIN == 'true' else '[COLOR red]OFF[/COLOR]'
    last = str(LOGINSAVE) if not LOGINSAVE == '' else 'Login data hasnt been saved yet.'
    addFile('[I]Several of these addons are PAID services.[/I]', '', icon=ICONLOGIN, themeit=THEME3)
    addFile('Save API Keys: %s' % login, 'togglesetting', 'keeplogin', icon=ICONLOGIN, themeit=THEME3)
    if KEEPLOGIN == 'true': addFile('Last Save: %s' % str(last), '', icon=ICONLOGIN, themeit=THEME3)
    if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONLOGIN, themeit=THEME3)

    for login in loginit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon(%s)' % LOGINID[login]['plugin']):
            name   = LOGINID[login]['name']
            path   = LOGINID[login]['path']
            saved  = LOGINID[login]['saved']
            file   = LOGINID[login]['file']
            user   = wiz.getS(saved)
            auser  = loginit.loginUser(login)
            icon   = LOGINID[login]['icon']   if os.path.exists(path) else ICONLOGIN
            fanart = LOGINID[login]['fanart'] if os.path.exists(path) else FANART
            menu = createMenu('saveaddon', 'Login', login)
            menu2 = createMenu('save', 'Login', login)
            menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=login)' %   (ADDON_ID, login)))

            addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME3)
            if not os.path.exists(path): addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
            elif not auser:              addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authlogin', login, icon=icon, fanart=fanart, menu=menu)
            else:                        addFile('[COLOR springgreen]Addon Data: %s[/COLOR]' % auser,'authlogin', login, icon=icon, fanart=fanart, menu=menu)
            if user == "":
                if os.path.exists(file): addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importlogin', login, icon=icon, fanart=fanart, menu=menu2)
                else :                   addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savelogin', login, icon=icon, fanart=fanart, menu=menu2)
            else:                        addFile('[COLOR springgreen]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)

    if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
    addFile('Save All Login Info',          'savelogin',    'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Recover All Saved Login Info', 'restorelogin', 'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Import Login Info',            'importlogin',  'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Clear All Addon Login Info',         'addonlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
    addFile('Clear All Saved Login Info',   'clearlogin',   'all', icon=ICONLOGIN,  themeit=THEME3)
    setView('files', 'viewType')


# MIGRATION: move to menu
def removeAddonMenu():
    fold = glob.glob(os.path.join(ADDONS, '*/'))
    addonnames = []; addonids = []
    for folder in sorted(fold, key = lambda x: x):
        foldername = os.path.split(folder[:-1])[1]
        if foldername in EXCLUDES: continue
        elif foldername in DEFAULTPLUGINS: continue
        elif foldername == 'packages': continue
        xml = os.path.join(folder, 'addon.xml')
        if os.path.exists(xml):
            f      = open(xml)
            a      = f.read()
            match  = wiz.parseDOM(a, 'addon', ret='id')

            addid  = foldername if len(match) == 0 else match[0]
            try:
                add = xbmcaddon.Addon(id=addid)
                addonnames.append(add.getAddonInfo('name'))
                addonids.append(addid)
            except:
                pass
    if len(addonnames) == 0:
        wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]No Addons To Remove[/COLOR]" % COLOR2)
        return
    if KODIV > 16:
        selected = DIALOG.multiselect("%s: Select the addons you wish to remove." % ADDONTITLE, addonnames)
    else:
        selected = []; choice = 0
        tempaddonnames = ["-- Click here to Continue --"] + addonnames
        while not choice == -1:
            choice = DIALOG.select("%s: Select the addons you wish to remove." % ADDONTITLE, tempaddonnames)
            if choice == -1: break
            elif choice == 0: break
            else:
                choice2 = (choice-1)
                if choice2 in selected:
                    selected.remove(choice2)
                    tempaddonnames[choice] = addonnames[choice2]
                else:
                    selected.append(choice2)
                    tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
    if selected == None: return
    if len(selected) > 0:
        wiz.addonUpdates('set')
        for addon in selected:
            removeAddon(addonids[addon], addonnames[addon], True)

        xbmc.sleep(500)

        if INSTALLMETHOD == 1: todo = 1
        elif INSTALLMETHOD == 2: todo = 0
        else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR red]Force Close[/COLOR][/B]")
        if todo == 1: wiz.reloadFix('remove addon')
        else: wiz.addonUpdates('reset'); wiz.killxbmc(True)

# MIGRATION: move to menu
def removeAddonDataMenu():
    if os.path.exists(ADDOND):
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data', 'removedata', 'all', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data for Uninstalled Addons', 'removedata', 'uninstalled', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Empty Folders in Addon_Data', 'removedata', 'empty', themeit=THEME2)
        addFile('[COLOR red][B][REMOVE][/B][/COLOR] %s Addon_Data' % ADDONTITLE, 'resetaddon', themeit=THEME2)
        if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
        fold = glob.glob(os.path.join(ADDOND, '*/'))
        for folder in sorted(fold, key = lambda x: x):
            foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
            icon = os.path.join(folder.replace(ADDOND, ADDONS), 'icon.png')
            fanart = os.path.join(folder.replace(ADDOND, ADDONS), 'fanart.png')
            folderdisplay = foldername
            replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR springgreen][SCRIPT] [/COLOR]', 'service.':'[COLOR springgreen][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
            for rep in replace:
                folderdisplay = folderdisplay.replace(rep, replace[rep])
            if foldername in EXCLUDES: folderdisplay = '[COLOR springgreen][B][PROTECTED][/B][/COLOR] %s' % folderdisplay
            else: folderdisplay = '[COLOR red][B][REMOVE][/B][/COLOR] %s' % folderdisplay
            addFile(' %s' % folderdisplay, 'removedata', foldername, icon=icon, fanart=fanart, themeit=THEME2)
    else:
        addFile('No Addon data folder found.', '', themeit=THEME3)
    setView('files', 'viewType')

# MIGRATION: move to menu
def changeFeq():
    feq        = ['Every Startup', 'Every Day', 'Every Three Days', 'Every Weekly']
    change     = DIALOG.select("[COLOR %s]How often would you list to Auto Clean on Startup?[/COLOR]" % COLOR2, feq)
    if not change == -1:
        wiz.setS('autocleanfeq', str(change))
        wiz.LogNotify('[COLOR %s]Auto Clean Up[/COLOR]' % COLOR1, '[COLOR %s]Fequency Now %s[/COLOR]' % (COLOR2, feq[change]))

# MIGRATION: move to menu
def developer():
    # addFile('Convert Text Files to 0.1.7',         'converttext',           themeit=THEME1)
    addFile('Create QR Code',                      'createqr',              themeit=THEME1)
    addFile('Test Notifications',                  'testnotify',            themeit=THEME1)
    addFile('Test Update',                         'testupdate',            themeit=THEME1)
    addFile('Test First Run',                      'testfirst',             themeit=THEME1)
    addFile('Test First Run Settings',             'testfirstrun',          themeit=THEME1)
    setView('files', 'viewType')



###########################
###### Build Install ######
###########################
# MIGRATION: move to menu
def buildWizard(name, type, theme=None, over=False):
    if over == False:
        testbuild = wiz.checkBuild(name, 'url')
        if testbuild == False:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Unabled to find build[/COLOR]" % COLOR2)
            return
        testworking = wiz.workingURL(testbuild)
        if testworking == False:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Build Zip Error: %s[/COLOR]" % (COLOR2, testworking))
            return
    if type == 'gui':
        if name == BUILDNAME:
            if over == True: yes = 1
            else: yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to apply the guifix for:' % COLOR2, '[COLOR %s]%s[/COLOR]?[/COLOR]' % (COLOR1, name), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Apply Fix[/COLOR][/B]')
        else:
            yes = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, "[COLOR %s][COLOR %s]%s[/COLOR] community build is not currently installed." % (COLOR2, COLOR1, name), "Would you like to apply the guiFix anyways?.[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Apply Fix[/COLOR][/B]')
        if yes:
            buildzip = wiz.checkBuild(name,'gui')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Invalid Zip Url![/COLOR]' % COLOR2); return
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading GuiFix:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s_guisettings.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(buildzip, lib, DP)
            xbmc.sleep(500)
            title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
            DP.update(0, title,'', 'Please Wait')
            extract.all(lib,USERDATA,DP, title=title)
            DP.close()
            wiz.defaultSkin()
            wiz.lookandFeelData('save')
            if KODIV >= 17:
                installed = grabAddons(lib)
                wiz.addonDatabase(installed, 1, True)
            if INSTALLMETHOD == 1: todo = 1
            elif INSTALLMETHOD == 2: todo = 0
            else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Gui fix has been installed.  Would you like to Reload the profile or Force Close Kodi?[/COLOR]" % COLOR2, yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
            if todo == 1: wiz.reloadFix()
            else: DIALOG.ok(ADDONTITLE, "[COLOR %s]To save changes you now need to force close Kodi, Press OK to force close Kodi[/COLOR]" % COLOR2); wiz.killxbmc('true')
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]GuiFix: Cancelled![/COLOR]' % COLOR2)
    elif type == 'fresh':
        freshStart(name)
    elif type == 'normal':
        if url == 'normal':
            if KEEPTRAKT == 'true':
                traktit.autoUpdate('all')
                wiz.setS('traktlastsave', str(THREEDAYS))
            if KEEPREAL == 'true':
                debridit.autoUpdate('all')
                wiz.setS('debridlastsave', str(THREEDAYS))
            if KEEPLOGIN == 'true':
                loginit.autoUpdate('all')
                wiz.setS('loginlastsave', str(THREEDAYS))
        temp_kodiv = int(KODIV); buildv = int(float(wiz.checkBuild(name, 'kodi')))
        if not temp_kodiv == buildv:
            if temp_kodiv == 16 and buildv <= 15: warning = False
            else: warning = True
        else: warning = False
        if warning == True:
            yes_pressed = DIALOG.yesno("%s - [COLOR red]WARNING!![/COLOR]" % ADDONTITLE, '[COLOR %s]There is a chance that the skin will not appear correctly' % COLOR2, 'When installing a %s build on a Kodi %s install' % (wiz.checkBuild(name, 'kodi'), KODIV), 'Would you still like to install: [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Yes, Install[/COLOR][/B]')
        else:
            if not over == False: yes_pressed = 1
            else: yes_pressed = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to Download and Install:' % COLOR2, '[COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Yes, Install[/COLOR][/B]')
        if yes_pressed:
            wiz.clearS('build')
            buildzip = wiz.checkBuild(name, 'url')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(buildzip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Build Install: Invalid Zip Url![/COLOR]' % COLOR2); return
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(buildzip, lib, DP)
            xbmc.sleep(500)
            title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version'))
            DP.update(0, title,'', 'Please Wait')
            percent, errors, error = extract.all(lib,HOME,DP, title=title)
            if int(float(percent)) > 0:
                wiz.fixmetas()
                wiz.lookandFeelData('save')
                wiz.defaultSkin()
                #wiz.addonUpdates('set')
                wiz.setS('buildname', name)
                wiz.setS('buildversion', wiz.checkBuild( name,'version'))
                wiz.setS('buildtheme', '')
                wiz.setS('latestversion', wiz.checkBuild( name,'version'))
                wiz.setS('lastbuildcheck', str(NEXTCHECK))
                wiz.setS('installed', 'true')
                wiz.setS('extract', str(percent))
                wiz.setS('errors', str(errors))
                wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
                try: os.remove(lib)
                except: pass
                if int(float(errors)) > 0:
                    yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s v%s[/COLOR]' % (COLOR2, COLOR1, name, wiz.checkBuild(name,'version')), 'Completed: [COLOR %s]%s%s[/COLOR] [Errors:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Would you like to view the errors?[/COLOR]', nolabel='[B][COLOR red]No Thanks[/COLOR][/B]', yeslabel='[B][COLOR springgreen]View Errors[/COLOR][/B]')
                    if yes:
                        if isinstance(errors, unicode):
                            error = error.encode('utf-8')
                        wiz.TextBox(ADDONTITLE, error)
                DP.close()
                themefile = wiz.themeCount(name)
                if not themefile == False:
                    buildWizard(name, 'theme')
                if KODIV >= 17: wiz.addonDatabase(ADDON_ID, 1)
                if INSTALLMETHOD == 1: todo = 1
                elif INSTALLMETHOD == 2: todo = 0
                else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
                if todo == 1: wiz.reloadFix()
                else: wiz.killxbmc(True)
            else:
                if isinstance(errors, unicode):
                    error = error.encode('utf-8')
                wiz.TextBox("%s: Error Installing Build" % ADDONTITLE, error)
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Build Install: Cancelled![/COLOR]' % COLOR2)
    elif type == 'theme':
        if theme == None:
            themefile = wiz.checkBuild(name, 'theme')
            themelist = []
            if not themefile == 'http://' and wiz.workingURL(themefile) == True:
                themelist = wiz.themeCount(name, False)
                if len(themelist) > 0:
                    if DIALOG.yesno(ADDONTITLE, "[COLOR %s]The Build [COLOR %s]%s[/COLOR] comes with [COLOR %s]%s[/COLOR] different themes" % (COLOR2, COLOR1, name, COLOR1, len(themelist)), "Would you like to install one now?[/COLOR]", yeslabel="[B][COLOR springgreen]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]"):
                        wiz.log("Theme List: %s " % str(themelist))
                        ret = DIALOG.select(ADDONTITLE, themelist)
                        wiz.log("Theme install selected: %s" % ret)
                        if not ret == -1: theme = themelist[ret]; installtheme = True
                        else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
                    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2); return
            else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: None Found![/COLOR]' % COLOR2)
        else: installtheme = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to install the theme:' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, theme), 'for [COLOR %s]%s v%s[/COLOR]?[/COLOR]' % (COLOR1, name, wiz.checkBuild(name,'version')), yeslabel="[B][COLOR springgreen]Install Theme[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Themes[/COLOR][/B]")
        if installtheme:
            themezip = wiz.checkTheme(name, theme, 'url')
            zipname = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
            if not wiz.workingURL(themezip) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Invalid Zip Url![/COLOR]' % COLOR2); return False
            if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
            DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme),'', 'Please Wait')
            lib=os.path.join(PACKAGES, '%s.zip' % zipname)
            try: os.remove(lib)
            except: pass
            downloader.download(themezip, lib, DP)
            xbmc.sleep(500)
            DP.update(0,"", "Installing %s " % name)
            test = False
            if url not in ["fresh", "normal"]:
                test = testTheme(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
                test2 = testGui(lib) if not wiz.currSkin() in ['skin.confluence', 'skin.estuary'] else False
                if test == True:
                    wiz.lookandFeelData('save')
                    swap = wiz.skinToDefault('Theme Install')
                    if swap == False: return False
                    xbmc.sleep(500)
            title = '[COLOR %s][B]Installing Theme:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, theme)
            DP.update(0, title,'', 'Please Wait')
            percent, errors, error = extract.all(lib,HOME,DP, title=title)
            wiz.setS('buildtheme', theme)
            wiz.log('INSTALLED %s: [ERRORS:%s]' % (percent, errors))
            DP.close()
            if url not in ["fresh", "normal"]:
                wiz.forceUpdate()
                if KODIV >= 17:
                    installed = grabAddons(lib)
                    wiz.addonDatabase(installed, 1, True)
                if test2 == True:
                    wiz.lookandFeelData('save')
                    wiz.defaultSkin()
                    gotoskin = wiz.getS('defaultskin')
                    wiz.swapSkins(gotoskin, "Theme Installer")
                    wiz.lookandFeelData('restore')
                elif test == True:
                    wiz.lookandFeelData('save')
                    wiz.defaultSkin()
                    gotoskin = wiz.getS('defaultskin')
                    wiz.swapSkins(gotoskin, "Theme Installer")
                    wiz.lookandFeelData('restore')
                else:
                    wiz.ebi("ReloadSkin()")
                    xbmc.sleep(1000)
                    wiz.ebi("Container.Refresh")
        else:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Theme Install: Cancelled![/COLOR]' % COLOR2)

###########################
###### Misc Functions######
###########################

# MIGRATION: move to menu
def createMenu(type, add, name):
    if   type == 'saveaddon':
        menu_items=[]
        add2  = urllib.quote_plus(add.lower().replace(' ', ''))
        add3  = add.replace('Debrid', 'Real Debrid')
        name2 = urllib.quote_plus(name.lower().replace(' ', ''))
        name = name.replace('url', 'URL Resolver')
        menu_items.append((THEME2 % name.title(),             ' '))
        menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Clear %s Data' % add3,              'RunPlugin(plugin://%s/?mode=clear%s&name=%s)' %   (ADDON_ID, add2, name2)))
    elif type == 'save'    :
        menu_items=[]
        add2  = urllib.quote_plus(add.lower().replace(' ', ''))
        add3  = add.replace('Debrid', 'Real Debrid')
        name2 = urllib.quote_plus(name.lower().replace(' ', ''))
        name = name.replace('url', 'URL Resolver')
        menu_items.append((THEME2 % name.title(),             ' '))
        menu_items.append((THEME3 % 'Register %s' % add3,                'RunPlugin(plugin://%s/?mode=auth%s&name=%s)' %    (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Import %s Data' % add3,             'RunPlugin(plugin://%s/?mode=import%s&name=%s)' %  (ADDON_ID, add2, name2)))
        menu_items.append((THEME3 % 'Clear Addon %s Data' % add3,        'RunPlugin(plugin://%s/?mode=addon%s&name=%s)' %   (ADDON_ID, add2, name2)))
    elif type == 'install'  :
        menu_items=[]
        name2 = urllib.quote_plus(name)
        menu_items.append((THEME2 % name,                                'RunAddon(%s, ?mode=viewbuild&name=%s)'  % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Fresh Install',                     'RunPlugin(plugin://%s/?mode=install&name=%s&url=fresh)'  % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Normal Install',                    'RunPlugin(plugin://%s/?mode=install&name=%s&url=normal)' % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Apply guiFix',                      'RunPlugin(plugin://%s/?mode=install&name=%s&url=gui)'    % (ADDON_ID, name2)))
        menu_items.append((THEME3 % 'Build Information',                 'RunPlugin(plugin://%s/?mode=buildinfo&name=%s)'  % (ADDON_ID, name2)))
    menu_items.append((THEME2 % '%s Settings' % ADDONTITLE,              'RunPlugin(plugin://%s/?mode=settings)' % ADDON_ID))
    return menu_items


# MIGRATION: move to check?
def buildInfo(name):
    if wiz.workingURL(BUILDFILE) == True:
        if wiz.checkBuild(name, 'url'):
            name, version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description = wiz.checkBuild(name, 'all')
            adult = 'Yes' if adult.lower() == 'yes' else 'No'
            extend = False
            if not info == "http://":
                try:
                    tname, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts = wiz.checkInfo(info)
                    extend = True
                except:
                    extend = False
            if extend == True:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] v[COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, version)
                msg += "[COLOR %s]Latest Update:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, created)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Extracted Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(extracted))))
                msg += "[COLOR %s]Zip Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(zipsize))))
                msg += "[COLOR %s]Skin Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, skin)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, description)
                msg += "[COLOR %s]Programs:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, programs)
                msg += "[COLOR %s]Video:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, video)
                msg += "[COLOR %s]Music:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, music)
                msg += "[COLOR %s]Pictures:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, picture)
                msg += "[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, repos)
                msg += "[COLOR %s]Scripts:[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, scripts)
            else:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, version)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, description)

            wiz.TextBox(ADDONTITLE, msg)
        else: wiz.log("Invalid Build Name!")
    else: wiz.log("Build text file not working: %s" % WORKINGURL)


###########################
## Making the Directory####
###########################

# MIGRATION: move to menu
def addDir(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
    u = sys.argv[0]
    if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
    if not name == None: u += "&name="+urllib.quote_plus(name)
    if not url == None: u += "&url="+urllib.quote_plus(url)
    ok=True
    if themeit: display = themeit % display
    liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
    liz.setProperty( "Fanart_Image", fanart )
    if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

# MIGRATION: move to menu
def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
    u = sys.argv[0]
    if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
    if not name == None: u += "&name="+urllib.quote_plus(name)
    if not url == None: u += "&url="+urllib.quote_plus(url)
    ok=True
    if themeit: display = themeit % display
    liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
    liz.setProperty( "Fanart_Image", fanart )
    if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

# MIGRATION: move to menu
def setView(content, viewType):
    if wiz.getS('auto-view')=='true':
        views = wiz.getS(viewType)
        if views == '50' and KODIV >= 17 and SKIN == 'skin.estuary': views = '55'
        if views == '500' and KODIV >= 17 and SKIN == 'skin.estuary': views = '50'
        wiz.ebi("Container.SetViewMode(%s)" %  views)