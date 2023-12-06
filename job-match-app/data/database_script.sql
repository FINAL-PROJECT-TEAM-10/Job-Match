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
  `address` VARCHAR(150) NOT NULL,
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
  `date_posted` DATETIME NULL DEFAULT NULL,
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
  `date_posted` DATETIME NULL DEFAULT NULL,
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

-- -----------------------------------------------------------------------------
-- The following code is intended for populating the database with information.
-- -----------------------------------------------------------------------------

ALTER TABLE job_match.admins AUTO_INCREMENT = 1;
ALTER TABLE job_match.companies AUTO_INCREMENT = 1;
ALTER TABLE job_match.company_contacts AUTO_INCREMENT = 1;
ALTER TABLE job_match.employee_contacts AUTO_INCREMENT = 1;
ALTER TABLE job_match.job_ads AUTO_INCREMENT = 1;
ALTER TABLE job_match.job_ads_has_locations AUTO_INCREMENT = 1;
ALTER TABLE job_match.job_ads_has_mini_cvs AUTO_INCREMENT = 1;
ALTER TABLE job_match.job_ads_has_requirements AUTO_INCREMENT = 1;
ALTER TABLE job_match.job_seekers AUTO_INCREMENT = 1;
ALTER TABLE job_match.locations AUTO_INCREMENT = 1;
ALTER TABLE job_match.mini_cv_has_locations AUTO_INCREMENT = 1;
ALTER TABLE job_match.mini_cvs AUTO_INCREMENT = 1;
ALTER TABLE job_match.mini_cvs_has_skills AUTO_INCREMENT = 1;
ALTER TABLE job_match.skills_or_requirements AUTO_INCREMENT = 1;
ALTER TABLE job_match.temporary_tokens AUTO_INCREMENT = 1;

-- 1. COMPANIES

INSERT INTO job_match.companies (username, password, description) VALUES ("ubisoft","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq","This is ubisoft");

INSERT INTO job_match.locations (city, country) VALUES ("Paris","France");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("ubisoft@gmail.com","International 2, avenue Pasteur 94160 Saint-Mandé", "0000000", 1, 1);


INSERT INTO job_match.companies (username, password, description) VALUES ("apple","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e","We are apple");

INSERT INTO job_match.locations (city, country) VALUES ("New York","United States");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("apple@gmail.com","One Apple Park Way 95014", "0000001", 2, 2);


INSERT INTO job_match.companies (username, password, description) VALUES ("amazon","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "This is Amazon");

INSERT INTO job_match.locations (city, country) VALUES ("Luxembourg City", "Luxembourg");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("amazon@gmail.com", "410 Terry Ave N 98109", "3333333", 3, 3);


INSERT INTO job_match.companies (username, password, description) VALUES ("google","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "We are Google");

INSERT INTO job_match.locations (city, country) VALUES ("Mountain View", "United States");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("google@gmail.com", "1600 Amphitheatre Parkway 94043", "2222222", 4, 4);


INSERT INTO job_match.companies (username, password, description) VALUES ("microsoft","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "This is Microsoft");

INSERT INTO job_match.locations (city, country) VALUES ("Seattle", "United States");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("microsoft@gmail.com", "One Microsoft Way 98052", "1111111", 5, 5);


INSERT INTO job_match.companies (username, password, description) VALUES ("facebook","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "We are Facebook");

INSERT INTO job_match.locations (city, country) VALUES ("Menlo Park", "United States");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("facebook@gmail.com", "1 Hacker Way 94025", "4444444", 6, 6);


INSERT INTO job_match.companies (username, password, description) VALUES ("uber","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "This is Uber");

INSERT INTO job_match.locations (city, country) VALUES ("San Francisco", "United States");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("uber@gmail.com", "1455 Market St 94103", "5555555", 7, 7);


INSERT INTO job_match.companies (username, password, description) VALUES ("netflix","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "We are Netflix");

INSERT INTO job_match.locations (city, country) VALUES ("Los Gatos", "United States");

INSERT INTO job_match.company_contacts (email, address, telephone, locations_id, company_id) VALUES ("netflix@gmail.com", "100 Winchester Cir 95032", "6666666", 8, 8);


-- 2. Job Seekers

INSERT INTO job_match.locations (city, country) VALUES ("Sofia", "Bulgaria");

INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("ivaylo@gmail.com","ul.Ivan Vazov", "0000000", 9);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("ivo21","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "Ivaylo", "Petrov", "Hello my name is Ivaylo", 0, 1);


INSERT INTO job_match.locations (city, country) VALUES ("Varna", "Bulgaria");

INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("john_doe@email.com", "123 Marketing St", "2222222", 10);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("john_doe","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "John", "Doe", "Passionate about marketing", 0, 2);


INSERT INTO job_match.locations (city, country) VALUES ("Athens", "Greece");

INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("sara@gmail.com", "15 Finance Avenue", "3333333", 11);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("sara87","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "Sara", "Smith", "Finance professional with 5+ years of experience", 0, 3);



INSERT INTO job_match.locations (city, country) VALUES ("Berlin", "Germany");

INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("alex@email.com", "123 Tech Street", "4444444", 12);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("alex25","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "Alex", "Johnson", "Detail-oriented project manager", 0, 4);



INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("emily@email.com", "789 Design Lane", "5555555", 1);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("emily88","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "Emily", "Miller", "Creative graphic designer", 0, 5);



INSERT INTO job_match.locations (city, country) VALUES ("Tokyo", "Japan");

INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("david@email.com", "456 IT Avenue", "6666666", 13);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("david12","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "David", "Taylor", "Skilled IT professional", 0, 6);




INSERT INTO job_match.locations (city, country) VALUES ("Sydney", "Australia");

INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("lucas@email.com", "456 Code Avenue", "7777777", 14);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("lucas94","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "Lucas", "Garcia", "Experienced software engineer", 0, 7);





INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("olivia@email.com", "789 Marketing Street", "8888888", 2);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("olivia17","$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "Olivia", "Lopez", "Marketing specialist with a focus on social media", 0, 8);



INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("liam@email.com", "123 Finance Lane", "9999999", 3);

INSERT INTO job_match.job_seekers (username, password, first_name, last_name, summary, busy, employee_contacts_id) VALUES ("liam03","$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "Liam", "Martinez", "Financial analyst with expertise in data analysis", 0, 9);


-- 3. Skills_or_Requirements

INSERT INTO job_match.skills_or_requirements (name) VALUES ("Python");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("JavaScript");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("C++");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("Java");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("Csharp");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("Django");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("Flask");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("FastApi");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("React");

INSERT INTO job_match.skills_or_requirements (name) VALUES ("NodeJS");


-- 4. Job ADs

INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("We are searching for employees", 2000, 5000, "active", 1);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (1, 1, 0);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (1, 2, "Beginner");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (1, 10, "Beginner");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (1, 1, "Beginner");



INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("Searching for new employees", 1000, 2000, "active", 2);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (2, 2, 0);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (2, 4, "Advanced");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (2, 1, "Advanced");



INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("Available positions for python Beginner juniour", 3000, 6000, "active", 3);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (3, 3, 0);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (3, 6, "Advanced");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (3, 1, "Intermediate");



INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("We are searching for employees", 1500, 4000, "active", 4);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (4, 6, 1);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (4, 7, "Intermediate");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (4, 1, "Beginner");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (4, 6, "Advanced");



INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("Available positions for javascript Beginner juniour", 2000, 5000, "active", 5);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (5, 8, 1);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (5, 3, "Intermediate");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (5, 4, "Intermediate");



INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("Searching for new employees", 1800, 3200, "active", 6);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (6, 6, 0);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (6, 8, "Intermediate");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (6, 9, "Beginner");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (6, 5, "Intermediate");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (6, 4, "Advanced");



INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("We are searching for employees", 1500, 3200, "active", 7);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (7, 7, 0);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (7, 3, "Advanced");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (7, 1, "Beginner");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (7, 7, "Intermediate");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (7, 4, "Advanced");



INSERT INTO job_match.job_ads (description, min_salary, max_salary, status, companies_id) VALUES ("Available positions for c# Beginner juniour", 1200, 2200, "active", 8);

INSERT INTO job_match.job_ads_has_locations (job_ads_id, locations_id, remote_status) VALUES (8, 8, 0);

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (8, 8, "Intermediate");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (8, 9, "Beginner");

INSERT INTO job_match.job_ads_has_requirements (job_ads_id, skills_or_requirements_id, level) VALUES (8, 5, "Intermediate");


-- 5. Mini Cvs

INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (1800, 5000, "Im searching for a good salary based company", "private", 1, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (1, 9, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (1, 2, "Intermediate");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (1, 5, "Beginner");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (1, 7, "Advanced");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (2000, 3000, "Searching for a good available position in the IT sector", "private", 2, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (2, 10, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (2, 1, "Advanced");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (2, 3, "Beginner");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (1200, 3200, "Skilled person with a lot of experiences", "private", 3, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (3, 11, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (3, 4, "Intermediate");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (3, 2, "Beginner");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (3, 8, "Advanced");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (1000, 4500, "Searching for a good available position in the IT sector", "private", 4, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (4, 12, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (4, 2, "Beginner");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (4, 8, "Beginner");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (3000, 4500, "Im searching for a good salary based company", "private", 5, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (5, 1, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (5, 2, "Intermediate");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (5, 1, "Beginner");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (5, 9, "Advanced");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (5, 7, "Advanced");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (2000, 3500, "Skilled person with a lot of experiences", "private", 6, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (6, 13, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (6, 2, "Intermediate");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (6, 4, "Beginner");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (3000, 4500, "Searching for a good available position in the IT sector", "private", 7, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (7, 14, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (7, 5, "Beginner");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (7, 1, "Beginner");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (7, 9, "Advanced");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (1500, 4500, "Im searching for a good salary based company", "private", 8, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (8, 2, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (8, 6, "Intermediate");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (8, 1, "Beginner");



INSERT INTO job_match.mini_cvs (min_salary, max_salary, description, status, job_seekers_id, main_cv) VALUES (2500, 4500, "Skilled person with a lot of experiences", "private", 9, 0);

INSERT INTO job_match.mini_cv_has_locations (mini_cv_id, locations_id, remote_status) VALUES (9, 3, 0);

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (9, 3, "Intermediate");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (9, 1, "Beginner");

INSERT INTO job_match.mini_cvs_has_skills (mini_cvs_id, skills_or_requirements_id, level) VALUES (9, 7, "Advanced");


-- 6. Admins
INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("margarett@gmail.com", "ul.Hristo Botev", "0033000", 9);

INSERT INTO job_match.admins (username, password, first_name, last_name, employee_contacts_id) VALUES ("Margarett", "$2b$12$1Xd3.PpvVgtZjpO3X1KKRean1nKtxmiOWEJUtJQsiaMQdETmpQt3e", "Margaret", "Hions", 10);


INSERT INTO job_match.employee_contacts (email, address, telephone, locations_id) VALUES ("simon1@gmail.com", "Unter den Linden", "0033000", 12);

INSERT INTO job_match.admins (username, password, first_name, last_name, employee_contacts_id) VALUES ("Simon1", "$2b$12$qHW5RyygTGBUoWpll.jZWuA0gyHMvoHCJSwsImGu.ksPH44qCVXTq", "Simon", "Higins", 11);