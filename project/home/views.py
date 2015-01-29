#################
#### imports ####
#################

from base64 import b64decode, b64encode
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename
from .forms import MessageForm
from project import db
from project.models import BlogPost

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


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
        print form.game.data
        new_message = BlogPost(
            form.title.data,
            b64encode(game_file.read()),
            game_file.filename,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        # flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
        for post in posts:
            post.game = b64decode(post.game)
        return render_template(
            'index.html', posts=posts, form=form, error=error)


@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template
