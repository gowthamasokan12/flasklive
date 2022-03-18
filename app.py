from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

db = SQLAlchemy(app)
class Students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   addr = db.Column(db.String(200))
   pin = db.Column(db.String(10))

print('working')

@app.route('/', methods=['GET','POST'])
def index():
    try:
        query = Students.query.all()
        studList = []
        for stud in query:
            studList.append({'Name':stud.name,'City':stud.city,'Address':stud.addr,'Pincode':stud.pin})
        return json.dumps(studList[0:3])
    except Exception as ae:
        return str(ae)

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)