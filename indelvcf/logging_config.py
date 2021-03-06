# -*- coding: utf-8 -*-

#logger.debug('debug message')
#logger.info('info message')
#logger.warning('warn message')
#logger.error('error message')
#logger.critical('critical message')

import os
import sys
import logging
import logging.config

import indelvcf.glv as glv
import indelvcf.utils as utl

class LogConf(object):

    def __init__(self):

        self.config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simpleFormatter': {
                    'format': \
'%(asctime)s %(levelname)s ' +
'%(module)s %(funcName)s %(lineno)s: %(message)s'
                }
            },
            'handlers': {
                'consoleHandler': {
                    'level': 'DEBUG',
                    'formatter': 'simpleFormatter',
                    'class': 'logging.StreamHandler',
                },
                'fileHandler': {
                    'level': 'DEBUG',
                    'formatter': 'simpleFormatter',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'logging.log',
                    'encoding': 'utf-8',
                }
            },
            'loggers': {
                '': {
                    'handlers': ['consoleHandler', 'fileHandler'],
                    'level': "DEBUG",
                }
            }
        }


    def conf_log_start(self, mod_name, out_dir, log_dir):

        file_name = '{}_log.txt'.format(glv.program_name)
        log_file_name = "{}/{}".format(log_dir, file_name)

        # for logging.config.dictConfig
        self.config['handlers']['fileHandler']['filename'] = log_file_name
        # False, before logging
        utl.save_to_tmpfile(log_file_name, False)

        # logging start
        log = LogConf.open_log(mod_name)
        log.info("Logging started at Conf.")
        return log


    @classmethod
    def open_log(cls, mod_name):

        logging.config.dictConfig(glv.conf.log.config)
        log = logging.getLogger(mod_name)
        log.info("logging start {}".format(mod_name))

        return log

