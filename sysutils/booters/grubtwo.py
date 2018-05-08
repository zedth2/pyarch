#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
from .. import pacmansetup
from sys import stdout

def grub_install_cmd():
    return ['grub-install', '--target=i386-pc', '--recheck']

def grub_mkconfig_cmd(bootdir):
    return ['grub-mkconfig', '-o', bootdir + '/grub/grub.cfg']

def run_grub(system, device='/dev/sda'):
    pacmansetup.pacstrap(system, groups=['grub'])
    cmd = grub_install_cmd()
    cmd.append(device)
    outs = system.exec_chroot(*cmd, stdout=stdout)
    if 0 != outs[0]:
        return outs[0]
    system.exec_chroot('cp', '/usr/share/locale/en\@quot/LC_MESSAGES/grub.mo', '/boot/grub/locale/en.mo')
    cmd = grub_mkconfig_cmd(system.config['booter']['bootdir'])
    cmd.append(device)
    outs = system.exec_chroot(*cmd, stdout=stdout)
    return outs[0]
