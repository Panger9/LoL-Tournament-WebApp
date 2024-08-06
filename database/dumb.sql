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

INSERT INTO users VALUES 
(1, 'mZFChQyv2o9RApIbqVEuQgzdqb3hEjoa16DrootWFlHIfXqFJs4u-86UjZp11c3Uun7YMT3FDiCsnQ', 'token_001', 'Sir Panger', 'EUW', 6102, 442, 'EMERALD', 'I'),
(2, 'hiRYfQC_MlqRjjA3MxduebV_Tpx9crqTssry9YsWz49u5Yba3M94OXO_T8M1WKcmREH68vhPJJ7j-g', 'token_002', 'Lanzus73', 'EUW', 6629, 817, 'DIAMOND', 'II'),
(3, 'VjLdj9VUzAUhbWqPveEvdRQ6f4VrBeVse5TIKwqVC7TLt2x3Eo45iYRp0qOZsDCg59bWZxnlSh0dow', 'token_003', 'Agurin', 'EUW', 4353, 1027, 'CHALLENGER', 'I'),
(4, 'hgOUTm2yUOdHrbeZAcu6j9WyKophL4YkR9W5W4G9_QLGG85xMRhU2DfNFM3S_yDn9gRq5WkjgzL_LA', 'token_004', 'school phobia', 'EUW', 1211, 675, 'CHALLENGER', 'I'),
(5, 'UBLPHAbSKFEkTnLFcIJzfOr78666XVcZg0V85N-WAXXWRtLQS2JmKQV8wlaHT3n2NAeXw-EjIpra0Q', 'token_005', 'Streaming Badboy', 'INT', 5131, 262, 'GRANDMASTER', 'I');

							
						 ;
-- Table structure for table `users`
CREATE TABLE teams (
  id int PRIMARY KEY NOT NULL DEFAULT '0',
  turnier_id int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO teams VALUES (1,1),(2,1),(3,1),(4,1),(5,2),(6,2),(7,2),(8,2);

CREATE TABLE turniere (
  id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name varchar(100) NOT NULL,
  team_size int NOT NULL DEFAULT 8,
  turnier_owner int NOT NULL,
  start_date varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
  
INSERT INTO turniere (id, name, team_size, turnier_owner, start_date) VALUES (1, 'Testturnier', 4, 6, '04.08.2024/20:15'),(2, 'Testturnier2', 4, 1, '06.08.2024/20:15');

CREATE TABLE user_team (
  user_id int,
  team_id int,
  role varchar(7),
  PRIMARY KEY (user_id, team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO user_team VALUES (1,1,'jgl'),(2,1,'top'),(3,1,'mid'),(4,1,'adc'), (5,1,'sup'),(1,5,'jgl'),(2,5,'top'),(3,5,'mid'),(4,5,'adc');

CREATE TABLE user_turnier (
  user_id int,
  turnier_id int,
  PRIMARY KEY (user_id, turnier_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO user_turnier VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(1,2),(2,2),(3,2),(4,2);



