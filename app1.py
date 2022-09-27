from flask import Flask, render_template, request, redirect
from  flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rmsidrk9!'
app.config['MYSQL_DB'] = 'flaskapp.db'
mysql = MySQL(app)

@app.route('/', methods=['GET' 'POST'])
def index():
    if request.method == 'POST':
        
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email VALUES(%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
    return render_template('index1.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = ("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)
if __name__ == '__main__':
    app.run(port=5001, debug=True)