create database if not exists defensor;
use defensor;

drop table if exists process;
drop table if exists host;

create table host (
    id int(10)  not null auto_increment,
    name varchar(20) not null unique,
    host_ip varchar(255) not null,
    asset_id varchar(255) ,
    region varchar(255) not null,
    description text,
    primary key(id)    
)engine=innodB  default charset=utf8;

create table process(
    id int(10) not null auto_increment,
    host_name varchar(100) not null,
    process_name varchar(255) not null,
    cmd_start varchar(255) not null,
    cmd_stop varchar(255) not null,
    cmd_restart varchar(255) not null,
    pid_file varchar(255) not null,
    primary key(id),
    foreign key(host_name) references host(name),
    unique key  process_name (host_name, process_name)
)engine=innodB  default charset=utf8;


