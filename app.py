from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------------------------
# Base de datos
# ---------------------------
def init_db():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------------------
# Rutas del sistema
# ---------------------------
@app.route('/')
def index():
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        ''', (nombre, categoria, precio, stock))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        cursor.execute('''
            UPDATE productos
            SET nombre = ?, categoria = ?, precio = ?, stock = ?
            WHERE id = ?
        ''', (nombre, categoria, precio, stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)