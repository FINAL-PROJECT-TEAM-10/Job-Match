-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema job_match
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema job_match
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `job_match` DEFAULT CHARACTER SET latin1 ;
USE `job_match` ;

-- -----------------------------------------------------
-- Table `job_match`.`locations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`locations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(100) NOT NULL,
  `country` VARCHAR(56) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 35
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`employee_contacts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`employee_contacts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) NOT NULL,
  `address` VARCHAR(45) NULL DEFAULT NULL,
  `telephone` VARCHAR(45) NULL DEFAULT NULL,
  `locations_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_employee_contacts_locations1_idx` (`locations_id` ASC) VISIBLE,
  CONSTRAINT `fk_employee_contacts_locations1`
    FOREIGN KEY (`locations_id`)
    REFERENCES `job_match`.`locations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 72
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`admins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`admins` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(60) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `picture` LONGBLOB NULL DEFAULT NULL,
  `employee_contacts_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `fk_admin_list_employee_contacts_idx` (`employee_contacts_id` ASC) VISIBLE,
  CONSTRAINT `fk_admin_list_employee_contacts`
    FOREIGN KEY (`employee_contacts_id`)
    REFERENCES `job_match`.`employee_contacts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`companies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`companies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(60) NOT NULL,
  `description` TEXT CHARACTER SET 'utf8mb4' NULL DEFAULT NULL,
  `logo` LONGBLOB NULL DEFAULT NULL,
  `blocked` TINYINT(1) NOT NULL DEFAULT 0,
  `approved` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`company_contacts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`company_contacts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `telephone` VARCHAR(45) NOT NULL,
  `locations_id` INT(11) NOT NULL,
  `company_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_company_contacts_locations1_idx` (`locations_id` ASC) VISIBLE,
  INDEX `fk_company_contacts_companies1_idx` (`company_id` ASC) VISIBLE,
  CONSTRAINT `fk_company_contacts_companies1`
    FOREIGN KEY (`company_id`)
    REFERENCES `job_match`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_company_contacts_locations1`
    FOREIGN KEY (`locations_id`)
    REFERENCES `job_match`.`locations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`job_ads`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`job_ads` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `description` TEXT CHARACTER SET 'utf8mb4' NULL DEFAULT NULL,
  `min_salary` INT(11) NOT NULL,
  `max_salary` INT(11) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `date_posted` DATETIME NOT NULL,
  `companies_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `companies_id`),
  INDEX `fk_job_ad_companies1_idx` (`companies_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ad_companies1`
    FOREIGN KEY (`companies_id`)
    REFERENCES `job_match`.`companies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 59
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`job_ads_has_locations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`job_ads_has_locations` (
  `job_ads_id` INT(11) NOT NULL,
  `locations_id` INT(11) NULL DEFAULT NULL,
  `remote_status` TINYINT(1) NOT NULL,
  PRIMARY KEY (`job_ads_id`),
  INDEX `fk_job_ads_has_locations_locations1_idx` (`locations_id` ASC) VISIBLE,
  INDEX `fk_job_ads_has_locations_job_ads1_idx` (`job_ads_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ads_has_locations_job_ads1`
    FOREIGN KEY (`job_ads_id`)
    REFERENCES `job_match`.`job_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_has_locations_locations1`
    FOREIGN KEY (`locations_id`)
    REFERENCES `job_match`.`locations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`job_seekers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`job_seekers` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(60) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `summary` TEXT CHARACTER SET 'utf8mb4' NULL DEFAULT NULL,
  `picture` LONGBLOB NULL DEFAULT NULL,
  `busy` TINYINT(1) NOT NULL,
  `blocked` TINYINT(1) NOT NULL DEFAULT 0,
  `approved` TINYINT(1) NOT NULL DEFAULT 1,
  `employee_contacts_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `employee_contacts_id_UNIQUE` (`employee_contacts_id` ASC) VISIBLE,
  INDEX `fk_job_seekers_employee_contacts1_idx` (`employee_contacts_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_seekers_employee_contacts1`
    FOREIGN KEY (`employee_contacts_id`)
    REFERENCES `job_match`.`employee_contacts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 59
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`mini_cvs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`mini_cvs` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `min_salary` INT(11) NOT NULL,
  `max_salary` INT(11) NOT NULL,
  `description` TEXT CHARACTER SET 'utf8mb4' NULL DEFAULT NULL,
  `status` VARCHAR(45) NOT NULL,
  `date_posted` DATETIME NOT NULL,
  `job_seekers_id` INT(11) NOT NULL,
  `main_cv` TINYINT(4) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_mini_cv_job_seekers1_idx` (`job_seekers_id` ASC) VISIBLE,
  CONSTRAINT `fk_mini_cv_job_seekers1`
    FOREIGN KEY (`job_seekers_id`)
    REFERENCES `job_match`.`job_seekers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 39
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`job_ads_has_mini_cvs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`job_ads_has_mini_cvs` (
  `job_ad_id` INT(11) NOT NULL,
  `mini_cv_id` INT(11) NOT NULL,
  `date_matched` DATETIME NULL DEFAULT NULL,
  `match_status` VARCHAR(40) NOT NULL,
  `sender` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`job_ad_id`, `mini_cv_id`),
  INDEX `fk_job_ad_has_mini_cv_mini_cv1_idx` (`mini_cv_id` ASC) VISIBLE,
  INDEX `fk_job_ad_has_mini_cv_job_ad1_idx` (`job_ad_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ad_has_mini_cvs_job_ad1`
    FOREIGN KEY (`job_ad_id`)
    REFERENCES `job_match`.`job_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ad_has_mini_cvs_mini_cv1`
    FOREIGN KEY (`mini_cv_id`)
    REFERENCES `job_match`.`mini_cvs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`skills_or_requirements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`skills_or_requirements` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(200) NULL DEFAULT NULL,
  `career_type` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 22
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`job_ads_has_requirements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`job_ads_has_requirements` (
  `job_ads_id` INT(11) NOT NULL,
  `skills_or_requirements_id` INT(11) NOT NULL,
  `level` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`job_ads_id`, `skills_or_requirements_id`),
  INDEX `fk_job_ads_has_skills_or_requirements_skills_or_requirement_idx` (`skills_or_requirements_id` ASC) VISIBLE,
  INDEX `fk_job_ads_has_skills_or_requirements_job_ads1_idx` (`job_ads_id` ASC) VISIBLE,
  CONSTRAINT `fk_job_ads_has_skills_or_requirements_job_ads1`
    FOREIGN KEY (`job_ads_id`)
    REFERENCES `job_match`.`job_ads` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_job_ads_has_skills_or_requirements_skills_or_requirements1`
    FOREIGN KEY (`skills_or_requirements_id`)
    REFERENCES `job_match`.`skills_or_requirements` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`mini_cv_has_locations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`mini_cv_has_locations` (
  `mini_cv_id` INT(11) NOT NULL,
  `locations_id` INT(11) NULL DEFAULT NULL,
  `remote_status` TINYINT(1) NOT NULL,
  PRIMARY KEY (`mini_cv_id`),
  INDEX `fk_mini_cv_has_locations_locations1_idx` (`locations_id` ASC) VISIBLE,
  INDEX `fk_mini_cv_has_locations_mini_cv1_idx` (`mini_cv_id` ASC) VISIBLE,
  CONSTRAINT `fk_mini_cv_has_locations_locations1`
    FOREIGN KEY (`locations_id`)
    REFERENCES `job_match`.`locations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_mini_cv_has_locations_mini_cv1`
    FOREIGN KEY (`mini_cv_id`)
    REFERENCES `job_match`.`mini_cvs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`mini_cvs_has_skills`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`mini_cvs_has_skills` (
  `mini_cvs_id` INT(11) NOT NULL,
  `skills_or_requirements_id` INT(11) NOT NULL,
  `level` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`mini_cvs_id`, `skills_or_requirements_id`),
  INDEX `fk_mini_cvs_has_skills_or_requirements_skills_or_requiremen_idx` (`skills_or_requirements_id` ASC) VISIBLE,
  INDEX `fk_mini_cvs_has_skills_or_requirements_mini_cvs1_idx` (`mini_cvs_id` ASC) VISIBLE,
  CONSTRAINT `fk_mini_cvs_has_skills_or_requirements_mini_cvs1`
    FOREIGN KEY (`mini_cvs_id`)
    REFERENCES `job_match`.`mini_cvs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_mini_cvs_has_skills_or_requirements_skills_or_requirements1`
    FOREIGN KEY (`skills_or_requirements_id`)
    REFERENCES `job_match`.`skills_or_requirements` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `job_match`.`temporary_tokens`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `job_match`.`temporary_tokens` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `token` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 24
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

