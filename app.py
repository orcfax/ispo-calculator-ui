from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
db_location = "database.sqlite"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key_value = request.form['key_value']

        db = sqlite3.connect(db_location)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM item WHERE id=?", (key_value,),)

        result = cursor.fetchone()
        if result:
            return render_template('rewards.html', result='yes')
        else:
            return render_template('rewards.html', result='no')
        

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)