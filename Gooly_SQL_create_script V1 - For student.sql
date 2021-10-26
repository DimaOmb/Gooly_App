DROP SCHEMA IF EXISTS Gooly;
CREATE SCHEMA Gooly;
USE Gooly;

 -- ================== Sadnaot ================== 
drop table if exists sadnaot;
CREATE TABLE sadnaot (
	sadna_id int primary key AUTO_INCREMENT,
	/*שמות עמודות - למלא*/
	
);

-- insert values
insert into sadnaot (/*שמות עמודות - למלא*/) 
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
	city varchar(50), 
		FOREIGN KEY (city) REFERENCES city(name) on delete restrict on update cascade,
    /*שמות עמודות - למלא*/
);

-- insert values
insert into customers (/*שמות עמודות - למלא*/)
values ('מועדון הגפן','שמרית המנהלת','רמת גן', 'רחוב ביאליק','0549120340', 61, NULL, NULL),
		('מתנס צעירי גבעתיים', 'אלי','גבעתיים','הלוחם', concat('05', round(rand() * 100000000)) ,round(rand()*100), round(rand()*100), round(rand()*5)),
		('בית ספר דגלים', 'רותם שאולי רכזת','רמת גן','הרואה', concat('05', round(rand() * 100000000)) ,round(rand()*100), round(rand()*100), round(rand()*5)),
		('יום הולדת לאלעד', 'האמא תמר שאולי','תל אביב','פארק הירקון', concat('05', round(rand() * 100000000)) ,NULL, NULL, NULL),
		('מועדונית נוער שחר', 'כרמית שרון', 'פתח תקווה','רחוב השבלול', concat('05', round(rand() * 100000000)) ,round(rand()*100), round(rand()*100), round(rand()*5));
	
-- ================== Payments ================== 
drop table if exists payments;
 create table payments (
	/*שמות עמודות - למלא*/
    );

-- insert values
 insert into payments (/*שמות עמודות - למלא*/) 
 values -- ערכים למלא
 
 -- ================== ORDERS ================== 
drop table if exists orders;
create table orders (
	order_id int primary key auto_increment,
    	/*שמות עמודות - למלא*/

    payment_id int default NUll,
    	FOREIGN KEY (payment_id) REFERENCES payments(payment_id) on delete SET NUll,
    UNIQUE KEY `duplicate constraint` (sadna_id, cust_id, order_date, start_time)
);

 -- insert values 
insert into orders (sadna_id, cust_id, order_date, start_time, price, taxi_cost, payment_id)
values (1, 1,'2020-07-15','18:00:00',700, default, default),
	-- להוסיף ערכים
    
;
-- set all prices that are NULL to the base price that is in the sadnaot table
update orders as o join sadnaot as s using (sadna_id)
set o.price = s.base_price
where (o.price is NULL);


-- =======  TRIGGERS =================================================================

DELIMITER $$
CREATE TRIGGER orders_before_INSERT before INSERT ON orders FOR EACH ROW
BEGIN
	if NEW.price is NULL then 
    set NEW.price = (select base_price from sadnaot where sadna_id = new.sadna_id); 
    end if;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER orders_before_UPDATE before UPDATE ON orders FOR EACH ROW
BEGIN
		if NEW.price is NULL then 
    set NEW.price = (select base_price from sadnaot where sadna_id = new.sadna_id); 
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