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
import sys
import logging 
from flask import Flask

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.api.Webapi import web_app 
from defensor.api.Agentapi import agent_app 
from defensor.common.DfsConfig import DfsConfig
from defensor.api.Mysqldriver import MysqlDriver
from defensor.api.Redisdriver import RedisDriver

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
#CONF_LOG_FILE_DEFAULT = "/var/log/defensor/api.log"
#CONF_ETC_FILE_DEFAULT = "/etc/defensor/api.conf"

CONF_API_HOST_DEFAULT = "0.0.0.0"
CONF_API_PORT_DEFAULT = 8181
CONF_API_PROCESSES_DEFAULT = 8

##############################################################################
# 
# Set flask app from here
#
##############################################################################
app = Flask(__name__)
app.register_blueprint(web_app)
app.register_blueprint(agent_app)

MYSQL = MysqlDriver()
REDIS = RedisDriver()


def load():
    LOG.info("Defensor Api Is Starting!")
    CONF.print_conf()

    #connect redis
    while (not REDIS.connect()):
        time.sleep(5) 

    #connect mysql
    while (not MYSQL.connect()):
        time.sleep(5) 


def get_api_params():
    host = CONF.get("api", "host")
    if not host:
        host = CONF_API_HOST_DEFAULT

    port = CONF.getint("api", "port")
    if not port:
        port = CONF_API_PORT_DEFAULT

    processes = CONF.getint("api", "processes")
    if not processes:
        processes = CONF_API_PROCESSES_DEFAULT    

    return host, port, processes
    #app.run(host=host, port=port, processes=processes)


    
