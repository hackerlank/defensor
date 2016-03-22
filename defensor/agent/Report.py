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
CONF_REPORT_URL_DEFAULT = "/report/%s"
CONF_REPORT_TIME_DEFAULT = 30

##############################################################################
# 
# Thread entry program seted in Agent.py from here
#
##############################################################################
def report():
    pool = eventlet.GreenPool()

    interval = CONF.getint("interval", "report_time")
    if not interval:
        interval = CONF_REPORT_TIME_DEFAULT
    
    LOG.debug("Begin report thread,cycletime is %ss" %interval)
    task  = PeriodTask("report", interval)
    task.set_fun(period_run, pool)
    task.run()

def period_run(pool):
    _report(pool)
    pool.waitall()

##############################################################################
# 
# Real thread work program from here
#
##############################################################################
def _report(pool):
    result = get_status()
    LOG.info("Report data: %s" %result)
    send_request(result)

def get_status():
    try:
        cmd = "/usr/local/bin/god status" 
        result = execute_cmd(cmd)

        status = parse_data(result)
        return status
    except Exception, e:
        LOG.error(e)

def parse_data(data):
    try:
        status = []
        if not data:
            return status
        if "The server is not available" in data:
            LOG.warn("God process is not running")
            return status

        data = data.split('\n')[:-1]
        for line in data:
            list_items=line.strip('\n').split(':')
            proc_name = list_items[0].strip()
            proc_status = list_items[1].strip()
            dict_item = {"proc_name":proc_name,"status":proc_status}
            status.append(dict_item)
        LOG.debug("Parse report data %s" % status)
        return status
    except Exception, e:
        LOG.error(e)

def send_request(data):
    """
    Http request template:
    { 
        "hostname"  : "host_name",
        "data"      : [{'proc_name': 'apache2', 'status': 'unmonitored'},]
    }
    """
    try:
        host = CONF.get("api", "host")
        if not host:    
            host = CONF_HOST_DEFAULT
        port = CONF.getint("api", "port")
        if not port:
            port = CONF_PORT_DEFAULT
        report_url = CONF.get("url", "report_url")
        if not report_url:
           report_url = CONF_REPORT_URL_DEFAULT 

        hostname = get_hostname()
        report_url = report_url % hostname
        
        body = {
                "hostname":hostname,
                "data": data,
                }

        httpcon = HttpCon(host, port, report_url)
        httpcon.post(body)

    except Exception, e:
        LOG.error(e)
    