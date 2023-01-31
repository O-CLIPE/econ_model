CREATE SCHEMA IF NOT EXISTS `market` DEFAULT CHARACTER SET utf8mb4;
USE `market`;

-- unique ids should all be the first table line
-- name should always be second

CREATE TABLE IF NOT EXISTS `market`.`good`(
`good_id` INT NOT NULL AUTO_INCREMENT,
`name` VARCHAR(50) UNIQUE NOT NULL,
`work` DECIMAL(19, 4) -- at average efficiency, work needed

PRIMARY KEY(`good_id`)

);

CREATE TABLE IF NOT EXISTS `market`.`entity`(
`entity_id` INT AUTO_INCREMENT,
`name` VARCHAR(50) UNIQUE NOT NULL,
`cash` FLOAT,
`value` FLOAT,
PRIMARY KEY(`entity_id`)
);

CREATE TABLE IF NOT EXISTS `market`.`product`(
`product_id` INT AUTO_INCREMENT,
`name` VARCHAR(50) UNIQUE NOT NULL,
`good_id` INT,
`producer_id` INT,
`value` DECIMAL(19, 4),
`cost` DECIMAL(19, 4),
`price` DECIMAL(19, 4),
`quantity` DECIMAL(19, 4),
`visibility` DECIMAL(5,4),
`quality` DECIMAL(5,4),
CONSTRAINT `chk_product` CHECK (`quality` <= 1.0 AND `quality` >= 0),
CONSTRAINT `chk_quality` CHECK (`visibility` <= 1.0 AND `visibility` >= 0)
-- if it is 0, it means product is worthless, or invisible

PRIMARY KEY(`product_id`),
INDEX `fk_good_idx` (`good_id` asc) visible,
CONSTRAINT `fk_good`
	FOREIGN KEY (`good_id`)
    REFERENCES `market`.`good`(`good_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

INDEX `fk_producer_idx` (`producer_id` asc) visible,
CONSTRAINT `fk_producer`
	FOREIGN KEY (`producer_id`)
    REFERENCES `market`.`entity`(`entity_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `market`.`buy`(
`index` INT,
-- no name
`product_id` INT,
`buyer_id` INT,
`price` DECIMAL(19, 4) NOT NULL,
`quantity` DECIMAL(19, 4) DEFAULT 1,
`is_asset` DECIMAL(19, 4) DEFAULT 1, -- if is asset = 0, consumption or total depreciation happened

PRIMARY KEY(`product_id`, `buyer_id`, `index`),

INDEX `fk_product_idx` (`product_id` ASC) VISIBLE,
CONSTRAINT `fk_product`
	FOREIGN KEY(`product_id`)
    REFERENCES `market`.`product`(`product_id`),

INDEX `fk_buyer_idx` (`buyer_id` ASC) VISIBLE,
CONSTRAINT `fk_buyer`
	FOREIGN KEY(`buyer_id`)
    REFERENCES `market`.`entity`(`entity_id`)
);

CREATE TABLE IF NOT EXISTS `market`.`production_good`(
`higher_good_id` INT,
`lesser_good_id` INT,
`quantity_per_unit` DECIMAL(19, 4) DEFAULT 1,

PRIMARY KEY(`higher_good_id`, `lesser_good_id`),

INDEX `fk_higher_good_idx` (`higher_good_id` )
CONSTRAINT `fk_higher_good`
    FOREIGN KEY(`higher_good_id`)
    REFERENCES `market`.`good` (`good_id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

CONSTRAINT `fk_lesser_good`
    FOREIGN KEY(`lesser_good_id`)
    REFERENCES `market`.`buy` (`good_id`)
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS `market`.`good_alternative`(
`good_id` INT,
`alternative_id` INT,

PRIMARY KEY(`alternative_id`),
CONSTRAINT `fk_good`
    FOREIGN KEY(`good_id`)
    REFERENCES `market`.`good` (`good_id`)
    ON UPDATE CASCADE,
CONSTRAINT `fk_alternative`
    FOREIGN KEY(`alternative_good_id`)
    REFERENCES `market`.`good` (`good_id`)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

