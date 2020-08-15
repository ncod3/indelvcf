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


class Concat(object):

    def __init__(self):

        pass

    def run(self):

        mod_name = 'concat'
        out_dir = utl.mk_outdir(mod_name)
        heterozygosity = glv.conf.heterozygosity

        dname = os.path.basename(glv.conf.out_dir)

        out_file1 = "{}/{}.{}.{}.{}{}".format(
            out_dir, mod_name, dname, 'SNP_INDEL', heterozygosity, '.vcf.gz')

        glv.outlist.outfile[mod_name] = list()
        glv.outlist.outfile[mod_name].append(out_file1)
        log.debug("{}".format(out_file1))

        all_vcf = " ".join(
            glv.outlist.outfile['snpfilter'] + \
            glv.outlist.outfile['indelfilter'])
        log.debug("{}".format(all_vcf))

        utl.save_to_tmpfile(out_file1)

        start = time.time()

        if heterozygosity != 'hetero':

            concat_nohetero = '{} {} {} -O v {} --threads {}'
            cmd1 = concat_nohetero.format(
                'bcftools',
                'concat',
                glv.conf.concat_nh_param,
                all_vcf,
                glv.conf.thread)

            pipe_view = '{} {} {} -O z -o {}'
            cmd2 = pipe_view.format(
                'bcftools',
                'view',
                glv.conf.concat_nh_view_param,
                out_file1)

            cmd1 = "{} | {}".format(cmd1, cmd2)

        else:
            concat_hetero = '{} {} {} -O z {} --threads {} -o {}'
            cmd1 = concat_hetero.format(
                'bcftools',
                'concat',
                glv.conf.concat_hetero_param,
                all_vcf,
                glv.conf.thread,
                out_file1)

        utl.try_exec(cmd1)
        utl.tabix(out_file1)

        log.info("concat finished {}".format(
            utl.elapsed_time(time.time(), start)))

