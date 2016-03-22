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
import logging 
import logging.handlers

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.common.DfsConfig import DfsConfig

##############################################################################
# 
# Set LOG and CONF from here
#
##############################################################################
CONF = DfsConfig()

CONF_LOG_DEBUG_DEFAULT = "False"

def log_set_up(logname):

    log_level_conf = CONF.get("log", "debug")
    if not log_level_conf:
        log_level_conf = CONF_LOG_DEBUG_DEFAULT

    if "True" == log_level_conf:
        log_level =  logging.DEBUG
    elif "False" == log_level_conf:
        log_level =  logging.INFO
    else:
        log_level =  logging.INFO


    logging.basicConfig(filename = logname,
                        level = log_level, 
                        format = '%(asctime)s %(name)\
                        -30s %(levelname)-8s %(message)s', 
                        datefmt = '%m-%d %H:%M') 
    console = logging.StreamHandler()  
    
    console.setLevel(log_level) 
    logging.getLogger('').addHandler(console)  

    #filehandler = logging.handlers.TimedRotatingFileHandler(
    #                logname, 'M', 1, 0)
    #filehandler.suffix = "%Y%m%d-%H%M.log"
    #logging.getLogger('').addHandler(filehandler)


