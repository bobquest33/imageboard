from flask import render_template
from app import app
from .forms import PostForm

@app.route('/')
@app.route('/index')
def index():
	form = PostForm()
	return render_template('index.html', title='Main Page', form=form)
