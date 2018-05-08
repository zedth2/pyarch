#!/usr/bin/python3
'''
Author : Zachary Harvey






'''
import sysdboot
import grubtwo

OPTIONS = {
            'systemd-boot' : sysdboot.runsysdboot,
            'grub2' : grubtwo.run_grub
          }

def booter(system, bootdir='/boot'):
    if system.config['booter']['name'] in OPTIONS.keys():
        return True, OPTIONS[system.config['booter']['name']](system, bootdir)
    else:
        return False, str(system.config['booter']['name']) + ' not currently supported'
