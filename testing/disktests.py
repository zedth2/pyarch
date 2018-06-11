#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from sysutils import SystemSetup
from sysutils.diskutils import FileSystem

from sysutils.helpers import ExecutionError

def tester():
    x = [{
            'device': 'sda',
            'label' : 'gpt',
            'partition': [ {'fs':'fat32',
                            'size' : '100MB',
                            'name' : 'BOOT',
                            'flag' : 'boot',
                            'type' : 'primary',
                            'mount': '/boot',
                            },
                            {'fs':'ext3',
                            'size' : '-1s',
                            'name' : 'ROOT',
                            'type' : 'primary',
                            'mount': '/',
                            }
                          ]
        }]
    system = SystemSetup()
    dev = FileSystem.fromDict(x)
    #recode, stdout, stderr = system.exec_chroot(*dev.make_script(), chroot=False)
    try:
        dev.createall(system)
        dev.mountall(system)
    except ExecutionError as e:
        print('stdout', e.stdout)
        print('stderr', e.stderr)




if __name__ == '__main__':
    tester()
