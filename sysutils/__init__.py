#!/usr/bin/python3
import pprint
from os.path import isfile
import json
import subprocess
import shlex
import sys

from . import pacmansetup
from . import filesystem
from . import locales
from . import timezones
from . import networking
from . import inits
from .booters import booter
from .helpers import debug

class SystemSetup:
    def __init__(self, config=''):
        self.loadconfig(config)

    def getconfig(self):
        return self.__class__.defaultconfig()

    def loadconfig(self, config=''):
        if '' == config or config is None:
            config = self.__class__.defaultconfig()
        elif isinstance(config, dict):
            pass
        elif isfile(config):
            config = json.loads(open(config).read())
        else:
            raise ValueError('config must either be a json file an empty string or a dictionary')
        self.mnt = config['mount']
        self.chrootcmd = config['chrootcmd']
        self.hostname = config['hostname']
        self.config = config


    def popenobj(self, *args, chroot=True, stdout=subprocess.PIPE, shell=False):
        usercmd = list(args)
        if 1 == len(args):
            usercmd = shlex.split(args[0])
        elif not len(args):
            raise ValueError('No command to execute')
        if chroot:
            usercmd = self.chroot_list() + usercmd
        return subprocess.Popen(usercmd, stdout=stdout, stderr=subprocess.PIPE, shell=shell)

    def exec_chroot(self, *args, chroot=True, stdout=subprocess.PIPE, shell=False):
        debug('Running Command : ', *args)
        pop = self.popenobj(*args, chroot=chroot, stdout=stdout, shell=shell)
        stdout, stderr = pop.communicate()
        return (pop.returncode, stdout, stderr)

    def chroot_list(self, shell='/bin/bash'):
        return [ self.chrootcmd,
                 self.mnt ]

    def getroot(self):
        return self.mnt

    def getpath(self, target):
        if not target.startswith('/'):
            target = '/'+target
        return self.getroot() + target

    def runningconfig(self):
        cfg = self.__class__.defaultconfig()
        cfg['mount'] = self.mnt
        cfg['chrootcmd'] = self.chrootcmd
        cfg['hostname'] = self.hostname
        return cfg

    def install_package(self, package, chroot=True):
        pass

    def keys(self, key):
        return self.config.keys()

    def __getitem__(self, key):
        return self.config[key]

    @staticmethod
    def defaultconfig():
        return {
            'hostname':'localhost',
            'keymap': 'us',
            'consolefont':'CP437',
            'network': 'dhcp',
            'time':{'zone': 'America/New_York',
                    'ntp' : True,
                    },
            'locale':'en_US.UTF-8', #A string or a list of locales
            'mount': '/mnt',
            'chrootcmd':'arch-chroot',
            'getmirrors':True,
            'booter':{'name':'systemd-boot',
                     'device':'/dev/sda',
                     'bootdir':'/boot'
                    },
        }


def InstallSystem(configfile):
    system = SystemSetup(configfile)
    outs = pacmansetup.pacstrap(system)
    print('Pacstrap done')
    filesystem.genfstab(system, fstabfile=system.getpath(filesystem.FSTAB_FILE))
    try:
        timezones.setzone(system['time']['zone'], system.getpath(timezones.LOCALTIME_FILE), system.getpath(timezones.ZONE_DIR))
    except KeyError: #Just ignore and don't set a timezone
        pass
    try:
        locales.localegen(system['locale'], system.getpath(locales.LOCALE_GEN))
        locales.runlocalegen(system)
    except KeyError: #Don't set a locale
        pass
    try:
        locales.setkeymap(system['keymap'], system.getpath(locales.KEYMAP_FILE))
    except KeyError:
        pass
    try:
        if system['hostname'] != 'localhost':
            networking(system['hostname'], system.getpath(networking.HOSTNAME_FILE), system.getpath(networking.HOSTS_FILE))
    except KeyError:
        pass
    inits.run_mkinitcpio(system)
    booter(system, system.config['booter']['bootdir'])


if __name__ == '__main__':
    x = SystemSetup()
    pprint.PrettyPrinter().pprint(x.getconfig())
