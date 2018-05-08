#!/usr/bin/python3
'''
Author : Zachary Harvey






'''

from gi.repository import Gtk
from sysutils import groups

class UserConfig(Gtk.VBox):
    def __init__(self, homogeneous=False, spacing=0, **kwargs):
        super().__init__(homogeneous=homogeneous, spacing=spacing, **kwargs)
        hold, lbl, self.txtUN = self.LabelWithEntry('Username:')
        self.pack_start(hold, False, True, 0)
        hold, lbl, self.txtPW = self.LabelWithEntry('Password:')
        self.pack_start(hold, False, True, 0)
        lst = self.ListChecks()
        self.pack_start(lst, True, True, 0)
        lst.show_all()


    def LabelWithEntry(self, lblText):
        nameHolder = Gtk.HBox()
        lbl = Gtk.Label(lblText)
        nameHolder.pack_start(lbl, False, True, 0)
        txt = Gtk.Entry()
        nameHolder.pack_start(txt, True, True, 0)
        return nameHolder, lbl, txt

    def ListChecks(self):
        scroll = Gtk.ScrolledWindow()
        lst = Gtk.ListBox()
        grps = groups.GetAllGroups()
        for g in grps:
            r = Gtk.ListBoxRow()
            h = Gtk.HBox()
            lbl = Gtk.Label(g, xalign=0)
            c = Gtk.CheckButton()
            h.pack_start(c, False, True, 0)
            h.pack_start(lbl, True, True, 0)
            r.add(h)
            lst.add(r)
        scroll.add(lst)
        return scroll

class Win(Gtk.Window):
    def __init__(self, winType=Gtk.WindowType.TOPLEVEL):
        super().__init__(winType)
        self.v = UserConfig()
        self.add(self.v)


if __name__ == '__main__':
    x= Win()
    x.show_all()
    Gtk.main()
