#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import errno
import time
import datetime

# global variables
import indelvcf.glv as glv
import indelvcf.utils as utl
from indelvcf.logging_config import LogConf

#--- read dir and log file set
glv.init('indelvcf')
log = LogConf.open_log(__name__)
log.info("logging start {}".format(__name__))

# using class
from indelvcf.mpileup import Mpileup
from indelvcf.snpfilter import SnpFilter
from indelvcf.svaba import Svaba
from indelvcf.indelfilter import IndelFilter
from indelvcf.concat import Concat


def main():

    start = time.time()
    log.info('program started')

    # run
    isnp = IndelSnp()
    isnp.run()

    log.info("program finished {}".format(
        utl.elapsed_time(time.time(), start)))


class IndelSnp(object):

    def __init__(self):

        self.mpileup = Mpileup()
        self.snpfilter = SnpFilter()
        self.svaba = Svaba()
        self.indelfilter = IndelFilter()
        self.concat = Concat()

    def run(self):

        # prepare
        self.prepare()
        utl.stop('prepare')

        # 1 bcftools mpileup
        self.mpileup.run()
        utl.stop('mpileup')

        # 2 snpfilter
        self.snpfilter.run()
        utl.stop('snpfilter')

        # 3 svaba
        self.svaba.run()
        utl.stop('svaba')

        # 4 indelfilter
        self.indelfilter.run()
        utl.stop('indelfilter')

        # 5 concat
        self.concat.run()


    def prepare(self):

        # read reference into global environment
        glv.ref = glv.ref.prepare_ref()


if __name__ == '__main__':
    main()

