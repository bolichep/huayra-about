# -*- coding: utf-8 -*-
# Copyright 2015 - Pedro Boliche <bolichep@gmail.com>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)
import markup
import info_table
import glob

from subprocess import check_output

from aptsources import sourceslist


def get_suites(sources):
    suites = []
    for entry in sources:
        if (not entry.disabled):
            suites.append(entry.dist)

    return suites


def proc_found(raw, done, distro):
    if distro in raw:
        done.append(distro)
        raw.remove(distro)

    return raw, done


def found_suites_from_sources():
    sources = sourceslist.SourcesList()

    found = list(set(get_suites(sources)))

    huayra_suites = ['brisa', 'mate-brisa', 'pampero', 'mate-pampero', 'sud', 'zonda', 'torbellino']
    huayras = []
    for suite in huayra_suites:
        found, huayras = proc_found(found, huayras, suite)
        found, huayras = proc_found(found, huayras, suite + '-updates')
        found, huayras = proc_found(found, huayras, suite + '-proposed')

    deb_suites = ['squeeze', 'oldoldstable', 'wheezy', 'oldstable', 'jessie', 'stable', 'stretch', 'testing', 'sid', 'unstable', 'experimental', 'rc-buggy']
    debians = []
    for suite in deb_suites:
        found, debians = proc_found(found, debians, suite)
        found, debians = proc_found(found, debians, suite + '-updates')
        found, debians = proc_found(found, debians, suite + '/updates')
        found, debians = proc_found(found, debians, suite + '-proposed-updates')
        found, debians = proc_found(found, debians, suite + '-backports')

    huayra = ",".join(str(i) for i in huayras)
    debian = ",".join(str(i) for i in debians)
    resto = ",".join(str(i) for i in found)

    return huayra, debian, resto


def check_sources_debian():
    nil, debian_sources_repos, nil = found_suites_from_sources()
    return debian_sources_repos


def check_sources_huayra():
    huayra_sources_repos, nil, nil = found_suites_from_sources()
    return huayra_sources_repos


def huayra():
    try:
        lsb_list = open('/etc/lsb-release').read().replace('\n', '=').split('=')
    except IOError as e:
        lsb_list = []
    lsb_release = dict(zip(lsb_list[0::2], lsb_list[1::2]))

    if lsb_release.get("DISTRIB_ID") == 'Huayra':  # lsb_release is aware of huayra
        huayra_raw_ver = lsb_release.get("DISTRIB_RELEASE")
        huayra_code_name = lsb_release.get("DISTRIB_CODENAME")

    else:
        try:
            huayra_raw_ver = open('/etc/huayra_version', 'r').read()[:-1]
            if huayra_raw_ver >= "4.0":
                huayra_code_name = 'zonda'
            elif huayra_raw_ver >= "3.0":
                huayra_code_name = 'sud'
            elif huayra_raw_ver >= "2.0":
                huayra_code_name = 'pampero'
        except IOError as e:  # huayra is not still aware of himself
            huayra_code_name = 'brisa'
            huayra_raw_ver = '1.X'

    # ? hay repos agregados ?
    huayra_sources_repos = check_sources_huayra()
    if huayra_code_name != huayra_sources_repos:
        huayra_sources_repos = '[' + huayra_sources_repos + ']'
    else:
        huayra_sources_repos = ''

    huayra_label = markup.label_set_markup('Versión')
    huayra_text = markup.text_set_markup('Huayra ' + huayra_raw_ver + ' (' + huayra_code_name + ') ' + huayra_sources_repos)

    return huayra_label, huayra_text


def debian():
    base_src_code_name = check_sources_debian()
    try:
        base_dist_ver = open('/etc/debian_version', 'r').read().split()
    except:
        base_dist_ver = ['']

    base_dist_issue = ['Debian']
    debian_label = markup.label_set_markup('Base')
    debian_text = markup.text_set_markup(base_dist_issue[0] + ' ' + base_dist_ver[0] + ' [' + base_src_code_name + ']')
    return debian_label, debian_text


info_table.add_row_to_table(huayra()[0], huayra()[1], 0, "Versión de Huayra\n[Repositorios habilitados]")
info_table.add_row_to_table(debian()[0], debian()[1], 1, "Versión base de Debian\n[Repositorios habilitados]")

#rint __name__
