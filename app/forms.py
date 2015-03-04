from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class PostForm(Form):
	title = StringField('title', validators=[DataRequired()])
	email = StringField('email')
	name = StringField('name')
	tripcode = StringField('trip')
	body = StringField('body', validators=[DataRequired()])
	file = FileField('file', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
	
class ReplyForm(Form):
	title = StringField('title')
	email = StringField('email')
	name = StringField('name')
	tripcode = StringField('trip')
	body = StringField('body', validators=[DataRequired()])
	file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
