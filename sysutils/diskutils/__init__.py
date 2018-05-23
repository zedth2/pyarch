#!/usr/bin/python3
'''
Author : Zachary Harvey


parted length appears to support the sizes of, B, kB, MB, GB, TB, KiB, MiB, GiB, TiB
will probably just support those because size will ultimately just get forwarded
to parted. Also may support percentages.
{
'device': 'sda',    #Required
'label' : 'gpt',    #Required
'partition': [ {'fs':'fat32',    #Required
                'size' : '100MiB',   #Required
                'name' : 'BOOT',  #Defaults to none
                'flag' : 'boot',  #Defaults to none
                'type' : 'primary',  #Defaults to primary
                'mount' : '/boot',
                },
                {'fs':'ext3',
                'size' : '50GiB',
                'name' : 'ROOT',
                'type' : 'primary',
                'mount' : '/',
                }
              ]
}



'''

import re
#A common error and a capturing REGEX for use in error handling.
'''
Error: You requested a partition from 0B to 100MB (sectors 0..195312).
The closest location we can manage is 17.4kB to 100MB (sectors 34..195312).
'''
REGEX_PART_BEGIN = re.compile('''Error: You requested a partition from [0-9.]+(?:B|kB|MB|GB|TB|PB|EB|ZB|YB|KiB|MiB|GiB|TiB|PiB|EiB|ZiB|YiB) to [0-9.]+(?:B|kB|MB|GB|TB|PB|EB|ZB|YB|KiB|MiB|GiB|TiB|PiB|EiB|ZiB|YiB) \(sectors ([0-9]+)..([0-9]+)\).
The closest location we can manage is [0-9.]+(?:B|kB|MB|GB|TB|PB|EB|ZB|YB|KiB|MiB|GiB|TiB|PiB|EiB|ZiB|YiB) to [0-9.]+(?:B|kB|MB|GB|TB|PB|EB|ZB|YB|KiB|MiB|GiB|TiB|PiB|EiB|ZiB|YiB) \(sectors ([0-9]+)..([0-9]+)\).
''')

from sysinfo.disks import Disk, DEV_PATH
from ..helpers import ExecutionError, debug
from glob import glob
from distutils import spawn
from os.path import exists

PART_TYPES = ['primary', 'logical', 'extended']
PART_TYPES_PRIMARY = PART_TYPES[0]
PART_TYPES_LOGICAL = PART_TYPES[1]
PART_TYPES_EXTENDED = PART_TYPES[2]

FLAGS = ["boot", "root", "swap", "hidden", "raid", "lvm", "lba", "legacy_boot", "irst", "esp", "palo"]
PART_FLAG_BOOT = FLAGS[0]
PART_FLAG_ROOT = FLAGS[1]
PART_FLAG_SWAP = FLAGS[2]
PART_FLAG_HIDDEN = FLAGS[3]
PART_FLAG_RAID = FLAGS[4]
PART_FLAG_LVM = FLAGS[5]
PART_FLAG_LBA = FLAGS[6]
PART_FLAG_LEG_BOOT = FLAGS[7]
PART_FLAG_IRST = FLAGS[8]
PART_FLAG_ESP = FLAGS[9]
PART_FLAG_PALO = FLAGS[10]

LABELS = ["aix", "amiga", "bsd", "dvh", "gpt", "loop", "mac", "msdos", "pc98", "sun"]
LABEL_AIX = LABELS[0]
LABEL_AMIGA = LABELS[1]
LABEL_BSD = LABELS[2]
LABEL_DVH = LABELS[3]
LABEL_GPT = LABELS[4]
LABEL_LOOP = LABELS[5]
LABEL_MAC = LABELS[6]
LABEL_MSDOS = LABELS[7]
LABEL_PC98 = LABELS[8]
LABEL_SUN = LABELS[9]

SIZE_BYTE = 'B'
SIZE_SECTOR = 's'
SIZES = [SIZE_SECTOR, SIZE_BYTE, 'kB', 'MB', 'MiB', 'GB', 'GiB', 'TB', 'TiB']

EXPONENTS = {
    SIZE_BYTE:    1,       # byte
    "kB":   1000**1, # kilobyte
    "MB":   1000**2, # megabyte
    "GB":   1000**3, # gigabyte
    "TB":   1000**4, # terabyte
    "PB":   1000**5, # petabyte
    "EB":   1000**6, # exabyte
    "ZB":   1000**7, # zettabyte
    "YB":   1000**8, # yottabyte

    "KiB":  1024**1, # kibibyte
    "MiB":  1024**2, # mebibyte
    "GiB":  1024**3, # gibibyte
    "TiB":  1024**4, # tebibyte
    "PiB":  1024**5, # pebibyte
    "EiB":  1024**6, # exbibyte
    "ZiB":  1024**7, # zebibyte
    "YiB":  1024**8  # yobibyte
}

MKFS_CMD = {
    'ext2' : ['mkfs.ext2'],
    'ext3' : ['mkfs.ext3'],
    'ext4' : ['mkfs.ext4'],
    'fat16' : ['mkfs.vfat', '-F', '16'],
    'fat32' : ['mkfs.vfat', '-F', '32'],
    'ntfs' : ['mkfs.ntfs']
}

def toBytes(size, units):
    return float(size) * EXPONENTS[units]

class Device:
    def __init__(self, disk, label):
        self.disk = Disk(disk)
        self.__setlabel(label)
        self.parts = []

    def getparts(self):
        parts = glob('/dev/{}[0-9]*'.format(self.disk.disk))
        return parts

    def addpart(self, newpart):
        if not isinstance(newpart, Partition):
            raise ValueError('Partitions must be of type Partition')
        self.parts.append(newpart)

    def __setlabel(self, newlabel):
        if newlabel not in LABELS:
            raise ValueError(str(newlabel) + ' is not in the accepted labels')
        self.__label = newlabel

    def __getlabel(self):
        return self.__label

    label = property(__getlabel, __setlabel)

    def make_script(self):
        curpos = toBytes(1, 'MiB')
        curpart = 1
        script = ['parted', '-m', '-s', self.disk.getDevPath(), 'mklabel', self.label]
        while curpart-1 < len(self.parts):
            p = self.parts[curpart-1]
            start = str(curpos) + SIZE_BYTE
            curpos += int(toBytes(p.size, p.unit))
            end = str(curpos) + SIZE_BYTE
            script += ['mkpart', p.type, p.fs, start, end]
            if p.name:
                script += ['name', str(curpart), p.name]
            if p.flag:
                script += ['set', str(curpart), p.flag]
            curpart += 1
        return script

    def create(self, system):
        begin = ['parted', '-m', '-s', '/dev/'+self.disk.disk]
        mklabel = begin + ['mklabel', self.label]
        ExecutionError.checkAndRaise(*system.exec_chroot(*mklabel, chroot=False))
        curPos = toBytes(1, 'MiB')
        curPart = 1
        for p in self.parts:
            curPos = p.createPart(system, begin, curPart, curPos)
            curPart += 1
        return True

    @classmethod
    def fromDict(cls, dct):
        new = cls(dct['device'], dct['label'])
        for p in dct['partition']:
            new.addpart(Partition.fromDict(p, new.disk))
        return new


class Partition:
    def __init__(self, parentDisk, size, fs, name='', type=PART_TYPES_PRIMARY, flag=''):
        self.parDisk = parentDisk
        self.size, self.unit = Partition.parseSize(size)
        self.fs = fs
        self.type = type
        self.flag = flag
        self.name = name
        self.path = None

        self.__tries = 0

    def __setunit(self, newunit):
        if newunit not in SIZES:
            raise ValueError(str(newunit) + ' not in the accepted units')
        self.__unit = newunit

    def __getunit(self):
        return self.__unit
    unit = property(__getunit, __setunit)

    def __setflag(self, newflag):
        if newflag not in FLAGS and newflag != '':
            raise ValueError(str(newflag) + ' must be empty or in the accepted flags')
        self.__flag = newflag
    def __getflag(self):
        return self.__flag
    flag = property(__getflag, __setflag)

    def __settype(self, newtype):
        if newtype not in PART_TYPES:
            raise ValueError(str(newtype) + ' is not in accepted partition types')
        self.__type = newtype
    def __gettype(self):
        return self.__type
    type = property(__gettype, __settype)

    def createPart(self, system, partcmd, curpart, curpos, end=None):
        self.__tries += 1
        start = str(curpos) + SIZE_BYTE
        newCurPos = end
        if end is None:
            newCurPos = self.toBytes(self.size, self.unit) + (curpos if self.size >= 0 else 0)
            end = str(newCurPos) + SIZE_BYTE
        else:
            end = str(end) + SIZE_BYTE
        mkpart = ['mkpart', self.type, self.fs, start, end]
        recode, stdout, stderr = system.exec_chroot(*partcmd, *mkpart, chroot=False)
        if 0 != recode:
            if self.__tries > 2: #Yeah if we've already tried it more than twice it's another error I don't know about
                raise ExecutionError(recode, stdout, stderr)
            err = self.beginPartErr(stderr.decode())
            if err is None: #Then I don't know what went wrong
                raise ExecutionError(recode, stdout, stderr)
            return self.createPart(system, partcmd, curpart, err['start'], err['end'])

        if self.name:
            mkpart = ['name', str(curpart), self.name]
            ExecutionError.checkAndRaise(*system.exec_chroot(*partcmd, *mkpart, chroot=False))
        if self.flag:
            mkpart = ['set', str(curpart), self.flag]
            ExecutionError.checkAndRaise(*system.exec_chroot(*partcmd, *mkpart, chroot=False))
        path = (DEV_PATH+str(curpart)).format(disk=self.parDisk.disk)
        if not exists(path):
            path = None
        else:
            self.path = path
            self.createFileSystem(system, self.path)
        return newCurPos

    def createFileSystem(self, system, path):
        if self.fs not in MKFS_CMD.keys():
            raise ValueError(self.fs + ' not in supported file system')
        ExecutionError.checkAndRaise(*system.exec_chroot(*MKFS_CMD[self.fs], path, chroot=False))

    def beginPartErr(self, stderr):
        beg = REGEX_PART_BEGIN.match(stderr)
        if beg is None:
            return beg
        #return int(beg.groups()[0]) * self.parDisk.logicalBlockSize
        return {"start" : int(beg.groups()[2]) * self.parDisk.logicalBlockSize,
                "end" : int(beg.groups()[3]) * self.parDisk.logicalBlockSize}

    def toBytes(self, size, units):
        if units == SIZE_SECTOR:
            size = size * self.parDisk.logicalBlockSize
            units = SIZE_BYTE
        if size < 0:
            s = toBytes(size * -1, units)
            return self.parDisk.totalSize - s

        return toBytes(size, units)

    @staticmethod
    def parseSize(size):
        if not isinstance(size, str):
            raise ValueError('Expecting a string for variable size')
        num = ''
        unit = ''
        cnt = 0
        while cnt < len(size):
            if size[cnt].isdigit() or size[cnt] == '-':
                num += size[cnt]
            else:
                break
            cnt += 1

        return float(num), size[cnt:]

    @classmethod
    def fromDict(cls, dct, parentDisk):
        size = dct['size']
        fs = dct['fs']
        name = ''
        type = PART_TYPES_PRIMARY
        flag = ''
        try:
            name = dct['name']
        except KeyError:
            pass

        try:
            type = dct['type']
        except KeyError:
            pass

        try:
            flag = dct['flag']
        except KeyError:
            pass

        return cls(parentDisk, size, fs, name, type, flag)



def depCheck(system):
    path = spawn.find_executable('parted')




def clean(path):
    wipe(glob('/dev/{}[0-9]*'.format(path)), '/dev/'+path)

def wipe(partition_names, path):
        """
        Wipe the block device of meta-data, be it file system, LVM, etc.
        This is not intended to be secure, but rather to ensure that
        auto-discovery tools don't recognize anything here.
        """
        for partition in partition_names:
            wipe_dev(partition)
        wipe_dev(path)

def wipe_dev(dev_path):
        """
        Wipe a device (partition or otherwise) of meta-data, be it file system,
        LVM, etc.
        @param dev_path:    Device path of the partition to be wiped.
        @type dev_path:     str
        """
        with open(dev_path, 'wb') as p:
            p.write(bytearray(1024))

if __name__ == '__main__':
    print(Device('sda').getparts())
    maker()
