from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    pass

class Skills(db.Model):
    pass

class Projects(db.Model):
    pass

class ProjectSkills(db.Model):
    pass

class Bookmark(db.Model):
    pass

class Comment(db.Model):
    pass

