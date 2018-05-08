#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from sys import stdout

FSTAB_FILE = '/etc/fstab'

def genfstab(system, *args, fstabfile=FSTAB_FILE):
    '''
    Brief:
        Will run genfstab on system.mnt. If args is empty it defaults to -U.
        system is still needed for the exec_chroot command. That should probably
        be brought into some kind of common file?
    '''
    if not len(args):
        args = ['-U']
    outs = system.exec_chroot('genfstab', *args, system.mnt, chroot=False)
    if 0 != outs[0]:
        return outs
    open(fstabfile, 'w').write(outs[1].decode())
    return outs[0]
