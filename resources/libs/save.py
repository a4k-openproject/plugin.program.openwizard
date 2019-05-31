## MIGRATION: move into save_data?
def manageSaveData(do):
    if do == 'import':
        TEMP = os.path.join(ADDONDATA, 'temp')
        if not os.path.exists(TEMP): os.makedirs(TEMP)
        source = DIALOG.browse(1, '[COLOR %s]Select the location of the SaveData.zip[/COLOR]' % COLOR2, 'files', '.zip', False, False, HOME)
        if not source.endswith('.zip'):
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
            return
        source   = xbmc.translatePath(source)
        tempfile = xbmc.translatePath(os.path.join(MYBUILDS, 'SaveData.zip'))
        if not tempfile == source:
            goto = xbmcvfs.copy(source, tempfile)
        if extract.all(xbmc.translatePath(tempfile), TEMP) == False:
            wiz.log("Error trying to extract the zip file!")
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
            return
        trakt  = os.path.join(TEMP, 'trakt')
        login  = os.path.join(TEMP, 'login')
        debrid = os.path.join(TEMP, 'debrid')
        super  = os.path.join(TEMP, 'plugin.program.super.favourites')
        xmls   = os.path.join(TEMP, 'xmls')
        x = 0
        overwrite = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you rather we overwrite all Save Data files or ask you for each file being imported?[/COLOR]" % (COLOR2), yeslabel="[B][COLOR springgreen]Overwrite All[/COLOR][/B]", nolabel="[B][COLOR red]No Ask[/COLOR][/B]")
        if os.path.exists(trakt):
            x += 1
            files = os.listdir(trakt)
            if not os.path.exists(traktit.TRAKTFOLD): os.makedirs(traktit.TRAKTFOLD)
            for item in files:
                old  = os.path.join(traktit.TRAKTFOLD, item)
                temp = os.path.join(trakt, item)
                if os.path.exists(old):
                    if overwrite == 1: os.remove(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: os.remove(old)
                shutil.copy(temp, old)
            traktit.importlist('all')
            traktit.traktIt('restore', 'all')
        if os.path.exists(login):
            x += 1
            files = os.listdir(login)
            if not os.path.exists(loginit.LOGINFOLD): os.makedirs(loginit.LOGINFOLD)
            for item in files:
                old  = os.path.join(loginit.LOGINFOLD, item)
                temp = os.path.join(login, item)
                if os.path.exists(old):
                    if overwrite == 1: os.remove(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: os.remove(old)
                shutil.copy(temp, old)
            loginit.importlist('all')
            loginit.loginIt('restore', 'all')
        if os.path.exists(debrid):
            x += 1
            files = os.listdir(debrid)
            if not os.path.exists(debridit.REALFOLD): os.makedirs(debridit.REALFOLD)
            for item in files:
                old  = os.path.join(debridit.REALFOLD, item)
                temp = os.path.join(debrid, item)
                if os.path.exists(old):
                    if overwrite == 1: os.remove(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: os.remove(old)
                shutil.copy(temp, old)
            debridit.importlist('all')
            debridit.debridIt('restore', 'all')
        if os.path.exists(xmls):
            x += 1
            files = ['advancedsettings.xml', 'sources.xml', 'favourites.xml', 'profiles.xml']
            for item in files:
                old = os.path.join(USERDATA, item)
                new = os.path.join(xmls, item)
                if not os.path.exists(new): continue
                if os.path.exists(old):
                    if not overwrite == 1:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                os.remove(old)
                shutil.copy(new, old)
        if os.path.exists(super):
            x += 1
            old = os.path.join(ADDOND, 'plugin.program.super.favourites')
            if os.path.exists(old):
                cont = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]Super Favourites[/COLOR] addon_data folder with the new one?" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]")
            else: cont = 1
            if cont == 1:
                wiz.cleanHouse(old)
                wiz.removeFolder(old)
                xbmcvfs.copy(super, old)
        wiz.cleanHouse(TEMP)
        wiz.removeFolder(TEMP)
        if not tempfile == source:
            xbmcvfs.delete(tempfile)
        if x == 0: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Failed[/COLOR]" % COLOR2)
        else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Complete[/COLOR]" % COLOR2)
    elif do == 'export':
        mybuilds = xbmc.translatePath(MYBUILDS)
        dir   = [traktit.TRAKTFOLD, debridit.REALFOLD, loginit.LOGINFOLD]
        xmls  = ['advancedsettings.xml', 'sources.xml', 'favourites.xml', 'profiles.xml']
        keepx = [KEEPADVANCED, KEEPSOURCES, KEEPFAVS, KEEPPROFILES, KEEPPLAYERCORE]
        traktit.traktIt('update', 'all')
        loginit.loginIt('update', 'all')
        debridit.debridIt('update', 'all')
        source = DIALOG.browse(3, '[COLOR %s]Select where you wish to export the savedata zip?[/COLOR]' % COLOR2, 'files', '', False, True, HOME)
        source = xbmc.translatePath(source)
        tempzip = os.path.join(mybuilds, 'SaveData.zip')
        superfold = os.path.join(ADDOND, 'plugin.program.super.favourites')
        zipf = zipfile.ZipFile(tempzip, mode='w')
        for fold in dir:
            if os.path.exists(fold):
                files = os.listdir(fold)
                for file in files:
                    fn = os.path.join(fold, file)
                    zipf.write(fn, fn[len(ADDONDATA):], zipfile.ZIP_DEFLATED)
        if KEEPSUPER == 'true' and os.path.exists(superfold):
            for base, dirs, files in os.walk(superfold):
                for file in files:
                    fn = os.path.join(base, file)
                    zipf.write(fn, fn[len(ADDOND):], zipfile.ZIP_DEFLATED)
        for item in xmls:
            if keepx[xmls.index(item)] == 'true' and os.path.exists(os.path.join(USERDATA, item)):
                zipf.write(os.path.join(USERDATA, item), os.path.join('xmls', item), zipfile.ZIP_DEFLATED)
        zipf.close()
        if source == mybuilds:
            DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))
        else:
            try:
                xbmcvfs.copy(tempzip, os.path.join(source, 'SaveData.zip'))
                DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, os.path.join(source, 'SaveData.zip')))
            except:
                DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))