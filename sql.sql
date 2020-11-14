DROP DATABASE IF EXISTS shop;
CREATE DATABASE shop;
USE shop;

DROP TABLE IF EXISTS members, purchase, goods, bills, items;

CREATE TABLE IF NOT EXISTS members (
    `Employee ID`         int NOT NULL AUTO_INCREMENT,
    `First Name`  varchar(20) NOT NULL,
    `Last Name`   varchar(20) NOT NULL,
    Username      varchar(20) NOT NULL,
    Password_SHA  varchar(64) NOT NULL,
    Address      varchar(100)     NULL,
    Email         varchar(30) NOT NULL,
    Admin             tinyint NOT NULL DEFAULT 0,
    PRIMARY KEY (`Employee ID`),
    UNIQUE KEY (Username, Email)
);

CREATE TABLE IF NOT EXISTS purchase (
    `Product Description`   varchar(50) NOT NULL,
    `Product ID`                 bigint NOT NULL,
    `External ID`                bigint     NULL,
    `Agent ID`                      int NOT NULL,
    Supplier                varchar(50) NOT NULL,
    Datetime                   datetime NOT NULL,
    Amount                          int NOT NULL,
    Price                 decimal(9, 2) NOT NULL,
    INDEX fk_agent_id_idx (`Agent ID` ASC),
    KEY (`Product ID`),
    KEY (`Product Description`),
    KEY (`External ID`),
    KEY (Price),
    KEY (Supplier),
    CONSTRAINT fk_agent_id FOREIGN KEY (`Agent ID`)
        REFERENCES members (`Employee ID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS goods (
    `Product ID`                 bigint NOT NULL,
    `Product Description`   varchar(50) NOT NULL,
    Stock                           int NOT NULL DEFAULT 0,
    `Buying Price`        decimal(9, 2) NOT NULL,
    `Selling Price`       decimal(9, 2) NOT NULL,
    `VAT %`                         int NOT NULL DEFAULT 27,
    `External ID`                bigint NOT NULL,
    Supplier                varchar(50) NOT NULL,
    Discount                        int NOT NULL DEFAULT 0,
    PRIMARY KEY (`Product ID`),
    INDEX fk_product_id_idx (`Product ID` ASC),
    CONSTRAINT fk_product_id FOREIGN KEY (`Product ID`)
        REFERENCES purchase (`Product ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_desc FOREIGN KEY (`Product Description`)
        REFERENCES purchase (`Product Description`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_buying_price FOREIGN KEY (`Buying Price`)
        REFERENCES purchase (Price)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT fk_external_id FOREIGN KEY (`External ID`)
        REFERENCES purchase (`External ID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
    CONSTRAINT fk_supplier FOREIGN KEY (Supplier)
        REFERENCES purchase (Supplier)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS bills (
    `Bill ID`           bigint NOT NULL AUTO_INCREMENT,
    `Cashier ID`           int NOT NULL,
    Total        decimal(9, 2) NOT NULL,
    Datetime          datetime NOT NULL,
    PRIMARY KEY (`Bill ID`),
    INDEX fk_cashier_id_idx (`Cashier ID` ASC),
    CONSTRAINT fk_cashier_id FOREIGN KEY (`Cashier ID`)
        REFERENCES members (`Employee ID`)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS items (
    `Bill ID`              bigint NOT NULL,
    `Product ID`           bigint NOT NULL,
    Quantity                  int NOT NULL DEFAULT 1,
    `Selling Price` decimal(9, 2) NOT NULL,
    INDEX fk_bill_id_idx (`Bill ID` ASC),
    INDEX fk_item_product_id_idx (`Product ID` ASC),
    CONSTRAINT fk_bill_id FOREIGN KEY (`Bill ID`)
        REFERENCES bills (`Bill ID`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_item_product_id FOREIGN KEY (`Product ID`)
        REFERENCES goods (`Product ID`)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);

INSERT INTO members
VALUE
(0, 'Admin', 'Admin', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '', 'n/a', 1);