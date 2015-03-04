from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app, db, models
from .forms import PostForm, ReplyForm
from .models import Post
from datetime import datetime, timezone
from sqlalchemy import func
from werkzeug import secure_filename
from config import ALLOWED_EXTENSIONS
import os
import hashlib

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
		
		timestamp = datetime.utcnow()
			
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			# path is hardcoded because using app.config appears to give different paths for save and send_from_directory, so they must be manually changed to be consistent
			# save will give a FileNotFoundError if the directory does not exist
			fname = time_filename(timestamp, filename)
			file.save("app/uploads/" + fname)
		
		nametrip = generate_tripcode(name)
		
		post = Post(body=form.body.data, 
					title=form.title.data, 
					name=nametrip[0],
					thread_id=new_thread_id,
					timestamp=timestamp,
					email=form.email.data,
					tripcode=nametrip[1],
					filename=filename,
					fname=fname)
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
			
		timestamp = datetime.utcnow()
			
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			fname = time_filename(timestamp, filename)
			file.save("app/uploads/" + fname)
			
			
		nametrip = generate_tripcode(name)
		
		
		post = Post(body=form.body.data,
					title="",
					name=nametrip[0],
					thread_id=thread_id,
					timestamp=datetime.utcnow(),
					email=form.email.data,
					tripcode=nametrip[1],
					filename=filename,
					fname=fname)
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
	# send_from_directory will attempt to load any particular file from either "uploads" or "app/uploads", chosen seemingly at random. link the two folders or it will not function consistently
	return send_from_directory("uploads", filename)
		
def time_filename(timestamp, filename):
	return str(int(timestamp.replace(tzinfo=timezone.utc).timestamp()*1000)) + "." + filename.rsplit('.', 1)[1]
	
def generate_tripcode(name):
	# returns a list containing the name and a hashed tripcode
	nametrip = name.rsplit(sep="#", maxsplit=1)
	if len(nametrip) == 1:
		nametrip.append("")
	else:
		hash_object = hashlib.md5(nametrip[1].encode())
		nametrip[1] = hash_object.hexdigest()[0:10]
	return nametrip

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500
