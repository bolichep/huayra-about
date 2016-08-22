# -*- coding: utf-8 -*-
# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import gtk

# Table
table = gtk.Table(6, 2, False)
table.set_col_spacings(10)
table.set_row_spacings(10)
table_row = 0
# cli
info_version = gtk.Label()  # Fake label to blow markup tags
salida_cli = ''


def add_row_to_table(label_label, label_text, row, tooltip="", destino="all"):
    global table
    global salida_cli
    global table_row
    label = gtk.Label()
    if destino == "all" or destino == "gui":
        label.set_alignment(1.0, 0.5)  # x right y center
        label.set_markup(label_label)
        label.set_selectable(False)
        table.attach(label, 0, 1, table_row, table_row + 1)
        text = gtk.Label()
        text.set_alignment(0.0, 0.5)  # x left y center
        text.set_markup(label_text)
        text.set_selectable(False)
        text.set_tooltip_text(tooltip)
        text.modify_base(gtk.STATE_PRELIGHT, gtk.gdk.Color('#FAD3B9'))
        table.attach(text, 1, 2, table_row, table_row + 1)
        table_row += 1

    if destino == "all" or destino == "cli":
        salida_cli += label_label + ': ' + label_text + '\n'


"""
info_version.set_markup(
      huayra()[0] + ': ' + huayra()[1] + '\n'
    + debian()[0] + ': ' + debian()[1] + '\n'
    + arch.Info.label() + ': ' + arch.Info.text() + '\n'
    + kernel()[2] + ': ' + kernel()[3] + '\n'
    + mem_label + ': ' + mem_texto + '\n'
    + micro_label + ': ' + micro_texto + '\n'
)
"""


#rint __name__
