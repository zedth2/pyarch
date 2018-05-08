#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import glob
from os import sep, symlink, remove
from os.path import exists

ZONE_DIR = '/usr/share/zoneinfo/'
LOCALTIME_FILE = '/etc/localtime'

def getzones(zonedir=ZONE_DIR):
    reLst = []

    for z in glob.iglob(zonedir+'**/*'):
        reLst.append(z.lstrip(zonedir))
    reLst.sort()
    return sorted(reLst, key=lambda s:s.lower())

def setzone(zone, localtime=LOCALTIME_FILE, zonedir=ZONE_DIR):
    if exists(localtime):
        remove(localtime)
    symlink(zonedir+'/'+zone, localtime)

if __name__ == '__main__':
    import pprint
    pprint.PrettyPrinter().pprint(getzones())
