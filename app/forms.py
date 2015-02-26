from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class PostForm(Form):
	title = StringField('title', validators=[DataRequired()])
	email = StringField('email')
	name = StringField('name')
	tripcode = StringField('trip')
	body = StringField('body', validators=[DataRequired()])
	
class ReplyForm(Form):
	title = StringField('title')
	email = StringField('email')
	name = StringField('name')
	tripcode = StringField('trip')
	body = StringField('body', validators=[DataRequired()])
