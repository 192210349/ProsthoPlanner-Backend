-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 30, 2026 at 05:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `prosthoplanner`
--

-- --------------------------------------------------------

--
-- Table structure for table `bone_measurements`
--

CREATE TABLE `bone_measurements` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `bone_density` float DEFAULT NULL,
  `bone_length` float DEFAULT NULL,
  `bone_width` float DEFAULT NULL,
  `measurement_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clinical_examinations`
--

CREATE TABLE `clinical_examinations` (
  `patient_id` int(11) NOT NULL,
  `edentulous_area` varchar(100) DEFAULT NULL,
  `kennedy_classification` varchar(50) DEFAULT NULL,
  `tissue_condition` varchar(50) DEFAULT NULL,
  `occlusion_type` varchar(50) DEFAULT NULL,
  `clinical_notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `imaging_analysis`
--

CREATE TABLE `imaging_analysis` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `analysis_result` text DEFAULT NULL,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `implant_simulations`
--

CREATE TABLE `implant_simulations` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `implant_type` varchar(100) DEFAULT NULL,
  `implant_size` varchar(50) DEFAULT NULL,
  `simulation_result` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `medical_history`
--

CREATE TABLE `medical_history` (
  `patient_id` int(11) NOT NULL,
  `is_diabetic` tinyint(1) DEFAULT 0,
  `has_hypertension` tinyint(1) DEFAULT 0,
  `has_thyroid` tinyint(1) DEFAULT 0,
  `has_asthma` tinyint(1) DEFAULT 0,
  `is_smoker` tinyint(1) DEFAULT 0,
  `drinks_alcohol` tinyint(1) DEFAULT 0,
  `allergies` text DEFAULT NULL,
  `medications` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `patient_name` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `diagnosis` text DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `patient_imaging`
--

CREATE TABLE `patient_imaging` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `image_type` enum('OPG','CBCT','INTRAORAL') NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `vision_analysis_json` text DEFAULT NULL,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `treatment_suggestions`
--

CREATE TABLE `treatment_suggestions` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `plan_a_treatment` varchar(255) NOT NULL,
  `plan_a_cost` decimal(10,2) DEFAULT NULL,
  `plan_a_time` varchar(100) DEFAULT NULL,
  `plan_b_treatment` varchar(255) NOT NULL,
  `plan_b_cost` decimal(10,2) DEFAULT NULL,
  `plan_b_time` varchar(100) DEFAULT NULL,
  `plan_c_treatment` varchar(255) NOT NULL,
  `plan_c_cost` decimal(10,2) DEFAULT NULL,
  `plan_c_time` varchar(100) DEFAULT NULL,
  `selected_plan` enum('A','B','C') DEFAULT NULL,
  `generated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile_number` varchar(15) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `otp` varchar(6) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `reset_otp` varchar(6) DEFAULT NULL,
  `reset_otp_expiry` datetime DEFAULT NULL,
  `otp_code` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `mobile_number`, `password_hash`, `role`, `created_at`, `otp`, `otp_expiry`, `is_verified`, `updated_at`, `reset_otp`, `reset_otp_expiry`, `otp_code`) VALUES
(3, 'John Doe', 'john.doe@example.com', '9876543211', 'scrypt:32768:8:1$LnWn8mHCy5hcmUhl$c0052ac13f8aa55c9912a3530053af1498c845d14dbce0bc8916fb98bb4d4858ad6a34f1837c723ea0d059260e6c743831d66e0c9e5befae37ba8cec0f205cef', NULL, '2026-03-26 12:25:42', NULL, '2026-03-26 18:05:42', 0, '2026-03-26 12:25:42', NULL, NULL, '2648'),
(4, 'chaitu', 'chaitanyaprakashkonisetty@gmail.com', '9876543212', 'scrypt:32768:8:1$HPU1vx3GjB51Kstt$e0386256b5fe094e000bab45f84cf0698f6a963775dbca4794fd3775b4ab979b2dcae36f1d694c4d4752455e1c2a36bb8cc19c96263c9c89d1335d03491cf851', NULL, '2026-03-26 12:26:46', NULL, '2026-03-29 16:53:29', 1, '2026-03-29 11:14:10', NULL, NULL, NULL),
(6, 'chaituu', 'user@gmail.com', '9876543213', 'scrypt:32768:8:1$je6Af3HxO2VDCmNx$2cb503b47804068748706db1cc04bc1792855367cf660af54820f2be0a314e4a915ea4f9314eb256536fca8a47602159328a827531dfff4eae9da8800dbc5bc2', NULL, '2026-03-26 12:35:03', NULL, '2026-03-26 18:15:03', 1, '2026-03-26 12:35:41', NULL, NULL, NULL),
(7, 'cherry', 'sscharithareddy@gmail.com', '9177548517', 'scrypt:32768:8:1$5yNJSh45AifwUrSU$d4a164a910e4bf0b770f90b5e0c3742350515fad926b12816620aa65087f7308ea48a9c92aa490f68c894c6c98377c7352bcf656391e6bbdec5c6c24d0d7b0c4', NULL, '2026-03-26 15:17:30', NULL, '2026-03-26 20:57:31', 1, '2026-03-26 15:18:27', NULL, NULL, NULL),
(8, 'prakash ', 'prakashkonisetty04@gmail.com', '9849184778', 'scrypt:32768:8:1$aHfyhdIfVoZGtTDi$7fe5f555f21944f9cee3079fe36e921bcb687e0c0ccfd9046a6fd30b6eb5c64bc6d0560368b6f7b8689f9183690c9c83d515f25e1db8f53d4b9ef9cf9100c018', NULL, '2026-03-28 02:11:05', NULL, '2026-03-28 09:36:46', 1, '2026-03-28 03:56:46', NULL, NULL, '5403');

-- --------------------------------------------------------

--
-- Table structure for table `users_temp`
--
-- Error reading structure for table prosthoplanner.users_temp: #1932 - Table &#039;prosthoplanner.users_temp&#039; doesn&#039;t exist in engine
-- Error reading data for table prosthoplanner.users_temp: #1064 - You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near &#039;FROM `prosthoplanner`.`users_temp`&#039; at line 1

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bone_measurements`
--
ALTER TABLE `bone_measurements`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clinical_examinations`
--
ALTER TABLE `clinical_examinations`
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `imaging_analysis`
--
ALTER TABLE `imaging_analysis`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `implant_simulations`
--
ALTER TABLE `implant_simulations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `medical_history`
--
ALTER TABLE `medical_history`
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patient_imaging`
--
ALTER TABLE `patient_imaging`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `treatment_suggestions`
--
ALTER TABLE `treatment_suggestions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `mobile_number` (`mobile_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bone_measurements`
--
ALTER TABLE `bone_measurements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `imaging_analysis`
--
ALTER TABLE `imaging_analysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `implant_simulations`
--
ALTER TABLE `implant_simulations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `patient_imaging`
--
ALTER TABLE `patient_imaging`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `treatment_suggestions`
--
ALTER TABLE `treatment_suggestions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `clinical_examinations`
--
ALTER TABLE `clinical_examinations`
  ADD CONSTRAINT `clinical_examinations_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `medical_history`
--
ALTER TABLE `medical_history`
  ADD CONSTRAINT `medical_history_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `patient_imaging`
--
ALTER TABLE `patient_imaging`
  ADD CONSTRAINT `patient_imaging_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `treatment_suggestions`
--
ALTER TABLE `treatment_suggestions`
  ADD CONSTRAINT `treatment_suggestions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
