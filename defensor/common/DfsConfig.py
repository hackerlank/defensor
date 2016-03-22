# -*- coding: utf-8 -*-
##############################################################################
# 
# Project   : Defensor
# Author    : Yy
# Email     : yangwanyuan@ztgame.com
# Date      : 2015.11 
#
##############################################################################

##############################################################################
# 
# Import system library from here
#
##############################################################################
import ConfigParser
import logging 

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.common.DfsSingleton import singleton

##############################################################################
# 
# Set LOG and CONF from here
#
##############################################################################
LOG = logging.getLogger(__name__)


@singleton
class DfsConfig(object):
    _filename = None
    _conf = None

    def __init__(self):
        pass

    def init_config(self, file_name):
        self._filename = file_name
        try:
            self._conf = ConfigParser.ConfigParser()
            self._conf.read(self._filename)
        except Exception, e: 
            LOG.error(e)

    def print_conf(self):
        LOG.info("="*60)
        LOG.info("Load conf file!")
        LOG.info("="*60)
        for sec in self.sections():
            for opt in self.options(sec):
                item = self.get(sec, opt)
                LOG.info("%-30s = %-30s" %(opt, item))

        LOG.info("="*60)
        LOG.info("Load conf file Success!")
        LOG.info("="*60)


    def sections(self):
        try:
            result = self._conf.sections()
            return result
        except Exception, e:
            LOG.error(e)
            return None


    def options(self, sec):
        try:
            result = self._conf.options(sec)
            return result
        except Exception, e:
            LOG.error(e)
            return None



    def items(self, sec):
        try:
            result = self._conf.items(sec)
            return result
        except Exception, e:
            LOG.error(e)
            return None


    def get(self, sec, opt):
        try:
            result = self._conf.get(sec, opt)
            return result
        except Exception, e:
            LOG.error(e)
            return None


    def getint(self, sec, opt):
        try:
            result = self._conf.getint(sec, opt)
            return result
        except Exception, e:
            LOG.error(e)
            return None



