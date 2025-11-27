-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-11-2025 a las 07:55:53
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `nutriapp`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `peso` decimal(5,2) NOT NULL,
  `altura` decimal(5,2) NOT NULL,
  `edad` int(11) NOT NULL,
  `imgPerfil` text DEFAULT NULL,
  `genero` varchar(20) NOT NULL,
  `actividad` varchar(30) NOT NULL,
  `objetivos` text DEFAULT NULL,
  `alergias` text DEFAULT NULL,
  `intolerancias` text DEFAULT NULL,
  `dietas` text DEFAULT NULL,
  `disgusta` text DEFAULT NULL,
  `nivel` varchar(50) DEFAULT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `correo`, `contraseña`, `peso`, `altura`, `edad`, `imgPerfil`, `genero`, `actividad`, `objetivos`, `alergias`, `intolerancias`, `dietas`, `disgusta`, `nivel`, `creado_en`) VALUES
(1, 'AARON', '23308060610451@cetis61.edu.mx', '12345678', 70.00, 173.00, 17, '', 'hombre', 'sedentario', NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-27 04:19:32'),
(2, 'sosa', 'sosa@gmail.com', '1234', 200.00, 200.00, 170, '', 'mujer', 'sedentario', NULL, NULL, NULL, NULL, NULL, NULL, '2025-11-27 04:26:39');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
