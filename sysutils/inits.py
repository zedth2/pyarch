#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from sys import stdout

MKINITCPIO_CMD = 'mkinitcpio'
DEFAULT_PRESET = 'linux'

def run_mkinitcpio(system, mkargs=['-p', DEFAULT_PRESET], mkcmd=MKINITCPIO_CMD, chroot=True):
    cmd = [mkcmd, *mkargs]
    return system.exec_chroot(*cmd, chroot=chroot, stdout=stdout)
