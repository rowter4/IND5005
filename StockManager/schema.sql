create database dr_db;

use dr_db;

create table trn_hist (
	trn_id int primary key,
	user_id varchar(64) not null,
	item_name varchar(512) not null,
	item_sn int,
	qty int,
	trns_mode varchar(8),
	date datetime
);

create table user (
	user_id varchar(64) not null primary key,
    password varchar(128) not null
);

insert into user (user_id,password) values ('admin','drlaser');

select * from user;