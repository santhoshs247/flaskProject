from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import 'text' for executing raw SQL

# CREATE THE FLASK APP
app = Flask(__name__)

# DATABASE CONFIGURATION
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sandy566@127.0.0.1:3306/mysql"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INITIALIZE DATABASE
db = SQLAlchemy(app)

# EXECUTE RAW SQL QUERIES WITH PROPER CONNECTION
with app.app_context():
    with db.engine.connect() as connection:
        # CREATE TABLE IF NOT EXISTS
         
        connection.execute(text('''
            CREATE TABLE IF NOT EXISTS stds (
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                passwd VARCHAR(50)
            );
        '''))
        
        # INSERT DATA INTO users TABLE
        connection.execute(text('''
            INSERT INTO users(email, first_name, last_name, passwd) VALUES         
            ('sai@gmail.com', 'sai', 'abhyankkar', 'sai@123')
        '''))
        connection.execute(text('''
            INSERT INTO stds(first_name, last_name, passwd) VALUES         
            ('sai', 'abhyankkar', 'sai@123'),
            ('shiva', 'abhyankkar', 'shiva@123'),
            ('krishna', 'raj', 'raj@123')
        '''))
        # COMMIT CHANGES
        connection.commit()
        
        # CLOSE THE CONNECTION
        connection.close()
    

# RUN THE APP
if __name__ == '__main__':
    app.run()