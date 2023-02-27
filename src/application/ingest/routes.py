"""
This module takes care of routing and other static functions related to '/ingest' path
"""

import os
from flask import Blueprint, request, render_template, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
from application import executor
from application.ingest.forms import UploadSingleForm
from application.ingest.ingestion_utility import IngestionUtility

INGEST = Blueprint('ingest', __name__)


@executor.job
def ingestion_task(ingestion_object):
    """
    Ingestion Background Task
    Params: ingestion_object --> ingestion object created in data_loader_single()/data_loader_batch
    """

    IngestionUtility.ingestor(self=ingestion_object)


def save_file(wx_data_directory, form_file):
    """
    Saves the submitted file into '/wx_data_files' directory
    """
    if not os.path.exists(wx_data_directory):
        os.mkdir(wx_data_directory)
    filename_secure = secure_filename(form_file.filename)
    upload_file_path = os.path.join(
        f'{wx_data_directory}', f'{filename_secure}')
    form_file.save(upload_file_path)
    return filename_secure


@INGEST.route('/ingest')
def data_loader_selector():
    """
    Landing page to ingest single file or batch ingest
    """
    return render_template('ingest/data_loader_selector.html', title='Upload')


@INGEST.route('/ingest/single', methods=['GET', 'POST'])
def data_loader_single():
    """
    Form to ingest a single wtx file
    """
    form = UploadSingleForm()
    if form.validate_on_submit():
        if form.file.data:
            data_loader_single.wx_data_directory = current_app.config['WX_DATA_DIR']
            data_loader_single.save_file_output = save_file(
                wx_data_directory=data_loader_single.wx_data_directory, form_file=form.file.data)
            flash(
                f'File {data_loader_single.save_file_output} saved successfully. Proceeding with ingestion.',
                'success')
            data_loader_single.ingestion_object = IngestionUtility(
                ingestion_files=[data_loader_single.save_file_output],
                ingestion_type=request.endpoint)
            ingestion_task.submit(
                ingestion_object=data_loader_single.ingestion_object)
    return render_template('ingest/data_loader_single.html', title='Upload Single', form=form)


@INGEST.route('/ingest/batch')
def data_loader_batch():
    """
    Form to batch load existing wtx files into database
    """
    data_loader_batch.wx_data_directory = current_app.config['WX_DATA_DIR']
    if not os.path.exists(data_loader_batch.wx_data_directory):
        flash('"wx_data_files" directory not found. Please contact admin.', 'danger')
    else:
        data_loader_batch.all_files = os.listdir(
            data_loader_batch.wx_data_directory)
        data_loader_batch.all_files.sort()
        for file in data_loader_batch.all_files:
            if '.txt' not in file:
                data_loader_batch.all_files.remove(file)
        if len(data_loader_batch.all_files) == 0:
            flash('No files found in "wx_data_files" directory. Upload single wx_data file or contact admin.',
                  'danger')
        else:
            data_loader_batch.ingestion_object = IngestionUtility(
                ingestion_files=data_loader_batch.all_files,
                ingestion_type=request.endpoint)
            ingestion_task.submit(
                ingestion_object=data_loader_batch.ingestion_object)
            flash(
                f'Ingestion of {len(data_loader_batch.all_files)} wx_data files in progress.',
                'success')
    return redirect(url_for('ingest.data_loader_selector'))
