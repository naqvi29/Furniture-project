-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 09, 2022 at 02:59 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `furniture`
--

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `brands`
--

INSERT INTO `brands` (`id`, `name`) VALUES
(1, 'InterWood'),
(2, 'Chenone homes'),
(3, 'Habitt'),
(4, 'Index Furniture');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Bedstore Sofas'),
(2, 'Corner Sofas'),
(3, 'Sofas'),
(4, 'Chairs'),
(5, 'Stools & Chaise Lounges'),
(6, 'Popular'),
(7, 'Free Broucher & Samples'),
(8, 'In Stock');

-- --------------------------------------------------------

--
-- Table structure for table `colors`
--

CREATE TABLE `colors` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `code` text NOT NULL,
  `product_ids` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`product_ids`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `colors`
--

INSERT INTO `colors` (`id`, `name`, `code`, `product_ids`) VALUES
(1, 'Black', '#000000', '[1, 2]'),
(2, 'Blue', '#0000FF', '[1, 2]'),
(3, 'Red', '#FF0000', '[1, 2]'),
(4, 'Purple', '#800080', '[2]'),
(5, 'Yellow', '#FFFF00', ''),
(6, 'Green', '#008000', '');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `brand_id` int(11) NOT NULL,
  `color_ids` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`color_ids`)),
  `category` text NOT NULL,
  `brand` text NOT NULL,
  `name` text NOT NULL,
  `price` float NOT NULL,
  `sizes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `description` text NOT NULL,
  `image` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `category_id`, `brand_id`, `color_ids`, `category`, `brand`, `name`, `price`, `sizes`, `tags`, `description`, `image`) VALUES
(1, 1, 1, '[1, 2, 3]', 'Bedstore Sofas', 'InterWood', 'Sofa Alva 2 Seater', 40000, '[S, M, L, XS]', '[sofa, interwood, furniture]', 'A recent addition to our collection, the London Bedstore Sofa brings with it the elegance and poise of a traditional bedstore, with a clean and contemporary edge.\n\nInspired by its namesake, this model mirrors the cool, cosmopolitan London spirit.\n\nA deep seat, supported with snug seat cushions against a traditional buttoned back, the London offers a softer sit, remaining surprisingly supportive around the back.\n\nHandcrafted with a single button border, studded trim, and mahogany-stained feet, the London captures the timeless characteristics of a traditional Bedstore with a contemporary style unique to this model.\n\nMake the London unique to your space with a choice of fabrics and leathers in a range of bold, muted, and traditional colours.', 'Untitled-design-91.png'),
(2, 2, 2, '[1, 2, 4]', 'Corner Sofas', 'Chenone homes', 'Sofa Alva 2 Seater', 42000, '[S, M, L, XS]', '[sofa, interwood, furniture]', 'A recent addition to our collection, the London Bedstore Sofa brings with it the elegance and poise of a traditional bedstore, with a clean and contemporary edge.\r\n\r\nInspired by its namesake, this model mirrors the cool, cosmopolitan London spirit.\r\n\r\nA deep seat, supported with snug seat cushions against a traditional buttoned back, the London offers a softer sit, remaining surprisingly supportive around the back.\r\n\r\nHandcrafted with a single button border, studded trim, and mahogany-stained feet, the London captures the timeless characteristics of a traditional Bedstore with a contemporary style unique to this model.\r\n\r\nMake the London unique to your space with a choice of fabrics and leathers in a range of bold, muted, and traditional colours.', 'Untitled-design-91.png');

-- --------------------------------------------------------

--
-- Table structure for table `sizes`
--

CREATE TABLE `sizes` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `product_ids` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sizes`
--

INSERT INTO `sizes` (`id`, `name`, `product_ids`) VALUES
(1, 'S', '[1,2]'),
(2, 'M', '[1,2]'),
(3, 'L', '[1]'),
(4, 'XS', '[1]');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` text NOT NULL,
  `name` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `name`, `password`) VALUES
(2, 'dev@test.com', 'Developer', '1234');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `colors`
--
ALTER TABLE `colors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sizes`
--
ALTER TABLE `sizes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `colors`
--
ALTER TABLE `colors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sizes`
--
ALTER TABLE `sizes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
