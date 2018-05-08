#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import subprocess

class SysOps:
    '''
    Brief:
        The point of this class is to give other functions the configuration of
        the install system.

    Properties:
        mntPoint : str
            This will be the root that all functions will operate from. So
            setting up the network will use mntPoint+'etc/hosts' to find it's
            files.
        chrootCmd : str
            This will be the chroot command to be used to run commands inside
            of. If this is empty then no chroot will be run.
    '''
    def __init__(self, mnt='/', chroot='arch-chroot'):
        self.mntPoint = mnt
        self.chrootCmd = 'arch-chroot'
'''
    def Popen(self, args):
        cmd = args
        if self.chrootCmd:
            if self.chrootCmd == 'arch-chroot':
                cmd = [self.chrootCmd, self.mntPoint, '/bin/bash', '-c', '
                '.join(
                cmd.insert(0, self.chrootCmd)
                cmd.insert(1, self.mntPoint)
                cmd.insert(2, '/bin/bash')
                cmd.insert(3, '-c')
                cmd.append(
'''
