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
import os 

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
CONF_ACTION_URL_DEFAULT = "/action/%s"
CONF_ACTION_TIME_DEFAULT = 5

CONF_GOD_ETC_DIR = "/etc/god/"

##############################################################################
# 
# Thread entry program seted in Agent.py from here
#
##############################################################################
def action():
    pool = eventlet.GreenPool()

    interval = CONF.getint("interval", "action_time")
    if not interval:
        interval = CONF_ACTION_TIME_DEFAULT

    LOG.debug("Begin action thread,cycletime is %ss" %interval)
    task  = PeriodTask("action", interval)
    task.set_fun(period_run, pool)
    task.run()

def period_run(pool):
    _action(pool)
    pool.waitall()

##############################################################################
# 
# Real thread work program from here
#
##############################################################################
def _action(pool):
    try:
        data = get_tasks()
        if not data:
            LOG.warn("Action can't request from api host")
            return 
        
        tasks = data.get("data")
        if not tasks:
            LOG.info("Action have not task to do")
            return 
        
        LOG.info("Action start to do tasks: %s" %tasks)
        handle_tasks(tasks)

    except Exception, e:
        LOG.error(e)

def get_tasks():
    """
    Http request template:
    { 
        "hostname" : "host_name",
        "data" : [
                    {"name":"apache2","action":"start"},
                    {"name":"apache2","action":"stop"},
                    {"name":"apache2","action":"restart"},
                    {"name":"apache2","action":"unmonitor"},
                    {"name":"apache2","action":"monitor"},
                    {"name":"apache2","action":"remove"},
                ]
    }
    """
    try:
        host = CONF.get("api", "host")
        if not host:    
            host = CONF_HOST_DEFAULT
        port = CONF.getint("api", "port")
        if not port:
            port = CONF_PORT_DEFAULT
        action_url = CONF.get("url", "action_url")
        if not action_url:
           action_url = CONF_ACTION_URL_DEFAULT 

        hostname = get_hostname()
        action_url = action_url % hostname
        
        httpcon = HttpCon(host, port, action_url)
        result = httpcon.get()

        return result
    except Exception, e:
        LOG.error(e)

def handle_tasks(tasks):
    action_map = {
                    'start':action_start,
                    'stop':action_stop,
                    'restart':action_restart,
                    'monitor':action_monitor,
                    'unmonitor':action_unmonitor,
                    'remove':action_remove,
                }
    
    try:
        for task in tasks:
            proc_name = task.get("name")
            proc_action = task.get("action")
            result = action_map[proc_action](proc_name)
            if not result:
                LOG.error("Action %s %s Failed!" %(proc_action, proc_name))
            LOG.info("Action %s %s Success!" %(proc_action, proc_name))
    except Exception, e:
        LOG.error(e)

def action_start(procname):
    try:
        cmd = "/usr/local/bin/god start %s" %procname
        execute_cmd(cmd)
        return True
    except Exception, e:
        LOG.error(e)

def action_stop(procname):
    try:
        cmd = "/usr/local/bin/god stop %s" %procname
        execute_cmd(cmd)
        return True
    except Exception, e:
        LOG.error(e)

def action_restart(procname):
    try:
        cmd = "/usr/local/bin/god restart %s" %procname
        execute_cmd(cmd)
        return True
    except Exception, e:
        LOG.error(e)

def action_monitor(procname):
    try:
        cmd = "/usr/local/bin/god monitor %s" %procname
        execute_cmd(cmd)
        return True
    except Exception, e:
        LOG.error(e)

def action_unmonitor(procname):
    try:
        cmd = "/usr/local/bin/god unmonitor %s" %procname
        execute_cmd(cmd)
        return True
    except Exception, e:
        LOG.error(e)

def action_remove(procname):
    try:
        cmd = "/usr/local/bin/god remove %s" %procname
        execute_cmd(cmd)

        result = delete_god_conf(procname)
        if not result:
            return False
        return True
    except Exception, e:
        LOG.error(e)

def delete_god_conf(procname):
    try:
        god_dir = CONF.get("god", "etc_dir")
        if not god_dir:    
            god_dir = CONF_GOD_ETC_DIR

        filename = procname + ".god"
        file_full_name = os.path.join(god_dir, filename)
    
        cmd = "rm -f %s" %file_full_name
        execute_cmd(cmd)
        return True
    except Exception, e:
        LOG.error(e)
