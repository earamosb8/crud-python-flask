from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb




app = Flask(__name__)
#mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'solidnetwork'
mysql = MySQL(app)
 # settings
app.secret_key = 'mysecretkey'

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
    cur.execute('DELETE FROM cliente WHERE id = {0}'.format(cedula))
    mysql.connection.commit()
    flash('Cliente Eliminado', 'confirmation')
    return redirect(url_for('index'))

"""ruta de pagos"""
@app.route('/pagos')
def pago():
    """agregar cliente"""
    return render_template('pagos.html')
    

if __name__ == '__main__':
  app.run(host='0.0.0.0', port = 7070, debug = True)
  