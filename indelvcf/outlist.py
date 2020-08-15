# -*- coding: utf-8 -*-

import sys
import os
import errno
import time

from indelvcf.logging_config import LogConf

# global configuration
import indelvcf.glv as glv
import indelvcf.utils as utl

from indelvcf.logging_config import LogConf


class OutList(object):

    def __init__(self):

        self.outf_prefix = {
            'prepare'       : {'no': 5, 'dn': ''},
            'mpileup'       : {'no': 10, 'dn': '010_mpileup'},
            'snpfilter'     : {'no': 20, 'dn': '020_snpfilter'},
            'svaba'         : {'no': 30, 'dn': '030_svaba'},
            'indelfilter'   : {'no': 40, 'dn': '040_indelfilter'},
            'concat'        : {'no': 50, 'dn': '050_concat'},
        }

        self.outfile = dict()


    def open_log(self):

        global log
        log = LogConf.open_log(__name__)


