from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = '7nx278n2rx7n2xn78t2xnt782xtn78    '  # Enkel hemmelig nøkkel for utvikling

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Database hjelpefunksjon
def get_db():
    db = sqlite3.connect('confessions.db')
    db.row_factory = sqlite3.Row
    return db

# Opprett databasetabell
with app.app_context():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS confessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,  
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    db.commit()
    db.close()

# Ruter
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error=True)
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    db = get_db()
    confessions = db.execute("SELECT * FROM confessions ORDER BY timestamp DESC").fetchall()
    db.close()
    return render_template('admin_dashboard.html', confessions=[dict(row) for row in confessions])

@app.route('/admin/delete/<int:confession_id>', methods=['POST'])
@login_required
def delete_confession(confession_id):
    db = get_db()
    db.execute("DELETE FROM confessions WHERE id = ?", (confession_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Slettet'})

@app.route('/confess', methods=['POST'])
def confess():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'Innhold kreves'}), 400
        
    db = get_db()
    db.execute("INSERT INTO confessions (content) VALUES (?)", (content,))
    db.commit()
    db.close()
    return jsonify({'message': 'Suksess'}), 201

@app.route('/confessions')
def get_confessions():
    db = get_db()
    confessions = db.execute("SELECT * FROM confessions ORDER BY timestamp DESC").fetchall()
    db.close()
    return jsonify([dict(row) for row in confessions])

if __name__ == '__main__':
    app.run(debug=True)
