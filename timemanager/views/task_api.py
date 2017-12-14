from flask_restplus import Namespace, Resource, fields, reqparse
from flask_login import login_required
from flask import g

from timemanager.models.task_model import Task as TaskModel

from timemanager.helpers.dao import BaseDAO
from timemanager.helpers.utils import AUTH_HEADER_DEFN
from timemanager.helpers.permissions import has_task_access, admin_only
from timemanager.helpers.custom_fields import DateTime
from timemanager.helpers.query_filters import parse_args


api = Namespace('tasks', description='Tasks', path='/')  # noqa

TASK = api.model('Task', {
    'id': fields.Integer(required=True),
    'title': fields.String(required=True),
    'minutes': fields.Integer(required=True),
    'date': DateTime(required=True),
    'comments': fields.String(),
    'user_id': fields.Integer()
})

TASK_POST = api.clone('TaskPost', TASK, {})
del TASK_POST['id']


class TaskDAO(BaseDAO):
    def fix_user_task_access(self, data):
        """
        fixes the situation where a normal user tries to assign task to another user
        """
        current_user = g.current_user
        if data.get('user_id') is None:  # give default user id
            data['user_id'] = current_user.id
        elif not current_user.is_admin:  # not an admin and cheating
            data['user_id'] = current_user.id
        return data['user_id']


DAO = TaskDAO(TaskModel, TASK_POST)


# DEFINE Query PARAMS

TASK_PARAMS = {
    'from': {
        'description': 'Start tasks from where (YYYY-MM-DD)'
    },
    'to': {
        'description': 'End tasks till where'
    }
}

class TaskResource():
    """
    Task Resource Base class
    """
    task_parser = reqparse.RequestParser()
    task_parser.add_argument('from', type=str, dest='__task_from')
    task_parser.add_argument('to', type=str, dest='__task_to')



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
        data = self.api.payload
        data['user_id'] = DAO.fix_user_task_access(data)
        return DAO.update(task_id, data)

    @login_required
    @has_task_access
    @api.header(*AUTH_HEADER_DEFN)
    @api.doc('delete_task')
    @api.marshal_with(TASK)
    def delete(self, task_id):
        """Delete a task given its id"""
        return DAO.delete(task_id, user_id=None)  # has_task_access already checks this


@api.route('/tasks')
class TaskList(Resource, TaskResource):
    @api.header(*AUTH_HEADER_DEFN)
    @login_required
    @api.doc('create_task')
    @api.marshal_with(TASK)
    @api.expect(TASK_POST)
    def post(self):
        """Create a task"""
        data = self.api.payload
        data['user_id'] = DAO.fix_user_task_access(data)
        return DAO.create(data, user_id=data['user_id'])

    @api.header(*AUTH_HEADER_DEFN)
    @login_required
    @api.doc('list_user_tasks', params=TASK_PARAMS)
    @api.marshal_list_with(TASK)
    def get(self):
        """List user tasks"""
        parsed_args = parse_args(self.task_parser)
        parsed_args['user_id'] = g.current_user.id
        return DAO.list(**parsed_args)


@api.route('/tasks/all')
class TaskListAll(Resource, TaskResource):
    @api.header(*AUTH_HEADER_DEFN)
    @login_required
    @admin_only
    @api.doc('list_all_tasks', params=TASK_PARAMS)
    @api.marshal_list_with(TASK)
    def get(self):
        """List all tasks in the database"""
        parsed_args = parse_args(self.task_parser)
        return DAO.list(**parsed_args)
