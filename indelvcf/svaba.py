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


class Svaba(object):

    def __init__(self):

        pass

    def run(self):

        mod_name = 'svaba'
        out_dir = utl.mk_outdir(mod_name)

        #        target_vcfs = [
        #    'svaba.indel.vcf', 'svaba.sv.vcf',
        #    'svaba.unfiltered.indel.vcf', 'svaba.unfiltered.sv.vcf']

        # continue to next phase
        glv.outlist.outfile[mod_name] = list()

        start = time.time()
        os.chdir(out_dir)

        for region in glv.conf.region_bed_list:

            title = "{}/indel_{}".format(out_dir, region)


            if utl.progress_check(mod_name) == False:
                log.info("progress={} so skip {}.".format(
                    glv.conf.progress,
                    mod_name))
                continue

            log.info("go on {}".format(mod_name))

            # normalize option
            norm = ''
            if len(glv.conf.svaba_normalize_bams_list) != 0:
                norm = " -n ".join(glv.conf.svaba_normalize_bams_list)
                norm = "-n " + norm

            log.debug("{}".format(norm))

            svaba = '{} {} -t {} -G {} -k {} {} -p {} {} -a {}'
            cmd1 = svaba.format(
                'svaba',
                'run',
                " -t ".join(glv.conf.bam_list),
                glv.conf.ref_fasta,
                region,
                norm,
                glv.conf.thread,
                glv.conf.svb_svaba_param,
                title)

            utl.try_exec(cmd1)

            # *.vcf
            #target_vcfs = list()
            #for fpath in glob.glob("{}*.vcf".format(out_dir)):
            #    target_vcfs.append(fpath)   
            target_vcfs = utl.check_for_files("{}/*.vcf".format(out_dir))
            log.debug("{}".format(target_vcfs))

            for t_vcf in target_vcfs:

                cmd2 = "bgzip -@ {} {}".format(
                    glv.conf.thread,
                    t_vcf)

                utl.try_exec(cmd2)
                utl.tabix("{}{}".format(t_vcf, '.gz'))

            if norm == '':
                glv.outlist.outfile[mod_name].append(
                    "{}.{}{}".format(title, 'svaba.indel.vcf', '.gz'))
            else:
                glv.outlist.outfile[mod_name].append(
                    "{}.{}{}".format(title, 'svaba.indel.vcf', '.gz'))
        
        os.chdir(glv.conf.cwd)

        log.info("svaba finished {}".format(
            utl.elapsed_time(time.time(), start)))

