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
import sys
import time 
import threading
import logging
import ConfigParser

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.common.DfsConfig import DfsConfig
from defensor.agent.Register import register
from defensor.agent.Dbsync import dbsync
from defensor.agent.Proctask import proctask
from defensor.agent.Action import action
from defensor.agent.Report import report
from defensor.agent.Heartbeat import heartbeat

##############################################################################
# 
# Set LOG and CONF from here
#
##############################################################################
LOG = logging.getLogger(__name__)
CONF = DfsConfig()

##############################################################################
# 
# Set config value default from here
#
##############################################################################
 

def start_dbsync_thread():
    LOG.debug("start dbsync thread")
    dbsync_thread =threading.Thread(target = dbsync, name = "dbsync")
    dbsync_thread.setDaemon(True)
    dbsync_thread.start()


def start_proctask_thread():
    LOG.debug("start proctask thread!")
    proctask_thread =threading.Thread(target = proctask, 
                                      name = "proctask")
    proctask_thread.setDaemon(True)
    proctask_thread.start()

def start_action_thread():
    LOG.debug("start action thread!")    
    action_thread =threading.Thread(target = action, name = "action")
    action_thread.setDaemon(True)
    action_thread.start()

def start_report_thread():
    LOG.debug("start report thread!")    
    report_thread =threading.Thread(target = report, name = "report")
    report_thread.setDaemon(True)
    report_thread.start()

def start_heartbeat_thread():
    LOG.debug("start heartbeat thread!")    
    heartbeat_thread =threading.Thread(target = heartbeat, name = "heartbeat")
    heartbeat_thread.setDaemon(True)
    heartbeat_thread.start()
    

##############################################################################
# 
# Project Agent service start program from here
#
##############################################################################
def start():
    LOG.info("Defensor Agent Is Starting!")
    CONF.print_conf()

    #register agent from here
    while(not register()):
        LOG.error("Register to api host failed, service will retry after 5s!")
        time.sleep(5) 

    #start all threads from here
    start_dbsync_thread()
    start_proctask_thread()
    start_action_thread()
    start_report_thread()
    start_heartbeat_thread()

    while True:
        time.sleep(1)

