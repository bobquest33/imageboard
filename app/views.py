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
		post = Post(body=form.body.data, 
					title=form.title.data, 
					name=form.name.data,
					thread_id=1,
					timestamp=datetime.utcnow(),
					email="",
					tripcode="")
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('index.html', title='Main Page', form=form)


@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500
