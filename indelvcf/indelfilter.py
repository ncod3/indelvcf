# -*- coding: utf-8 -*-

import sys
import os
import errno
import time
import re
import gzip

from indelvcf.logging_config import LogConf
log = LogConf.open_log(__name__)

# global configuration
import indelvcf.glv as glv
import indelvcf.utils as utl


class IndelFilter(object):

    def __init__(self):

        pass

    def run(self):

        mod_name = 'indelfilter'
        out_dir = utl.mk_outdir(mod_name)
        heterozygosity = glv.conf.heterozygosity

        # continue to next phase
        glv.outlist.outfile[mod_name] = list()

        start = time.time()

        # for each region
        for (input_file, region) in zip(
                glv.outlist.outfile['svaba'],
                glv.conf.region_bed_list):

            # for sbava debug
            input_base_gz = os.path.basename(input_file)
            input_base = re.sub(r"\.gz$", "", input_base_gz)
            out_file0 = "{}/{}".format(out_dir, input_base)
            out_file0_gz = "{}/{}".format(out_dir, input_base_gz)

            out_file1 = "{}/{}_{}.{}{}".format(
                out_dir, mod_name, region, 'annote', '.vcf.gz')
            out_file2 = "{}/{}_{}.{}{}".format(
                out_dir, mod_name, region, 'norm', '.vcf.gz')
            out_file3 = "{}/{}_{}.{}{}".format(
                out_dir, mod_name, region, 'homo', '.vcf.gz')

            if heterozygosity == 'homo':
                glv.outlist.outfile[mod_name].append(out_file3)
            else:
                glv.outlist.outfile[mod_name].append(out_file2)

            if utl.progress_check(mod_name) == False:
                log.info("progress={} so skip {}.".format(
                    glv.conf.progress,
                    mod_name))
                continue

            log.info("go on {}".format(mod_name))

            # for svaba bug
            with open(out_file0, mode='w') as f:
                with gzip.open(input_file, "rt") as fi:
                    for liner in fi:
                        r_line = liner.strip()
                        if r_line.startswith('#'):
                            f.write("{}\n".format(r_line))
                        else:
                            w_line = list()
                            for col_n, item in enumerate(r_line.split('\t')):
                                if col_n <= 8:
                                    w_line += [item]
                                else:
                                    if '/' in item:
                                        w_line += [item]
                            f.write("{}\n".format('\t'.join(w_line)))

            utl.save_to_tmpfile(out_file0_gz)

            cmd1 = "bgzip -@ {} {}".format(
                glv.conf.thread,
                out_file0)

            utl.try_exec(cmd1)
            utl.tabix(out_file0_gz)

            input_valid_vcf = "{}/{}".format(out_dir, input_base_gz)

            view1 = '{} {} {} -O v -r {} {}'
            v1_cmd = view1.format(
                'bcftools',
                'view',
                glv.conf.indf_view1_param,
                region,
                input_valid_vcf)

            pipe_annotate = '{} {} {} -O z --threads {} -o {}'
            # use threads only -O z|b
            an_cmd = pipe_annotate.format(
                'bcftools',
                'annotate',
                glv.conf.indf_annotate_param,
                glv.conf.thread,
                out_file1)

            cmd1 = '{} | {}'.format(v1_cmd, an_cmd)
            utl.try_exec(cmd1)
            utl.tabix(out_file1)

            norm = '{} {} {} -O z --threads {} -f {} -o {} {}'
            # use threads only -O z|b
            cmd2 = norm.format(
                'bcftools',
                'norm',
                glv.conf.indf_norm_param,
                glv.conf.thread,
                glv.conf.ref_fasta,
                out_file2,
                out_file1)

            utl.try_exec(cmd2)
            utl.tabix(out_file2)

            tabix1 = "{}.tbi".format(out_file1)
            os.remove(out_file1)
            os.remove(tabix1)
            log.info("remove {} {}".format(out_file1, tabix1))

            #-------------------------
            if heterozygosity != 'homo':
                continue

            view2 = '{} {} {} -O z --threads {} -r {} -o {} {}'
            cmd3 = view2.format(
                'bcftools',
                'view',
                glv.conf.indf_view2_param,
                glv.conf.thread,
                region,
                out_file3,
                out_file2)

            #utl.save_to_tmpfile(out_file3)
            utl.try_exec(cmd3)
            utl.tabix(out_file3)

            tabix2 = "{}.tbi".format(out_file2)
            os.remove(out_file2)
            os.remove(tabix2)

            log.info("remove {} {}".format(out_file2, tabix2))

        log.info("indelfilter finished {}".format(
            utl.elapsed_time(time.time(), start)))


