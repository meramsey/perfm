import os
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if len(sys.argv) == 1:
    path = os.getenv("PWD")
else:
    path = sys.argv[1]

def path_liststore(path):
    store = Gtk.ListStore(str)
    for f in os.listdir(path):
        store.append([f])
    def compare(model, row1, row2, user_data):
        sort_column, _ = model.get_sort_column_id()
        value1 = model.get_value(row1, sort_column)
        value2 = model.get_value(row2, sort_column)
        if value1 < value2:
            return -1
        elif value1 == value2:
            return 0
        else:
            return 1
    store.set_sort_func(0, compare, None)
    return store

def treeview(model, path):
    tree = Gtk.TreeView(model=model)
    column = Gtk.TreeViewColumn(f"Files in {path}", Gtk.CellRendererText(), text=0)
    column.set_sort_column_id(0)
    tree.append_column(column)
    return tree

def scrollable(widget):
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    scrolled.add(widget)
    return scrolled

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)
win.add(scrollable(treeview(path_liststore(path), path)))
win.show_all()
Gtk.main()
