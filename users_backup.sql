-- --------------------------------------------------------
-- Host:                         35.166.251.127
-- Server version:               5.7.18-0ubuntu0.16.04.1 - (Ubuntu)
-- Server OS:                    Linux
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table dnc.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `company` varchar(45) DEFAULT NULL,
  `email` varchar(60) NOT NULL,
  `username` varchar(15) NOT NULL,
  `password` text NOT NULL,
  `admin` bit(1) DEFAULT b'0',
  `Deleted` bit(1) DEFAULT b'0',
  `date_acknowledged` datetime DEFAULT NULL,
  `name_as_typed` varchar(45) DEFAULT NULL,
  `company_as_typed` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- Dumping data for table dnc.users: ~11 rows (approximately)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT IGNORE INTO `users` (`id`, `firstname`, `lastname`, `company`, `email`, `username`, `password`, `admin`, `Deleted`, `date_acknowledged`, `name_as_typed`, `company_as_typed`) VALUES
	(1, 'Karissa', 'Martin', 'Vista', 'kmartin@vistaenergymarketing.com', 'karissa', '$pbkdf2-sha256$29000$RIjxfm9trbUWgtBaS8n53w$b8FH50sjeA7UBr0c0dfxo.gbXaJW3Qn4XzYzfLUKDA0', b'1', b'0', '2017-07-13 10:51:59', 'Karissa Martin', 'Vista Energy Marketing'),
	(2, 'Vista', 'Vendor', 'sample', 'abc@com', 'dfghjk', '$pbkdf2-sha256$29000$SOk9J0TofW8tRch5r5Uypg$XvWvSoVHleqrH/N4YdtyWhayp41auOWbmakK4Ksq.0s', b'0', b'1', NULL, NULL, NULL),
	(3, 'Karissa', 'Martin', 'Vista', 'kmartin@vistaenergymarketing.com', 'karissa2', '$pbkdf2-sha256$29000$nVMKAYAwBkCo1dpb6x2D8A$1yb2PX0aq9md9AlO5wPfOzMn1gqW1VqCWzuM64Z3UKw', b'1', b'0', NULL, NULL, NULL),
	(4, 'Paul', 'Atha', 'Vista Energy Marketing, LP', 'patha@vistaenergymarketing.com', 'patha', '$pbkdf2-sha256$29000$x7iXsra2tlbq/T8HYAwhBA$aagQD/uW/EjkQWkUaOIJKeDhWSXydA.BPI48kIPnnfc', b'1', b'0', NULL, NULL, NULL),
	(5, 'test', 'user', 'vista', 'paul@vista.com', 'test', '$pbkdf2-sha256$29000$2Nt7r5Vy7n0PoVSKsbY2hg$9Fqocha6lxsA1a61vq0.AVIGrZcz8RaFdbgBTqJQWPA', b'1', b'0', NULL, NULL, NULL),
	(6, 'another', 'guy', 'another', 'guy@guy.com', 'another', '$pbkdf2-sha256$29000$fe9da63VOmcsZQyhNCbEuA$kK6ND9HSYwO0m2xuvyQpYzilwR0SGmSac7qX8K8Chqg', b'0', b'1', NULL, NULL, NULL),
	(7, 'this', 'is', 'a', 'test@test.com', 'this', '$pbkdf2-sha256$29000$Y8zZ.z.HUOpdaw1BqPVeyw$33L.yi7DHPQMi7ehgiuG/MbfEXgoo3ruWb0ZNudMBz8', b'0', b'1', NULL, NULL, NULL),
	(8, 'test', 'user', 'testing', 'test@test.com', 'karissatest', '$pbkdf2-sha256$29000$GaO09h6DcO7dmxOidM6ZEw$g13kDYY4UhTiEoi5fVNwpRyGTx0KHuAK/fxyUqQtYbA', b'0', b'1', NULL, NULL, NULL),
	(9, 'james', 'martin', 'dss', 'jmartin@test.com', 'jmartin', '$pbkdf2-sha256$29000$KkWolZKythaiFKL0HmPMGQ$167V8fNkPeDmoTdE9MvxGAIQ8yDOeBTM.aWVP25m.Io', b'0', b'1', NULL, NULL, NULL),
	(10, 'Standard', 'User', 'Vista', 'test@gmail.com', 'standard', '$pbkdf2-sha256$29000$ipFSSolxLuUcY4yxVopRag$Y1Ij/WWuyEsoZIqH1ILE.iPriuB36bJz09RoGIJxayA', b'0', b'0', '2017-07-13 11:57:26', 'Standard User', 'Anyone'),
	(11, 'sample', 'deleteme', 'Vista Energy Marketing', 'Vista@gmail.com', 'sample', '$pbkdf2-sha256$29000$y/mfs1bKmVOqlVKKce6d8w$CwGsiKogktlvmwiqx5cbW6cFjAzD6WEe8CtxrQAtcys', b'0', b'0', NULL, NULL, NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
