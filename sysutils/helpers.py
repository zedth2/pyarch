#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

PACMAN = 'pacman'

def installer_cmd():
    return [PACMAN, '-S', '--noconfirm']

def pacman_package_install(system, package):
    cmd = installer_cmd()
    cmd.append(package)
    # system.


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def debug(*args, **kwargs):
    printColor(OKBLUE, '  DEBUG :', *args, **kwargs)

def error(*args, **kwargs):
    printColor(FAIL, '  ERROR :', *args, **kwargs)

def warning(*args, **kwargs):
    printColor(WARNING, '  WARNING :', *args, **kwargs)

def happy(*args, **kwargs):
    printColor(OKGREEN, *args, **kwargs)

def printColor(clr, *args, **kwargs):
    print(clr, sep='', end='')
    print(*args, **kwargs)
    print(ENDC, sep='', end='')



class ExecutionError(Exception):
    def __init__(self, returnCode, stdout, stderr):
        super().__init__()
        self.returnCode = returnCode
        self.stdout = stdout
        self.stderr = stderr


    @staticmethod
    def checkAndRaise(returnCode, stdout, stderr):
        if 0 != returnCode:
            raise ExecutionError(returnCode, stdout, stderr)
        return returnCode, stdout, stderr
