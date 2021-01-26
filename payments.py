from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb
import unittest


payments = Blueprint('payments', __name__)
"""ruta de pagos"""
@payments.route('/payments', methods=['GET', 'POST'])
def list():
    """traer pagos de un cliente especifico"""
    us = None
    if 'username' in session:
        us = session['username']
        if us:
            if request.method == 'POST':
                filter_id = request.form['filter_id']
                print(filter_id)
                from app import app
                mysql = MySQL(app)
                cur = mysql.connection.cursor()
                cur.execute('SELECT * FROM pagos WHERE id = {0}'.format(filter_id))
                data_filter = cur.fetchall()
                if  data_filter:
                    return render_template('pagos.html',pagos = data_filter , rol=session['rol'])
                else:
                    flash('El usuario no existe', 'not_found')
                    return redirect(url_for('payments.list'))
            if request.method == 'GET':
                """traer pagos de todos los clientes"""
                from app import app
                mysql = MySQL(app)
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM pagos")
                data_pagos = cur.fetchall()
                print(data_pagos)
                """renderiza clientes"""
                return render_template('pagos.html',pagos = data_pagos, rol=session['rol'])
    else:
        return render_template('no_conexion.html',error="Debes iniciar sesion")      



@payments.route('/add_payment', methods=['POST'])
def agregar_pago():
    error = ""
    """add user"""
    if request.method == 'POST':
        cedula = request.form['cedula']
        mes = request.form['mes']
        valor = request.form['valor']
        print(cedula)
        print(mes)
        print(valor)
        """check fields before to execute sql sentence"""
        if cedula and mes and valor:
            try:
                from app import app
                mysql = MySQL(app)
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO pagos (id, fecha, valor) VALUES (%s, %s, %s)",
                (cedula, mes, valor))
                mysql.connection.commit()
                flash('Cliente Agregado','confirmation')
                return redirect(url_for('payments.list'))
            except MySQLdb.Error as e:
                print(e)
                flash("El Usuario con la "+ cedula + " no existe", 'error')
                return redirect(url_for('payments.list'))
        else:
            flash('Campos Vacios','error')
            return redirect(url_for('payments.list'))

@payments.route('/delete_payment/<string:id>')
def borrar_pago(id):
    """eliminar cliente"""
    
    from app import app
    mysql = MySQL(app)
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pagos WHERE pago_id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro Eliminado', 'confirmation')
    return redirect(url_for('payments.list'))

@payments.route('/edit_payment/<string:id>', methods=['GET', 'POST'])
def obtener_pago(id):
    """edit payment"""
    from app import app
    mysql = MySQL(app)
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pagos WHERE pago_id = {0}'.format(id))
        data = cur.fetchall()
        print(data[0])
        return render_template('edit_pago.html', pago = data[0])
    
    if request.method == 'POST':
        id_value = request.form['id']
        date_value = request.form['payment_date']
        cost_value = request.form['value']
        payment_id = id
        if id_value and date_value and cost_value:
            try:
                cur = mysql.connection.cursor()
                cur.execute("""
                UPDATE pagos
                SET id = %s,
                    fecha = %s,
                    valor = %s
                WHERE pago_id = %s
                """,(id_value, date_value, cost_value, payment_id))
                mysql.connection.commit()
                flash('Pago Actualizado','confirmation')
                return redirect(url_for('payments.list'))
            except MySQLdb.Error as e:
                print(e)
                flash("No se pudo actualizar el pago", 'error')
                return redirect(url_for('payments.list'))
        else:
            flash('Hay Campos Vacios','error')
            return redirect(url_for('payments.list'))