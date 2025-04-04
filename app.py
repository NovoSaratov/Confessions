from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = '7nx278n2rx7n2xn78t2xnt782xtn78'  # Hemmelig nøllel

# Database konfigurasjon
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1488Aa!.', 
    'database': 'confessions_db'
}

# Tilkobling verifikasjon
def get_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin_login():
    if session.get('logged_in'):
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == 'admin' and password == '1234':  # 
        session['logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html', error=True)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
        
    connection = get_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM confessions ORDER BY timestamp DESC")
            confessions = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('admin_dashboard.html', confessions=confessions)
        except Error as e:
            print(f"Error fetching confessions: {e}")
            return "Database error", 500
    return "Database connection error", 500

@app.route('/admin/delete/<int:confession_id>', methods=['POST'])
def delete_confession(confession_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
        
    connection = get_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM confessions WHERE id = %s", (confession_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'Deleted'})
        except Error as e:
            print(f"Error deleting confession: {e}")
            return "Database error", 500
    return "Database connection error", 500

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/confess', methods=['POST'])
def confess():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Content required'}), 400
        
    connection = get_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO confessions (content) VALUES (%s)", (content,))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'Success'}), 201
        except Error as e:
            print(f"Error inserting confession: {e}")
            return "Database error", 500
    return "Database connection error", 500

@app.route('/confessions')
def get_confessions():
    connection = get_db()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM confessions ORDER BY timestamp DESC")
            confessions = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(confessions)
        except Error as e:
            print(f"Error fetching confessions: {e}")
            return "Database error", 500
    return "Database connection error", 500

if __name__ == '__main__':
    app.run(debug=True)
