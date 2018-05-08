#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

LOADKEYS_CMD = 'loadkeys'

import subprocess


def GetMaps():
    pass

def SetKeyMap(mapFile, loadcmd=LOADKEYS_CMD):
    if mapFile.endswith('.map.gz'):
        mapFile = mapFile.strip('.map.gz')
    p = subprocess.Popen([loadcmd, mapFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
