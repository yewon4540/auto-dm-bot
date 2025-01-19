USE lms;

DROP TABLE IF EXISTS `message_slack`;

CREATE TABLE `message_slack` (
    `row_num` bigint(20) NOT NULL AUTO_INCREMENT UNIQUE KEY,
    `mcode` VARCHAR(255) NOT NULL PRIMARY KEY,
    `status` VARCHAR(255),
    `ms_success` BIT(1),
    `created_time` datetime(6) DEFAULT current_timestamp(6)
);

DROP TABLE IF EXISTS `member_slack`;

CREATE TABLE `member_slack` (
    `no` INT NOT NULL PRIMARY KEY,
    `username` VARCHAR(255),
    `userid` VARCHAR(255),
    `name` VARCHAR(255),
    `name_same` INT,
    `mail_same` INT
);

LOAD DATA INFILE '/tmp/first/init_sql_df.csv'
INTO TABLE `member_slack`
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(no, username, userid, name, name_same, mail_same)