# -*- coding: utf-8 -*-

import sys
import os
import errno
import re

# global variants
import indelvcf.glv as glv
import indelvcf.utils as utl

# https://qiita.com/mimitaro/items/3506a444f325c6f980b2
import configparser
# https://docs.python.org/ja/3/library/configparser.html

# class
from indelvcf.param import Param
from indelvcf.logging_config import LogConf

class Conf(object):

    def __init__(self):

        self.init_version = 0.0

        self.ini_file = ''
        self.ini_file_path = ''
        self.ini = configparser.ConfigParser()
        # don't convert to lower case
        self.ini.optionxform = str

        # log
        self.log = LogConf()

        self.region_bed_list = list()
        self.bam_list = list()

        self.cwd = os.getcwd()

        self.ref_dir = ''
        self.log_dir = ''
        self.out_dir = ''
        self.out_bak_dir = ''

        # ------------------------
        self.ref_fasta = ''
        self.ref_fasta_chrom_list = ''
        self.ref_fasta_fai = ''
        self.ref_fasta_pickle = ''
        self.ref_fasta_slink_system = ''
        self.ref_fasta_user = ''

        # svaba
        self.svaba_normalize_bams_list = list()

        self.progress = ''
        self.stop = 'no'

        # -------------------------
        self.init_version = 0.0
        self.heterozygosity = ''
        self.thread = 0
        self.bams = ''
        self.bams_txt = ''
        self.region_bed = ''
        self.ref = ''
        self.progress = ''
        self.mpl_mpileup_param = ''
        self.mpl_call_param = ''
        self.mpl_filter_param = ''
        self.snpf_DP = 0
        self.snpf_FREQ = 0.0
        self.snpf_view1_param = ''
        self.snpf_annotate_param = ''
        self.snpf_view2_param = ''
        self.svb_normalize_bam = ''
        self.svb_normalize_bam_txt = ''
        self.svb_svaba_param = ''
        self.indf_DP = 0
        self.indf_FREQ = 0.0
        self.indf_view1_param = ''
        self.indf_annotate_param = ''
        self.indf_norm_param = ''
        self.indf_view2_param = ''
        self.concat_nh_param = ''
        self.concat_nh_view_param = ''
        self.concat_hetero_param = ''


    def read_ini(self):

        # ---------------------------------------------------------------
        # ini_file from param.p['config'] absolute or relative path
        self.ini_file = glv.param.p.config
        print("ini_file = {}".format(self.ini_file))
        # ---------------------------------------------------------------

        # ini_file_path
        self.ini_file_path = "{}/{}".format(
            self.cwd, self.ini_file)
        print("self.ini_file_path = {}".format(self.ini_file_path))

        # read ini_file
        if os.path.exists(self.ini_file_path):
            print("found {}".format(self.ini_file_path))

            # https://docs.python.org/ja/3/library/configparser.html
            with open(self.ini_file_path, encoding='utf-8') as fp:
                self.ini.read_file(fp)

                # adjustment of variable format
                self._rectify_variable()
                #
                self._ini_into_variable()

                # several path and logging start
                self._set_path_and_all_start()


                # 1) region_bed
                self._read_region_bed()
                # 2) bams
                self._read_bams()
                # 3) svaba normalize bam
                self._read_normalize_bams()
                # 4) hetero
                self._rectify_hetero()
                # 5) merge
                self._merge_conf()
                # 6) log all conf
                self._print_conf()

        else:
            print("Not found {}, exit.".format(self.ini_file_path))
            #raise FileNotFoundError(errno.ENOENT,
            #    os.strerror(errno.ENOENT),
            #    self.ini_file_path)
            sys.exit(1)

        return self

    def _print_conf(self):

        log.info("")
        log.info("Adopted configurations:")

        log.info("[global]")
        log.info("init_version={}".format(self.init_version))
        log.info("heterozygosity={}".format(self.heterozygosity))
        log.info("thread={}".format(self.thread))
        log.info("bams={}".format(self.bams))
        log.info("bams_txt={}".format(self.bams_txt))
        log.info("region_bed={}".format(self.region_bed))
        log.info("ref={}".format(self.ref))

        log.info("ref_dir={}".format(self.ref_dir))
        log.info("log_dir={}".format(self.log_dir))
        log.info("out_dir={}".format(self.out_dir))

        log.info("progress={}".format(self.progress))
        log.info("<stop={}>".format(self.stop))

        log.info("[mpileup]")
        log.info("mpl_mpileup_param={}".format(self.mpl_mpileup_param))
        log.info("mpl_call_param={}".format(self.mpl_call_param))
        log.info("mpl_filter_param={}".format(self.mpl_filter_param))

        log.info("[snpfilter]")
        log.info("snpf_DP={}".format(self.snpf_DP))
        log.info("snpf_FREQ={}".format(self.snpf_FREQ))

        log.info("snpf_view1_param={}".format(self.snpf_view1_param))
        log.info("snpf_annotate_param={}".format(self.snpf_annotate_param))
        log.info("snpf_view2_param={}".format(self.snpf_view2_param))

        log.info("[svaba]")
        log.info("svb_normalize_bam={}".format(self.svb_normalize_bam))
        log.info("svb_normalize_bam_txt={}".format(
            self.svb_normalize_bam_txt))
        log.info("svb_svaba_param={}".format(self.svb_svaba_param))

        log.info("[indelfilter]")
        log.info("indf_DP={}".format(self.indf_DP))
        log.info("indf_FREQ={}".format(self.indf_FREQ))
        log.info("indf_view1_param={}".format(self.indf_view1_param))
        log.info("indf_annotate_param={}".format(self.indf_annotate_param))
        log.info("indf_norm_param={}".format(self.indf_norm_param))
        log.info("indf_view2_param={}".format(self.indf_view2_param))

        log.info("[concat]")
        log.info("concat_nh_param={}".format(self.concat_nh_param))
        log.info("concat_nh_view_param={}".format(self.concat_nh_view_param))
        log.info("concat_hetero_param={}".format(self.concat_hetero_param))

        log.info("")


    def _ini_into_variable(self):

        sect = 'global'

        self.init_version = \
            float(self._set_default(sect, 'init_version', 1.0))
        self.heterozygosity = \
            str(self._set_default(sect, 'heterozygosity', 'homo'))
        self.thread = \
            int(self._set_default(sect, 'thread', 2))
        self.bams = \
            str(self._set_default(sect, 'bams', ''))
        self.bams_txt = \
            str(self._set_default(sect, 'bams_txt', ''))
        self.region_bed = \
            str(self._set_default(sect, 'region_bed', ''))
        self.ref = \
            str(self._set_default(sect, 'ref', ''))
        self.progress = \
            str(self._set_default(sect, 'progress', 'all'))

        self.ref_dir = \
            str(self._set_default(sect, 'ref_dir', 'refs'))
        self.log_dir = \
            str(self._set_default(sect, 'log_dir', 'logs'))
        self.out_dir = \
            str(self._set_default(sect, 'out_dir', 'out_dir'))
        self.out_bak_dir = ''

        sect = 'mpileup'

        self.mpl_mpileup_param = \
            utl.clp(str(self._set_default(sect, 'mpl_mpileup_param', '')))
        self.mpl_call_param = \
            utl.clp(str(self._set_default(sect, 'mpl_call_param', '')))
        self.mpl_filter_param = \
            utl.clp(str(self._set_default(sect, 'mpl_filter_param', '')))

        sect = 'snpfilter'

        self.snpf_DP = \
            int(self._set_default(sect, 'snpf_DP', 5))
        self.snpf_FREQ = \
            float(self._set_default(sect, 'snpf_FREQ', 0.5))
        self.snpf_view1_param = \
            utl.clp(str(self._set_default(sect, 'snpf_view1_param', '')))
        self.snpf_annotate_param = \
            utl.clp(str(self._set_default(sect, 'snpf_annotate_param', '')))
        self.snpf_view2_param = \
            utl.clp(str(self._set_default(sect, 'snpf_view2_param', '')))

        sect = 'svaba'

        self.svb_normalize_bam = \
            str(self._set_default(sect, 'svb_normalize_bam', ''))
        self.svb_normalize_bam_txt = \
            str(self._set_default(sect, 'svb_normalize_bam_txt', ''))
        self.svb_svaba_param = \
            utl.clp(str(self._set_default(sect, 'svb_svaba_param', '')))

        sect = 'indelfilter'
        self.indf_DP = \
            int(self._set_default(sect, 'indf_DP', 5))
        self.indf_FREQ = \
            float(self._set_default(sect, 'indf_FREQ', 0.5))
        self.indf_view1_param = \
            utl.clp(str(self._set_default(sect, 'indf_view1_param', '')))
        self.indf_annotate_param = \
            utl.clp(str(self._set_default(sect, 'indf_annotate_param', '')))
        self.indf_norm_param = \
            utl.clp(str(self._set_default(sect, 'indf_norm_param', '')))
        self.indf_view2_param = \
            utl.clp(str(self._set_default(sect, 'indf_view2_param', '')))

        sect = 'concat'

        self.concat_nh_param = \
            utl.clp(str(self._set_default(sect, 'concat_nh_param', '')))
        self.concat_nh_view_param = \
            utl.clp(str(self._set_default(sect, 'concat_nh_view_param', '')))
        self.concat_hetero_param = \
            utl.clp(str(self._set_default(sect, 'concat_hetero_param', '')))



    def _rectify_hetero(self):

        if self.heterozygosity != 'homo':
            self.heterozygosity = 'hetero'
        else:
            self.heterozygosity = 'homo'


    def _read_region_bed(self):

        # 指定がなければ全部
        self.region_bed_list = list()

        if self.region_bed != '':
            if not os.path.exists(self.region_bed):
                log.error("{} not found, exit.".format(self.region_bed))
                sys.exit(1)

            with open(self.region_bed, mode='r') as r:
                for liner in r:
                    r_line = liner.strip()
                    r_line = utl.strip_hash_comment(r_line)
                    if r_line == '':
                        continue

                    region_list = r_line.split('\t')
                    region_line = region_list[0]

                    if len(region_list) > 2:
                        region_line = "{}:{}-{}".format(
                            region_list[0],
                            region_list[1],
                            region_list[2])

                    self.region_bed_list.append(region_line)


    def _read_normalize_bams(self):

        # normalize_bam =
        # normalize_bam_txt = data/yam_96F1_bam.txt

        if self.svb_normalize_bam != '':
            svaba_norm_bams_line = self.svb_normalize_bam

            svaba_norm_bams_line = re.sub(r";+", ",", svaba_norm_bams_line)
            svaba_norm_bams_line = re.sub(r"\s+", ",", svaba_norm_bams_line)
            svaba_norm_bams_line = re.sub(r",+", ",", svaba_norm_bams_line)

            self.svaba_normalize_bams_list = svaba_norm_bams_line.split(',')

        else:
            if self.svb_normalize_bam_txt == '':
                return

            normalize_bam_txt = self.svb_normalize_bam_txt
            if not os.path.exists(normalize_bam_txt):
                log.error("{} not found, exit.".format(normalize_bam_txt))
                sys.exit(1)

            with open(normalize_bam_txt, mode='r') as r:
                for liner in r:
                    r_line = liner.strip()
                    r_line = utl.strip_hash_comment(r_line)
                    if r_line == '':
                        continue
                    self.svaba_normalize_bams_list.append(r_line)

        log.debug("{}".format(self.svaba_normalize_bams_list))


    def _read_bams(self):

        # set to self.bam_list
        if self.bams != '':
            bams_line = self.bams

            bams_line = re.sub(r";+", ",", bams_line)
            bams_line = re.sub(r"\s+", ",", bams_line)
            bams_line = re.sub(r",+", ",", bams_line)

            self.bam_list = bams_line.split(',')

        else:
            bams_txt = self.bams_txt
            if not os.path.exists(bams_txt):
                log.error("{} not found, exit.".format(bams_txt))
                sys.exit(1)

            with open(bams_txt, mode='r') as r:
                for liner in r:
                    r_line = liner.strip()
                    r_line = utl.strip_hash_comment(r_line)
                    if r_line == '':
                        continue
                    self.bam_list.append(r_line)

        #log.debug("{}".format(self.bam_list))

    def _set_default(self, sect, key, value):

        if key in self.ini[sect]:
            return self.ini[sect][key]
        else:
            return value


    def _merge_conf(self):

        # update by param

        if glv.param.p.thread != None:
            glv.conf.thread = glv.param.p.thread

        if glv.param.p.ref != None:
            glv.conf.ref = glv.param.p.ref

        if glv.param.p.hetero != None:
            glv.conf.heterozygosity = glv.param.p.hetero

        if glv.param.p.progress != None:
            glv.conf.progress = glv.param.p.progress

        if glv.param.p.stop != None:
            glv.conf.stop = glv.param.p.stop

        log.info("glv.param.p={}".format(glv.param.p))

        return self


    def _set_path_and_all_start(self):

        #---------------------------------------------------
        # out_dir
        if glv.param.p.out_dir != None:
            self.out_dir = glv.param.p.out_dir

        # result out dir
        self.out_dir =  "{}/{}".format(self.cwd, self.out_dir)

        # logs dir under out dir
        self.log_dir = "{}/{}".format(self.out_dir, self.log_dir)

        # system reference dir
        self.ref_dir = "{}/{}".format(self.cwd, self.ref_dir)

        # out_bak_dir
        self.out_bak_dir =  "{}/{}".format(self.out_dir, 'bak')

        # make dir
        self._make_dir_tree()

        # set to LogConf
        global log
        log = self.log.conf_log_start(__name__, self.out_dir, self.log_dir)

        # log for utils
        utl.start_log()

        # cp ini file to outdir
        self._copy_ini_file()


    def _copy_ini_file(self):

        # ini file
        self.ini_file_path
        # out_dir
        self.out_dir

        # back up
        ini_base = os.path.basename(self.ini_file_path)
        out_dir_ini_file = "{}/{}".format(self.out_dir, ini_base)
        utl.save_to_tmpfile(out_dir_ini_file)

        cmd = "cp {} {}".format(self.ini_file_path, out_dir_ini_file)
        utl.try_exec(cmd)


    def _make_dir_tree(self):

        # already made at conf
        dirs = [
            self.out_dir,
            self.log_dir,
            self.out_bak_dir,
            self.ref_dir,
        ]

        for dir in dirs:
            os.makedirs(dir, exist_ok=True) # refs


    def _rectify_variable(self):

        for section in self.ini.sections():
            for key in self.ini[section]:

                val = self.ini[section][key]
                # hash comment remove
                val = utl.strip_hash_comment(val)

                # remove \n at the beginning of value
                val = val.lstrip()

                # replace internal \n to semicolons
                val = val.replace('\n', ';')

                # replace white space to one space
                val = re.sub(r"\s+", " ", val)

                # reset
                self.ini[section][key] = val



