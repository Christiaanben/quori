-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 30, 2018 at 07:18 AM
-- Server version: 5.5.38-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `prac3`
--

-- --------------------------------------------------------

--
-- Table structure for table `q_and_a`
--

CREATE TABLE IF NOT EXISTS `q_and_a` (
  `qID` int(11) NOT NULL AUTO_INCREMENT,
  `type` tinyint(3) unsigned NOT NULL,
  `question` varchar(90) NOT NULL,
  `answer` varchar(90) NOT NULL,
  `wrong1` varchar(90) DEFAULT NULL,
  `wrong2` varchar(90) DEFAULT NULL,
  `reason` varchar(90) NOT NULL,
  PRIMARY KEY (`qID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `q_and_a`
--

INSERT INTO `q_and_a` (`qID`, `type`, `question`, `answer`, `wrong1`, `wrong2`, `reason`) VALUES
(1, 1, 'Dragon Ball Z is the best show of all time', 'true', NULL, NULL, 'No debating this.'),
(2, 1, 'I stayed up all night making this website', 'true', NULL, NULL, 'Yeah, I''m stupid. I should''ve started earlier.'),
(3, 2, 'You''re stranded on an island, what hand-sized object should you have with you???', 'Book: How to build a raft', 'Boat', 'Cell phone', 'A boat is not hand-sized. There is no reception for phone.'),
(4, 3, 'Just select everything', 'everything', 'select', 'Just', 'A very simple command. Choose everything. I couldn''t have made it easier.'),
(5, 4, '&pi;', '3.1415926535...', NULL, NULL, 'Did you not watch life of Pi?'),
(6, 4, 'e', '2.7182818284...', NULL, NULL, 'Ok, I understand how you could''ve missed this one.'),
(7, 4, '&radic;2', '1.4142135623...', NULL, NULL, 'You should really practice your square root skills.'),
(8, 4, 'cos(30&deg)', '0.8660254037...', NULL, NULL, 'This is the easy one. It''s the only one that is less than one.'),
(9, 5, 'Who created this:', 'bennie', NULL, NULL, 'Come on you could''ve just asked.'),
(10, 1, 'Is this hoodie cool???', 'false', NULL, NULL, '');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `score` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`uID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uID`, `username`, `password`, `score`) VALUES
(1, 'bennie', '1235;lk', 5),
(2, 'HP', 'kd9iek', 3),
(3, 'HACKER', 'HAHA', 6);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
