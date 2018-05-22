#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from os.path import exists



SYSFS_BLOCK_PATH = '/sys/block/{disk}'
DEV_PATH = '/dev/{disk}'

class Disk:
    def __init__(self, disk):
        if exists(DEV_PATH.format(disk=disk)) and exists(SYSFS_BLOCK_PATH.format(disk=disk)):
            self.__disk = disk
        else:
            raise ValueError('Invalid disk {} : SYSFS {} and device {} does not exist'.format(disk, SYSFS_BLOCK_PATH.format(disk=disk), DEV_PATH.format(disk=disk)))

    @property
    def disk(self):
        return self.__disk


    @property
    def logicalBlockSize(self):
        '''
        Block Size I believe is always in bytes.
        '''
        path = (SYSFS_BLOCK_PATH + '/device/block/{disk}/queue/logical_block_size').format(disk=self.disk)
        size = open(path).readlines()
        return int(size[0].strip())

    @property
    def totalSize(self):
        '''
        Returns the disk size in bytes.
        '''
        path = (SYSFS_BLOCK_PATH + '/device/block/{disk}/size').format(disk=self.disk)
        size = open(path).readlines()
        return int(size[0].strip()) * self.logicalBlockSize

    @property
    def getDevPath(self):
        return DEV_PATH.format(disk=self.disk)


    @property
    def getPartitions(self):
        pass
