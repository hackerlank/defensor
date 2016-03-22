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
import redis
import json
import logging 

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.common.DfsConfig import DfsConfig
from defensor.common.DfsSingleton import singleton

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
CONF_REDIS_HOST_DEFAULT = "127.0.0.1"
CONF_REDIS_PORT_DEFAULT = 6379

@singleton
class RedisDriver(object):
    def __init__(self):
        pass

    def connect(self):
        try:
            redis_host = CONF.get("redis", "redis_host")
            if not redis_host:
                redis_host = CONF_REDIS_HOST_DEFAULT
            redis_port = CONF.getint("redis", "redis_port")
            if not redis_port:
                redis_port = CONF_REDIS_PORT_DEFAULT
            
            self.client = redis.Redis(host=redis_host, port=redis_port, db=0)
            self.client.ping()
            LOG.info("Redis Connect %s:%s Sucess!" %(redis_host, redis_port))
            return True
        except Exception, e:
            LOG.error(e)
            LOG.error("Redis Connect %s:%s Failed!" %(redis_host, redis_port))

    def set_proctask(self, hostname, data):
        try: 
            key = "proctask-" + hostname
            for proc in data:
                proc_name = proc.get("name")
                proc_data = json.dumps(proc)
                self.client.hset(key, proc_name, proc_data)
            return True
        except Exception, e:
            LOG.error(e)

    def get_proctask(self, hostname):
        try:
            key = "proctask-" + hostname
            name_list = self.client.hkeys(key)
            body = []
            for procname in name_list:
                proc_data = self.client.hget(key, procname)
                proc = json.loads(proc_data)
                body.append(proc)
                self.client.hdel(key, procname)
            return body
        except Exception, e:
            LOG.error(e)

    def set_action(self, hostname, data):
        try:
            key = "action-" + hostname
            for action in data:
                action_data = json.dumps(action)
                self.client.lpush(key, action_data)
            return True
        except Exception, e:
            LOG.error(e)

    def get_action(self, hostname):
        try:
            key = "action-" + hostname
            body = []
            while(True):
                action_data = self.client.rpop(key)
                if not action_data:
                    break
                action = json.loads(action_data)
                body.append(action) 
            return body
        except Exception, e:
            LOG.error(e)

    def set_report(self, hostname, data):
        try:
            key = "report-" + hostname
            for report in data:
                proc_name = report.get("proc_name")
                proc_status = json.dumps(report)
                self.client.hset(key, proc_name, proc_status)
            return True
        except Exception, e:
            LOG.error(e)


    def get_report(self, hostname):
        try:
            key = "report-" + hostname
            name_list = self.client.hkeys(key)
            body = []
            for procname in name_list:
                report_data = self.client.hget(key, procname)
                report = json.loads(report_data)
                body.append(report)
                #self.client.hdel(key, procname)
            return body
        except Exception, e:
            LOG.error(e)

    def set_heartbeat(self, hostname, data):
        try:
            key = "heartbeat-" + hostname
            self.client.set(key, data)
            return True
        except Exception, e:
            LOG.error(e)

    def get_heartbeat(self, hostname):
        try:
            key = "heartbeat-" + hostname
            body = self.client.get(key)
            return body
        except Exception, e:
            LOG.error(e)


if __name__ == '__main__':
    hostname = "ywy"

    proctask_data = [{
                        "name":"apache2",
                        "cmd_start":"/etc/init.d/apache2 start",
                        "cmd_stop":"/etc/init.d/apache2 stop",
                        "cmd_restart":"/etc/init.d/apache2 restart",
                        "pid_file":"/var/run/apache2.pid"},
                    ]
    #client1 = RedisDriver()
    #client1.set_proctask(hostname, proctask_data)
    #result = client1.get_proctask(hostname)
    #print result

    action_data =   [
                        #{"name":"apache2","action":"start"},
                        #{"name":"apache2","action":"stop"},
                        #{"name":"apache2","action":"restart"},
                        {"name":"apache2","action":"unmonitor"},
                        {"name":"apache2","action":"monitor"},
                        #{"name":"apache2","action":"remove"},
                    ]
    #client2 = RedisDriver()
    #client2.set_action(hostname, action_data)
    #result = client2.get_action(hostname)
    #print result


    report_data =  [{'proc_name': 'apache2', 'status': 'unmonitored'},]
    #client3 = RedisDriver()
    #client3.set_report(hostname, report_data)
    #result = client3.get_report(hostname)
    #print result
