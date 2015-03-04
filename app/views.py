from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app, db, models
from .forms import PostForm, ReplyForm
from .models import Post
from datetime import datetime
from sqlalchemy import func
from werkzeug import secure_filename
from config import ALLOWED_EXTENSIONS
import os

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	form = PostForm()
	if form.validate_on_submit():
		flash("Post submitted")
		# type isn't an int if the db has no entries
		if type(db.session.query(db.func.max(Post.id)).scalar()) == int:
			new_thread_id = db.session.query(db.func.max(Post.id)).scalar() + 1
		else:
			new_thread_id = 1
			
		if form.name.data=="":
			name = "Anonymous"
		else:
			name = form.name.data
		
			
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save("app/uploads/" + filename)
		
		post = Post(body=form.body.data, 
					title=form.title.data, 
					name=name,
					thread_id=new_thread_id,
					timestamp=datetime.utcnow(),
					email=form.email.data,
					tripcode="",
					filename=filename)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
		
	posts = models.Post.query.join(models.Post.thread_posts, aliased=True).group_by(models.Post).order_by(func.max(models.Post.timestamp).desc())
	return render_template('index.html', title='Main Page', form=form, posts=posts)
	
	
@app.route('/thread/<int:thread_id>', methods=['GET','POST'])
def thread(thread_id):
	form = ReplyForm()
	if form.validate_on_submit():
		flash("Reply submitted")
		
		if form.name.data=="":
			name = "Anonymous"
		else:
			name = form.name.data
			
		post = Post(body=form.body.data,
					title="",
					name=name,
					thread_id=thread_id,
					timestamp=datetime.utcnow(),
					email="",
					tripcode="")
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('thread', thread_id=thread_id))
	posts = models.Post.query.filter(models.Post.thread_id==thread_id)
	return render_template('thread.html', title='Thread '+str(thread_id), form=form, posts=posts)


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
		
@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
	#return render_template('image.html')
	return send_from_directory("uploads", filename)
		

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500
