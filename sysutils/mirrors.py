#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from urllib import request

MIRROR_URL='https://www.archlinux.org/mirrorlist/?'
MIRROR_FILE = '/etc/pacman.d/mirrorlist'

def getmirrors(country='US', http=True, ipv4=True, https=True, ipv6=False, mirrorStatus=False):
    mir = MIRROR_URL
    if not country:
        country = 'all'
    mir += 'country='+country
    if http:
        mir += '&protocol=http'
    if https:
        mir += '&protocol=https'
    if ipv4:
        mir += '&ip_version=4'
    if ipv6:
        mir += '&ip_version=6'
    if mirrorStatus:
        mir += '&use_mirror_status=on'
    mirrors = []
    with request.urlopen(mir) as u:
        mirrors = u.readlines()
    return b''.join(mirrors).decode()

def writemirrors(outText='', outFile=MIRROR_FILE, uncomment=True):
    if not outText:
        outText = getmirrors()
    with open(outFile, 'w') as f:
        out = outText
        if uncomment:
            out = uncomment(out)
        f.write(out)
    return


def uncomment(mirrors):
    out = ''
    for l in outText.splitlines():
        out += l[1:]
    return out
