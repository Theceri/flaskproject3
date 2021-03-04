from flask import Flask, render_template, request, redirect, url_for
from configs.base_config import *
import psycopg2

app = Flask(__name__)
app.config.from_object(Development)

# Connect to an existing database
conn = psycopg2.connect("dbname='psycopg2' user='postgres' host='localhost' password='1234'")

#Open a cursor to perform database operations
cur = conn.cursor()

#Execute a command: this creates a new table
cur.execute("CREATE TABLE IF NOT EXISTS users (fname varchar, lname varchar, email varchar);")

@app.route('/', methods=['POST', 'GET'])
def base_page():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']

        # Pass data to fill a query placeholders and let Psycopg perform
        cur.execute("INSERT INTO users (fname, lname, email) VALUES (%s, %s, %s)",(fname, lname, email))
        
        # Make the changes to the database persistent
        conn.commit()

        return redirect(url_for("base_page"))
    
    cur.execute("SELECT * from users")
    rows = cur.fetchall()
    print(rows)
    
    return render_template('child.html', rows = rows)

if __name__ == '__main__':
    app.run()