from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Project, Comment, ProjectSkill, Skill, Bookmark

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)




@app.route('/')
def index():
    return jsonify({"message": "Welcome to the portfoliopro API"})

class UserData(Resource): 
    def get(self, user_id=None):
         if user_id:
            # Get a specific user
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            return {
                "id": user.id,
                "username": user.username,  # Fixed from 'name' to 'username'
                "email": user.email,
                "role": user.role,
                "projects": [{"id": p.id, "title": p.title} for p in user.projects]
            }, 200
         
         # Get all users
         users = User.query.all()
         return [{"id": user.id, "username": user.username, "email": user.email} for user in users], 200

    def post(self):
        # Create a new user
        data = request.json
        new_user = User(username=data['name'], email=data['email'], role=data['role'])  # 'name' -> 'username'
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Username or email exists"}, 400
        return {"message": f"User {new_user.username} created"}, 201  # 'name' -> 'username'
    


    def put(self, user_id):
        # Update a user
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
    
        data = request.json
        if "name" in data:
            user.username = data["name"]  
        if "email" in data:
            user.email = data["email"]
        if "role" in data:
            user.role = data["role"]

        try:
            db.session.commit()
            return {"message": f"User {user.username} updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating user"}, 500
        

api.add_resource(UserData, '/user', '/user/<int:user_id>')
        
     
if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
      

