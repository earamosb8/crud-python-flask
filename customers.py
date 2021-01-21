from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager
import MySQLdb
import unittest


customers = Blueprint('customers', __name__)

@customers.route('/')
def list_customers():
    from app import app
    mysql = MySQL(app)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cliente")
    data = cur.fetchall()
    print(data)
    """agregar cliente"""
    return render_template('index.html', clientes = data)

@customers.route('/add_customers', methods=['POST'])
def add():
    from app import app
    mysql = MySQL(app)
    error = ""
    """add user"""
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        print(cedula)
        print(nombre)
        print(telefono)
        print(direccion)
        print(correo)
        """check fields before to execute sql sentence"""
        if cedula and nombre and telefono and direccion:
            try:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO cliente (id, nombre, direccion, telefono, correo) VALUES (%s, %s, %s, %s,%s)",
                (cedula, nombre, direccion, telefono, correo))
                mysql.connection.commit()
                flash('Cliente Agregado','confirmation')
                return redirect(url_for('customers.list_customers'))
            except MySQLdb.Error as e:
                print(e)
                flash("El Usuario con la "+ cedula + " ya existe", 'error')
                return redirect(url_for('customers.list_customers'))
        else:
            flash('Campos Vacios','error')
            return redirect(url_for('customers.list_customers'))

@customers.route('/edit_customer/<string:cedula>' , methods = ['GET','POST'])
def get_contact(cedula):
    """edit user"""
    from app import app
    mysql = MySQL(app)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE id = {0}'.format(cedula))
        data = cur.fetchall()
        print(data[0])
        return render_template('edit_contact.html', cliente = data[0])
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']

        if cedula and nombre and telefono and direccion:
            try:
                from app import app
                mysql = MySQL(app)
                cur = mysql.connection.cursor()
                cur.execute("""
                UPDATE cliente
                SET nombre = %s,
                    direccion = %s,
                    telefono = %s,
                    correo = %s
                WHERE id = %s
                """,(nombre, direccion, telefono, correo, cedula))
                mysql.connection.commit()
                flash('Cliente Actualizado','confirmation')
                return redirect(url_for('customers.list_customers'))
            except MySQLdb.Error as e:
                print(e)
                flash("No se pudo actualizar el usuario", 'error')
                return redirect(url_for('customers.list_customers'))
        else:
            flash('Hay Campos Vacios','error')
            return redirect(url_for('customers.list_customers'))
    
        
@customers.route('/delete_customer/<string:cedula>')
def delete_contact(cedula):
    """eliminar cliente"""
    from app import app
    mysql = MySQL(app)
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pagos WHERE id = {0}'.format(cedula))
    cur.execute('DELETE FROM cliente WHERE id = {0}'.format(cedula))
    
    mysql.connection.commit()
    flash('Cliente Eliminado', 'confirmation')
    return redirect(url_for('customers.list_customers'))

