from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail

app=Flask(__name__)
app.secret_key = 'super-secret-key'


with open('config.json','r') as c:
    params=json.load(c)['params']

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mirzadanish7218@gmail.com'
app.config['MAIL_PASSWORD'] = 'sgmcsziwsqstvkyd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


db=SQLAlchemy(app)

class Client(db.Model):
    sn=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    subject=db.Column(db.String(50),nullable=False)
    comment=db.Column(db.String(50),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)


class Todo(db.Model):
    sn=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    


@app.route('/')
def home():
    return render_template("index.html",params=params)

@app.route('/about')
def about():
    return render_template("about.html",params=params)

@app.route('/contact', methods=["GET",'POST'])
def contact():
    if request.method=="POST":
       name=request.form ["names"]
       email=request.form["emails"]
       subjct=request.form["subjects"]
       comment=request.form["comments"]
       entry=Client(name=name,email=email,subject=subjct,comment=comment)
       db.session.add(entry)
       db.session.commit()
       mail.send_message("the message from"+name+"  "+email,
       sender=email,
       recipients=["mirzadanish7218@gmail.com"],
       body = 'Hello Flask message sent from Flask-Mail'
       )
      




    return render_template("contact.html",params=params)

    
@app.route('/services')
def services():
    return render_template("services.html")



@app.route('/login', methods=['GET','POST'])
def login():
    if "user" in session and  session['user']==params['username']:
        return render_template("dashboard.html",params=params)
        
    if request.method=='POST':
        username=request.form.get("username")
        password=request.form.get("password")
        if username==params['username'] and password==params['password']:
          session['user']=username
          return redirect("/dashboard")
       
    else:
        return render_template("login.html")

    return render_template("login.html",params=params)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
     if request.method=='POST':
            adds=request.form['inputfeild']
            ntry=Todo(title=adds)
            db.session.add(ntry)
            db.session.commit()
           
          
            # return redirect("/dashboard")
       
     jindagiss=Todo.query.all()
     return render_template("dashboard.html",params=params,jindagis=jindagiss)





    
@app.route('/update/<int:sn>',methods=['GET','POST'])
def update(sn):
    if request.method=='POST':
        add=request.form['inputfeild'] 
        
        jindagiss=Todo(title=add)
        jindagiss=Todo.query.filter_by(sn=sn).first()
        jindagiss.title=add
        db.session.add(jindagiss)
        db.session.commit()
      
        return redirect("/dashboard")
    jindagiss=Todo.query.filter_by(sn=sn).first()    
    return render_template('update.html',jindagi=jindagiss)

    
@app.route('/delete/<int:sn>')
def delete(sn):
    todo=Todo.query.filter_by(sn=sn).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/dashboard')


    
    


@app.route('/new',methods=['GET','POST'])
def new():
 


    return render_template('new.html')

            

    

    


if __name__ == "__main__":
    app.run(debug=True,port=5001)






# hcpkfnhbrrhzfbay


