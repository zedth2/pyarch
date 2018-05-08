#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

HOSTNAME_FILE = '/etc/hostname'
HOSTS_FILE = '/etc/hosts'

def SetHostname(host, hostnamefile=HOSTNAME_FILE, hostsfile=HOSTS_FILE):
    open(hostnamefile,'w').write(str(host)+'\n')
    curHost = '127.0.1.1\t{0}.localdomain {0}\n'.format(host)
    hosts = open(hostsfile).readlines()
    hosts.append(curHost)
    open(hostsfile,'w').writelines(hosts)


if __name__ == '__main__':
    SetHostname('butts')
