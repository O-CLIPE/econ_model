create schema if not exists market default character set utf8mb4;
use market;

create table if not exists market.good(
`good_id` int not null auto_increment,
`name` varchar(50) unique not null,
# value 
`price` float,

primary key(`good_id`)
);

create table if not exists market.entity(
`entity_id` int auto_increment,
`name` varchar(50) unique not null,
`income` float,
`expenses` float,
`value` float,
# ebit
# produce -- fk em outra tabela
# consume -- fk em outro tabela diferente

primary key(`entity_id`)
);

create table if not exists market.product(
`product_id` int auto_increment,
`good_id` int,
`producer_id` int,
`name` varchar(50) unique not null,
`value` float,
`price` float,
`supply` int,
# `demand` int,

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

create table if not exists market.consume(
`product_id` int,
`consumer_id` int,
`index` int unique not null auto_increment,
`price` float not null,

primary key(`product_id`, `consumer_id`),
index `fk_product_idx` (`product_id` asc) visible,
constraint `fk_product`
	foreign key(`product_id`)
    references `market`.`product`(`product_id`)
    on update cascade
    on delete cascade,
index `fk_consumer_idx` (`consumer_id` asc) visible,
constraint `fk_consumer`
	foreign key(`consumer_id`)
    references `market`.`entity`(`entity_id`)
    on update cascade
    on delete cascade
    -- this is the exchange table --
);

