# -*- coding: utf-8 -*-
# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import markup
import info_table
import os

from subprocess import check_output


def kernel():
    running_kernel = os.uname()
    kver_label = markup.label_set_markup('Kernel versión')
    kver_text = markup.text_set_markup(" ".join(running_kernel[3].split()[2:4]))

    return kver_label, kver_text


info_table.add_row_to_table(kernel()[0], kernel()[1], 5, "Versión de compilación del kernel")

#rint __name__
