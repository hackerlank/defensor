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
import time
import httplib
import logging 
import json 
import socket
import subprocess

##############################################################################
# 
# Set LOG and CONF from here
#
##############################################################################
LOG = logging.getLogger(__name__)

##############################################################################
# 
# Class PeriodTask for create periodtask thread from here 
#
##############################################################################
class PeriodTask:
    def __init__(self, name = None, interval = None):
        self.name = name
        self.interval = interval

    def set_fun(self, fun, *args):
        self.fun = fun
        self.args = args

    def run(self):
        while True:
            try:
                time_pre = time.time()
                self.fun(*self.args)
                time_now = time.time()
                monitor_time = time_now - time_pre
                if monitor_time < self.interval:
                    #LOG.debug("%s thread cost time %ss" \
                    #    %(self.name, round(monitor_time,3)))
                    time.sleep(self.interval + time_pre - time_now)
                else:
                    LOG.warn("%s thread cost too long time %ss" \
                        %(self.name, round(monitor_time,3)))
            except Exception, e:
                LOG.error("%s thread error" %self.name)
                LOG.error(e)

##############################################################################
# 
# Class HttpCon for create http reqeest from here 
#
##############################################################################
class HttpCon():
    def __init__(self, host = None, port = None, url = None, timeout = 30):
        self.host = host
        self.port = port
        self.url = url
        self.timeout = 30
        self.headers = {"Content-type":"application/json",
                        "Accept": "text/plain"}


    def get(self):
        httpClient = None
        try:
            data = ''
            LOG.debug("Http request GET  %s:%s%s start" \
                %(self.host, self.port, self.url))

            httpClient = httplib.HTTPConnection(self.host, self.port, \
                self.timeout)
            httpClient.request('GET', self.url, data, self.headers)
            response = httpClient.getresponse()
            status = response.status 

            if status != 200:
                LOG.warn("Http request GET  %s:%s%s Failed, status = %s" \
                    %(self.host, self.port, self.url, status))
                return None
            
            result = json.loads(response.read())
            LOG.debug("Http request GET  %s:%s%s Success" \
                %(self.host, self.port, self.url))
            return result

        except Exception, e:
            LOG.error("Http request GET  %s:%s%s Failed" \
                    %(self.host, self.port, self.url))
            LOG.error(e)

        finally:
            if httpClient:
                httpClient.close()

    def post(self, body):
        httpClient = None
        try:
            data = json.dumps(body)
            LOG.debug("Http request POST  %s:%s%s, body=%s start" \
                %(self.host, self.port, self.url, data))

            httpClient = httplib.HTTPConnection(self.host, \
                self.port, self.timeout)
            httpClient.request('POST', self.url, data, self.headers)
            response = httpClient.getresponse()
            status = response.status 

            if status != 200:
                LOG.warn("Http request POST  %s:%s%s, body=%s Failed, \
status = %s" %(self.host, self.port, self.url, data, status))
                return None

            result = json.loads(response.read())
            LOG.debug("Http request POST  %s:%s%s, body=%s Success" \
                %(self.host, self.port, self.url, data))
            return result

        except Exception, e:
            LOG.error("Http request GET  %s:%s%s Failed" \
                    %(self.host, self.port, self.url))
            LOG.error(e)

        finally:
            if httpClient:
                httpClient.close()

##############################################################################
# 
# Function get hostname from here
#
##############################################################################
def get_hostname():
    try:
        hostname = socket.gethostname()
        return hostname
    except Exception, e:
        LOG.error("Get hostname Failed!")
        LOG.error(e)


##############################################################################
# 
# Function execute shell comand from here
#
##############################################################################
def execute_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
        LOG.debug("Execute cmd %s Success!"%cmd)
        result = process.stdout.read()
        return result
    except Exception, e:
        LOG.error("Execute cmd %s Failed!"%cmd)
        LOG.error(e)



if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8181
    register_url="/register/ywy"
    dbsync_url="/dbsync/ywy"
    proctask_url="/proctask/ywy"
    action_url="/action/ywy"
    report_url="/report/ywy"
    heartbeat_url="/heartbeat/ywy"

    #httpclient = HttpCon(host, port, register_url)
    httpclient = HttpCon(host, port, dbsync_url)
    #httpclient = HttpCon(host, port, proctask_url)
    #httpclient = HttpCon(host, port, action_url)
    #httpclient = HttpCon(host, port, report_url)
    #httpclient = HttpCon(host, port, heartbeat_url)
 
    body = {"a":1, "b":2}
    #result = httpclient.post(body)   
    result = httpclient.get()
    print result