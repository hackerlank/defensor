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
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
from sqlalchemy.ext.declarative import declarative_base

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
CONF_DATABASE_DB_HOST_DEFAULT = "127.0.0.1"
CONF_DATABASE_DB_PORT_DEFAULT = 3306
CONF_DATABASE_DB_USER_DEFAULT = "root"
CONF_DATABASE_DB_PASS_DEFAULT = "" 
CONF_DATABASE_DB_DBNAME_DEFAULT = "defensor"

BASE = declarative_base() 


class Host(BASE):
    __tablename__ = 'host' 
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(20), unique=True, nullable=False)
    host_ip = Column(VARCHAR(255), nullable=False)
    asset_id = Column(VARCHAR(255), unique=True)
    region = Column(VARCHAR(255), nullable=False)
    description = Column(TEXT)

    def __init__(self, name= None, host_ip= None, 
                 region= None, asset_id = None,  
                 description = None):
        self.name = name
        self.host_ip = host_ip
        self.asset_id = asset_id
        self.region = region
        self.description = description


class Process(BASE):
    __tablename__ = 'process'
    id = Column(Integer, primary_key=True)
    host_name = Column(VARCHAR(100), ForeignKey('host.name'), nullable=False)
    process_name = Column(VARCHAR(255), nullable=False)
    cmd_start = Column(VARCHAR(255), nullable=False)
    cmd_stop = Column(VARCHAR(255), nullable=False)
    cmd_restart = Column(VARCHAR(255), nullable=False)
    pid_file = Column(VARCHAR(255), nullable=False)
    __table_args__ = (UniqueConstraint('host_name', 'process_name',
                                         name='process_name'),)

    def __init__(self, host_name = None, process_name = None, 
                 cmd_start = None, cmd_stop = None, cmd_restart = None, 
                 pid_file = None):
        self.host_name = host_name
        self.process_name = process_name
        self.cmd_start =cmd_start
        self.cmd_stop = cmd_stop
        self.cmd_restart = cmd_restart
        self.pid_file = pid_file


@singleton
class MysqlDriver(object):
    def __init__(self):
        pass

    def connect(self):
        try:
            db_host = CONF.get("database", "db_host")
            if not db_host:
                db_host = CONF_DATABASE_DB_HOST_DEFAULT
        
            db_port = CONF.getint("database", "db_port")
            if not db_port:
                db_port = CONF_DATABASE_DB_PORT_DEFAULT
        
            db_user = CONF.get("database", "db_user")
            if not db_user:
                db_user = CONF_DATABASE_DB_USER_DEFAULT

            db_pass = CONF.get("database", "db_pass")
            if not db_pass:
                db_pass = CONF_DATABASE_DB_PASS_DEFAULT

            db_dbname = CONF.get("database", "db_dbname")
            if not db_dbname:
                db_dbname = CONF_DATABASE_DB_DBNAME_DEFAULT
            
            self.engine = create_engine("mysql://%s:%s@%s:%s/%s" 
                %(db_user, db_pass, db_host, db_port, db_dbname))
            self.engine.connect()
            LOG.info("Mysql Connect mysql://%s:%s@%s:%s/%s Sucess!"
                %(db_user, db_pass, db_host, db_port, db_dbname))
            return True
        except Exception, e:
            LOG.error(e)
            LOG.error("Mysql Connect mysql://%s:%s@%s:%s/%s Failed!"
                %(db_user, db_pass, db_host, db_port, db_dbname))
        

    def insert_host(self, body):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()

            name = body.get("name")
            host_ip = body.get("host_ip")
            region = body.get("region")
            asset_id = body.get("asset_id")
            description = body.get("description")

            new_host = Host(name = name, host_ip = host_ip, 
                            region = region,asset_id = asset_id, 
                            description = description)
            session.add(new_host)
            session.commit()        
            session.close()
            return True
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()


    def update_host(self, body):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            name = body.get("name")
            session.query(Host).\
                    filter(Host.name == name).\
                    update(body,synchronize_session='evaluate')
            session.commit()
            session.close()
            return True
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()

    def delete_host_by_hostname(self, hostname):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            session.query(Host).\
                    filter(Host.name == hostname).\
                    delete(synchronize_session='evaluate')
            session.commit()
            session.close()
            return True
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()

    def get_hosts(self):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            result = []
            query_list = session.query(Host)
            session.close()
            for query in query_list:
                item = {
                        "name":query.name,
                        "host_ip":query.host_ip,
                        "asset_id":query.asset_id,
                        "region":query.region,
                        "description":query.description,
                        }
                result.append(item)
            return result 
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()

    def get_host_by_name(self, name):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            query = session.query(Host).\
                            filter(Host.name == name).\
                            first()
            session.close()
            if not query:
                return None
            item = {
                    "name":query.name,
                    "host_ip":query.host_ip,
                    "asset_id":query.asset_id,
                    "region":query.region,
                    "description":query.description,
                    }
            return item
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()


    def insert_process(self, body):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()

            host_name = body.get("host_name")
            process_name = body.get("process_name")
            cmd_start = body.get("cmd_start")
            cmd_stop = body.get("cmd_stop")
            cmd_restart = body.get("cmd_restart")
            pid_file = body.get("pid_file")

            new_process = Process(host_name = host_name, 
                                  process_name = process_name, 
                                  cmd_start = cmd_start,
                                  cmd_stop = cmd_stop, 
                                  cmd_restart = cmd_restart, 
                                  pid_file = pid_file)
            session.add(new_process)
            session.commit()        
            session.close()
            return True
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()

    def update_process(self, body):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            host_name = body.get("host_name")
            process_name = body.get("process_name")

            session.query(Process).\
                    filter(Process.host_name == host_name).\
                    filter(Process.process_name == process_name).\
                    update(body,synchronize_session='evaluate')
            session.commit()
            session.close()
            return True
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()

    def delete_process_by_host_and_process(self, host_name, process_name):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            session.query(Process).\
                    filter(Process.host_name == host_name).\
                    filter(Process.process_name == process_name).\
                    delete()
            session.commit()
            session.close()
            return True
        except Exception, e:
            LOG.error(e)
        finally:
            if session:
                session.close()

    def get_processes_by_host(self, host_name):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            result = []
            query_list = session.query(Process).\
                                 filter(Process.host_name == host_name)
            session.close()
            for query in query_list:
                item = {
                        "host_name":query.host_name,
                        "process_name":query.process_name,
                        "cmd_start":query.cmd_start,
                        "cmd_stop":query.cmd_stop,
                        "cmd_restart":query.cmd_restart,
                        "pid_file":query.pid_file,
                        }
                result.append(item)
            return result
        except Exception, e:
            LOG.error(e)
            print e
        finally:
            if session:
                session.close()

    def get_process_by_host_and_process(self, host_name, process_name):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            query = session.query(Process).\
                            filter(Process.host_name == host_name).\
                            filter(Process.process_name == process_name).\
                            first()
            session.close()
            if not query:
                return None
            item = {
                    "host_name":query.host_name,
                    "process_name":query.process_name,
                    "cmd_start":query.cmd_start,
                    "cmd_stop":query.cmd_stop,
                    "cmd_restart":query.cmd_restart,
                    "pid_file":query.pid_file,
                    }
            return item
        except Exception, e:
            LOG.error(e)
            print e
        finally:
            if session:
                session.close()

    def register_models(self):
        models = (Host,
                  Process,
                  )
        for model in models:
            model.metadata.create_all(self.engine)

if __name__ == "__main__":

    #sql_client = MysqlDriver()
    host_body = {
            "name": "test", 
            "host_ip": "127.0.0.1",
            "region": "BJ", 
            "asset_id":  "001101", 
            "description": ""}
    #sql_client.insert_host(host_body)
    #print sql_client.get_hosts()
    #print sql_client.get_host_by_name("test")

    #host_body_new = {
    #        "name": "test", 
    #        "host_ip": "127.0.0.1",
    #        "region": "BJ", 
    #        "asset_id":  "001101", 
    #        "description": "111111111111"}
    #sql_client.update_host(host_body_new)
    #print sql_client.get_hosts()
    #print sql_client.get_host_by_name("test")



    #sql_client2 = MysqlDriver()
    process_body = {
                    "host_name" : "test",
                    "process_name" : "aaa",
                    "cmd_start" : "start",
                    "cmd_stop" : "stop",
                    "cmd_restart" : "restart",
                    "pid_file" : "pid_file!!",
                    }
    #sql_client2.insert_process(process_body)
    #print sql_client2.get_processes_by_host("test")
    #print sql_client2.get_process_by_host_and_process("test", "aaa")

    #process_body_new = {
    #                    "host_name" : "test",
    #                    "process_name" : "aaa",
    #                    "cmd_start" : "start",
    #                    "cmd_stop" : "stop",
    #                    "cmd_restart" : "restart",
    #                    "pid_file" : "1111",
    #                    }
    #sql_client2.update_process(process_body_new)
    #print sql_client2.get_processes_by_host("test")
    #print sql_client2.get_process_by_host_and_process("test", "aaa")

    #sql_client2.delete_process_by_host_and_process("test", "aaa")
    #print sql_client2.get_processes_by_host("test")
    #print sql_client2.get_process_by_host_and_process("test", "aaa")


    #sql_client.delete_host_by_hostname("test")
    #print sql_client.get_hosts()
    #print sql_client.get_host_by_name("test")
