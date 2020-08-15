# -*- coding: utf-8 -*-

import sys
import os
import errno
import time

# global configuration
import indelvcf.glv as glv

import argparse
from multiprocessing import Pool
import multiprocessing as multi
from indelvcf.__init__ import __version__
from indelvcf.logging_config import LogConf


class Param(object):

    def __init__(self):
        ''' can't write log directly
        '''

    def open_log(self):

        global log
        log = LogConf.open_log(__name__)


    def get_args(self):

        parser = self._get_options()

        if len(sys.argv) == 1:
            self.p = parser.parse_args(['-h'])
        else:
            self.p = parser.parse_args()

        #log.info("{}".format(param))

        return self


    def _get_options(self):

        # https://docs.python.org/ja/3/library/argparse.html
        parser = argparse.ArgumentParser(
            description='indelvcf version {}'.format(__version__),
            formatter_class=argparse.RawTextHelpFormatter)
        parser.usage = ('indelvcf ...\n')

        # set options
        parser.add_argument('-V',
                            '--version',
                            action='version',
                            version='%(prog)s {}'.format(__version__))

        parser.add_argument('-c',
                            '--config',
                            required=True,
                            action='store',
                            default='',
                            type=str, metavar='',
                            help="required")

        parser.add_argument('-t',
                            '--thread',
                            action='store', #required=True,
                            type=str, metavar='',
                            help=".")

        parser.add_argument('-r',
                            '--ref',
                            action='store', #required=True,
                            type=str, metavar='',
                            help=".")

        parser.add_argument('-z',
                            '--hetero',
                            action='store',
                            type=str, metavar='',
                            help=".")

        parser.add_argument('-o',
                            '--out_dir',
                            action='store', #required=True,
                            type=str, metavar='',
                            help=".")

        # self.progress = ''
        parser.add_argument('-p',
                            '--progress',
                            action='store', #required=True,
                            type=str, metavar='',
                            help=".")

        parser.add_argument('-s',
                            '--stop',
                            action='store', #required=True,
                            type=str, metavar='',
                            help=".")

        return parser

