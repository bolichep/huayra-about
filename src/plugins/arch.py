#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright 2015 Ignacio Juan Martín Benedetti <tranceway@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import markup
import info_table
import os.path
import subprocess


LABEL = u'Arquitectura'


class Info(object):
    @staticmethod
    def text():
        cmd = ['uname', '-m']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = process.communicate()
        info = out.strip()

        if os.path.exists('/sys/firmware/efi'):
            info += ' (modo UEFI)'
        else:
            info += ' (modo BIOS)'

        return info

    @staticmethod
    def label():
        return LABEL

if __name__ == '__main__':
    print '{0}: {1}'.format(Info.label(), Info.text())

else:
    info_table.add_row_to_table( markup.label_set_markup(Info.label()), markup.text_set_markup(Info.text()), 2, "Arquitectura del sistema." )

    print __name__
