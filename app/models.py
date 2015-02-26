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

	def __repr__(self):
		return '<Post %r>' % self.id
		
	def thread_posts(self):
		return Post.query.filter(Post.thread_id==self.thread_id).order_by(models.Post.timestamp.desc())
