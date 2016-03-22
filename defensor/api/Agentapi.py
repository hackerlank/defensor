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
from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.api.Mysqldriver import MysqlDriver
from defensor.api.Redisdriver import RedisDriver

from defensor.api.Common import create_ok_body
from defensor.api.Common import create_error_body
from defensor.api.Common import get_time

##############################################################################
# 
# Set flask app from here
#
##############################################################################
agent_app = Blueprint('agent_app', __name__,
                        template_folder='templates')

MYSQL = MysqlDriver()
REDIS = RedisDriver()

@agent_app.route("/register/<host_name>", methods=['POST'])
def register(host_name=None):
    req_body = request.get_json()
    msg_from = req_body.get("message_from")
    db_body = {
                "name": req_body.get("hostname"),
                "host_ip": req_body.get("ip"),
                "region": req_body.get("region"),
                "asset_id": req_body.get("asset"),
                "description": req_body.get("description"),
                }

    if "agent" == msg_from:
        host = MYSQL.get_host_by_name(host_name)
        if not host:
            result = MYSQL.insert_host(db_body)
            if not result:
                body = create_error_body("Can't insert to DB!") 
            else:
                body = create_ok_body("Register Sucess!")
        else:
            body = create_ok_body("Register Sucess!")

    elif "webclient" ==  msg_from:
            result = MYSQL.update_host(db_body)
            if not result:
                body = create_error_body("Can't update to DB!")
            else:
                body = create_ok_body("Host update Sucess!")
    
    else:
        body = create_error_body("Can't find message_from")

    return jsonify(body)

@agent_app.route("/dbsync/<host_name>", methods=['GET'])
def configDbSync(host_name=None):
    """
    Http request template:
    body = { 
        "hostname" : host_name,
        "data" : [{
                    "name":"apache2",
                    "cmd_start":"/etc/init.d/apache2 start",
                    "cmd_stop":"/etc/init.d/apache2 stop",
                    "cmd_restart":"/etc/init.d/apache2 restart",
                    "pid_file":"/var/run/apache2.pid"},]
            }
    """
    conf_data = MYSQL.get_processes_by_host(host_name)
    body = { 
            "hostname" : host_name,
            "data" : conf_data,
            }
    return jsonify(body)

@agent_app.route("/proctask/<host_name>", methods=['GET'])
def configProctask(host_name=None):
    """
    Http request template:
    body = { 
            "hostname" : host_name,
            "data" : [{
                        "name":"apache2",
                        "cmd_start":"/etc/init.d/apache2 start",
                        "cmd_stop":"/etc/init.d/apache2 stop",
                        "cmd_restart":"/etc/init.d/apache2 restart",
                        "pid_file":"/var/run/apache2.pid"},]
            }
    """
    conf_data = REDIS.get_proctask(host_name)
    body = { 
            "hostname" : host_name,
            "data" : conf_data,
            }
    return jsonify(body)

@agent_app.route("/action/<host_name>", methods=['GET'])
def action(host_name=None):
    """
    Http request template:
    body = { 
            "hostname" : host_name,
            "data" : [
                        #{"name":"apache2","action":"start"},
                        #{"name":"apache2","action":"stop"},
                        #{"name":"apache2","action":"restart"},
                        {"name":"apache2","action":"unmonitor"},
                        {"name":"apache2","action":"monitor"},
                        #{"name":"apache2","action":"remove"},
                    ]
            }
    """
    action_data = REDIS.get_action(host_name)
    body = { 
            "hostname" : host_name,
            "data" : action_data,
            }
    return jsonify(body)

@agent_app.route("/report/<host_name>", methods=['POST'])
def set_status(host_name=None):
    """
    Http request template:
    body = {"message":"ok"}
    """
    req_body = request.get_json()
    report_data = req_body.get("data")
    result = REDIS.set_report(host_name, report_data)
    if not result:
        body = create_error_body("Can't insert to Redis!")
    else:
        body =  create_ok_body("Report Success")
    return jsonify(body)

@agent_app.route("/heartbeat/<host_name>", methods=['POST'])
def heartbeat(host_name=None):
    """
    Http request template:
    body =  {"message":"ok"}
    """
    #req_body = request.get_json()
    #report_data = req_body.get("data")
    report_data = get_time()
    result = REDIS.set_heartbeat(host_name, report_data)
    if not result:
        body = create_error_body("Can't insert to Redis!")
    else:
        body =  create_ok_body("Heartbeat Success")
    return jsonify(body)