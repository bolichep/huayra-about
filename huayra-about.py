#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
import gtk
import glib
from subprocess import check_output
import re
import glob

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

def check_sources_debian():
   sources = get_sources()
   
   found = re.findall(r'^deb.*\s(squeeze|wheezy|jessie|oldstable|stable|testing).*$', sources, re.MULTILINE )

   result=''
   if 'squeeze' in found:
       result += 'squeeze,'
   if 'wheezy' in found:
       result += 'wheezy,'
   if 'jessie' in found:
       result += 'jessie,'
   if 'oldstable' in found:
       result += 'oldstable,'
   if 'stable' in found:
       result += 'stable,'
   if 'testing' in found:
       result += 'testing,'

   return result[:-1]
###
def check_sources_huayra():
   sources = get_sources()
   
   found = re.findall(r'^deb.*\s(brisa|pampero|sud|torbellino).*$', sources, re.MULTILINE )

   result=''
   if 'brisa' in found:
       result += 'brisa,'
   if 'pampero' in found:
       result += 'pampero,'
   if 'sud' in found:
       result += 'sud,'
   if 'torbellino' in found:
       result += 'torbellino,'
   return result[:-1]
###
def huayra():

  lsb_release = check_output(['lsb_release','-sirc']).split()
  if lsb_release[0] == 'Huayra': ### lsb_release is aware of huayra
    huayra_raw_ver = lsb_release[1]
    huayra_code_name = lsb_release[2]
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
  
  huayra_text ='Versión: ' + '<span size="large" >Huayra ' 
  huayra_text += huayra_raw_ver + ' (' + huayra_code_name +') ' +  huayra_sources_repos + '</span>' 

  return huayra_text 
###
def debian():

  base_src_code_name = check_sources_debian()
  try:
     base_dist_ver = open('/etc/debian_version','r').read().split()
  except:
     base_dist_ver = ['']

  base_dist_issue = ['Debian']
  debian_text = 'Base: ' + base_dist_issue[0] + ' ' + base_dist_ver[0] + ' (' + base_src_code_name + ')\n'

  return debian_text
###
def kernel():

  running_kernel = check_output(['uname','-r','-v']).split()
  kernel_text =  'Kernel lanzamiento: ' + running_kernel[0] + '\n' 
  kernel_text += 'Kernel versión: ' + running_kernel[3] + ' ' + running_kernel[4]

  return kernel_text
###
def set_clipboard(text):
    clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(text)

### ### ###
window = gtk.Window()
window.set_title("Acerca de Huayra")
window_icon = os.path.dirname(os.path.realpath(__file__))+"/huayra-menu-huayra.svg"
window.set_icon_from_file(window_icon)

width=600
height=400
window.set_geometry_hints( window, width, height, width, height, width, height, 0, 0, 1.5 , 1.5 )
window.set_position(gtk.WIN_POS_CENTER)
window.connect("delete-event", lambda w,e: False )
window.connect("destroy", lambda w: gtk.main_quit() )
window.set_border_width(width/20)

hbox = gtk.HBox(False,spacing=width/20)

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
   
info_version = gtk.Label()
info_version.set_justify(gtk.JUSTIFY_LEFT)
info_version.set_markup(huayra() + '\n' + debian() + kernel())
info_version.set_selectable(False)

button_close = gtk.Button(label="Cerrar")
button_copy = gtk.Button(label="  Copiar al \nPortapapeles")
button_close.connect("clicked", lambda x: gtk.main_quit() )
button_copy.connect("clicked", lambda x: set_clipboard( info_version.get_text() ) )
bbox = gtk.VButtonBox()
bbox.add(button_copy)
bbox.add(button_close)
bbox.set_layout(gtk.BUTTONBOX_END)
bbox.set_spacing(30)
window.set_focus(button_close)

def draw_background(widget, event):
   try:
      background = gtk.gdk.pixbuf_new_from_file('/usr/share/huayra-about/huayra-about-background.svg') # ret pixbuf
      background = background.scale_simple(width,height,1)
      widget.window.draw_pixbuf(vbox.style.bg_gc[gtk.STATE_NORMAL], background, 0, 0, 0, 0 )
   except glib.GError as exc:
      pass
   
vbox.connect('expose-event', draw_background)
vbox.add(gtk.Label()) # void label
vbox.add(hbox)
hbox.add(info_version)
hbox.add(bbox)

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

