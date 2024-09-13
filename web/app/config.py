import os
APP_ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


class Config(object):
    root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
    SECRET_KEY = 'secret'
    USER_APP_NAME = "DriveVibe"