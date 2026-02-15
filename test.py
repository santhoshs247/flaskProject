from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    test = {
        "name": "santhosh",
        "age": 20
    }

    return render_template("main.html",test=test)

if __name__ == '__main__':
    app.run(debug=True)
