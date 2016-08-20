# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
# -*- coding: utf-8 -*-
import imp
import fnmatch
import os


def load():
    PLUGINSPATH = os.path.dirname(os.path.realpath(__file__)) + '/plugins'
    plugs = sorted(os.listdir(PLUGINSPATH))

    for fname in plugs:
        if not os.path.isdir(fname) and fnmatch.fnmatch(fname, '*.py'):
            plug = fname[:fname.find('.')]
            #rint plug, "$"
        else:
            continue
        if True:
#        try:
            fp, path, desc = imp.find_module(plug, [PLUGINSPATH])
            imp.load_module(plug, fp, path, desc)
#            print path
#        except:
            # print "Except"
            # pass
#        finally:
            if fp:
                fp.close()


#rint __name__
