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
from flask import render_template
from flask import abort
from jinja2 import TemplateNotFound

##############################################################################
# 
# Import project file from here
#
##############################################################################
from defensor.api.Mysqldriver import MysqlDriver
from defensor.api.Redisdriver import RedisDriver

##############################################################################
# 
# Set flask app from here
#
##############################################################################
web_app = Blueprint('web_app', __name__,
                        template_folder='templates')


MYSQL = MysqlDriver()
REDIS = RedisDriver()

@web_app.route("/")
@web_app.route("/hello/<name>")
def hello(name=None):
    try:
        #return "Hello Defensor!!"
        return render_template('hello.html', name=name)
    except TemplateNotFound:
        abort(404)