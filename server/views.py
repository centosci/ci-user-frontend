from flask import Blueprint
from app import app, db
from flask_restplus import Api, Resource, fields
from models import *
from utils import login_required

api = Api(app, title='API documentation', description='UI representation of the APIs for testing')

class UuidField(fields.Raw):
    __schema_format__ = 'uuid'

request = api.model('Requests', {
    'user_id': UuidField('Unique user ID.'),
    'project_name': fields.String('Name of Project requested.')
})

new_request = api.clone('Requests', request, {
    'role': fields.String("Role granted to user. Represents permissions the user has to perform actions."),
    'email': fields.String('Email address of the user.'),
    'gpg_key': fields.String("User's GPG key required for password hashing.")
})

class Requests(Resource): 

    @api.marshal_with(request)  # only returns fields as defined in the api model
    @api.response(404, 'No requests found.')
    def get(self):
        '''Get all project requests'''
        return Request.query.all()

    @api.expect(new_request)        # only accepts payload as defined in the api model
    @api.response(201, 'Request created successfully.')
    def post(self):
        '''Create a new project request'''
        request = Request(**api.payload)
        db.session.add(request)
        db.session.commit()
        return None, 201
        # return {'message': f"Your request with ID: {request.id} has been created."}, 201

api.add_resource(Requests, '/requests', endpoint="requests")