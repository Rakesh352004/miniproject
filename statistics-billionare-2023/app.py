from flask import Flask, render_template

app =  Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ =='__main__':
    app.run(host='127.0.0.1',port=5002,debug=True)