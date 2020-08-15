#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import glob
import time
import re
import datetime

import logging
import logging.config

# global configuration
import indelvcf.glv as glv

import subprocess as sbp
from subprocess import PIPE


def start_log():
    ''' from conf.py _set_paths
    '''

    logging.config.dictConfig(glv.conf.log.config)
    global log
    log = logging.getLogger(__name__)
    log.info("logging start {}".format(__name__))


def clp(str):
    ''' clean parameter
    '''
    param = re.sub(r";+", " ", str)
    return param


def save_to_tmpfile(file_path, can_log = True):
    """
    """

    ret = False
    if os.path.isfile(file_path):
        # /a/b/c.txt
        # /a/b/bak/c.txt
        dirname_file = os.path.dirname(file_path)
        basename_file = os.path.basename(file_path)

        file_bak_path = "{}/{}".format(
            glv.conf.out_bak_dir,
            basename_file)

        ret = True
        ts = time.time()
        new_file_path = "{}.{}.bak".format(file_bak_path, ts)

        os.rename(file_path, new_file_path)

        if can_log:
            log.info("{} exist. mv to {}".format(
                file_path, new_file_path))

    return ret


def progress_check(now_progress):

    stat = False    # False if don't do this progress
    param_progress = glv.conf.progress

    log.info("now_progress={} param_progress={}".format(
        now_progress, param_progress))

    #log.debug("now_progress={} {} param_progress={} {}".format(
    #    now_progress,
    #    now_progress_no,
    #    param_progress,
    #    param_progress_no))

    if param_progress == 'all':
        stat = True

    else:
        now_progress_no = glv.outlist.outf_prefix[now_progress]['no']
        param_progress_no = glv.outlist.outf_prefix[param_progress]['no']
        if now_progress_no >= param_progress_no:
            stat = True

    return stat


def stop(now_progress):

    if glv.conf.stop == 'no':
        return

    now_progress_no = glv.outlist.outf_prefix[now_progress]['no']
    param_stop_no = glv.outlist.outf_prefix[glv.conf.stop]['no']
    if now_progress_no >= param_stop_no:
        log.info("stop {}".format(glv.conf.stop))
        sys.exit(1)


def check_for_files(filepath):

    # filepath is pattern
    fobj_list = list()

    for filepath_object in glob.glob(filepath):

        if os.path.isfile(filepath_object):
            fobj_list.append(filepath_object)

    return fobj_list


def strip_hash_comment(line):
    return line.split('#')[0].strip()


def elapsed_time(now_time, start_time):

    elapsed_time = now_time - start_time
    #3:46:11.931354
    return "elapsed_time {}".format(
        datetime.timedelta(seconds=elapsed_time))


def try_exec(cmd):

    try:
        log.info("do {}".format(cmd))

        sbp.run(cmd,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            shell=True,
            check=True)

    except sbp.CalledProcessError as e:
        log.error("{}.".format(e.stderr))
        sys.exit(1)


def tabix(vcf_file):

    #-f -p vcf
    cmd1 = "{} {} {}".format(
        'tabix',
        '-f -p vcf',
        vcf_file)

    try_exec(cmd1)


def mk_outdir(mod_name):

    out_dir = "{}/{}".format(
        glv.conf.out_dir,
        glv.outlist.outf_prefix[mod_name]['dn'])

    if os.path.exists(out_dir):
        log.info("exist directory {}".format(out_dir))
    else:
        log.info("not exist directory {}".format(out_dir))
        os.makedirs(out_dir, exist_ok=True) # refs
        log.info("prepare directory {}".format(out_dir))

    return out_dir

