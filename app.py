from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager
import MySQLdb

loginmanager = LoginManager()


app = Flask(__name__)
#mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'solidnetwork'
mysql = MySQL(app)
 # settings
app.secret_key = 'mysecretkey'


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cliente")
    data = cur.fetchall()
    print(data)
    """agregar cliente"""
    return render_template('index.html', clientes = data)

@app.route('/add_contact', methods=['POST'])
def add():
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
                return redirect(url_for('index'))
            except MySQLdb.Error as e:
                print(e)
                flash("El Usuario con la "+ cedula + " ya existe", 'error')
                return redirect(url_for('index'))
        else:
            flash('Campos Vacios','error')
            return redirect(url_for('index'))

@app.route('/edit/<string:cedula>')
def get_contact(cedula):
    """edit user"""
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE id = {0}'.format(cedula))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit_contact.html', cliente = data[0])

@app.route('/update/<string:cedula>', methods = ['POST'])
def update_contact(cedula):
    """actualizar cliente"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']

        if cedula and nombre and telefono and direccion:
            try:
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
                return redirect(url_for('index'))
            except MySQLdb.Error as e:
                print(e)
                flash("No se pudo actualizar el usuario", 'error')
                return redirect(url_for('index'))
        else:
            flash('Hay Campos Vacios','error')
            return redirect(url_for('index'))
            

@app.route('/delete/<string:cedula>')
def delete_contact(cedula):
    """eliminar cliente"""
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pagos WHERE id = {0}'.format(cedula))
    cur.execute('DELETE FROM cliente WHERE id = {0}'.format(cedula))
    
    mysql.connection.commit()
    flash('Cliente Eliminado', 'confirmation')
    return redirect(url_for('index'))

"""ruta de pagos"""
@app.route('/pagos', methods=['GET', 'POST'])
def pagos():
    """traer pagos de un cliente especifico"""
    if request.method == 'POST':
        filter_id = request.form['filter_id']
        print(filter_id)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pagos WHERE id = {0}'.format(filter_id))
        data_filter = cur.fetchall()
        if  data_filter:
            return render_template('pagos.html',pagos = data_filter)
        else:
            flash('El usuario no existe', 'not_found')
            return redirect(url_for('pagos'))
    else:
        """traer pagos de todos los clientes"""
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pagos")
        data_pagos = cur.fetchall()
        print(data_pagos)
        """renderiza clientes"""
        return render_template('pagos.html',pagos = data_pagos)

@app.route('/agregar_pago', methods=['POST'])
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
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO pagos (id, fecha, valor) VALUES (%s, %s, %s)",
                (cedula, mes, valor))
                mysql.connection.commit()
                flash('Cliente Agregado','confirmation')
                return redirect(url_for('pagos'))
            except MySQLdb.Error as e:
                print(e)
                flash("El Usuario con la "+ cedula + " no existe", 'error')
                return redirect(url_for('pagos'))
        else:
            flash('Campos Vacios','error')
            return redirect(url_for('pagos'))

@app.route('/borrar_pago/<string:id>')
def borrar_pago(id):
    """eliminar cliente"""
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pagos WHERE pago_id = {0}'.format(id))
    mysql.connection.commit()
    flash('Registro Eliminado', 'confirmation')
    return redirect(url_for('pagos'))

@app.route('/editar_pago/<string:id>')
def obtener_pago(id):
    """edit user"""
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pagos WHERE pago_id = {0}'.format(id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit_pago.html', pago = data[0])


@app.route('/login_post()', methods=['POST'])
def login_post():
    return redirect(url_for(login_post))

@app.route('/login')
def login():
    
    return render_template('login.html')
    
  
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 7070, debug = True)