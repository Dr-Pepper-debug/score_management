from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    composer = db.Column(db.String(30), nullable=False)
    arranger = db.Column(db.String(30), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)

    else:
        number = request.form.get('number')
        title = request.form.get('title')
        composer = request.form.get('composer')
        arranger = request.form.get('arranger')
        
        new_post = Post(number=number, title=title, composer=composer, arranger=arranger)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@app.route('/add', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        form_number = request.form.get("number")  # str
        form_title = request.form.get("title")  # str
        form_composer = request.form.get("composer")  # str
        form_arranger = request.form.get("arranger")  # str

        score = Post(
            number = form_number,
            title = form_title,
            composer = form_composer,
            arranger = form_arranger
        )
        db.session.add(score)
        db.session.commit()
        return render_template('add.html')
        

@app.route('/score_list')
def score_list():
    scores = Post.query.all()
    return render_template('score_list.html', scores=scores)

if __name__ == "__main__":
    app.run(debug=True)