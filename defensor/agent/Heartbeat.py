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
import eventlet
import logging 
import time

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.agent.Common import PeriodTask
from defensor.agent.Common import HttpCon
from defensor.agent.Common import get_hostname
from defensor.agent.Common import execute_cmd
from defensor.common.DfsConfig import DfsConfig

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
CONF_HOST_DEFAULT = "127.0.0.1"
CONF_PORT_DEFAULT = "8181"
CONF_HEARTBEAT_URL_DEFAULT = "/heartbeat/%s"
CONF_HEARTBEAT_TIME_DEFAULT = 60

##############################################################################
# 
# Thread entry program seted in Agent.py from here
#
##############################################################################
def heartbeat():
    pool = eventlet.GreenPool()

    interval = CONF.getint("interval", "heartbeat_time")
    if not interval:
        interval = CONF_HEARTBEAT_TIME_DEFAULT

    LOG.debug("Begin heartbeat thread,cycletime is %ss" %interval)
    task  = PeriodTask("heartbeat", interval)
    task.set_fun(period_run, pool)
    task.run()

def period_run(pool):
    _heartbeat(pool)
    pool.waitall()

##############################################################################
# 
# Real thread work program from here
#
##############################################################################
def _heartbeat(pool):
    result = get_time()
    if not result:
        LOG.warn("Heartbeat can not get time")
        return
    LOG.info("Heartbeat time: %s" %result)
    send_request(result)

def get_time():
    try:
        data = time.ctime()
        return data
    except Exception, e:
        LOG.error(e)

def send_request(data):
    """
    Http request template:
    { 
        "hostname"  : "host_name",
        "data"      : 10000.0
    }
    """
    try:
        host = CONF.get("api", "host")
        if not host:    
            host = CONF_HOST_DEFAULT
        port = CONF.getint("api", "port")
        if not port:
            port = CONF_PORT_DEFAULT
        heartbeat_url = CONF.get("url", "heartbeat_url")
        if not heartbeat_url:
           heartbeat_url = CONF_HEARTBEAT_URL_DEFAULT 

        hostname = get_hostname()
        heartbeat_url = heartbeat_url % hostname
        
        body = {
                "hostname":hostname,
                "data": data,
                }

        httpcon = HttpCon(host, port, heartbeat_url)
        httpcon.post(body)

    except Exception, e:
        LOG.error(e)
