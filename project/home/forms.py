from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, Length


class MessageForm(Form):
    # title = TextField('Title', validators=[DataRequired()])
    # description = TextField(
    #     'Description', validators=[DataRequired(), Length(max=140)])
    title = SelectField(u'Game', choices=[('maze', 'Maze Game'), ('shooter', 'Shooter Game'), ('platform', 'Platform Game')])
    game = FileField('GameFile')