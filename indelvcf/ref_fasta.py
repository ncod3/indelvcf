#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import errno
import time

from indelvcf.logging_config import LogConf

# global configuration
import indelvcf.glv as glv

import subprocess as sbp
import pandas as pd

import indelvcf.utils as utl
from indelvcf.logging_config import LogConf


class RefFasta(object):

    def __init__(self):

        pass

    def open_log(self):

        global log
        log = LogConf.open_log(__name__)


    def prepare_ref(self):

        # user's fasta: convert relative path to absolute path based on cwd
        if glv.conf.ref.startswith('/'):
            # originally absolute path
            glv.conf.ref_fasta_user = glv.conf.ref
        else:
            # cwd + relative path
            glv.conf.ref_fasta_user = "{}/{}".format(
                glv.conf.cwd, glv.conf.ref)

        log.info("glv.conf.ref_fasta_user {}".format(glv.conf.ref_fasta_user))

        # ref_fasta_user: existence confirmation
        if os.path.isfile(glv.conf.ref_fasta_user):
            log.info("{} found.".format(glv.conf.ref_fasta_user))
        else:
            log.info("{} not found. exit.".format(glv.conf.ref_fasta_user))
            sys.exit(1)
            
        # ext, basename, without_ext
        # https://note.nkmk.me/python-os-basename-dirname-split-splitext/
        basename_user = os.path.basename(glv.conf.ref_fasta_user)
        root_ext_pair = os.path.splitext(glv.conf.ref_fasta_user)
        without_ext = root_ext_pair[0]
        basename_without_ext = os.path.basename(without_ext)
        ext = root_ext_pair[1]

        # ref_fasta_slink_system
        # make symlink user's fasta to sys_ref_dir as .org(.gz)
        if ext != '.gz':
            glv.conf.ref_fasta_slink_system = "{}/{}{}".format(
                glv.conf.ref_dir, basename_user, '.org_slink')

            glv.conf.ref_fasta = "{}/{}".format(
                glv.conf.ref_dir, basename_user)

        else:
            glv.conf.ref_fasta_slink_system = "{}/{}{}".format(
                glv.conf.ref_dir, basename_user, '.org_slink.gz')

            glv.conf.ref_fasta = "{}/{}".format(
                glv.conf.ref_dir, basename_without_ext)


        if os.path.isfile(glv.conf.ref_fasta_slink_system):
            log.info("{} exist.".format(glv.conf.ref_fasta_slink_system))
        else:
            log.info("os.symlink {} {}.".format(
                glv.conf.ref_fasta_user, glv.conf.ref_fasta_slink_system))

            os.symlink(
                glv.conf.ref_fasta_user, glv.conf.ref_fasta_slink_system)

        log.info("ext ({}).".format(ext))


        # convert to bgz if ext is .gz and set to ref_fasta
        if ext != '.gz':
            # it should be convert to bgz in ref_dir
            glv.conf.ref_fasta = "{}/{}".format(
                glv.conf.ref_dir, basename_user)

            if os.path.isfile(glv.conf.ref_fasta):
                log.info("symlink exist {}".format(
                    glv.conf.ref_fasta))
            else:
                os.symlink(
                    glv.conf.ref_fasta_user, glv.conf.ref_fasta)
                log.info("symlink {} {}".format(
                    glv.conf.ref_fasta_user, glv.conf.ref_fasta))

        else:

            # it should be convert to bgz in ref_dir
            cmd1 = 'bgzip -cd -@ {} {} > {}'.format(
                        glv.conf.thread,
                        glv.conf.ref_fasta_slink_system,
                        glv.conf.ref_fasta)

            # execute
            if os.path.isfile(glv.conf.ref_fasta):
                log.debug("{} exist.".format(glv.conf.ref_fasta))

            else:
                log.debug("{} not exist. do cmd={}".format(
                    glv.conf.ref_fasta, cmd1))

                utl.try_exec(cmd1)

 
        # make fai file
        cmd2 = 'samtools faidx {}'.format(
            glv.conf.ref_fasta, glv.conf.log_dir)

        glv.conf.ref_fasta_fai = "{}{}".format(glv.conf.ref_fasta, '.fai')

        if os.path.isfile(glv.conf.ref_fasta_fai):
            log.debug("{} exist.".format(glv.conf.ref_fasta_fai))

        else:
            log.debug("{} not exist. do {}".format(
                glv.conf.ref_fasta_fai, cmd2))
            utl.try_exec(cmd2)

        # ref to makeblastdb
        self._make_bwaidx()

        return self


    def _make_bwaidx(self):

        bwaidx = "{}{}".format(glv.conf.ref_fasta, '.bwt')
        bwaidx_title = os.path.basename(glv.conf.ref_fasta)

        if os.path.isfile(bwaidx):
            log.debug("{} exist.".format(bwaidx))

        else:
            os.chdir(glv.conf.ref_dir)
            cmd1 = "bwa index -p {} {}".format(
                bwaidx_title, glv.conf.ref_fasta)
            utl.try_exec(cmd1)

        log.info("pwd {}".format(os.getcwd()))
        os.chdir(glv.conf.cwd)


