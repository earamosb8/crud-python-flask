from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager
import MySQLdb
import unittest
from customers import customers
from payments import payments


loginmanager = LoginManager()


app = Flask(__name__)
app.register_blueprint(customers)
app.register_blueprint(payments)

#mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'solidnetwork'
mysql = MySQL(app)
 # settings
app.secret_key = 'mysecretkey'



@app.cli.command()
def test():
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(test)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error=error)





@app.route('/login_post()', methods=['POST'])
def login_post():
    return redirect(url_for(login_post))

@app.route('/login')
def login():
    
    return render_template('login.html')
    
  
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 7070, debug = True)