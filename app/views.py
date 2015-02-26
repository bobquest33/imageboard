from flask import render_template, flash, redirect, url_for
from app import app, db, models
from .forms import PostForm
from .models import Post
from datetime import datetime


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		flash("Post submitted")
		new_thread_id=db.session.query(db.func.max(Post.id)).scalar() + 1
		post = Post(body=form.body.data, 
					title=form.title.data, 
					name=form.name.data,
					thread_id=new_thread_id,
					timestamp=datetime.utcnow(),
					email="",
					tripcode="")
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	posts = models.Post.query.filter(models.Post.id==models.Post.thread_id).all()
	return render_template('index.html', title='Main Page', form=form, posts=posts)
	
	
@app.route('/thread/<int:thread_id>', methods=['GET','POST'])
def thread(thread_id):
	form = PostForm()
	if form.validate_on_submit():
		flash("Reply submitted")
		post = Post(body=form.body.data,
					title="",
					name=form.name.data,
					thread_id=thread_id,
					timestamp=datetime.utcnow(),
					email="",
					tripcode="")
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('thread', thread_id=thread_id))
	posts = models.Post.query.filter(models.Post.thread_id==thread_id).all()
	return render_template('index.html', title='coming soon', form=form, posts=posts)


@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500
