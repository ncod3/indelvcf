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


class SnpFilter(object):

    def __init__(self):

        pass

    def run(self):

        mod_name = 'snpfilter'
        out_dir = utl.mk_outdir(mod_name)
        heterozygosity = glv.conf.heterozygosity

        # continue to next phase
        glv.outlist.outfile[mod_name] = list()

        start = time.time()

        # for each region
        for (input_file, region) in zip(
                glv.outlist.outfile['mpileup'],
                glv.conf.region_bed_list):

            out_file1 = "{}/{}_{}.{}{}".format(
                out_dir, mod_name, region, 'annote', '.vcf.gz')
            out_file2 = "{}/{}_{}.{}{}".format(
                out_dir, mod_name, region, 'homo', '.vcf.gz')

            if heterozygosity == 'homo':
                glv.outlist.outfile[mod_name].append(out_file2)
            else:
                glv.outlist.outfile[mod_name].append(out_file1)

            if utl.progress_check(mod_name) == False:
                log.info("progress={} so skip {}.".format(
                    glv.conf.progress,
                    mod_name))
                continue

            log.info("go on {}".format(mod_name))

            view1 = '{} {} {} -O v -r {} {}'
            v1_cmd = view1.format(
                'bcftools',
                'view',
                glv.conf.snpf_view1_param,
                region,
                input_file)

            pipe_annotate = '{} {} {} -O z --threads {} -o {}'
            an_cmd = pipe_annotate.format(
                'bcftools',
                'annotate',
                glv.conf.snpf_annotate_param,
                glv.conf.thread,
                out_file1)

            cmd1 = '{} | {}'.format(v1_cmd, an_cmd)

            utl.try_exec(cmd1)
            utl.tabix(out_file1)

            #-------------------------
            if heterozygosity != 'homo':
                continue

            view2 = '{} {} {} -O z --threads {} -r {} -o {} {}'
            cmd2 = view2.format(
                'bcftools',
                'view',
                glv.conf.snpf_view2_param,
                glv.conf.thread,
                region,
                out_file2,
                out_file1)

            utl.save_to_tmpfile(out_file2)

            utl.try_exec(cmd2)
            utl.tabix(out_file2)

            tabix1 = "{}.tbi".format(out_file1)
            os.remove(out_file1)
            os.remove(tabix1)
            log.info("remove {} {}".format(out_file1, tabix1))

        log.info("snpfilter finished {}".format(
            utl.elapsed_time(time.time(), start)))


