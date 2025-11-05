-- -----------------------------------------------------
-- Schema USE `middleware_odoo` ;
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `middleware_odoo` ;

CREATE SCHEMA IF NOT EXISTS `middleware_odoo` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `middleware_odoo` ;
CREATE USER 'netdata'@'localhost' IDENTIFIED BY 'S0port31';
GRANT ALL PRIVILEGES ON middleware_odoo.* TO 'netdata'@'localhost';
FLUSH PRIVILEGES;

-- -----------------------------------------------------
-- Table `original_message`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `original_message` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `original_message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `file` VARCHAR(60) NULL DEFAULT NULL,
  `entity` VARCHAR(45) NULL DEFAULT NULL COMMENT 'saveCT - Productos de CT | saveSYS - Productos de Syscom | saveAddress - Direcciones | saveOther - Otras entidades a mandar a Odoo',
  `status` CHAR(1) NULL DEFAULT NULL COMMENT 'S exitoso | R recibido | P en proceso | F error',
  `request` TEXT NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;


-- -----------------------------------------------------
-- Table `unit_message`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `unit_message` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `unit_message` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `message` JSON NULL DEFAULT NULL,
  `original_message_id` INT NOT NULL,
  `entity` VARCHAR(45) NULL DEFAULT NULL COMMENT 'saveCT - Productos de CT | saveSYS - Productos de Syscom | saveAddress - Direcciones | saveOther - Otras entidades a mandar a Odoo',
  `status` CHAR(1) NULL DEFAULT NULL COMMENT 'S exitoso | R recibido | P en proceso | F error',
  `active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '0 inactivo | 1 activo',
  `response` TEXT NULL DEFAULT NULL,
  `run_at` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '0 inactivo | 1 activo',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SHOW WARNINGS;