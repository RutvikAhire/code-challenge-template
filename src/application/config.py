import os
#from os import urandom


class Config:
    """
    Application configuration established at the time of create_app()
    """
    SECRET_KEY = str(os.urandom(20))
    SQLALCHEMY_DATABASE_URI = 'sqlite://///home/rutvik/Documents/code-challenge-template/src/application/database.db'
    EXECUTOR_PROPAGATE_EXCEPTIONS = True
    ROOT_DIR = '/home/rutvik/Documents/code-challenge-template/src'
    WX_DATA_DIR = '/home/rutvik/Documents/code-challenge-template/wx_data'
    SWAGGER_UI_JSONEDITOR = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_SUPPORTED_SUBMIT_METHODS = ['get']
