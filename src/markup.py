#! /usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
### 0
label_start_markup = '<span font_style="normal" font_weight="bold" color="black">'
label_end_markup   = '</span>'
text_start_markup  = '<span size="smaller" color="black">'
text_end_markup    = '</span>'
### 1
def label_set_markup(label):
	return label_start_markup + label + label_end_markup
### 1
def text_set_markup(text):
	return text_start_markup + text + text_end_markup


