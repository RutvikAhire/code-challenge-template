"""
This module contains forms related to '/ingest' url paths
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, InputRequired
from wtforms import SubmitField


class UploadSingleForm(FlaskForm):
    """
    Form for ingesting a single wx_data file into database.db
    """
    file = FileField(
        "", validators=[DataRequired(), InputRequired(), FileAllowed(["txt"])]
    )
    submit = SubmitField("Submit")
