# MIGRATION: move to menu
def testTheme(path):
    zfile = zipfile.ZipFile(path)
    for item in zfile.infolist():
        wiz.log(str(item.filename))
        if '/settings.xml' in item.filename:
            return True
    return False

# MIGRATION: move to menu
def testGui(path):
    zfile = zipfile.ZipFile(path)
    for item in zfile.infolist():
        if '/guisettings.xml' in item.filename:
            return True
    return False

##########################
### DEVELOPER MENU #######
##########################
# MIGRATION: move to test
def testnotify():
    url = wiz.workingURL(NOTIFICATION)
    if url == True:
        try:
            id, msg = wiz.splitNotify(NOTIFICATION)
            if id == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Notification: Not Formated Correctly[/COLOR]" % COLOR2); return
            notify.notification(msg, True)
        except Exception, e:
            wiz.log("Error on Notifications Window: %s" % str(e), xbmc.LOGERROR)
    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Invalid URL for Notification[/COLOR]" % COLOR2)

# MIGRATION: move to test
def testupdate():
    if BUILDNAME == "":
        notify.updateWindow()
    else:
        notify.updateWindow(BUILDNAME, BUILDVERSION, BUILDLATEST, wiz.checkBuild(BUILDNAME, 'icon'), wiz.checkBuild(BUILDNAME, 'fanart'))

# MIGRATION: move to test
def testfirst():
    notify.firstRun()

# MIGRATION: move to test
def testfirstRun():
    notify.firstRunSettings()oi