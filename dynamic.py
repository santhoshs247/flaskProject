from flask import Flask, render_template, request
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
    
    # Fetch results for display
    rows = result.fetchall()
    
    return f"<h2>Thank you! Your data has been stored successfully.</h2>"

# RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)