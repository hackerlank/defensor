#!/bin/bash
yum install -y  python-devel MySQL-python

yum install -y redis  
systemctl start redis.service

yum install -y mariadb-server 
systemctl start mariadb.service

mysql < schema.sql
