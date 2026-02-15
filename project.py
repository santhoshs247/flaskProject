from flask import Flask
app = Flask(__name__)
@app.route(rule='/')
def index():
    return "<h1>Hello Flask</h1>"
@app.route('/hello')
def hello():
    return "<h1>Hello Friends</h1>"
@app.route('/hello/<name>')
def hello_name(name):
    return f"<h1>Hello Guys, I am {name}!</h1>"
@app.route('/hello/<name>/<age>')
def hello_age(name, age):
    return f"<h1>Hello Friends, I am {name} and I am {age} years old!</h1>"
if __name__ == '__main__':
    app.run(debug=True)