###########################
###### Fresh Install ######
###########################
# MIGRATION: move to install?
def freshStart(install=None, over=False):
    if KEEPTRAKT == 'true':
        traktit.autoUpdate('all')
        wiz.setS('traktlastsave', str(THREEDAYS))
    if KEEPREAL == 'true':
        debridit.autoUpdate('all')
        wiz.setS('debridlastsave', str(THREEDAYS))
    if KEEPLOGIN == 'true':
        loginit.autoUpdate('all')
        wiz.setS('loginlastsave', str(THREEDAYS))
    if over == True: yes_pressed = 1
    elif install == 'restore': yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you wish to restore your" % COLOR2, "Kodi configuration to default settings", "Before installing the local backup?[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    elif install: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you wish to restore your" % COLOR2, "Kodi configuration to default settings", "Before installing [COLOR %s]%s[/COLOR]?" % (COLOR1, install), nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    else: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you wish to restore your" % COLOR2, "Kodi configuration to default settings?[/COLOR]", nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Continue[/COLOR][/B]')
    if yes_pressed:
        if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
            swap = wiz.skinToDefault('Fresh Install')
            if swap == False: return False
            xbmc.sleep(1000)
        if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Skin Swap Failed![/COLOR]' % COLOR2)
            return
        wiz.addonUpdates('set')
        xbmcPath=os.path.abspath(HOME)
        DP.create(ADDONTITLE,"[COLOR %s]Calculating files and folders" % COLOR2,'', 'Please Wait![/COLOR]')
        total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0
        DP.update(0, "[COLOR %s]Gathering Excludes list." % COLOR2)
        EXCLUDES.append('My_Builds')
        EXCLUDES.append('archive_cache')
        if KEEPREPOS == 'true':
            repos = glob.glob(os.path.join(ADDONS, 'repo*/'))
            for item in repos:
                repofolder = os.path.split(item[:-1])[1]
                if not repofolder == EXCLUDES:
                    EXCLUDES.append(repofolder)
        if KEEPSUPER == 'true':
            EXCLUDES.append('plugin.program.super.favourites')
        if KEEPWHITELIST == 'true':
            pvr = ''
            whitelist = wiz.whiteList('read')
            if len(whitelist) > 0:
                for item in whitelist:
                    try: name, id, fold = item
                    except: pass
                    if fold.startswith('pvr'): pvr = id
                    depends = dependsList(fold)
                    for plug in depends:
                        if not plug in EXCLUDES:
                            EXCLUDES.append(plug)
                        depends2 = dependsList(plug)
                        for plug2 in depends2:
                            if not plug2 in EXCLUDES:
                                EXCLUDES.append(plug2)
                    if not fold in EXCLUDES:
                        EXCLUDES.append(fold)
                if not pvr == '': wiz.setS('pvrclient', fold)
        if wiz.getS('pvrclient') == '':
            for item in EXCLUDES:
                if item.startswith('pvr'):
                    wiz.setS('pvrclient', item)
        DP.update(0, "[COLOR %s]Clearing out files and folders:" % COLOR2)
        latestAddonDB = wiz.latestDB('Addons')
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in files:
                del_file += 1
                fold = root.replace('/','\\').split('\\')
                x = len(fold)-1
                if name == 'sources.xml' and fold[-1] == 'userdata' and KEEPSOURCES == 'true': wiz.log("Keep Sources: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name == 'favourites.xml' and fold[-1] == 'userdata' and KEEPFAVS == 'true': wiz.log("Keep Favourites: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name == 'profiles.xml' and fold[-1] == 'userdata' and KEEPPROFILES == 'true': wiz.log("Keep Profiles: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name == 'playercorefactory.xml' and fold[-1] == 'userdata' and KEEPPLAYERCORE == 'true': wiz.log("Keep playercorefactory.xml: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and KEEPADVANCED == 'true':  wiz.log("Keep Advanced Settings: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                elif name in LOGFILES: wiz.log("Keep Log File: %s" % name, xbmc.LOGNOTICE)
                elif name.endswith('.db'):
                    try:
                        if name == latestAddonDB and KODIV >= 17: wiz.log("Ignoring %s on v%s" % (name, KODIV), xbmc.LOGNOTICE)
                        else: os.remove(os.path.join(root,name))
                    except Exception, e:
                        if not name.startswith('Textures13'):
                            wiz.log('Failed to delete, Purging DB', xbmc.LOGNOTICE)
                            wiz.log("-> %s" % (str(e)), xbmc.LOGNOTICE)
                            wiz.purgeDb(os.path.join(root,name))
                else:
                    DP.update(int(wiz.percentage(del_file, total_files)), '', '[COLOR %s]File: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '')
                    try: os.remove(os.path.join(root,name))
                    except Exception, e:
                        wiz.log("Error removing %s" % os.path.join(root, name), xbmc.LOGNOTICE)
                        wiz.log("-> / %s" % (str(e)), xbmc.LOGNOTICE)
            if DP.iscanceled():
                DP.close()
                wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
                return False
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in dirs:
                DP.update(100, '', 'Cleaning Up Empty Folder: [COLOR %s]%s[/COLOR]' % (COLOR1, name), '')
                if name not in ["Database","userdata","temp","addons","addon_data"]:
                    shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
            if DP.iscanceled():
                DP.close()
                wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
                return False
        DP.close()
        wiz.clearS('build')
        if over == True:
            return True
        elif install == 'restore':
            return True
        elif install:
            buildWizard(install, 'normal', over=True)
        else:
            if INSTALLMETHOD == 1: todo = 1
            elif INSTALLMETHOD == 2: todo = 0
            else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
            if todo == 1: wiz.reloadFix('fresh')
            else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
    else:
        if not install == 'restore':
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Cancelled![/COLOR]' % COLOR2)
            wiz.refresh()

# MIGRATION: move to downloader?
def packInstaller(name, url):
    if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    urlsplits = url.split('/')
    lib = xbmc.makeLegalFilename(os.path.join(PACKAGES, urlsplits[-1]))
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
    DP.update(0, title,'', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
    installed = grabAddons(lib)
    if KODIV >= 17: wiz.addonDatabase(installed, 1, True)
    DP.close()
    wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s: Installed![/COLOR]' % (COLOR2, name))
    wiz.ebi('UpdateAddonRepos()')
    wiz.ebi('UpdateLocalAddons()')
    wiz.refresh()

# MIGRATION: move to dwonloader?
def skinInstaller(name, url):
    if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    urlsplits = url.split('/')
    lib = xbmc.makeLegalFilename(os.path.join(PACKAGES, urlsplits[-1]))
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
    DP.update(0, title,'', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    percent, errors, error = extract.all(lib,HOME,DP, title=title)
    installed = grabAddons(lib)
    if KODIV >= 17: wiz.addonDatabase(installed, 1, True)
    DP.close()
    wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s: Installed![/COLOR]' % (COLOR2, name))
    wiz.ebi('UpdateAddonRepos()')
    wiz.ebi('UpdateLocalAddons()')
    for item in installed:
        if item.startswith('skin.') == True and not item == 'skin.shortcuts':
            if not BUILDNAME == '' and DEFAULTIGNORE == 'true': wiz.setS('defaultskinignore', 'true')
            wiz.swapSkins(item, 'Skin Installer')
    wiz.refresh()

# MIGRATION: move to downloader?
def addonInstaller(plugin, url):
    if not ADDONFILE == 'http://':
        if url == None: url = ADDONFILE
        ADDONWORKING = wiz.workingURL(url)
        if ADDONWORKING == True:
            link = wiz.textCache(url).replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
            match = re.compile('name="(.+?)".+?lugin="%s".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % plugin).findall(link)
            if len(match) > 0:
                for name, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
                    if os.path.exists(os.path.join(ADDONS, plugin)):
                        do        = ['Launch Addon', 'Remove Addon']
                        selected = DIALOG.select("[COLOR %s]Addon already installed what would you like to do?[/COLOR]" % COLOR2, do)
                        if selected == 0:
                            wiz.ebi('RunAddon(%s)' % plugin)
                            xbmc.sleep(500)
                            return True
                        elif selected == 1:
                            wiz.cleanHouse(os.path.join(ADDONS, plugin))
                            try: wiz.removeFolder(os.path.join(ADDONS, plugin))
                            except: pass
                            if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to remove the addon_data for:" % COLOR2, "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, plugin), yeslabel="[B][COLOR springgreen]Yes Remove[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
                                removeAddonData(plugin)
                            wiz.refresh()
                            return True
                        else:
                            return False
                    repo = os.path.join(ADDONS, repository)
                    if not repository.lower() == 'none' and not os.path.exists(repo):
                        wiz.log("Repository not installed, installing it")
                        if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to install the repository for [COLOR %s]%s[/COLOR]:" % (COLOR2, COLOR1, plugin), "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, repository), yeslabel="[B][COLOR springgreen]Yes Install[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
                            ver = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': repository})
                            if len(ver) > 0:
                                repozip = '%s%s-%s.zip' % (repositoryurl, repository, ver[0])
                                wiz.log(repozip)
                                if KODIV >= 17: wiz.addonDatabase(repository, 1)
                                installAddon(repository, repozip)
                                wiz.ebi('UpdateAddonRepos()')
                                #wiz.ebi('UpdateLocalAddons()')
                                wiz.log("Installing Addon from Kodi")
                                install = installFromKodi(plugin)
                                wiz.log("Install from Kodi: %s" % install)
                                if install:
                                    wiz.refresh()
                                    return True
                            else:
                                wiz.log("[Addon Installer] Repository not installed: Unable to grab url! (%s)" % repository)
                        else: wiz.log("[Addon Installer] Repository for %s not installed: %s" % (plugin, repository))
                    elif repository.lower() == 'none':
                        wiz.log("No repository, installing addon")
                        pluginid = plugin
                        zipurl = url
                        installAddon(plugin, url)
                        wiz.refresh()
                        return True
                    else:
                        wiz.log("Repository installed, installing addon")
                        install = installFromKodi(plugin, False)
                        if install:
                            wiz.refresh()
                            return True
                    if os.path.exists(os.path.join(ADDONS, plugin)): return True
                    ver2 = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': plugin})
                    if len(ver2) > 0:
                        url = "%s%s-%s.zip" % (url, plugin, ver2[0])
                        wiz.log(str(url))
                        if KODIV >= 17: wiz.addonDatabase(plugin, 1)
                        installAddon(plugin, url)
                        wiz.refresh()
                    else:
                        wiz.log("no match"); return False
            else: wiz.log("[Addon Installer] Invalid Format")
        else: wiz.log("[Addon Installer] Text File: %s" % ADDONWORKING)
    else: wiz.log("[Addon Installer] Not Enabled.")

# MIGRATION: move to downloader?
def installFromKodi(plugin, over=True):
    if over == True:
        xbmc.sleep(2000)
    #wiz.ebi('InstallAddon(%s)' % plugin)
    wiz.ebi('RunPlugin(plugin://%s)' % plugin)
    if not wiz.whileWindow('yesnodialog'):
        return False
    xbmc.sleep(500)
    if wiz.whileWindow('okdialog'):
        return False
    wiz.whileWindow('progressdialog')
    if os.path.exists(os.path.join(ADDONS, plugin)): return True
    else: return False

# MIGRATION: move to downloader
def installAddon(name, url):
    if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
    if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
    DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    urlsplits = url.split('/')
    lib=os.path.join(PACKAGES, urlsplits[-1])
    try: os.remove(lib)
    except: pass
    downloader.download(url, lib, DP)
    title = '[COLOR %s][B]Installing:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
    DP.update(0, title,'', '[COLOR %s]Please Wait[/COLOR]' % COLOR2)
    percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
    DP.update(0, title,'', '[COLOR %s]Installing Dependencies[/COLOR]' % COLOR2)
    installed(name)
    installlist = grabAddons(lib)
    wiz.log(str(installlist))
    if KODIV >= 17: wiz.addonDatabase(installlist, 1, True)
    installDep(name, DP)
    DP.close()
    wiz.ebi('UpdateAddonRepos()')
    wiz.ebi('UpdateLocalAddons()')
    wiz.refresh()
    for item in installlist:
        if item.startswith('skin.') == True and not item == 'skin.shortcuts':
            if not BUILDNAME == '' and DEFAULTIGNORE == 'true': wiz.setS('defaultskinignore', 'true')
            wiz.swapSkins(item, 'Skin Installer')

# MIGRATION: move to downloader?
def installDep(name, DP=None):
    dep=os.path.join(ADDONS,name,'addon.xml')
    if os.path.exists(dep):
        source = open(dep,mode='r'); link = source.read(); source.close();
        match  = wiz.parseDOM(link, 'import', ret='addon')
        for depends in match:
            if not 'xbmc.python' in depends:
                if not DP == None:
                    DP.update(0, '', '[COLOR %s]%s[/COLOR]' % (COLOR1, depends))
                try:
                    add   = xbmcaddon.Addon(id=depends)
                    name2 = add.getAddonInfo('name')
                except:
                    wiz.createTemp(depends)
                    if KODIV >= 17: wiz.addonDatabase(depends, 1)
                # continue
                # dependspath=os.path.join(ADDONS, depends)
                # if not os.path.exists(dependspath):
                    # zipname = '%s-%s.zip' % (depends, match2[match.index(depends)])
                    # depzip = urljoin("%s%s/" % (MODURL2, depends), zipname)
                    # if not wiz.workingURL(depzip) == True:
                        # depzip = urljoin(MODURL, '%s.zip' % depends)
                        # if not wiz.workingURL(depzip) == True:
                            # wiz.createTemp(depends)
                            # if KODIV >= 17: wiz.addonDatabase(depends, 1)
                            # continue
                    # lib=os.path.join(PACKAGES, '%s.zip' % depends)
                    # try: os.remove(lib)
                    # except: pass
                    # DP.update(0, '[COLOR %s][B]Downloading Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends),'', 'Please Wait')
                    # downloader.download(depzip, lib, DP)
                    # xbmc.sleep(100)
                    # title = '[COLOR %s][B]Installing Dependency:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, depends)
                    # DP.update(0, title,'', 'Please Wait')
                    # percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
                    # if KODIV >= 17: wiz.addonDatabase(depends, 1)
                    # installed(depends)
                    # installDep(depends)
                    # xbmc.sleep(100)
                    # DP.close()

# MIGRATION: deprecate?
def installed(addon):
    url = os.path.join(ADDONS,addon,'addon.xml')
    if os.path.exists(url):
        try:
            list  = open(url,mode='r'); g = list.read(); list.close()
            name = wiz.parseDOM(g, 'addon', ret='name', attrs = {'id': addon})
            icon  = os.path.join(ADDONS,addon,'icon.png')
            wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, name[0]), '[COLOR %s]Addon Enabled[/COLOR]' % COLOR2, '2000', icon)
        except: pass

# MIGRATION: move to downloader?
def apkInstaller(apk, url):
    wiz.log(apk)
    wiz.log(url)
    if wiz.platform() == 'android':
        yes = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to download and install:" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, apk), yeslabel="[B][COLOR springgreen]Download[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
        if not yes: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Install Cancelled[/COLOR]' % COLOR2); return
        display = apk
        if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
        if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]APK Installer: Invalid Apk Url![/COLOR]' % COLOR2); return
        DP.create(ADDONTITLE,'[COLOR %s][B]Downloading:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, display),'', 'Please Wait')
        lib=os.path.join(PACKAGES, "%s.apk" % apk.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', ''))
        try: os.remove(lib)
        except: pass
        downloader.download(url, lib, DP)
        xbmc.sleep(100)
        DP.close()
        notify.apkInstaller(apk)
        wiz.ebi('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:'+lib+'")')
    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: None Android Device[/COLOR]' % COLOR2)