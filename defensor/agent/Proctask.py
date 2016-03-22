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
from defensor.agent.Template import conf_template

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
CONF_PROCTASK_URL_DEFAULT = "/proctask/%s"
CONF_PROCTASK_TIME_DEFAULT = 30

CONF_GOD_ETC_DIR = "/etc/god/"


##############################################################################
# 
# Thread entry program seted in Agent.py from here
#
##############################################################################
def proctask():
    pool = eventlet.GreenPool()

    interval = CONF.getint("interval", "proctask_time")
    if not interval:
        interval = CONF_PROCTASK_TIME_DEFAULT

    LOG.debug("Begin proctask thread,cycletime is %ss" %interval)
    task  = PeriodTask("proctask", interval)
    task.set_fun(period_run, pool)
    task.run()

def period_run(pool):
    _proctask(pool)
    pool.waitall()

##############################################################################
# 
# Real thread work program from here
#
##############################################################################
def _proctask(pool):
    try:
        data = get_tasks()
        if not data:
            LOG.warn("Proctask can't request from api host")
            return 
        
        tasks = data.get("data")
        if not tasks:
            LOG.info("Proctask have not task to do")
            return 
        
        LOG.info("Proctask start to do tasks: %s" %tasks)
        handle_tasks(tasks)

    except Exception, e:
        LOG.error(e)

def get_tasks():
    """
    Http request template:
    { 
        "hostname" : host_name,
        "data" : [{
                    "name":"apache2",
                    "cmd_start":"/etc/init.d/apache2 start",
                    "cmd_stop":"/etc/init.d/apache2 stop",
                    "cmd_restart":"/etc/init.d/apache2 restart",
                    "pid_file":"/var/run/apache2.pid"
                    },
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
        proctask_url = CONF.get("url", "proctask_url")
        if not proctask_url:
           proctask_url = CONF_PROCTASK_URL_DEFAULT 

        hostname = get_hostname()
        proctask_url = proctask_url % hostname
        
        httpcon = HttpCon(host, port, proctask_url)
        result = httpcon.get()

        return result
    except Exception, e:
        LOG.error(e)


def handle_tasks(tasks):
    for task in tasks:
        LOG.debug("God config process %s Start!" % task.get("name"))
        result = handle_task(task)
        if not result:
            LOG.error("God config process %s Failed!" % task.get("name"))
        else:
            LOG.info("God config process %s Success!" % task.get("name"))
    return True


def handle_task(task):
    try:
        proc_name, conf_file = build_god_conf(task)
        file_path = write_god_conf(proc_name, conf_file)
        god_reload_conf(file_path)
        return True
    except Exception, e:
        LOG.error(e)

def build_god_conf(task):
    try:
        process_name = task.get("name")
        cmd_start = task.get("cmd_start")
        cmd_stop = task.get("cmd_stop")
        cmd_restart = task.get("cmd_restart")
        pid_file = task.get("pid_file")

        god_conf = conf_template % (process_name, cmd_start, cmd_stop, \
                                cmd_restart, pid_file)

        return process_name, god_conf
    except Exception, e:
        LOG.error(e)

def write_god_conf(filename, file_data):
    try:
        god_dir = CONF.get("god", "etc_dir")
        if not god_dir:    
            god_dir = CONF_GOD_ETC_DIR

        filename = filename + ".god"
        file_full_name = os.path.join(god_dir, filename)
    
        _file = file(file_full_name, "w")
        _file.write(file_data)
        _file.close()
        return file_full_name
    except Exception, e:
        LOG.error(e)

def god_reload_conf(filename):
    try:
        cmd = "/usr/local/bin/god load %s" %filename
        execute_cmd(cmd)
    except Exception, e:
        LOG.error(e)
