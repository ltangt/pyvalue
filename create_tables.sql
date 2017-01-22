-- MorningStar data tables
CREATE TABLE `investment`.`morningstar_book_value_per_share`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `BOOK_VALUE_PER_SHARE` DOUBLE NOT NULL,
  `CURRENCY` VARCHAR(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'USD',
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_annual_net_income`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `NET_INCOME_MIL` DOUBLE NOT NULL,
  `CURRENCY` VARCHAR(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'USD',
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_annual_free_cash_flow`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `FREE_CASH_FLOW_MIL` DOUBLE NOT NULL,
  `CURRENCY` VARCHAR(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'USD',
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_annual_revenue`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `REVENUE_MIL` DOUBLE NOT NULL,
  `CURRENCY` VARCHAR(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'USD',
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_share_outstanding`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `SHARE_MIL` DOUBLE NOT NULL,
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_annual_operating_income`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `OPERATING_INCOME_MIL` DOUBLE NOT NULL,
  `CURRENCY` VARCHAR(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'USD',
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_annual_gross_margin`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `GROSS_MARGIN` DOUBLE NOT NULL,
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_annual_dividends`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `DIVIDENDS` DOUBLE NOT NULL,
  `CURRENCY` VARCHAR(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'USD',
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_debt_to_equity`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `DEBT_TO_EQUITY` DOUBLE NOT NULL,
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_current_ratio`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `CURRENT_RATIO` DOUBLE NOT NULL,
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_current_ratio`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `CURRENT_RATIO` DOUBLE NOT NULL,
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`morningstar_stock_price`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `CLOSE_PRICE` DOUBLE DEFAULT NULL,
  `HIGHEST_PRICE` DOUBLE DEFAULT NULL,
  `LOWEST_PRICE` DOUBLE DEFAULT NULL,
  `OPEN_PRICE` DOUBLE DEFAULT NULL,
  `CURRENCY` VARCHAR(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'USD',
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;



------------------------------------------------------------------------------------------------------------
-- Yahoo Finance tables
CREATE TABLE `investment`.`yahoo_finance_stock_quote`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TRADE_DATETIME_UTC` DATETIME NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `PRICE` DOUBLE DEFAULT NULL,
  `DAYS_HIGH` DOUBLE DEFAULT NULL,
  `DAYS_LOW` DOUBLE DEFAULT NULL,
  `PRICE_CHANGE` DOUBLE DEFAULT NULL,
  `VOLUME` DOUBLE DEFAULT NULL,
  `MARKET_CAP_IN_MILLIONS` DOUBLE DEFAULT NULL,
  `BOOK_VALUE` DOUBLE DEFAULT NULL,
  `EBITDA_IN_MILLIONS` DOUBLE DEFAULT NULL,
  `DIVIDEND_SHARE` DOUBLE DEFAULT NULL,
  `DIVIDEND_YIELD` DOUBLE DEFAULT NULL,
  `EARNING_SHARE` DOUBLE DEFAULT NULL,
  `PRICE_BOOK` DOUBLE DEFAULT NULL,
  `PRICE_SALES` DOUBLE DEFAULT NULL,
  PRIMARY KEY(`STOCK`, `TRADE_DATETIME_UTC`, `VERSION`)
) ENGINE = InnoDB;

CREATE TABLE `investment`.`yahoo_finance_stock_historical`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` DATE NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `TS` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `CLOSE` DOUBLE DEFAULT NULL,
  `OPEN` DOUBLE DEFAULT NULL,
  `LOW` DOUBLE DEFAULT NULL,
  `HIGH` DOUBLE DEFAULT NULL,
  `ADJ_CLOSE` DOUBLE DEFAULT NULL,
  `VOLUME` DOUBLE DEFAULT NULL,
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;

