from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ =  'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    #relationships
    project = db.relationship('Project', backref='user', lazy=True)
    bookmarks = db.relationship('Bookmark', back_populates='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)



   

class Skill(db.Model):
    __tablename__ =  'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    
    

class Project(db.Model):
    __tablename__ =  'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   
   #relationships
    skills = db.relationship('ProjectSkill', backref='project', lazy=True, cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', back_populates='project', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='project', lazy=True, )

    

class ProjectSkill(db.Model):
    __tablename__ =  'project_skills'
    id = db.Column(db.Integer, primary_key=True)
    #relationships
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False )
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)


    #uniqueconstraint
    __table_args__ = (db.UniqueConstraint('project_id', 'skill_id', name='unique_project_skill'),)

    

class Bookmark(db.Model):
    __tablename__ =  'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    #relationship
    user = db.relationship('User', back_populates='bookmarks', lazy=True)
    project = db.relationship('Project', back_populates='bookmarks', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    #relationships
    user = db.relationship('User', back_populates='comments', lazy=True)
    project = db.relationship('Project', back_populates='comments', lazy=True)
    

