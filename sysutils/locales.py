#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import re
from sys import stdout
LOCALE_CONF = '/etc/locale.conf'
LOCALE_GEN = '/etc/locale.gen'
LOCALE_CMD = 'locale-gen'

KEYMAP_FILE = '/etc/vconsole.conf'

def writeconf(system, locales='en_US.UTF-8', conf=LOCALE_CONF):
    try:
        with open(conf) as c:
            conf = ''.join(c.readlines())
    except FileNotFoundError:
        pass
    if isinstance(locales, str):
        conf = conf + '\nLANG=' + locales
    #conf += '\nLANG='
    with open(conf, 'w') as c:
        c.writelines(conf)
    return

def localegen(locales='en_US.UTF-8', gen=LOCALE_GEN):
    compl = ''.join(open(gen).readlines())
    if isinstance(locales, str):
        locales = [locales]
    for l in locales:
        match = re.search('#'+re.escape(l), compl)
        if not match:
            continue
        spans = match.span()
        compl = compl[:spans[0]] + compl[spans[0]+1:]
    open(gen, 'w').write(compl)

def runlocalegen(system, cmd=LOCALE_CMD):
    return system.exec_chroot(cmd, stdout=stdout)


def getlocales(gen=LOCALE_GEN):
    locales = []
    with open(gen) as g:
        for l in g.readlines():
            try:
                if l[1] != ' ' and l.strip() != '#':
                    if l[0] == '#':
                        locales.append(l[1:].strip())
                    else:
                        locales.append(l)
            except IndexError:
                continue
    return locales


def setkeymap(keymap='us', keyfile=KEYMAP_FILE):
    lines = []
    try:
        lines = open(keyfile).readlines()
    except FileNotFoundError:
        pass
    lines.append('KEYMAP='+keymap)
    open(keyfile,'w').writelines(lines)


if __name__ == '__main__':
    localegen()
