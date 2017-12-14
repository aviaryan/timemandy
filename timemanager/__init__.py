import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ.get('CONFIG', 'config.LocalConfig'))

# Database
db = SQLAlchemy(app)

# Logger
logger = logging.getLogger('time_manager_logger')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(relativeCreated)6d %(threadName)s %(message)s'
))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# late import views
import timemanager.views  # noqa
