drop database if exist dr_db;

create database dr_db;

use dr_db;

create table trn_hist (
	trn_id int primary key,
	user_id varchar(64) not null,
	stock_name varchar(512) not null,
	item_sn int,
	qty int,
	trns_mode varchar(8),
	date datetime,
	trns_details varchar(128)
);

create table user (
	user_id varchar(64) not null primary key,
    password varchar(128) not null,
	staff_id int,
	access_rights char(1)
);


create table stock_list (
	supplier_name_inp varchar(128), 
	item_name_inp varchar(128), 
	item_no_inp varchar(64) primary key, 
	description_inp varchar(64), 
	unit_inp varchar(8), 
	reorder_lvl_inp int, 
	reorder_days_inp int, 
	reorder_qty_inp int, 
	stock_add_date_time datetime,
	serial_no varchar(64),
	item_location varchar(128),
	cost_per_item double,
	stock_qty int,
	inventory_value double
);



insert into user (user_id,password,staff_id, access_rights) 
	values  ('admin','dradmin',111,A),
			('admin2','dradmin2',222,A),
			('system','drsystem1',333,S),
			('system2','drsystem2',444,S),
			('user1','drlaser1',555,U),
			('user2','drlaser2',666,U),
			('user3','drlaser3',777,U) ;

select * from user;

DELETE FROM dr_db.stock_list WHERE 'item_no_inp' = '2323AA';

-- will need to decommission these tables since was part of intial testing
--  -> stock_1
--  -> stock_dtl