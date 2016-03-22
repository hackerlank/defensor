#!/bin/bash 

yum instll -y python-devel
yum install -y ruby ruby-devel

gem sources -r https://rubygems.org
gem sources -a https://ruby.taobao.org/

gem install god 

mkdir -p /etc/god
god 
