from app import db

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	thread_id = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime)
	title = db.Column(db.String(64))
	name = db.Column(db.String(64))
	tripcode = db.Column(db.String(64))
	email = db.Column(db.String(64))
	body = db.Column(db.String(1000))

	def is_thread(self):
		return id == thread_id

	def threads():
		return Post.query.filter(is_thread).order_by(Post.timestamp.desc())