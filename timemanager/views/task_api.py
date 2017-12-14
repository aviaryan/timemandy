from flask_restplus import Namespace  #, Resource, fields

from timemanager.models.task_model import Task as TaskModel  # noqa



api = Namespace('tasks', description='Tasks', path='/')  # noqa
