from flask_restplus import Namespace, Resource, fields
from flask_login import login_required
from flask import g

from timemanager.models.task_model import Task as TaskModel

from timemanager.helpers.dao import BaseDAO
from timemanager.helpers.utils import AUTH_HEADER_DEFN
from timemanager.helpers.permissions import has_task_access, admin_only


api = Namespace('tasks', description='Tasks', path='/')  # noqa

TASK = api.model('Task', {
    'id': fields.Integer(required=True),
    'title': fields.String(required=True),
    'minutes': fields.Integer(required=True),
    'date': fields.DateTime(required=True),
    'comments': fields.String(),
    'user_id': fields.Integer()
})

TASK_POST = api.clone('TaskPost', TASK, {})
del TASK_POST['id']


class TaskDAO(BaseDAO):
    pass


DAO = TaskDAO(TaskModel, TASK_POST)


@api.route('/tasks/<int:task_id>')
class Task(Resource):
    @login_required
    @has_task_access
    @api.header(*AUTH_HEADER_DEFN)
    @api.doc('get_user')
    @api.marshal_with(TASK)
    def get(self, task_id):
        """Fetch a task given its id"""
        return DAO.get(task_id)

    @login_required
    @has_task_access
    @api.header(*AUTH_HEADER_DEFN)
    @api.doc('update_task')
    @api.marshal_with(TASK)
    @api.expect(TASK_POST)
    def put(self, task_id):
        """Update a task given its id"""
        return DAO.update(task_id, self.api.payload)

    @login_required
    @has_task_access
    @api.header(*AUTH_HEADER_DEFN)
    @api.doc('delete_task')
    @api.marshal_with(TASK)
    def delete(self, task_id):
        """Delete a task given its id"""
        return DAO.delete(task_id, user_id=None)  # has_task_access already checks this


@api.route('/task')
class TaskList(Resource):
    @api.header(*AUTH_HEADER_DEFN)
    @login_required
    @api.doc('create_task')
    @api.marshal_with(TASK)
    @api.expect(TASK_POST)
    def post(self):
        """Create a task"""
        return DAO.create(self.api.payload, user_id=g.current_user.id)

    @api.header(*AUTH_HEADER_DEFN)
    @login_required
    @admin_only
    @api.doc('list_tasks')
    @api.marshal_list_with(TASK)
    def get(self):
        """List all tasks"""
        # TODO: admin only, also think about levels
        return DAO.list()
