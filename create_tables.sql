CREATE TABLE `morningstar`.`book_value_per_share`(
  `STOCK` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `DATE` DATE NOT NULL,
  `VERSION` VARCHAR(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `BOOK_VALUE_PER_SHARE` DOUBLE NOT NULL,
  PRIMARY KEY(`STOCK`, `DATE`, `VERSION`)
) ENGINE = InnoDB;
