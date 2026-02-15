from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("app.html")
@app.route('/form_post',methods=['POST'])
def form_post():
    username=request.form.get('username')
    email=request.form.get('email')
    age=request.form.get('age')
    
    return render_template('formdata.html',username=username,email=email,age=age)

if __name__ == '__main__':
    app.run(debug=True)
