CREATE DATABASE  IF NOT EXISTS `lolturnier`;
USE `lolturnier`;

-- drop all tables 
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS turniere;
DROP TABLE IF EXISTS user_team;
DROP TABLE IF EXISTS user_turnier;

-- Table structure for table `users`
CREATE TABLE users (
  id INT NOT NULL ,
  puuid VARCHAR(100) NOT NULL DEFAULT '',
  token VARCHAR(100) NOT NULL DEFAULT '',
  gameName VARCHAR(100) NOT NULL DEFAULT '',
  tagLine VARCHAR(100) NOT NULL DEFAULT '',
  profileIconId INT NOT NULL DEFAULT 0,
  summonerLevel INT NOT NULL DEFAULT 0,
  tier VARCHAR(100) NOT NULL DEFAULT '',
  `rank` VARCHAR(10) NOT NULL DEFAULT '',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table structure for table `users`
CREATE TABLE teams (
  id int PRIMARY KEY NOT NULL DEFAULT '0',
  turnier_id bigint NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE turniere (
  id bigint PRIMARY KEY NOT NULL,
  name varchar(100) NOT NULL,
  team_size int NOT NULL DEFAULT 8,
  turnier_owner int NOT NULL,
  start_date varchar(50) NOT NULL,
  access ENUM()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
  

CREATE TABLE user_team (
  user_id int,
  team_id int,
  role varchar(7),
  PRIMARY KEY (user_id, team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE user_turnier (
  user_id int,
  turnier_id bigint,
  PRIMARY KEY (user_id, turnier_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





