-- create database
CREATE DATABASE solidnetwork;

--UTILIZANDO DATABASE
use solidnetwork;

--create table cliente

CREATE TABLE cliente (
    id INT(20) UNSIGNED,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono INT(20) UNSIGNED,
    correo VARCHAR(50),
    PRIMARY KEY (id)
) ENGINE=InnoDB;


CREATE TABLE pagos ( 
        pago_id INT(20) UNSIGNED AUTO_INCREMENT,
        id INT(20) UNSIGNED,
        fecha VARCHAR(50) NOT NULL,
        valor INT(20) UNSIGNED,
        PRIMARY KEY (pago_id),
        FOREIGN KEY (id) REFERENCES cliente(id)
)ENGINE=InnoDB;

ALTER TABLE pagos 
   ADD CONSTRAINT fk_anios
   FOREIGN KEY (id) 
   REFERENCES cliente(id);

--MOSTRAR TABLAS

SHOW TABLES;

--DESCRIBIR LA TABLA

describe cliente;
