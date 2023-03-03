import os

# from os import urandom


class Config:
    """
    Application configuration established at the time of create_app()
    """

    ROOT_DIR = os.getcwd()
    SECRET_KEY = str(os.urandom(20))
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{ROOT_DIR}/application/database.db"
    EXECUTOR_PROPAGATE_EXCEPTIONS = True
    _wx_path = ROOT_DIR.split("/src")[0]
    WX_DATA_DIR = f"{_wx_path}/wx_data"
    SWAGGER_UI_JSONEDITOR = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_SUPPORTED_SUBMIT_METHODS = ["get"]
