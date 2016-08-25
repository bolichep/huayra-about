#! /usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# Copyright 2015 - Ignacio Juan Martín Benedetti <tranceway@gmail.com>
# Copyleft 2015 - Diego Accorinti (mejoras memoria y modelo de cpu)
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import rasti    # automatic plugin load
import markup
import info_table  # table to add rows 'crappy(only) plugin api'
import argparse
import glib
import glob
import gtk  # k
import os  # k

from subprocess import check_output, Popen, PIPE

APP_PATH = os.path.dirname(os.path.realpath(__file__))

# Cargo plugins
rasti.load()

#
# Callbacks
#


def button_press(widget, event):
    if event.type == gtk.gdk.BUTTON_PRESS:
        widget.popup(None, None, None, event.button, event.time)
        return True
    return False


def menu_item_copy_response(widget, string):
    set_clipboard(info_table.solo_texto())


def set_clipboard(text):
    clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(text)


def on_window_delete_event(widget, event):
    return False


def on_window_destroy(widget):
    gtk.main_quit()
    return False


def on_close_clicked(widget):
    gtk.main_quit()
    return False


# row -> present
# gui

window = gtk.Window()
window.set_title("Acerca de Huayra")
window_icon = os.path.join(APP_PATH, 'media', 'huayra-menu-huayra.svg')
window.set_icon_from_file(window_icon)

width = 600
height = 420
window.set_geometry_hints(window, width, height, width, height, width, height, 0, 0, 1.5, 1.5)
window.set_position(gtk.WIN_POS_CENTER)
window.connect("delete-event", on_window_delete_event)
window.connect("destroy", on_window_destroy)
window.set_border_width(width / 30)  # 20

vbox = gtk.VBox(True, spacing=0)

icon_theme = gtk.icon_theme_get_default()
logo = gtk.Image()
side = width / 5 * 2 / 5
wish_icon = "applications-huayra"
emer_icon = window_icon
if icon_theme.has_icon(wish_icon):
    pixbuf = icon_theme.load_icon(wish_icon, side, gtk.ICON_LOOKUP_FORCE_SVG)
else:
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(emer_icon, side, side)

    except glib.GError as exc:
        pass

if 'pixbuf' in locals():
    logo.set_from_pixbuf(pixbuf)


fixed = gtk.Fixed()

button_close = gtk.Button(label=" Cerrar ")
button_close.connect("clicked", on_close_clicked)
button_close.connect_object("clicked", gtk.Widget.destroy, window)
button_close.set_tooltip_text("Cerrar acerca de Huayra")

menu = gtk.Menu()
menu_item_copy = gtk.MenuItem("Copiar")
menu_item_copy.set_tooltip_text("Copia al portapapeles")
menu.append(menu_item_copy)
menu_item_copy.connect("activate", menu_item_copy_response, " Texto")
menu_item_copy.show()
button_menu = gtk.Button(label="  Más  ")
button_menu.connect_object("event", button_press, menu)


def draw_background(widget, event):
    try:
        background = gtk.gdk.pixbuf_new_from_file(os.path.join(APP_PATH, 'media', 'huayra-about-background.svg'))  # ret pixbuf
        background = background.scale_simple(width, height, 1)
        widget.window.draw_pixbuf(vbox.style.bg_gc[gtk.STATE_NORMAL], background, 0, 0, 0, 0)

    except glib.GError as exc:
        pass

vbox.connect('expose-event', draw_background)


fixed.put(info_table.table, 0, 220)
fixed.put(button_menu, 480, 280)
fixed.put(button_close, 480, 330)

vbox.add(fixed)

window.set_focus(button_close)
window.add(vbox)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gui', help='Muestra una ventana con la información de versión de huayra', action='store_true')
    parser.add_argument('-t', '--tty', help='Muestra la información de versión de huayra en la terminal', action='store_true', default=True)
    args = parser.parse_args()


    if args.gui:
        window.show_all()
        gtk.main()
    if args.tty:
        print info_table.solo_texto()
