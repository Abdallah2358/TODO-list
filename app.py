from flask import Flask ,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import PrimaryKeyConstraint 
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class todo (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column (db.String (200), nullable= False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow )

def __repr__(self):
    return '<Task %r>'% self.id 


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/' , methods = ['POST','GET'])
def index ():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return  redirect('/')
        except:
            return"you are not good person :("
    else:
        Tasks =todo.query.order_by(todo.date_created).all()
        return render_template("index.html",tasks=Tasks)
         
@app.route('/delete/<int:id>')

def delete(id):
    task_to_delete =todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')    
    except:
        return "you should really do it "


@app.route('/update/<int:id>', methods =['GET', 'POST'])
def update(id):
    task_to_update = todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content =request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "you really should start doing it "
    else:
        return render_template('update.html' , task = task_to_update)


 
if __name__ == "__main__":
    app.run(debug=True)