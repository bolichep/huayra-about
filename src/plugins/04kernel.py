# -*- coding: utf-8 -*-
# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import markup
import info_table

from subprocess import check_output


def kernel():
    running_kernel = check_output(['uname', '-r', '-v']).split()
    krel_label = markup.label_set_markup('Kernel lanzamiento')
    krel_text = markup.text_set_markup(running_kernel[0])
    kver_label = markup.label_set_markup('Kernel versión')
    kver_text = markup.text_set_markup(running_kernel[3] + ' ' + running_kernel[4])

    return krel_label, krel_text, kver_label, kver_text


info_table.add_row_to_table(kernel()[2], kernel()[3], 5, "Versión de compilación del kernel")

#rint __name__
