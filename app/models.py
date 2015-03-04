from app import db
from datetime import datetime

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	thread_id = db.Column(db.Integer, db.ForeignKey(id))
	timestamp = db.Column(db.DateTime)
	title = db.Column(db.String(64))
	name = db.Column(db.String(64))
	tripcode = db.Column(db.String(64))
	email = db.Column(db.String(64))
	filename = db.Column(db.String(64))
	fname = db.Column(db.String(64))
	body = db.Column(db.String(1000))
	thread_posts = db.relationship('Post',
									backref=db.backref('thread', remote_side=[id]))

	def __repr__(self):
		return '<Post %r>' % self.id
		
	#def __init__(self, thread_id, timestamp=utcnow, last_active=None, title=None, name=None, tripcode=None, email=None, body):
	#	self.thread_id = thread_id
	#	self 

