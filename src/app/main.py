from flask import Flask
from flask.ext import restful
from flask.ext.restful import fields, marshal_with, reqparse
from google.appengine.ext import ndb
import dateutil.parser

app = Flask('checkit-flask-test')


@app.route('/')
def welcome():
    return 'Hello Dudes!'


class KeyField(fields.Raw):
    def format(self, value):
        return value.urlsafe()


todo_fields = {
    'task': fields.String,
    'due': fields.DateTime,
    'notes': fields.List(fields.String),
    'key': KeyField,
}

todo_collection_fields = {
    'todos': fields.List(fields.Nested(todo_fields))
}


class Todo(ndb.Model):
    task = ndb.StringProperty()
    due = ndb.DateTimeProperty()
    notes = ndb.StringProperty(repeated=True)


api = restful.Api(app, prefix='/api/v1')

todo_parser = reqparse.RequestParser()
todo_parser.add_argument('task', type=unicode, required=True)
todo_parser.add_argument(
    'due', type=lambda *args, **kwargs: dateutil.parser.parse(
        args[0], ignoretz=True))
todo_parser.add_argument('notes', type=list, default=[])


class TodoCollection(restful.Resource):

    @marshal_with(todo_collection_fields)
    def get(self):
        todos = Todo.query().fetch() or []
        return {'todos': todos}

    @marshal_with(todo_fields)
    def post(self):
        args = todo_parser.parse_args()
        todo = Todo(**args)
        key = todo.put()
        todo = key.get()
        return todo.to_dict()


class TodoResource(restful.Resource):

    @marshal_with(todo_fields)
    def get(self, todo_key_string):
        key = ndb.Key(urlsafe=todo_key_string)
        todo = key.get()
        return todo

api.add_resource(TodoCollection, '/todos')
api.add_resource(TodoResource, '/todos/<string:todo_key_string>')
