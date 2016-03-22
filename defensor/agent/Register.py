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
import socket
#import socket, fcntl, struct  

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.common.DfsConfig import DfsConfig
from defensor.agent.Common import HttpCon, get_hostname
from defensor.agent.Common import execute_cmd

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
CONF_PORT_DEFAULT = 8181
CONF_REGISTER_URL_DEFAULT = "/register/%s"


def register():
    ensure_god_start()

    host = CONF.get("api", "host")
    if not host:    
        host = CONF_HOST_DEFAULT

    port = CONF.getint("api", "port")
    if not port:
        port = CONF_PORT_DEFAULT

    register_url = CONF.get("url", "register_url")
    if not register_url:
        register_url = CONF_REGISTER_URL_DEFAULT

    hostname = get_hostname()
    register_url = register_url % hostname
    httpcon = HttpCon(host, port, register_url)

    body = get_body(hostname)
  
    result = httpcon.post(body)
    if not result:
        LOG.warn("register Failed!")
        return False

    LOG.info("register Success! request = %s" % (result))
    return True

def get_body(hostname):
    ip = get_ip(hostname)
    region = get_region(hostname)
    asset = get_asset(hostname)
    data = {
            "message_from":"agent",
            "hostname":hostname,
            "ip":ip,
            "region":region,
            "asset":asset,
            "description":None,
            }
    return data

def get_ip(hostname):
    ip = socket.gethostbyname(hostname) 
    return ip

def get_region(hostname):
    region = hostname.split("-")[0]
    return region

def get_asset(hostnmae):
    return "00000"

def ensure_god_start():
    cmd = "god"
    execute_cmd(cmd)
    return 

#def get_ip_by_nic(ifname = 'eth0'):  
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
#    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
#    ret = socket.inet_ntoa(inet[20:24])  
#    return ret  