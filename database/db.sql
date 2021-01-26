-- create database
CREATE DATABASE solidnetwork;

--UTILIZANDO DATABASE
use solidnetwork;

--create table cliente

CREATE TABLE IF NOT EXISTS cliente (
    id INT(20) UNSIGNED,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono INT(20) UNSIGNED,
    correo VARCHAR(50),
    PRIMARY KEY (id)
) ENGINE=InnoDB;


CREATE TABLE IF NOT EXISTS pagos ( 
        pago_id BIGINT UNSIGNED AUTO_INCREMENT,
        id INT(20) UNSIGNED,
        fecha date NOT NULL,
        valor INT(20) UNSIGNED,
        PRIMARY KEY (pago_id),
        FOREIGN KEY (id) REFERENCES cliente(id)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS users (
    id INT(3) UNSIGNED UNIQUE,
    user VARCHAR(50) NOT NULL,
    pass VARCHAR(50) NOT NULL,
    rol VARCHAR(2) NOT NULL,
    PRIMARY KEY (user)
);

select * from pagos where id = 23423 order by fecha limit 3;
--MOSTRAR TABLAS

SHOW TABLES;

--DESCRIBIR LA TABLA

describe cliente;

INSERT INTO users VALUES(1, 'solu',SHA1('12345'), 1);
