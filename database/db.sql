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
        pago_id BIGINT UNSIGNED AUTO_INCREMENT,
        id INT(20) UNSIGNED,
        fecha date NOT NULL,
        valor INT(20) UNSIGNED,
        PRIMARY KEY (pago_id),
        FOREIGN KEY (id) REFERENCES cliente(id)
)ENGINE=InnoDB;

CREATE TABLE users (
    user VARCHAR(50) NOT NULL,
    pass VARCHAR(50) NOT NULL,
    rol VARCHAR(2) NOT NULL,
    PRIMARY KEY (user)
);

select * from pagos where id = 1062286458 order by fecha limit 4;
--MOSTRAR TABLAS

SHOW TABLES;

--DESCRIBIR LA TABLA

describe cliente;
