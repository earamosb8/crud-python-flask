-- create database
CREATE DATABASE solidnetwork;

--UTILIZANDO DATABASE
use solidnetwork;

--create table cliente

CREATE TABLE cliente (
    id INT(20) UNSIGNED PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono INT(20) UNSIGNED
);

--MOSTRAR TABLAS

SHOW TABLES;

--DESCRIBIR LA TABLA

describe cliente;
