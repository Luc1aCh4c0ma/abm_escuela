CREATE DATABASE IF NOT EXISTS ESCUELA;

USE ESCUELA;

CREATE TABLE Carreras (
IDCARRERA INT PRIMARY KEY auto_increment ,
NOMBRE VARCHAR(255) NOT NULL,
DURACION INT
);

CREATE TABLE EstadoAlumno (
IDESTADOALUMNO INT PRIMARY KEY auto_increment,
NOMBRE VARCHAR(255) NOT NULL
);

CREATE TABLE Alumnos (

IDALUMNO INT PRIMARY KEY auto_increment,
NOMBRE VARCHAR(255) NOT NULL,
APELLIDO VARCHAR(255) NOT NULL,
DNI VARCHAR(20) NOT NULL,
IDCARRERA INT NOT NULL,
IDESTADOALUMNO INT NOT NULL,
FOREIGN KEY (IDCARRERA) REFERENCES Carreras(IDCARRERA),
FOREIGN KEY (IDESTADOALUMNO) REFERENCES EstadoAlumno(IDESTADOALUMNO)
);

INSERT INTO EstadoAlumno (nombre)VALUES 
('REGULAR'),
('LIBRE'),
('PROMOCIONADO');

INSERT INTO Carreras (nombre, duracion) VALUES
('SOFTWARE', 3),
('DISEÑO', 2),
('TURISMO', 4);

INSERT INTO Alumnos (nombre, apellido, dni, idcarrera, idestadoalumno) VALUES
('Carlos', 'Juarez', '33.589.560', 2, 1),
('Luis', 'Gonzalez', '44.123.789', 1, 2),
('Ana', 'Perez', '22.456.890', 3, 3),
('Maria', 'Lopez', '12.345.678', 2, 1),
('Diego', 'Martinez', '89.765.432', 1, 2),
('Laura', 'Rodriguez', '55.678.901',2,3),
('Pedro', 'Hernandez', '44.567.890.', 3, 1),
('Sofia', 'Garcia', '11.234.567', 2, 2),
('Juan', 'Diaz', '09.876.543', 1, 3),
('Monica', 'Fernandez', '66.789.012', 3, 1);

use escuela;
ALTER TABLE alumnos
ADD COLUMN Estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo';



