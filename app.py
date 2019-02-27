from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
import datetime

app = Flask(__name__)

#app.py => sqlalchemy 설정
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db에 app 연동
db.init_app(app)

#migrations
migrate=Migrate(app,db)


@app.route("/")
def index():
    todos=Todo.query.all()
    return render_template("index.html",todos=todos)
    
    
# @app.route("/new")
# def new():
#     return render_template("new.html")

# @app.route("/create", methods=["POST"])
# def create():
#     title=request.form["title"]
#     deadline=request.form["deadline"]
#     deadline=datetime.datetime.strptime(deadline,'%Y-%m-%d')
    
#     todo=Todo(title=title,deadline=deadline)
    
#     db.session.add(todo)
#     db.session.commit()
    
#     return redirect('/')
    
    
@app.route("/create",methods=["POST","GET"])
def create():
    if request.method == "POST":
        #POST방식으로 들어왔을 때
        title=request.form["title"]
        deadline=request.form["deadline"]
        deadline=datetime.datetime.strptime(deadline,'%Y-%m-%d')
        
        todo=Todo(title=title,deadline=deadline)
        
        db.session.add(todo)
        db.session.commit()
        
        return redirect('/')
    else:
        #GET방식으로 들어왔을 때
        return render_template("new.html")
        

@app.route("/<int:id>/delete")
def delete(id):
    todo=Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    
    return redirect('/')
    
@app.route("/<int:id>/update",methods=["POST","GET"])
def update(id):
    todo=Todo.query.get(id) #원본데이터 저장 되어있는 곳
    if request.method == "POST":
        title=request.form["title"]
        deadline=request.form["deadline"]
        deadline=datetime.datetime.strptime(deadline,'%Y-%m-%d')
        
        todo.title=title
        todo.deadline=deadline
        
        db.session.commit()
        
        return redirect('/')
        
    else:
        return render_template("update.html",todo=todo)


@app.route("/<int:id>")
def read(id):
    todo=Todo.query.get(id)
    return render_template("read.html",todo=todo)
    
@app.route("/<int:id>/comment", methods=["POST"])
def comment(id):
    content=request.form["content"]
    
    comment=Comment(content=content)
    
    todo = Todo.query.get(id)
    todo.comments.append(comment)
    
    db.session.add(comment)
    db.session.commit()
    
    return redirect(f"/{id}")



if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)