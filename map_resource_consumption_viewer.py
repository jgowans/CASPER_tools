#!/usr/bin/env python

'''This script parses the resource consumption section of 
a system_map.mrp file and displays it in a GUI tree view'''

import tkinter
import tkinter.ttk as ttk

class MrpFile:
    def __init__(self, filename):
        # parse filename
        pass

class MrpEntry:
    def __init__(self, parent, children):
        pass

    def get_iid(self):
        return self.iid

    def set_iid(self, iid):
        self.iid = iid


root = tkinter.Tk()
tree = ttk.Treeview(root)

tree["columns"]=("one","two")
tree.column("one", stretch=True)
tree.column("two", stretch=True)
tree.heading("one", text="coulmn A")
tree.heading("two", text="column B")
 
tree.insert("" , 0,    text="Line 1", values=("1A","1b"))
 
id2 = tree.insert("", 1, "dir2", text="Dir 2")
tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
 
##alternatively:
tree.insert("", 3, "dir3", text="Dir 3")
tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))
 
tree.pack()
root.mainloop()
