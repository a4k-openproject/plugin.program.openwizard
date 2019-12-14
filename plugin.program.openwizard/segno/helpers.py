# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2019 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Additional factory functions for common QR Codes.

The factory functions which return a QR Code with the minimum error correction
level "L" (or better). To create a (Micro) QR Code which should use a specific
error correction level or version etc., use the "_data" factory functions which
return a string which can be used as input for :py:func:`segno.make()`.
"""
from __future__ import absolute_import, unicode_literals
import re
import segno
try:  # pragma: no cover
    from urllib.parse import urlsplit, quote
    str_type = str
except ImportError:  # pragma: no cover
    from urlparse import urlsplit
    from urllib import quote
    str = unicode
    str_type = basestring


_MECARD_ESCAPE = {
    ord('\\'): '\\\\',
    ord(';'): '\\;',
    ord(':'): '\\:',
    ord('"'): '\\"',
}


_VCARD_ESCAPE = {
    ord(','): '\\,',
    ord(';'): '\\;',
}


def _escape_mecard(s):
    """\
    Escapes ``\\``, ``;``, ``"`` and ``:`` in the provided string.

    :param str s: The string to escape.
    :rtype str
    """
    return str(s).translate(_MECARD_ESCAPE)


def _escape_vcard(s):
    """\
    Escapes ``\\``, ``;``, ``"`` and ``:`` in the provided string.

    :param str s: The string to escape.
    :rtype str
    """
    return str(s).translate(_VCARD_ESCAPE)


def make_wifi_data(ssid, password, security, hidden=False):
    """\
    Creates WIFI configuration string.

    :param str ssid: The SSID of the network.
    :param str|None password: The password.
    :param str|None security: Authentication type; the value should
            be "WEP" or "WPA". Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
    :param bool hidden: Indicates if the network is hidden (default: ``False``)
    :rtype: str
    """
    def quotation_mark(x):
        """\
        Returns '"' if x could be interpreted as hexadecimal value, otherwise
        an empty string.

        See: <https://github.com/zxing/zxing/wiki/Barcode-Contents>
        [...] Enclose in double quotes if it is an ASCII name, but could be
        interpreted as hex (i.e. "ABCD") [...]
        """
        try:
            int(x, 16)
        except ValueError:
            return ''
        return '"'

    escape = _escape_mecard
    data = 'WIFI:'
    if security:
        data += 'T:{0};'.format(security.upper() if security != 'nopass' else security)
    data += 'S:{1}{0}{1};'.format(escape(ssid), quotation_mark(ssid))
    if password:
        data += 'P:{1}{0}{1};'.format(escape(password), quotation_mark(password))
    data += 'H:true;' if hidden else ';'
    return data


def make_wifi(ssid, password, security, hidden=False):
    """\
    Creates a WIFI configuration QR Code.

    :param str ssid: The SSID of the network.
    :param str|None password: The password.
    :param str|None security: Authentication type; the value should
            be "WEP" or "WPA". Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
    :param bool hidden: Indicates if the network is hidden (default: ``False``)
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_wifi_data(ssid, password, security, hidden))


def make_mecard_data(name, reading=None, email=None, phone=None, videophone=None,
                     memo=None, nickname=None, birthday=None, url=None,
                     pobox=None, roomno=None, houseno=None, city=None,
                     prefecture=None, zipcode=None, country=None):
    """\
    Creates a string encoding the contact information as MeCard.

    :param str name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param str|None reading: Designates a text string to be set as the
            kana name in the phonebook
    :param str|iterable email: E-mail address. Multiple values are
            allowed.
    :param str|iterable phone: Phone number. Multiple values are
            allowed.
    :param str|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str memo: A notice for the contact.
    :param str nickname: Nickname.
    :param (str|int|date) birthday: Birthday. If a string is provided,
            it should encode the date as YYYYMMDD value.
    :param str|iterable url: Homepage. Multiple values are allowed.
    :param str|None pobox: P.O. box (address information).
    :param str|None roomno: Room number (address information).
    :param str|None houseno: House number (address information).
    :param str|None city: City (address information).
    :param str|None prefecture: Prefecture (address information).
    :param str|None zipcode: Zip code (address information).
    :param str|None country: Country (address information).
    :rtype: str
    """
    def make_multifield(name, val):
        if val is None:
            return ()
        if isinstance(val, str_type):
            val = (val,)
        return ['{0}:{1};'.format(name, escape(i)) for i in val]

    escape = _escape_mecard
    data = ['MECARD:N:{0};'.format(escape(name))]
    if reading:
        data.append('SOUND:{0};'.format(escape(reading)))
    data.extend(make_multifield('TEL', phone))
    data.extend(make_multifield('TELAV', videophone))
    data.extend(make_multifield('EMAIL', email))
    if nickname:
        data.append('NICKNAME:{0};'.format(escape(nickname)))
    if birthday:
        try:
            birthday = birthday.strftime('%Y%m%d')
        except AttributeError:
            pass
        data.append('BDAY:{0};'.format(birthday))
    data.extend(make_multifield('URL', url))
    adr_properties = (pobox, roomno, houseno, city, prefecture, zipcode, country)
    if any(adr_properties):
        adr_data = [escape(i or '') for i in adr_properties]
        data.append('ADR:{0},{1},{2},{3},{4},{5},{6};'.format(*adr_data))
    if memo:
        data.append('MEMO:{0};'.format(escape(memo)))
    data.append(';')
    return ''.join(data)


def make_mecard(name, reading=None, email=None, phone=None, videophone=None,
                memo=None, nickname=None, birthday=None, url=None, pobox=None,
                roomno=None, houseno=None, city=None, prefecture=None,
                zipcode=None, country=None):
    """\
    Returns a QR Code which encodes a `MeCard <https://en.wikipedia.org/wiki/MeCard>`_

    :param str name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param str|None reading: Designates a text string to be set as the
            kana name in the phonebook
    :param str|iterable email: E-mail address. Multiple values are
            allowed.
    :param str|iterable phone: Phone number. Multiple values are
            allowed.
    :param str|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str memo: A notice for the contact.
    :param str nickname: Nickname.
    :param str|int|date birthday: Birthday. If a string is provided,
            it should encode the date as YYYYMMDD value.
    :param str|iterable url: Homepage. Multiple values are allowed.
    :param str|None pobox: P.O. box (address information).
    :param str|None roomno: Room number (address information).
    :param str|None houseno: House number (address information).
    :param str|None city: City (address information).
    :param str|None prefecture: Prefecture (address information).
    :param str|None zipcode: Zip code (address information).
    :param str|None country: Country (address information).
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_mecard_data(name=name, reading=reading,
                                          email=email, phone=phone,
                                          videophone=videophone, memo=memo,
                                          nickname=nickname, birthday=birthday,
                                          url=url, pobox=pobox, roomno=roomno,
                                          houseno=houseno, city=city,
                                          prefecture=prefecture, zipcode=zipcode,
                                          country=country))


_looks_like_datetime = re.compile(r'^\d{4}\-\d{2}\-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:(?:\-?\d{2}:\d{2})|Z)?)?$').match

def make_vcard_data(name, displayname, email=None, phone=None, fax=None,
                    videophone=None, memo=None, nickname=None, birthday=None,
                    url=None, pobox=None, street=None, city=None, region=None,
                    zipcode=None, country=None, org=None, lat=None, lng=None,
                    source=None, rev=None, title=None, photo_uri=None):
    """\
    Creates a string encoding the contact information as vCard 3.0.

    Only a subset of available vCard properties is supported.

    :param str name: The name. If it contains a semicolon, , the first part
            is treated as lastname and the second part is treated as forename.
    :param str displayname: Common name.
    :param str|iterable email: E-mail address. Multiple values are allowed.
    :param str|iterable phone: Phone number. Multiple values are allowed.
    :param str|iterable fax: Fax number. Multiple values are allowed.
    :param str|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str memo: A notice for the contact.
    :param str nickname: Nickname.
    :param str|date birthday: Birthday. If a string is provided,
            it should encode the date as YYYY-MM-DD value.
    :param str|iterable url: Homepage. Multiple values are allowed.
    :param str|None pobox: P.O. box (address information).
    :param str|None street: Street address.
    :param str|None city: City (address information).
    :param str|None region: Region (address information).
    :param str|None zipcode: Zip code (address information).
    :param str|None country: Country (address information).
    :param str org: Company / organization name.
    :param float lat: Latitude.
    :param float lng: Longitude.
    :param str source: URL where to obtain the vCard.
    :param str|date rev: Revision of the vCard / last modification date.
    :param str|iterable|None title: Job Title. Multiple values are allowed.
    :param str|iterable|None photo_uri: Photo URI. Multiple values are allowed.
    :rtype: str
    """
    def make_multifield(name, val):
        if val is None:
            return ()
        if isinstance(val, str_type):
            val = (val,)
        return ['{0}:{1}'.format(name, escape(i)) for i in val]

    escape = _escape_vcard
    data = ['BEGIN:VCARD', 'VERSION:3.0',
            'N:{0}'.format(name),
            'FN:{0}'.format(escape(displayname))]
    if org:
        data.append('ORG:{0}'.format(escape(org)))
    data.extend(make_multifield('EMAIL', email))
    data.extend(make_multifield('TEL', phone))
    data.extend(make_multifield('TEL;TYPE=FAX', fax))
    data.extend(make_multifield('TEL;TYPE=VIDEO', videophone))
    data.extend(make_multifield('URL', url))
    data.extend(make_multifield('TITLE', title))
    data.extend(make_multifield('PHOTO;VALUE=uri', photo_uri))
    if nickname:
        data.append('NICKNAME:{0}'.format(escape(nickname)))
    adr_properties = (pobox, street, city, region, zipcode, country)
    if any(adr_properties):
        adr_data = [escape(i or '') for i in adr_properties]
        data.append('ADR:{0};;{1};{2};{3};{4};{5}'.format(*adr_data))
    if birthday:
        try:
            birthday = birthday.strftime('%Y-%m-%d')
        except AttributeError:
            pass
        if not _looks_like_datetime(birthday):
            raise ValueError('"birthday" does not seem to be a valid date or date/time representation')
        data.append('BDAY:{0};'.format(birthday))
    if lat or lng and (not(all((lat, lng)))):
        raise ValueError('Incomplete geo information, please specify latitude and longitude.')
    if lat and lng:
        data.append('GEO:{0};{1}'.format(lat, lng))
    if source:
        data.append('SOURCE:{0}'.format(escape(url)))
    if memo:
        data.append('NOTE:{0}'.format(escape(memo)))
    if rev:
        if not _looks_like_datetime(rev):
            raise ValueError('"rev" does not seem to be a valid date or date/time representation')
        data.append('REV:{0}'.format(rev))
    data.append('END:VCARD')
    data.append('')
    return '\r\n'.join(data)


def make_vcard(name, displayname, email=None, phone=None, fax=None,
               videophone=None, memo=None, nickname=None, birthday=None,
               url=None, pobox=None, street=None, city=None, region=None,
               zipcode=None, country=None, org=None, lat=None, lng=None,
               source=None, rev=None, title=None):
    """\
    Creates a QR Code which encodes a `vCard <https://en.wikipedia.org/wiki/VCard>`_
    version 3.0.

    Only a subset of available vCard properties is supported.

    :param str name: The name. If it contains a semicolon, , the first part
            is treated as lastname and the second part is treated as forename.
    :param str displayname: Common name.
    :param str|iterable email: E-mail address. Multiple values are allowed.
    :param str|iterable phone: Phone number. Multiple values are allowed.
    :param str|iterable fax: Fax number. Multiple values are allowed.
    :param str|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str memo: A notice for the contact.
    :param str nickname: Nickname.
    :param str|date birthday: Birthday. If a string is provided,
            it should encode the date as YYYY-MM-DD value.
    :param str|iterable url: Homepage. Multiple values are allowed.
    :param str|None pobox: P.O. box (address information).
    :param str|None street: Street address.
    :param str|None city: City (address information).
    :param str|None region: Region (address information).
    :param str|None zipcode: Zip code (address information).
    :param str|None country: Country (address information).
    :param str org: Company / organization name.
    :param float lat: Latitude.
    :param float lng: Longitude.
    :param str source: URL where to obtain the vCard.
    :param str|date rev: Revision of the vCard / last modification date.
    :param str|iterable|None title: Job Title. Multiple values are allowed.

    :rtype: segno.QRCode
    """
    return segno.make_qr(make_vcard_data(name, displayname, email=email,
                                         phone=phone, fax=fax,
                                         videophone=videophone, memo=memo,
                                         nickname=nickname, birthday=birthday,
                                         url=url, pobox=pobox, street=street,
                                         city=city, region=region,
                                         zipcode=zipcode, country=country,
                                         org=org, lat=lat, lng=lng,
                                         source=source, rev=rev, title=title))


def make_geo_data(lat, lng):
    """\
    Creates a geo location URI.

    :param float lat: Latitude
    :param float lng: Longitude
    :rtype: str
    """
    def float_to_str(f):
        return '{0:.8f}'.format(f).rstrip('0')

    return 'geo:{0},{1}'.format(float_to_str(lat), float_to_str(lng))


def make_geo(lat, lng):
    """\
    Returns a QR Code which encodes geographic location using the ``geo`` URI
    scheme.

    :param float lat: Latitude
    :param float lng: Longitude
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_geo_data(lat, lng))


def make_make_email_data(to, cc=None, bcc=None, subject=None, body=None):
    """\
    Creates either a simple "mailto:" URL or complete e-mail message with
    (blind) carbon copies and a subject and a body.

    :param str|iterable to: The email address (recipient). Multiple
            values are allowed.
    :param str|iterable|None cc: The carbon copy recipient. Multiple
            values are allowed.
    :param str|iterable|None bcc: The blind carbon copy recipient.
            Multiple values are allowed.
    :param str|None subject: The subject.
    :param str|None body: The message body.
    """
    def multi(val):
        if not val:
            return ()
        if isinstance(val, str_type):
            return (val,)
        return tuple(val)

    delim = '?'
    data = ['mailto:']
    if not to:
        raise ValueError('"to" must not be empty or None')
    data.append(','.join(multi(to)))
    for key, val in (('cc', cc), ('bcc', bcc)):
        vals = multi(val)
        if vals:
            data.append('{0}{1}={2}'.format(delim, key, ','.join(vals)))
            delim = '&'
    for key, val in (('subject', subject), ('body', body)):
        if val is not None:
            data.append('{0}{1}={2}'.format(delim, key, quote(val.encode('utf-8'))))
        delim = '&'
    return ''.join(data)


def make_email(to, cc=None, bcc=None, subject=None, body=None):
    """\
    Encodes either a simple e-mail address or a complete message with
    (blind) carbon copies and a subject and a body.

    :param str|iterable to: The email address (recipient). Multiple
            values are allowed.
    :param str|iterable|None cc: The carbon copy recipient. Multiple
            values are allowed.
    :param str|iterable|None bcc: The blind carbon copy recipient.
            Multiple values are allowed.
    :param str|None subject: The subject.
    :param str|None body: The message body.
    """
    return segno.make_qr(make_make_email_data(to=to, cc=cc, bcc=bcc,
                                              subject=subject, body=body))
