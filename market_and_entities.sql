create schema if not exists `market` default character set utf8mb4;
use `market`;

create table if not exists `market`.`good`(
`good_id` int not null auto_increment,
`name` varchar(50) unique not null,
# value 
`price` float,

primary key(`good_id`)
);

create table if not exists `market`.`entity`(
`entity_id` int auto_increment,
`name` varchar(50) unique not null,
`cash` float,
`value` float,
primary key(`entity_id`)
);

create table if not exists `market`.`product`(
`product_id` int auto_increment,
`good_id` int,
`producer_id` int,
`name` varchar(50) unique not null,
`value` float,
`price` float,
`quantity` int,

primary key(`product_id`),
index `fk_good_idx` (`good_id` asc) visible,
constraint `fk_good`
	foreign key (`good_id`)
    references `market`.`good`(`good_id`)
    on delete cascade
    on update cascade,
index `fk_producer_idx` (`producer_id` asc) visible,
constraint `fk_producer`
	foreign key (`producer_id`)
    references `market`.`entity`(`entity_id`)
    on delete cascade
    on update cascade
);

create table if not exists `market`.`buy`(
`product_id` int,
`buyer_id` int,
`index` int unique not null auto_increment,
`price` float not null,
`quantity` int default 1,
`is_asset` int default 1, -- if is asset = 0, consumption or total depreciation happened

primary key(`product_id`, `buyer_id`),
index `fk_product_idx` (`product_id` asc) visible,
constraint `fk_product`
	foreign key(`product_id`)
    references `market`.`product`(`product_id`)
    on update cascade
    on delete cascade,
index `fk_buyer_idx` (`buyer_id` asc) visible,
constraint `fk_buyer`
	foreign key(`buyer_id`)
    references `market`.`entity`(`entity_id`)
    on update cascade
    on delete cascade
    -- this is the exchange table --
);


