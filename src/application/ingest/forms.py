from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, InputRequired
from wtforms import SubmitField


class UploadSingleForm(FlaskForm):
    file = FileField(
        "", validators=[DataRequired(), InputRequired(), FileAllowed(["txt"])]
    )
    submit = SubmitField("Submit")
