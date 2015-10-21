#! /usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# Copyright 2015 - Ignacio Juan Martín Benedetti <tranceway@gmail.com>
# Copyleft 2015 - Diego Accorinti (mejoras memoria y modelo de cpu)
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


import argparse
import glib
import glob
import gtk
import os
import re

from subprocess import check_output, Popen, PIPE

from plugins import arch


APP_PATH = os.path.dirname(os.path.realpath(__file__))


def get_sources():
    allsources = glob.glob('/etc/apt/sources.list.d/*.list')
    allsources.insert(0, '/etc/apt/sources.list' )

    result = ''
    for src in allsources:
        try:
            result += open(src).read()
        except:
            pass

    return result
###
###
def proc_found(raw, done, distro):
    if distro in raw:
        done.append( distro )
        raw.remove( distro )

    return raw, done
###
def found_suites_from_sources():
    sources = get_sources()

    found = list ( set ( re.findall(r'^\s*deb(?:\s+\[.*\])?\s+(?:(?:https?://)|(?:ftp://))?(?:(?:[\w])+(?:[\./]+)?)+\s([-\w/]+).*$', sources, re.MULTILINE ) ) )

    huayra_suites = [ 'brisa','mate-brisa','pampero','mate-pampero','sud','torbellino' ]
    huayras = []
    for suite in huayra_suites:
        found, huayras = proc_found( found , huayras, suite )
        found, huayras = proc_found( found , huayras, suite + '-updates' )
        found, huayras = proc_found( found , huayras, suite + '-proposed' )

    deb_suites = [ 'squeeze','oldoldstable','wheezy','oldstable','jessie','stable','stretch','testing','sid','unstable','experimental','rc-buggy' ]
    debians = []
    for suite in deb_suites:
        found, debians = proc_found( found , debians, suite )
        found, debians = proc_found( found , debians, suite + '-updates' )
        found, debians = proc_found( found , debians, suite + '/updates' )
        found, debians = proc_found( found , debians, suite + '-proposed-updates' )
        found, debians = proc_found( found , debians, suite + '-backports' )


    huayra = ",".join(str(i) for i in huayras)
    debian = ",".join(str(i) for i in debians)
    resto  = ",".join(str(i) for i in found)

    return huayra, debian, resto
###
def check_sources_debian():
    nil, debian_sources_repos, nil = found_suites_from_sources()
    return debian_sources_repos
###
def check_sources_huayra():
    huayra_sources_repos, nil, nil = found_suites_from_sources()
    return huayra_sources_repos
###
label_start_markup = '<span font_style="normal" font_weight="bold" color="black">'
label_end_markup   = '</span>'
text_start_markup  = '<span size="smaller" color="black">'
text_end_markup    = '</span>'
def label_set_markup(label):
    return label_start_markup + label + label_end_markup
###
def text_set_markup(text):
    return text_start_markup + text + text_end_markup
###
def huayra():
    try:
        lsb_list = open('/etc/lsb-release').read().replace('\n','=').split('=')
    except IOError as e:
        lsb_list = []
    lsb_release = dict(zip(lsb_list[0::2], lsb_list[1::2]))

    if lsb_release.get("DISTRIB_ID") == 'Huayra': ### lsb_release is aware of huayra
        huayra_raw_ver = lsb_release.get("DISTRIB_RELEASE")
        huayra_code_name = lsb_release.get("DISTRIB_CODENAME")
    else:
        try:
            huayra_raw_ver = open('/etc/huayra_version','r').read()[:-1]
            if huayra_raw_ver >= "3.0" :
                huayra_code_name = 'sud'
            elif huayra_raw_ver >="2.0" :
                huayra_code_name = 'pampero'
        except IOError as e: ### huayra is not still aware of himself
            huayra_code_name = 'brisa'
            huayra_raw_ver = '1.X'

    # ? hay repos agregados ?
    huayra_sources_repos =  check_sources_huayra()
    if huayra_code_name != huayra_sources_repos :
        huayra_sources_repos = '[' + huayra_sources_repos + ']'
    else:
        huayra_sources_repos = ''

    huayra_label = label_set_markup ( 'Versión' )
    huayra_text = text_set_markup ( 'Huayra ' + huayra_raw_ver + ' (' + huayra_code_name +') ' +  huayra_sources_repos )

    return huayra_label,huayra_text
###
def debian():

    base_src_code_name = check_sources_debian()
    try:
        base_dist_ver = open('/etc/debian_version','r').read().split()
    except:
        base_dist_ver = ['']

    base_dist_issue = ['Debian']
    debian_label = label_set_markup( 'Base' )
    debian_text = text_set_markup( base_dist_issue[0] + ' ' + base_dist_ver[0] + ' [' + base_src_code_name + ']' )
    return debian_label, debian_text
###
def kernel():

    running_kernel = os.uname()
    kver_label = label_set_markup( 'Kernel versión')
    kver_text = text_set_markup( " ".join(running_kernel[3].split()[2:4]) )

    return kver_label, kver_text
###
# Callbacks
###
def set_clipboard(text):
    clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(text)
###
def on_window_delete_event(widget,event):
    return False
###
def on_window_destroy(widget):
    gtk.main_quit()
    return False
###
def on_close_clicked(widget):
    gtk.main_quit()
    return False
### ### ###
window = gtk.Window()
window.set_title("Acerca de Huayra")
window_icon = os.path.join(APP_PATH, 'media', 'huayra-menu-huayra.svg')
window.set_icon_from_file(window_icon)

width=600
height=420
window.set_geometry_hints( window, width, height, width, height, width, height, 0, 0, 1.5 , 1.5 )
window.set_position(gtk.WIN_POS_CENTER)
window.connect("delete-event", on_window_delete_event )
window.connect("destroy", on_window_destroy )
window.set_border_width(width/30) # 20

vbox = gtk.VBox(True,spacing=0)

icon_theme = gtk.icon_theme_get_default()
logo = gtk.Image()
side = width/5*2/5
wish_icon = "applications-huayra"
emer_icon = window_icon
if icon_theme.has_icon(wish_icon):
    pixbuf = icon_theme.load_icon(wish_icon, side, gtk.ICON_LOOKUP_FORCE_SVG)
else:
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size( emer_icon, side, side)
    except glib.GError as exc:
        pass

if 'pixbuf' in locals():
    logo.set_from_pixbuf(pixbuf)

# Link
web_label = label_start_markup+"Web"+label_end_markup
web_link = text_start_markup+"<a href='http://huayra.conectarigualdad.gob.ar/'>http://huayra.conectarigualdad.gob.ar/</a>"+text_end_markup

# Table
info_table = gtk.Table(6,2,False)
info_table.set_col_spacings(10)
info_table.set_row_spacings(10)

# Memoria
memo = (Popen(['free', '-m'], stdout=PIPE).stdout.read()).split( )
mem_label = label_set_markup ( 'Memoria' )
mem_texto = text_set_markup (memo[7] + " Mb")

#CPU
s = ""
micro = Popen(['lscpu'], stdout=PIPE).stdout.read()
micro = (s.join(micro)).split()
micro_label = label_set_markup ( 'Microprocesador' )

x = 0
while micro[x] <> "name:":
    x += 1
micro_texto = ""
while micro[x+1] <> "Stepping:":
    micro_texto = micro_texto + micro[x+1] + " "
    x += 1
micro_texto = text_set_markup(micro_texto)


def add_row_to_table( label_label, label_text, row, tooltip="" ):
    global info_table
    label = gtk.Label()
    label.set_alignment( 1.0, 0.5) # x right y center
    label.set_markup( label_label )
    label.set_selectable(False)
    info_table.attach(label,0, 1, row, row+1)
    text = gtk.Label()
    text.set_alignment( 0.0, 0.5) # x left y center
    text.set_markup( label_text )
    text.set_selectable(False)
    text.set_tooltip_text(tooltip)
    text.modify_base(gtk.STATE_PRELIGHT, gtk.gdk.Color( '#FAD3B9' ) )
    info_table.attach(text ,1, 2, row, row+1)

add_row_to_table( huayra()[0], huayra()[1] , 0 , "Versión de Huayra\n[Repositorios habilitados]" )
add_row_to_table( debian()[0], debian()[1] , 1 , "Versión base de Debian\n[Repositorios habilitados]" )
add_row_to_table( label_set_markup(arch.Info.label()), text_set_markup(arch.Info.text()), 2, "Arquitectura del sistema." )
add_row_to_table( mem_label  , mem_texto , 3 , "Memoria disponible" )
add_row_to_table( micro_label  , micro_texto , 4 , "Modelo de microprocesador" )
add_row_to_table( kernel()[0], kernel()[1] , 5 , "Versión de compilación del kernel" )
add_row_to_table( web_label  , web_link    , 6 )


#

info_version = gtk.Label() # Fake label to blow markup tags
info_version.set_markup(
      huayra()[0] + ': ' + huayra()[1] + '\n'
    + debian()[0] + ': ' + debian()[1] + '\n'
    + arch.Info.label() + ': ' + arch.Info.text() + '\n'
    + kernel()[0] + ': ' + kernel()[1] + '\n'
    + mem_label + ': ' + mem_texto + '\n'
    + micro_label + ': ' + micro_texto + '\n'
)

fixed = gtk.Fixed()

button_close = gtk.Button(label=" Cerrar ")
button_copy = gtk.Button(label=" Copiar ")
button_copy.set_tooltip_text("Copia al portapapeles")
button_close.connect("clicked", on_close_clicked )
button_close.connect_object("clicked", gtk.Widget.destroy, window) #
button_copy.connect("clicked", lambda x: set_clipboard( info_version.get_text() ) )


def draw_background(widget, event):
    try:
        background = gtk.gdk.pixbuf_new_from_file(os.path.join(APP_PATH, 'media', 'huayra-about-background.svg')) # ret pixbuf
        background = background.scale_simple(width,height,1)
        widget.window.draw_pixbuf(vbox.style.bg_gc[gtk.STATE_NORMAL], background, 0, 0, 0, 0 )
    except glib.GError as exc:
        pass

vbox.connect('expose-event', draw_background)


fixed.put(info_table, 0, 220 )
fixed.put(button_copy, 480, 280 )
fixed.put(button_close, 480, 330 )

vbox.add(fixed)

window.set_focus(button_close)
window.add(vbox)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-g','--gui', help='Muestra una ventana con la información de versión de huayra',action='store_true')
    parser.add_argument('-t','--tty', help='Muestra la información de versión de huayra en la terminal',action='store_true',default=True)
    args = parser.parse_args()
    if args.gui:
        window.show_all()
        gtk.main()
    if args.tty:
        print info_version.get_text()
