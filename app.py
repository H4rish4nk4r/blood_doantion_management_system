# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hari123'
app.config['MYSQL_DB'] = 'project'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = mysql.cursor()

# Home page with the form
@app.route('/')
def index():
    return render_template('index1.html')

# User registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        hospid = request.form['hospid']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='sha256')

        cursor.execute("INSERT INTO hospitals (hospid, password) VALUES (%s, %s)", (hospid, hashed_password))
        mysql.commit()

        flash('Account created successfully', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hospid = request.form['hospid']
        password = request.form['password']

        cursor.execute("SELECT * FROM hospitals WHERE hospid = %s", (hospid,))
        hospital = cursor.fetchone()

        if hospital and check_password_hash(hospital[1], password):  # Assuming password is the second column
            flash('Login successful', 'success')
            # Add session handling or user authentication here if needed
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your Hospital ID and password.', 'danger')

    return render_template('login.html')

# Handling form submission
@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    age = int(request.form['age'])
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    blood_group = request.form['bloodGroup']

    # Insert the data into the UserInformation table
    cursor.execute("""
        INSERT INTO UserInformation (name, age, email, phone, address, bloodGroup)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, age, email, phone, address, blood_group))

    mysql.commit()

    return render_template('registration_completed.html')

# Search users by blood type
@app.route('/search_users', methods=['GET', 'POST'])
def search_users():
    if request.method == 'POST':
        blood_type = request.form['bloodType']
        # Query the database to get users with the selected blood type
        cursor.execute("""
            SELECT * FROM UserInformation WHERE bloodGroup = %s
        """, (blood_type,))
        users = cursor.fetchall()
        return render_template('search_users.html', users=users)

    return render_template('search_users.html', users=None)

if __name__ == '__main__':
    app.run(debug=True,port=5001)
