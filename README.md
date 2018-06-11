# pyarch
Arch Linux Install scripts


# Examples

```python
{
    "hostname":"localhost",
    "keymap": "us",
    "consolefont":"CP437",
    "network": "dhcp",
    "time":{"zone": "America/New_York",
            "ntp" : True,
            },
    "locale":"en_US.UTF-8", #A string or a list of locales
    "mount": "/mnt",
    "chrootcmd":"arch-chroot",
    "getmirrors":True,
    "booter":{"name":"systemd-boot",
             "device":"/dev/sda",
             "bootdir":"/boot"
            },
    "disks" : [{
        "device": "sda",    #Required
        "label" : "gpt",    #Required for partitioning
        "partition": [ {"fs":"fat32",    #Required
                        "size" : "100MiB",   #Required
                        "name" : "BOOT",  #Defaults to none
                        "flag" : "boot",  #Defaults to none
                        "type" : "primary",  #Defaults to primary
                        "mount" : "/boot", #Required
                        },
                        {"fs":"ext3",
                        "size" : "50GiB",
                        "name" : "ROOT",
                        "type" : "primary",
                        "mount" : "/",
                        }
                      ]
                },
        {"device" : "sdb",
        "partition" : [
                    {
                "fs" : "ntfs",
                "disk" : "sdb1",
                "mount" : "/run/media/tux/expand"
                    }
                        ]}],
}
```
