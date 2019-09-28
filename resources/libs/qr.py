import xbmcgui

import os

from resources.libs.config import CONFIG


def generate_code(url, filename):
    import segno

    if not os.path.exists(CONFIG.QRCODES):
        os.makedirs(CONFIG.QRCODES)
    imagefile = os.path.join(CONFIG.QRCODES, '{0}.png'.format(filename))
    generated_qr = segno.make(url)
    generated_qr.save(imagefile, scale=10)
    return imagefile


def create_code():
    from resources.libs import logging
    from resources.libs import tools
    
    dialog = xbmcgui.Dialog()

    url = tools.get_keyboard('', "{0}: Insert the URL for the QR Code.".format(CONFIG.ADDONTITLE))
    if not url:
        logging.log_notify("[COLOR {0}]Create QR Code[/COLOR]".format(CONFIG.COLOR1),
                           '[COLOR {0}]Create QR Code Cancelled![/COLOR]'.format(CONFIG.COLOR2))
        return
    if not url.startswith('http://') and not url.startswith('https://'):
        logging.log_notify("[COLOR {0}]Create QR  Code[/COLOR]".format(CONFIG.COLOR1),
                           '[COLOR {0}]Not a Valid URL![/COLOR]'.format(CONFIG.COLOR2))
        return
    if url == 'http://' or url == 'https://':
        logging.log_notify("[COLOR {0}]Create QR Code[/COLOR]".format(CONFIG.COLOR1),
                           '[COLOR {0}]Not a Valid URL![/COLOR]'.format(CONFIG.COLOR2))
        return
    working = tools.check_url(url)
    if not working:
        if not dialog.yesno(CONFIG.ADDONTITLE,
                                "[COLOR {0}]It seems the URL you entered isn\'t working, Would you like to create it anyways?[/COLOR]".format(CONFIG.COLOR2),
                                "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, working),
                                yeslabel="[B][COLOR red]Yes Create[/COLOR][/B]",
                                nolabel="[B][COLOR springgreen]No Cancel[/COLOR][/B]"):
            return
    name = tools.get_keyboard('', "{0}: Insert the name for the QR Code.".format(CONFIG.ADDONTITLE))
    name = "QR_Code_{0}".format(tools.id_generator(6)) if name == "" else name
    image = generate_code(url, name)
    dialog.ok(CONFIG.ADDONTITLE,
                  "[COLOR {0}]The QR Code image has been created and is located in the addon_data directory:[/COLOR]".format(CONFIG.COLOR2),
                  "[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, image.replace(CONFIG.HOME, '')))
