from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import 'text' for executing raw SQL

# CREATE THE FLASK APP
app = Flask(__name__)

# DATABASE CONFIGURATION - Use 'flask' database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sandy566@127.0.0.1:3306/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INITIALIZE DATABASE
db = SQLAlchemy(app)

# ROUTE TO DISPLAY THE FORM
@app.route('/')
def sql_form():
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
        # Login successful 
        return render_template('flask.html')
    else:
        # Login failed error
        return f"<p>Invalid username or password</p>"

# ROUTE TO DISPLAY USERS IN DB PAGE
@app.route('/db')
def show_db_users():
    # Query all users from the database
    with app.app_context():
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT name, email FROM form'))
            users = result.fetchall()
            connection.close()
    
    return render_template('db.html', users=users)

# RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)
