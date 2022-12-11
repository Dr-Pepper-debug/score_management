from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30))
    title = db.Column(db.String(30))
    composer = db.Column(db.String(30))
    arranger = db.Column(db.String(30))

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
        
        new_score = Post(number=number, title=title, composer=composer, arranger=arranger)

        db.session.add(new_score)
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

@app.route('/score_search', methods=['GET', 'POST'])
def score_search():
    if request.method == 'GET':
        return render_template('score_search.html')
    if request.method == 'POST':
        form_title = request.form.get("title")  # str
        search_results = db.session.query(Post).filter(Post.title == form_title)
        return render_template('result.html', search_results=search_results)

        # scores = Post.query.all()
        # return render_template('score_search.html', scores=scores)

@app.route('/scores/<int:id>/delete', methods=['POST'])  
def score_delete(id):  
    score = Post.query.get(id)   
    db.session.delete(score)  
    db.session.commit()  
    return redirect(url_for('score_list'))

@app.route('/scores/<int:id>/edit', methods=['GET'])
def score_edit(id):
    # 編集ページ表示用
    score = Post.query.get(id)
    return render_template('score_edit.html', score=score)

@app.route('/scores/<int:id>/update', methods=['POST'])
def score_update(id):
    score = Post.query.get(id)  # 更新するデータをDBから取得
    score.number = request.form.get("number")  # str
    score.title = request.form.get("title")  # str
    score.composer = request.form.get("composer")  # str
    score.arranger = request.form.get("arranger")  # str

    db.session.merge(score)
    db.session.commit()
    return redirect(url_for('score_list'))

if __name__ == "__main__":
    app.run(debug=True)