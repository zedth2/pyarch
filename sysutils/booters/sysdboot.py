#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from os.path import isfile
from os import makedirs

DEFAULT_LOADER = 'default arch\ntimeout 5\neditor 0\n'

DEFAULT_ENTRY = 'title Arch Linux\nlinux /vmlinuz-linux\ninitrd /initramfs-linux.img\noptions root={DRIVE} rw'

def sysdbootinstall(system, bootdir='/boot'):
    '''
    Brief: Chroot into system and run bootctl --path=/boot install
    '''
    system.exec_chroot('bootctl', '--path='+bootdir, 'install')


def setuploader(system, bootdir='/boot'):
    makedirs(system.mnt + bootdir + '/loader/', exist_ok=True)
    loader = system.mnt + bootdir + '/loader/loader.conf'
    if isfile(loader):
        return 2
    open(loader, 'w').write(DEFAULT_LOADER)
    return 1

def setupentry(system, bootdir='/boot'):
    makedirs(system.mnt + bootdir + '/loader/entries', exist_ok=True)
    entry = system.mnt + bootdir + '/loader/entries/arch.conf'
    content = DEFAULT_ENTRY.format(DRIVE=system.config['booter']['device'])
    if isfile(entry):
        return 2
    open(entry, 'w').write(content)


def runsysdboot(system, bootdir='/boot'):
    sysdbootinstall(system, bootdir)
    setuploader(system, bootdir)
    setupentry(system, bootdir)
