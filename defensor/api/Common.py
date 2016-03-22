# -*- coding: utf-8 -*-
##############################################################################
# 
# Project   : Defensor
# Author    : Yy
# Email     : yangwanyuan@ztgame.com
# Date      : 2015.11 
#
##############################################################################
from time import time, mktime, strptime, ctime

def create_ok_body(data):
    body = {"message": "ok", "body": data}
    return body


def create_error_body(data):
    body = {"message": "error", "body": data}
    return body

def get_time():
    data = ctime()
    return data

def is_time_expire(data):
    time_last = mktime(strptime(data))
    time_now = time()
    epoch = time_now - time_last
    if epoch > 600 :
        return False
    else:
        return True
