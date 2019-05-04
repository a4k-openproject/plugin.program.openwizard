import xbmcgui



def get_setting(name):
    try:
        return vars.ADDON.getSetting(name)
    except:
        return False


def set_setting(name, value):
    try:
        vars.ADDON.setSetting(name, value)
    except:
        return False


def read_from_file(file):
    f = open(file)
    a = f.read()
    f.close()
    return a


def write_to_file(file, content):
    f = open(file, 'w')
    f.write(content)
    f.close()


def get_date(days=0, now=False):
    from datetime import date
    from datetime import datetime
    from datetime import timedelta

    if not now:
        if days == 0:
            return date.today()
        else:
            return date.today() + timedelta(days)
    else:
        return datetime.now()

