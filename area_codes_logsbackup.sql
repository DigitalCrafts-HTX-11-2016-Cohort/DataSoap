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

-- Dumping structure for table dnc.logs
DROP TABLE IF EXISTS `logs`;
CREATE TABLE IF NOT EXISTS `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `file_in_name` varchar(80) NOT NULL,
  `file_in_record_count` int(11) NOT NULL,
  `file_in_timestamp` text NOT NULL,
  `file_out_name` varchar(80) NOT NULL,
  `file_out_record_count` int(11) NOT NULL,
  `file_out_timestamp` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8;

-- Dumping data for table dnc.logs: ~105 rows (approximately)
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT IGNORE INTO `logs` (`id`, `userid`, `file_in_name`, `file_in_record_count`, `file_in_timestamp`, `file_out_name`, `file_out_record_count`, `file_out_timestamp`) VALUES
	(9, 4, 'entrust-corp-dummydata.csv', 245, '201701132304', '201701132304entrust-corp-dummydata.csv', 245, '201701132304'),
	(10, 4, 'dnctestingtable.csv', 4, '201701141723', '201701141723dnctestingtable.csv', 3, '201701141755'),
	(11, 4, 'dnctestingtable.csv', 4, '201701141715', '201701141715dnctestingtable.csv', 3, '201701141715'),
	(12, 4, 'dnctestingtable.csv', 4, '201701141831', '201701141831dnctestingtable.csv', 3, '201701141845'),
	(13, 4, 'dnctestingtable.csv', 4, '201701141837', '201701141837dnctestingtable.csv', 3, '201701141817'),
	(14, 14, 'dnctestingtable.csv', 4, '201701141838', '201701141838dnctestingtable.csv', 3, '201701141800'),
	(15, 1, 'dnctestingtable.csv', 4, '201701141816', '201701141816dnctestingtable.csv', 3, '201701141816'),
	(16, 1, 'dnctestingtable.csv', 4, '201701141852', '201701141852dnctestingtable.csv', 3, '201701141852'),
	(17, 1, 'dnctestingtable.csv', 4, '201701141845', '201701141845dnctestingtable.csv', 3, '201701141845'),
	(18, 1, '3-7-2016leads.csv', 15751, '201701131823', '2017011418233-7-2016leads.csv', 15749, '201701131825'),
	(19, 1, '3-7-2016leads.csv', 15751, '201701121810', '2017011418103-7-2016leads.csv', 15749, '201701121813'),
	(20, 1, 'dnctestingtable.csv', 20456, '201701141848', '201701141848dnctestingtable.csv', 18765, '201701141849'),
	(21, 1, 'dnctestingtable.csv', 10444, '201701101857', '201701141857dnctestingtable.csv', 10234, '201701101857'),
	(22, 1, 'dnctestingtable.csv', 63001, '201701111839', '201701141839dnctestingtable.csv', 44654, '201701111853'),
	(23, 1, 'dnctestingtable.csv', 32, '201701141857', '201701141857dnctestingtable.csv', 29, '201701141857'),
	(24, 1, 'dnctestingtable.csv', 4, '201701141819', '201701141819dnctestingtable.csv', 3, '201701141819'),
	(25, 1, 'dnctestingtable.csv', 4, '201701141836', '201701141836dnctestingtable.csv', 3, '201701141836'),
	(26, 1, 'dnctestingtable.csv', 4, '201701141927', '201701141927dnctestingtable.csv', 3, '201701141934'),
	(27, 1, 'dnctestingtable.csv', 4, '201701141930', '201701141930dnctestingtable.csv', 3, '201701141930'),
	(28, 1, 'dnc_test.csv', 3, '201701161513725927', '201701161513725927dnc_test.csv', 3, '201701161514916407'),
	(29, 1, 'dnc_test.csv', 3, '201701161559686476', '201701161559686476dnc_test.csv', 3, '201701161521453967'),
	(30, 1, 'dnc_test.csv', 4, '201701161606228202', '201701161606228202dnc_test.csv', 3, '201701161632036475'),
	(31, 1, 'dnc_test.csv', 3, '201701161638195578', '201701161638195578dnc_test.csv', 3, '201701161638284007'),
	(32, 1, 'dnc_test.csv', 4, '201701161604195813', '201701161604195813dnc_test.csv', 3, '201701161618112158'),
	(33, 1, 'dnc_test.csv', 4, '201701161638933143', '201701161638933143dnc_test.csv', 3, '201701161639024605'),
	(34, 1, 'dnc_test.csv', 3, '201701161638933143', '201701161638933143dnc_test.csv', 3, '201701161626304012'),
	(37, 1, 'classtesting.csv', 7, '201701161900595345', '201701161900595345classtesting.csv', 6, '201701161903612856'),
	(38, 1, 'dnc_test.csv', 3, '201701162041459986', '201701162041459986dnc_test.csv', 3, '201701162044409376'),
	(39, 1, 'dnc_test.csv', 3, '201701162033042680', '201701162033042680dnc_test.csv', 3, '201701162057916377'),
	(40, 1, 'dnc_test.csv', 3, '201701162041459986', '201701162041459986dnc_test.csv', 3, '201701162021971925'),
	(41, 1, 'dnc_test.csv', 3, '201701162033042680', '201701162033042680dnc_test.csv', 3, '201701162009873953'),
	(42, 1, 'dnc_test.csv', 3, '201701162041459986', '201701162041459986dnc_test.csv', 3, '201701162007657683'),
	(43, 1, 'classtesting.csv', 7, '201701162033042680', '201701162033042680classtesting.csv', 6, '201701162037510906'),
	(44, 1, 'classtesting.csv', 7, '201701162033042680', '201701162033042680classtesting.csv', 6, '201701162048100110'),
	(45, 1, 'small_test.csv', 6, '201701162033042680', '201701162033042680small_test.csv', 0, '201701162022762128'),
	(46, 1, 'small_test.csv', 6, '201701162033042680', '201701162033042680small_test.csv', 0, '201701162020108712'),
	(47, 1, 'small_test.csv', 6, '201701162033042680', '201701162033042680small_test.csv', 0, '201701162051142893'),
	(48, 1, 'classtesting.csv', 7, '201701162033042680', '201701162033042680classtesting.csv', 6, '201701162051882606'),
	(49, 17, 'classtesting.csv', 7, '201701162033042680', '201701162033042680classtesting.csv', 6, '201701162035250668'),
	(50, 18, 'small_test.csv', 6, '201701162033042680', '201701162033042680small_test.csv', 0, '201701162024502743'),
	(51, 18, '3-7-2016leads.csv', 15751, '201701162041459986', '2017011620414599863-7-2016leads.csv', 15751, '201701162125026554'),
	(52, 18, '3-7-2016leads.csv', 15751, '201701162041459986', '2017011620414599863-7-2016leads.csv', 15751, '201701162109825337'),
	(53, 19, 'test.csv', 3, '201701162033042680', '201701162033042680test.csv', 1, '201701162243122034'),
	(54, 1, 'classtesting.csv', 7, '201701192156449944', '201701192156449944classtesting.csv', 6, '201701192134730722'),
	(55, 1, 'classtesting.csv', 7, '201701192156449944', '201701192156449944classtesting.csv', 6, '201701192146083144'),
	(56, 1, '201701161513725927dnc_test.csv', 3, '201701192105237056', '201701192105237056201701161513725927dnc_test.csv', 3, '201701192156916735'),
	(57, 1, 'entrust-corp-dummydata.csv', 245, '201701192156449944', '201701192156449944entrust-corp-dummydata.csv', 245, '201701192120239157'),
	(58, 1, 'classtesting.csv', 7, '201701200045801352', '201701200045801352classtesting.csv', 6, '201701200013646783'),
	(59, 1, 'dnctestingtable.csv', 6, '201701200044685628', '201701200044685628dnctestingtable.csv', 6, '201701200032441086'),
	(60, 1, 'entrust-corp-dummydata_1.csv', 245, '201701200643407998', '201701200643407998entrust-corp-dummydata_1.csv', 245, '201701201440465820'),
	(61, 1, 'leadlist_addressproductcode_aepcoh_20170118.csv', 51638, '201701201453511071', '201701201453511071leadlist_addressproductcode_aepcoh_20170118.csv', 51638, '201701201400003564'),
	(62, 1, '3-7-2016leads.csv', 15751, '201702221651946130', '2017022216519461303-7-2016leads.csv', 15749, '201702222307907539'),
	(63, 1, '3-7-2016leads.csv', 15749, '201703012353555986', '2017030123535559863-7-2016leads.csv', 15749, '201703012300661521'),
	(64, 1, 'leadlist_addressproductcode_aepcoh_20170118.csv', 51638, '201703060817699933', '201703060817699933leadlist_addressproductcode_aepcoh_20170118.csv', 51638, '201703070233815258'),
	(65, 1, '3-7-2016leads.csv', 15749, '201703240848532638', '2017032408485326383-7-2016leads.csv', 15749, '201703242121136447'),
	(66, 1, '3-7-2016leads.csv', 15749, '201703240848532638', '2017032408485326383-7-2016leads.csv', 15749, '201703242219176102'),
	(67, 1, 'luke_pa_leads.csv', 176, '201703291410819000', '201703291410819000luke_pa_leads.csv', 176, '201703291423155000'),
	(68, 1, 'luke_pa_leads.csv', 176, '201703290927501378', '201703290927501378luke_pa_leads.csv', 176, '201703291936335696'),
	(69, 1, 'luke_pa_leads.csv', 176, '201703291501949000', '201703291501949000luke_pa_leads.csv', 176, '201703291518'),
	(70, 1, 'luke_pa_leads.csv', 176, '201703291504690000', '201703291504690000luke_pa_leads.csv', 176, '201703291536'),
	(71, 1, 'luke_pa_leads2.csv', 176, '201703291504690000', '201703291504690000luke_pa_leads2.csv', 176, '201703291542'),
	(72, 1, '33747000luke_pa_leads2.csv', 176, '201703301212502000', '20170330121250200033747000luke_pa_leads2.csv', 176, '201703301235344000'),
	(73, 1, '54144000luke_pa_leads2.csv', 176, '201703301211855000', '201703301211855000luke_pa_leads2.csv', 176, '201703301255566000'),
	(74, 1, '36299000luke_pa_leads2.csv', 176, '201703301312380000', '201703301312380000luke_pa_leads2.csv', 176, '201703301337830000'),
	(75, 1, '28769000luke_pa_leads2.csv', 176, '201703301503574000', '201703301503574000luke_pa_leads2.csv', 176, '201703301530284000'),
	(76, 1, '593989953-7-2016leads.csv', 15749, '201703311601498898', '2017033116014988983-7-2016leads.csv', 15749, '201703311703122836'),
	(77, 1, '08814000luke_pa_leads2.csv', 176, '201704031546434000', '201704031546434000luke_pa_leads2.csv', 176, '201704031510335000'),
	(78, 1, '49547000luke_pa_leads.csv', 176, '201704031517658000', '201704031517658000luke_pa_leads.csv', 176, '201704031551062000'),
	(79, 1, '36998000luke_pa_leads.csv', 176, '201704031536998000', '201704031536998000luke_pa_leads.csv', 176, '201704031538523000'),
	(80, 1, '47878000luke_pa_leads.csv', 176, '201704031847878000', '201704031847878000luke_pa_leads.csv', 176, '201704031849247000'),
	(81, 1, '29954000luke_pa_leads.csv', 176, '201704031929954000', '201704031929954000luke_pa_leads.csv', 176, ''),
	(82, 1, '20810000luke_pa_leads.csv', 176, '201704031920810000', '201704031920810000luke_pa_leads.csv', 176, ''),
	(83, 1, '43857000book1.csv', 9, '201704041943857000', '201704041943857000book1.csv', 9, ''),
	(84, 1, '01156000book1.csv', 9, '201704041901156000', '201704041901156000book1.csv', 9, ''),
	(85, 1, '02352000book1.csv', 9, '201704042002352000', '201704042002352000book1.csv', 9, ''),
	(86, 1, '03756000book1.csv', 9, '201704042003756000', '201704042003756000book1.csv', 9, ''),
	(87, 1, '49589000book1.csv', 9, '201704042049589000', '201704042049589000book1.csv', 9, ''),
	(88, 1, '55221000book1.csv', 9, '201704042055221000', '201704042055221000book1.csv', 9, ''),
	(89, 5, '06034190luke_pa_leads.csv', 176, '201704111206034200', '201704111206034200luke_pa_leads.csv', 176, ''),
	(90, 1, '10590000luke_pa_leads2.csv', 176, '201705261910590000', '201705261910590000luke_pa_leads2.csv', 176, ''),
	(91, 1, '15753000luke_pa_leads2.csv', 176, '201705261915753000', '201705261915753000luke_pa_leads2.csv', 176, ''),
	(92, 1, '13486000luke_pa_leads2.csv', 176, '201705261913486000', '201705261913486000luke_pa_leads2.csv', 176, ''),
	(93, 1, '48401468luke_pa_leads2.csv', 176, '201706151748401491', '201706151748401491luke_pa_leads2.csv', 176, ''),
	(94, 1, '15654582luke_pa_leads_fake_phones.csv', 176, '201706151715654607', '201706151715654607luke_pa_leads_fake_phones.csv', 176, ''),
	(95, 1, '51655594luke_pa_leads_fake_phones.csv', 176, '201706151751655620', '201706151751655620luke_pa_leads_fake_phones.csv', 176, ''),
	(96, 1, '05876394luke_pa_leads2.csv', 176, '201706151705876419', '201706151705876419luke_pa_leads2.csv', 176, ''),
	(97, 1, '56966150luke_pa_leads_fake_phones.csv', 176, '201706151756966177', '201706151756966177luke_pa_leads_fake_phones.csv', 176, ''),
	(98, 1, '31718470luke_pa_leads2.csv', 176, '201706151731718525', '201706151731718525luke_pa_leads2.csv', 176, ''),
	(99, 1, '17096997luke_pa_leads2.csv', 176, '201706151817097022', '201706151817097022luke_pa_leads2.csv', 176, ''),
	(100, 1, '08790849luke_pa_leads2.csv', 176, '201706151808790871', '201706151808790871luke_pa_leads2.csv', 176, '201706151808991196'),
	(101, 1, '07857259luke_pa_leads2.csv', 176, '201706151807857282', '201706151807857282luke_pa_leads2.csv', 176, '201706151807901722'),
	(102, 1, '06991538luke_pa_leads2.csv', 176, '201706151806991549', '201706151806991549luke_pa_leads2.csv', 176, '201706151807039182'),
	(103, 1, '12213214luke_pa_leads2.csv', 176, '201706151812213237', '201706151812213237luke_pa_leads2.csv', 176, '201706151812256779'),
	(104, 8, '09411576luke_pa_leads2.csv', 176, '201706151809411598', '201706151809411598luke_pa_leads2.csv', 176, '201706151809453729'),
	(105, 1, '26887819luke_pa_leads2.csv', 176, '201706152026887830', '201706152026887830luke_pa_leads2.csv', 176, '201706152026932046'),
	(106, 1, '28086644tryit.txt', 345, '201707031428086686', '201707031428086686tryit.txt', 22, '201707031429449602'),
	(107, 1, '10792309tryit.txt', 345, '201707031410792352', '201707031410792352tryit.txt', 273, '201707031412737701'),
	(108, 1, '04457000luke_pa_leads_fake_phones.csv', 176, '201707061304457000', '201707061304457000luke_pa_leads_fake_phones.csv', 134, '201707061305824000'),
	(109, 1, '25769000luke_pa_leads2.csv', 176, '201707061325769000', '201707061325769000luke_pa_leads2.csv', 134, '201707061327033000'),
	(110, 1, '27195000dnc_nexxa20170616_064339373.txt', 345, '201707061327195000', '201707061327195000dnc_nexxa20170616_064339373.txt', 273, '201707061328520000'),
	(111, 1, '28577365dnc_nexxa20170616_064339373.txt', 345, '201707062028577383', '201707062028577383dnc_nexxa20170616_064339373.txt', 273, '201707062028636610'),
	(112, 1, '38244000dnc_nexxa20170616_064339373.txt', 345, '201707071838244000', '201707071838244000dnc_nexxa20170616_064339373.txt', 273, '201707071839652000'),
	(113, 1, '08252000dnc_nexxa20170616_064339373.txt', 345, '201707071808252000', '201707071808252000dnc_nexxa20170616_064339373.txt', 273, '201707071809646000'),
	(114, 1, '04861241dnc_nexxa20170616_064339373.txt', 345, '201707072004861257', '201707072004861257dnc_nexxa20170616_064339373.txt', 273, '201707072004936393'),
	(115, 1, '44100531luke_pa_leads.csv', 176, '201707171944100553', '201707171944100553luke_pa_leads.csv', 140, '201707171944149700');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;

-- Dumping structure for table dnc.log_removed_numbers
DROP TABLE IF EXISTS `log_removed_numbers`;
CREATE TABLE IF NOT EXISTS `log_removed_numbers` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `phone` varchar(50) NOT NULL,
  `result` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- Dumping data for table dnc.log_removed_numbers: ~4 rows (approximately)
/*!40000 ALTER TABLE `log_removed_numbers` DISABLE KEYS */;
INSERT IGNORE INTO `log_removed_numbers` (`id`, `userid`, `timestamp`, `phone`, `result`) VALUES
	(1, 1, '2017-07-17 19:25:19', '2095135137', 'Your Subscription does not include this area code'),
	(2, 1, '2017-07-17 19:39:47', '2095135137', 'Your Subscription does not include this area code'),
	(3, 1, '2017-07-17 19:39:55', '2098328939', 'DO NOT CALL this number'),
	(4, 1, '2017-07-20 17:44:37', '2089564562', 'This number is Squeaky Clean!');
/*!40000 ALTER TABLE `log_removed_numbers` ENABLE KEYS */;

-- Dumping structure for table dnc.PurchasedCodes
DROP TABLE IF EXISTS `PurchasedCodes`;
CREATE TABLE IF NOT EXISTS `PurchasedCodes` (
  `AreaCode` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table dnc.PurchasedCodes: ~75 rows (approximately)
/*!40000 ALTER TABLE `PurchasedCodes` DISABLE KEYS */;
INSERT IGNORE INTO `PurchasedCodes` (`AreaCode`) VALUES
	(209),
	(213),
	(215),
	(216),
	(217),
	(219),
	(220),
	(224),
	(234),
	(260),
	(267),
	(272),
	(309),
	(310),
	(312),
	(317),
	(323),
	(330),
	(331),
	(380),
	(408),
	(412),
	(415),
	(419),
	(424),
	(440),
	(442),
	(484),
	(510),
	(513),
	(530),
	(559),
	(562),
	(567),
	(570),
	(574),
	(610),
	(614),
	(618),
	(619),
	(626),
	(628),
	(630),
	(650),
	(657),
	(661),
	(669),
	(707),
	(708),
	(714),
	(717),
	(724),
	(740),
	(747),
	(760),
	(765),
	(773),
	(779),
	(805),
	(812),
	(814),
	(815),
	(818),
	(831),
	(847),
	(858),
	(872),
	(878),
	(909),
	(916),
	(925),
	(930),
	(937),
	(949),
	(951);
/*!40000 ALTER TABLE `PurchasedCodes` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
