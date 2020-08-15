# -*- coding: utf-8 -*-

import sys
import os
import errno
import time

# using class
from indelvcf.param import Param
from indelvcf.conf import Conf
from indelvcf.ref_fasta import RefFasta
from indelvcf.outlist import OutList


def init(prog_name):

    global program_name
    program_name = prog_name

    global param
    param = Param()

    global conf
    conf = Conf()

    global ref
    ref = RefFasta()

    global outlist
    outlist = OutList()

    # read parameter into global environment
    param = param.get_args()

    # read ini file into global environment
    conf = conf.read_ini()

    # open_log in glv
    param.open_log()
    ref.open_log()
    outlist.open_log()

