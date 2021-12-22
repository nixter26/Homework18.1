from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy
from sqlalchemy_pagination import paginate

app = Flask(__name__)

#spajamo na bazu podataka

db = SQLAlchemy("sqlite:///db.sqlite")

#definiramo tablicu unutar baze

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)

#kreiranje baze
db.create_all()

@app.route("/", methods=["GET"])
def index():
    page = request.args.get("page")

    if not page:
        page=1

    messages_query = db.query(Message)

    messages = paginate(query=messages_query, page=int(page), page_size=5)

    return render_template("index.html", messages=messages)

@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.form.get("username")
    text = request.form.get("text")

    print(username)
    print(text)

    message = Message(author=username, text=text)
    message.save()

    return redirect("/")

if __name__ == "__main__":
    app.run()