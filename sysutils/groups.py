#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

import subprocess

import grp
import pwd

GROUP_FILE = '/etc/group'
USER_FILE = '/etc/passwd'

def GetAllGroupsFile(groupsfile=GROUP_FILE):
    return _GetAll(groupsfile)

def GetAllUsersFile(userfile=USER_FILE):
    return _GetAll(userfile)

def _GetAll(ugfile):
    users = []
    for l in open(userfile).readlines():
        users.append(l.split(':')[0])
    return users

def GetAllGroups():
    return [g.gr_name for g in grp.getgrall()]


def GetAllUsers():
    return [u.pw_name for u in pwd.getpwall()]


def AddUser(un, groups, pw, shl):
    '''
    Brief:
        This will add a user using the useradd command.
    '''
    p = subprocess.Popen(['useradd', '-G', ','.join(groups), '-p', pw, '-m', '-s',shl, un], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    extCode = p.poll()
    return (extCode, out[0], out[1])
