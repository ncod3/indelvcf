# -*- coding: utf-8 -*-

import sys
import os
import errno
import time
import re

from indelvcf.logging_config import LogConf
log = LogConf.open_log(__name__)

# global configuration
import indelvcf.glv as glv
import indelvcf.utils as utl


class Mpileup(object):

    def __init__(self):

        pass

    def run(self):

        mod_name = 'mpileup'
        out_dir = utl.mk_outdir(mod_name)

        # continue to next phase
        glv.outlist.outfile[mod_name] = list()

        start = time.time()

        # for each region
        for region in glv.conf.region_bed_list:

            out_file1 = "{}/{}_{}.{}{}".format(
                out_dir, mod_name, region, 1, '.vcf.gz')

            glv.outlist.outfile[mod_name].append(out_file1)
            log.debug("{}".format(out_file1))

            if utl.progress_check(mod_name) == False:
                log.info("progress={} so skip {}.".format(
                    glv.conf.progress,
                    mod_name))
                continue

            log.info("go on {}".format(mod_name))

            mpileup = '{} {} {} -O u -r {} -f {} {}'
            mp_cmd = mpileup.format(
                'bcftools',
                'mpileup',
                glv.conf.mpl_mpileup_param,
                region,
                glv.conf.ref_fasta,
                " ".join(glv.conf.bam_list))

            pipe_call = '{} {} {} -O u'
            ca_cmd = pipe_call.format(
                'bcftools',
                'call',
                glv.conf.mpl_call_param)

            pipe_filter = '{} {} {} -O z --threads {} -o {}'
            fi_cmd = pipe_filter.format(
                'bcftools',
                'filter',
                glv.conf.mpl_filter_param,
                glv.conf.thread,
                out_file1)

            cmd1 = "{} | {} | {}".format(mp_cmd, ca_cmd, fi_cmd)

            utl.save_to_tmpfile(out_file1)
            utl.try_exec(cmd1)
            utl.tabix(out_file1)

        log.info("mpileup finished {}".format(
            utl.elapsed_time(time.time(), start)))



