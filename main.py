#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from sysutils import InstallSystem, SystemSetup


def main():
    #x = SystemSetup()
    InstallSystem(SystemSetup.defaultconfig())
    #pprint.PrettyPrinter().pprint(x.getconfig())


if __name__ == '__main__':
    main()
