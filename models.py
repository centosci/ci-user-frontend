from app import db
import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):

    __tablename__ = 'user'

    Roles = ['user', 'admin', 'superuser']

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid1(), unique=True, primary_key=True)
    username = db.Column(db.String())
    role = db.Column(db.Enum(*Roles, name='user_role'), default='user')
    email = db.Column(db.String())
    gpg_key = db.Column(db.String())
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<id {self.id}>'


class Request(db.Model):

    __tablename__ = 'request'

    RequestStatus = ['pending', 'approved', 'declined']

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid1(), unique=True, primary_key=True)
    user_id = db.Column(UUID(), db.ForeignKey(User.id), nullable=False)
    project_name = db.Column(db.String())
    project_desc = db.Column(db.String())
    status = db.Column(db.Enum(*RequestStatus, name='request_status'), default='pending')
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<id {self.id}>'


class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid1(), unique=True, primary_key=True)
    request_id = db.Column(UUID(), db.ForeignKey(Request.id), nullable=False)
    user_id = db.Column(UUID(), db.ForeignKey(User.id), nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<id {self.id}>'


ProjectMember = db.Table(
    'project_member',
    db.Column('user_id', UUID(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', UUID(), db.ForeignKey('project.id'), primary_key=True)
    )


class Project(db.Model):

    __tablename__ = 'project'

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid1(), unique=True, primary_key=True)
    project_name = db.Column(db.String())
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    members = db.relationship('User', secondary=ProjectMember, lazy=True, backref=db.backref('projects', lazy=True))

    def __repr__(self):
        return f'<id {self.id}>'
