from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'finanzas_personales'
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deudas', methods=['GET', 'POST'])
def deudas():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        fecha = datetime.now().strftime('%Y-%m-%d')

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO deudas (descripcion, monto, fecha) VALUES (%s, %s, %s)', (descripcion, monto, fecha))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('deudas'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM deudas')
    deudas = cursor.fetchall()
    cursor.close()

    return render_template('deudas.html', deudas=deudas)

@app.route('/ingresos', methods=['GET', 'POST'])
def ingresos():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        fecha = datetime.now().strftime('%Y-%m-%d')

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO ingresos (descripcion, monto, fecha) VALUES (%s, %s, %s)', (descripcion, monto, fecha))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('ingresos'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM ingresos')
    ingresos = cursor.fetchall()
    cursor.close()

    return render_template('ingresos.html', ingresos=ingresos)

@app.route('/historial')
def historial():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM deudas')
    deudas = cursor.fetchall()
    
    cursor.execute('SELECT * FROM ingresos')
    ingresos = cursor.fetchall()
    
    cursor.close()
    
    return render_template('historial.html', deudas=deudas, ingresos=ingresos)

if __name__ == '__main__':
    app.run(debug=True)
