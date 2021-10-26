DROP SCHEMA IF EXISTS Gooly;
CREATE SCHEMA Gooly;
USE Gooly;

 -- ================== Sadnaot ================== 
drop table if exists sadnaot;
CREATE TABLE sadnaot (
	sadna_id int primary key AUTO_INCREMENT,
    name varchar(50) NOT NULL unique,
    description varchar(50) default NULL, -- free text 
    duration time NOT NULL default '1:15:00',
    base_cost int NOT NULL,
    base_price int NOT NULL
);
-- insert values
insert into sadnaot (name,description, base_cost, base_price, duration) 
values ('סדנאת פעמונים',default, 100, 800, default),
	('סדאנת לוחות שעם','מתאים לימי הולדת',  150, 1000, '1:30:00'),
	('סדנאת צילום בסמארטפון',default, 50, 700, default),
	('סדנת בטון',default, 200, 1100, '1:00:00'),
	('סדנת קופסת אוצר',default, 150, 900, default);
    
 -- ================== City ================== 
drop table if exists city;
CREATE TABLE city (
    name varchar(50) primary key 
);

-- insert values
insert into city (name) 
values ('רמת גן'), ('גבעתיים'), ('פתח תקווה'), ('תל אביב'), 
    ('בני ברק'), ('חולון'), ('ראשון לציון'), ('רחובות');
  
 -- ================== Customers ================== 
drop table if exists customers;
CREATE TABLE customers (
	cust_id int primary key AUTO_INCREMENT,
    name varchar(50) NOT NULL unique,
    contact_name varchar(50) default NULL, -- free text 
    phone_number char(10) NOT NULL ,
	city varchar(50), 
		FOREIGN KEY (city) REFERENCES city(name) on delete restrict on update cascade,
    address_street varchar(50) NOT NULL,
    address_house int default NULL,
    address_appartment int default NULL,
    address_entrence varchar(10) default NULL
);
-- insert values
insert into customers (name, contact_name,  city, address_street, phone_number, address_house, address_appartment, address_entrence)
values ('מועדון הגפן','שמרית המנהלת','רמת גן', 'רחוב ביאליק','0549120340', 61, NULL, NULL),
		('מתנס צעירי גבעתיים', 'אלי','גבעתיים','הלוחם', concat('05', round(rand() * 100000000)) ,round(rand()*100), round(rand()*100), round(rand()*5)),
		('בית ספר דגלים', 'רותם שאולי רכזת','רמת גן','הרואה', concat('05', round(rand() * 100000000)) ,round(rand()*100), round(rand()*100), round(rand()*5)),
		('יום הולדת לאלעד', 'האמא תמר שאולי','תל אביב','פארק הירקון', concat('05', round(rand() * 100000000)) ,NULL, NULL, NULL),
		('מועדונית נוער שחר', 'כרמית שרון', 'פתח תקווה','רחוב השבלול', concat('05', round(rand() * 100000000)) ,round(rand()*100), round(rand()*100), round(rand()*5));
	

 -- ================== Payments ================== 
drop table if exists payments;
 create table payments (
	payment_id int primary key auto_increment,
    cust_id int not null,
		FOREIGN KEY (cust_id) REFERENCES customers(cust_id) on delete restrict on update cascade,
    payment_date date not null DEFAULT (now()),
    payment_sum int unsigned not null
    );

-- insert values
 insert into payments (cust_id, payment_date,payment_sum) 
 values (1,'2020-08-01', 600),
		 (1,'2020-09-01', 700),
		 (2,'2020-08-10', 900),
		 (3,'2020-08-01', 2000),
		 (4,'2020-08-01', 1000);
 
 -- ================== ORDERS ================== 
drop table if exists orders;
create table orders (
	order_id int primary key auto_increment,
    order_date date not null, 
    sadna_id int,
		FOREIGN KEY (sadna_id) REFERENCES sadnaot(sadna_id) on delete restrict on update cascade,
	cust_id int,
		FOREIGN KEY (cust_id) REFERENCES customers(cust_id) on delete restrict on update cascade,
    start_time time NOT NULL,
    price int unsigned,
    taxi_cost int default 50,
    payment_id int default NUll,
    	FOREIGN KEY (payment_id) REFERENCES payments(payment_id) on delete SET NUll,
    UNIQUE KEY `duplicate constraint` (sadna_id, cust_id, order_date, start_time)
);


 -- insert values 
insert into orders (sadna_id, cust_id, order_date, start_time, price, taxi_cost, payment_id)
values (1, 1,'2020-07-15','18:00:00',700, default, default),
	(1, 2, '2020-07-17','19:00:00',NULL, default, default),
    (1, 5, '2020-08-16','19:00:00',NULL, default, default),
    (2, 4, '2020-08-20','13:00:00',NULL, 100, default),
    (2, 2,'2020-08-30','19:00:00',NULL, default, 2),
    (3, 1,'2020-09-07','19:00:00',NULL, default, default),
    (3, 2,'2020-09-08','19:00:00',NULL, default, default),
    (3, 5,'2020-09-20','19:00:00',NULL, default, default),
    (2, 5,'2020-10-01','19:00:00',NULL, default, 5);
    
    
-- set all prices that are NULL to the base price that is in the sadnaot table
update orders as o join sadnaot as s using (sadna_id)
set o.price = s.base_price
where (o.price is NULL);

-- =======  TRIGGERS =================================================================

DELIMITER $$
CREATE TRIGGER orders_before_INSERT before INSERT ON orders FOR EACH ROW
BEGIN
	if NEW.price is NULL then 
    set NEW.price  = (select base_price from sadnaot where sadna_id = new.sadna_id); 
    end if;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER orders_before_UPDATE before UPDATE ON orders FOR EACH ROW
BEGIN
		if NEW.price is NULL then 
    set NEW.price  = (select base_price from sadnaot where sadna_id = new.sadna_id); 
    end if;
END$$
DELIMITER ;

-- =======  VIEWS =================================================================
create view orders_for_gui_view as
SELECT 
    order_id,
    s.name AS sadna,
    c.name AS customer,
    o.start_time,
    o.order_date,
    concat(c.city,", ", ifnull(c.address_street,''),
		"  ", 
        ifnull(c.address_house, ''),
        ifnull(concat('/',c.address_appartment),''),
        ifnull(concat(' כניסה ', address_entrence),'')) as location,
    price,
    taxi_cost,
    p.payment_date
FROM
    orders AS o 
    JOIN sadnaot AS s USING (sadna_id)
    JOIN customers AS c USING (cust_id)
    left join payments as p USING (payment_id);
	
-----------------------------------------------------
create view order_for_payment_gui_view as
SELECT 
    order_id,
    c.name AS customer,
    s.name AS sadna,
    o.order_date,
    price + taxi_cost as total_price,
    p.payment_sum,
	p.payment_date
FROM
    orders AS o 
    JOIN sadnaot AS s USING (sadna_id)
    JOIN customers AS c USING (cust_id)
    left join payments as p USING (payment_id)
order by customer, order_date desc