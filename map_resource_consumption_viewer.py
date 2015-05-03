#!/usr/bin/env python

'''This script parses the resource consumption section of 
a system_map.mrp file and displays it in a GUI tree view'''

import tkinter
import tkinter.ttk as ttk
import re

class MrpFile:
    def __init__(self, filename):
        file_data = self.parse_file(filename)
        self.columns = file_data['columns']
        self.blocks_usage = file_data['blocks_usage']
        self.root_blocks = []  # contains pointers to the root MrpEntry objects. All child blocks are pointed to by root blocks
        self.parse_blocks()

    def parse_file(self, filename):
        '''This yucky block of code finds and extracts the things we are interested in from the file:
        - the columns headings of each resource being measured
        - the amount of resources consumed by each block'''
        with open(filename) as f:
            full_file = f.readlines()
        assert(full_file.count("Section 13 - Utilization by Hierarchy\n") == 2) # first in TOC, 2nd with information
        idx_of_start_of_toc = full_file.index("Section 13 - Utilization by Hierarchy\n")
        idx_of_data = full_file.index("Section 13 - Utilization by Hierarchy\n", idx_of_start_of_toc + 1) # look for next occurance after TOC
        raw_header = full_file[idx_of_data+3]
        raw_blocks_usage = full_file[idx_of_data+5:] # there will be some other info at the end of this chunk - we should avoid trying to parse it
        columns = [x.strip() for x in raw_header.split('|')[2:-1]] # first and last columns are empty. Second column is 'Module' which is not necessary.
        blocks_usage = []
        for block in raw_blocks_usage:
            block_split = block.split('|')
            if len(block_split) == len(columns) + 3:  # remember the empty first, second  and last columns
                blocks_usage.append([x.strip() for x in block_split[1:-1]]) # remove empty first and last
        print('Found {b} blocks'.format(b=len(blocks_usage)))
        return {'columns': columns, 'blocks_usage': blocks_usage}

    def parse_blocks(self):
        last_touched = None # initial block should be root, so this *should* be safe...
        for raw_block in self.blocks_usage:
            block = MrpEntry(raw_block[0], raw_block[1:])
            if block.depth() == 0:
                self.root_blocks.append(block)
            else:
                depth_difference = last_touched.depth() - block.depth()
                if depth_difference == -1: # going down
                    last_touched.add_child(block)
                elif depth_difference >= 0:
                    ancestor = last_touched.get_ancestor(depth_difference + 1) # go up. When the difference is 0 we actuall want to go up by 1 to get the parent of the last touched.
                    ancestor.add_child(block)
                else:
                    raise('We somehow attempted to decend by more than 1 node. Should never happen.')
            last_touched = block

class MrpEntry:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.parent = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def parent(self):
        return self.parent

    def depth(self):
        '''Count how many '+' symbols there are at the start of the name. This indicates depth'''
        match = re.match('\++', self.name)
        return 0 if match == None else len(match.group())

    def get_ancestor(self, n):
        if n == 0:
            return self
        else:
            return self.parent.get_ancestor(n-1)

    def add_self_and_children(self, tree_ptr):
        if self.parent == None:
            self.iid = tree_ptr.insert('', 'end', text=self.name, values=self.data)
        else:
            self.iid = tree_ptr.insert(self.parent.iid, 'end', text=self.name, values=self.data)

        for child in self.children:
            child.add_self_and_children(tree_ptr)

print('Enter mrp filename to parse: ')
#mrp_file = MrpFile(input())
mrp_file = MrpFile('/home/jgowans/system_standard_fft.mrp')

root = tkinter.Tk()
tree = ttk.Treeview(root)

tree["columns"]=tuple(mrp_file.columns)
for col in mrp_file.columns:
    tree.column(col, stretch=True)
    tree.heading(col, text=col)

for root_block in mrp_file.root_blocks:
    root_block.add_self_and_children(tree)
 
 
tree.pack()
root.mainloop()
