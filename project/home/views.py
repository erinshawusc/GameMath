#################
#### imports ####
#################
import os

from base64 import b64decode, b64encode
from flask import render_template, Blueprint, request, flash, redirect, url_for, send_from_directory
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename
from .forms import MessageForm
from project import db
from project.models import BlogPost
from project import app

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

upload_folder = os.getcwd() + '/uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

################
#### routes ####
################

# use decorators to link the function to a url
@home_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        game_file = request.files['game']
        if game_file:
            filename = secure_filename(game_file.filename)
            print 'file path: ' + str(os.path.join(upload_folder, filename))
            game_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print form.game.data
        new_message = BlogPost(
            form.title.data,
            b64encode(game_file.read()),
            game_file.filename,
            current_user.id,
            str(os.path.join(upload_folder, filename))
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
        for post in posts:
            post.game = b64decode(post.game)
        return render_template(
            'index.html', posts=posts, form=form, error=error)

@home_blueprint.route('/uploads/<filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template
