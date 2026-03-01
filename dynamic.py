from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import 'text' for executing raw SQL
from datetime import datetime, timedelta

# CREATE THE FLASK APP
app = Flask(__name__)

# SECRET KEY FOR SESSION MANAGEMENT
app.secret_key = 'sandy566'

# DATABASE CONFIGURATION - Use 'flask' database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sandy566@127.0.0.1:3306/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INITIALIZE DATABASE
db = SQLAlchemy(app)

# SESSION TIMEOUT IN MINUTES
SESSION_TIMEOUT = 1

# FUNCTION TO CHECK SESSION VALIDITY
def check_session():
    if 'logged_in' not in session:
        return False
    
    # Check if session has expired (1 minute timeout)
    last_activity = session.get('last_activity')
    if last_activity:
        elapsed = datetime.now() - datetime.fromisoformat(last_activity)
        if elapsed > timedelta(minutes=SESSION_TIMEOUT):
            # Session expired
            session.clear()
            return False
    
    # Update last activity time
    session['last_activity'] = datetime.now().isoformat()
    return True

# ROUTE TO DISPLAY THE FORM (PROTECTED)
@app.route('/')
def sql_form():
    # If user is already logged in, redirect to flask page
    if check_session():
        return redirect(url_for('flask_page'))
    return render_template('sql.html')

# ROUTE TO HANDLE FORM SUBMISSION
@app.route('/submit', methods=['POST'])
def submit_form():
    # GET VALUES FROM THE FORM
    a = request.form.get('name')
    b = request.form.get('email')
    c = request.form.get('password')
    
    # INSERT DATA INTO form TABLE
    with app.app_context():
        with db.engine.connect() as connection:
            # Use text() to wrap raw SQL strings for SQLAlchemy 2.0+
            connection.execute(text('CREATE TABLE IF NOT EXISTS form (name VARCHAR(50), email VARCHAR(50), password VARCHAR(50))'))
            connection.execute(
                text('INSERT INTO form (name, email, password) VALUES (:name, :email, :password)'),
                {'name': a, 'email': b, 'password': c})
            result = connection.execute(text('SELECT * FROM form'))
            connection.commit()
            connection.close()
    
    # Fetch results for display
    rows = result.fetchall()
    
    return render_template('login.html')

# ROUTE FOR LOGIN PAGE
@app.route('/login')
def login():
    # If user is already logged in, redirect to flask page
    if check_session():
        return redirect(url_for('flask_page'))
    # Clear any existing session on login page visit
    session.clear()
    return render_template('login.html')

# ROUTE TO HANDLE LOGIN FORM SUBMISSION
@app.route('/login', methods=['POST'])
def login_submit():
    name = request.form.get('name')
    password = request.form.get('password')
    
    # Query database to verify credentials
    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(
                text('SELECT * FROM form WHERE name = :name AND password = :password'),
                {'name': name, 'password': password}
            )
            user = result.fetchone()
            connection.close()
    
    # Check if user exists and credentials match
    if user:
        # Login successful - set session variables
        session['logged_in'] = True
        session['username'] = name
        session['last_activity'] = datetime.now().isoformat()
        # Redirect to flask.html after successful login
        return redirect(url_for('flask_page'))
    else:
        # Login failed error
        return f"<p>Invalid username or password</p>"

# ROUTE TO DISPLAY USERS IN DB PAGE (PROTECTED)
@app.route('/db')
def show_db_users():
    # Check session validity - redirect to login if not valid
    if not check_session():
        return redirect(url_for('login'))
    
    # Query all users from the database
    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT name, email FROM form'))
            users = result.fetchall()
            connection.close()
    
    return render_template('db.html', users=users)

# ROUTE FOR FLASK.HTML (PROTECTED)
@app.route('/flask')
def flask_page():
    # Check session validity - will redirect to login if not valid
    if not check_session():
        return redirect(url_for('login'))
    return render_template('flask.html')

# ROUTE TO LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)
