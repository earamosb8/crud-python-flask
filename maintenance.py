from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash , make_response, session
from flask_mysqldb import MySQL
import MySQLdb
import unittest
import pdfkit


maintenance = Blueprint('maintenance', __name__)

@maintenance.route('/maintenance', methods = ['GET','POST'])
def view_maintenance():
    us = None
    if 'username' in session:
        us = session['username']
        print(session['rol'])
        if us:
            if request.method == 'GET':
                return render_template('maintenance.html', rol = session['rol'])
            if request.method == 'POST':
                from app import app
                mysql = MySQL(app)
                try:
                    cur = mysql.connection.cursor()
                    cur.execute('DROP TABLE IF EXISTS pagos')
                    cur = mysql.connection.cursor()
                    cur.execute("""CREATE TABLE IF NOT EXISTS pagos ( 
                                    pago_id BIGINT UNSIGNED AUTO_INCREMENT,
                                    id INT(20) UNSIGNED,
                                    fecha date NOT NULL,
                                    valor INT(20) UNSIGNED,
                                    PRIMARY KEY (pago_id),
                                    FOREIGN KEY (id) REFERENCES cliente(id)
                                    )ENGINE=InnoDB;""")
                except MySQLdb.Error as e:
                    print(e)
                    return render_template('no_conexion.html',error=e)

                return render_template('maintenance.html', rol = session['rol'], msj = "Mantenimiento Realizado")
    else:
        return render_template('no_conexion.html',error="Debes iniciar sesion")