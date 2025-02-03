from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import datetime
from validations import  validate_user_data, validate_project_data
from models import db, User, Project, Comment, ProjectSkill, Skill, Bookmark
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
cors = CORS(app)

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
                "username": user.username, 
                "email": user.email,
                "role": user.role,
                "projects": [{"id": p.id, "title": p.title} for p in user.project]
            }, 200
         
        # Get all users
        users = User.query.all()
        return [{"id": user.id, "username": user.username, "email": user.email, "role": user.role} for user in users], 200

    def post(self):
        # Create a new user
        data = request.json
        errors = validate_user_data(data)
        if errors :
            return jsonify({'errors': errors}), 400

        new_user = User(username=data['username'], email=data['email'], role=data['role'])  
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Username or email exists"}), 400
        return jsonify({"message": f"User {new_user.username} created"}), 201 

    def put(self, user_id):
        # Update a user
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
    
        data = request.json
        if "username" in data:
            user.username = data["username"]
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
        
    def delete(self, user_id):
        # Delete a user
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User {user.username} deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting user"}, 500

class ProjectData(Resource):
    def get(self, project_id=None):
        if project_id:
            # Get a specific project
            project = Project.query.get(project_id)
            if not project:
                return {"message": "Project not found"}, 404
            return {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "image": project.image,
            "user_id": project.user_id,
        }, 200
        else:
            # Get all projects
            projects = Project.query.all()
            return [{"id": project.id, "title": project.title, "description": project.description} for project in projects], 200
        
    def post(self):
        # Create a new project
        data = request.json
        errors = validate_project_data(data)
        if errors:
            return jsonify({'errors': errors}),404
        
        new_project = Project(title=data["title"], description=data["description"],image=data["image"] ,user_id=data["user_id"])
        db.session.add(new_project)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating project"}, 500 
        return {"message": f"Project {new_project.title} created"}, 201

    def put(self, project_id):
        # Update a project
        project = Project.query.get(project_id)
        if not project:
            return {"message": "Project not found"}, 404
        
        data = request.json
        project.title = data.get("title", project.title)
        project.description = data.get("description", project.description)
        project.image = data.get("image", project.image)
        project.user_id = data.get("user_id", project.user_id)
        try:
            db.session.commit()
            return {"message": f"Project {project.title} updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating project"}, 500

    def delete(self, project_id):
        # Delete a project
        project = Project.query.get(project_id)
        if not project:
            return {"message": "Project not found"}, 404
        
        try:
            db.session.delete(project)
            db.session.commit()
            return {"message": f"Project {project.title} deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting project"}, 500

class BookmarkData(Resource):
    def get(self):
        # Fetch all bookmarks of a specific user
        user_id = request.args.get('user_id') 
        if user_id:
            bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
            if not bookmarks:
                return {"message": "No bookmarks found for this user"}, 404
            return [
                {
                    "id": bookmark.id,
                    "project_id": bookmark.project_id,
                    "project_title": bookmark.project.title if bookmark.project else None,
                    "created_at": bookmark.created_at.isoformat(),
                }
                for bookmark in bookmarks
            ], 200

        # Fetch all bookmarks
        bookmarks = Bookmark.query.all()
        return [
            {
                "id": bookmark.id,
                "user_id": bookmark.user_id,
                "project_id": bookmark.project_id,
                "project_title": bookmark.project.title if bookmark.project else None,
                "created_at": bookmark.created_at.isoformat(),
            }
            for bookmark in bookmarks
        ], 200
    
    def post(self):
        data = request.json
        user_id = data.get('user_id')
        project_id = data.get('project_id')
        action = data.get('action')  # "bookmark" or "unbookmark"

        if not user_id or not project_id or not action:
            return {"message": "'user_id', 'project_id', and 'action' are required"}, 400

        if action == "bookmark":
            # Check if the bookmark already exists
            existing_bookmark = Bookmark.query.filter_by(user_id=user_id, project_id=project_id).first()
            if existing_bookmark:
                return {"message": "This project is already bookmarked by the user"}, 400

            # Create a new bookmark
            new_bookmark = Bookmark(user_id=user_id, project_id=project_id)
            db.session.add(new_bookmark)
            try:
                db.session.commit()
                return {"message": f"Project {project_id} bookmarked by user {user_id}"}, 201
            except Exception as e:
                db.session.rollback()
                return {"message": "Error creating bookmark"}, 500

        elif action == "unbookmark":
            # Check if the bookmark exists
            bookmark = Bookmark.query.filter_by(user_id=user_id, project_id=project_id).first()
            if not bookmark:
                return {"message": "Bookmark not found"}, 404

            # Delete the bookmark
            try:
                db.session.delete(bookmark)
                db.session.commit()
                return {"message": f"Bookmark for project {project_id} by user {user_id} deleted"}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": "Error deleting bookmark"}, 500

        else:
            return {"message": "Invalid action"}, 400

    def delete(self) :
        # Delete a bookmark
        data = request.json
        user_id = data.get('user_id')
        project_id = data.get('project_id')

        if not user_id or not project_id:
            return {"message": "Both 'user_id' and 'project_id' are required"}, 400

        # Check if the bookmark exists
        bookmark = Bookmark.query.filter_by(user_id=user_id, project_id=project_id).first()
        if not bookmark:
            return {"message": "Bookmark not found"}, 404

        # Delete the bookmark
        try:
            db.session.delete(bookmark)
            db.session.commit()
            return {"message": f"Bookmark for project {project_id} by user {user_id} deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting bookmark"}, 500
        
class CommentData(Resource):
    def get(self):
        # Fetch all comments or comments for a specific project or user
        project_id = request.args.get('project_id')  # Optional query parameter
        user_id = request.args.get('user_id')  # Optional query parameter

        if project_id:
            # Get comments for a specific project
            comments = Comment.query.filter_by(project_id=project_id).all()
            if not comments:
                return {"message": "No comments found for this project"}, 404
            return [
                {
                    "id": comment.id,
                    "user_id": comment.user_id,
                    "content": comment.content,
                    "created_at": comment.created_at.isoformat(),
                    "updated_at": comment.updated_at.isoformat(),
                }
                for comment in comments
            ], 200

        elif user_id:
            # Get comments by a specific user
            comments = Comment.query.filter_by(user_id=user_id).all()
            if not comments:
                return {"message": "No comments found for this user"}, 404
            return [
                {
                    "id": comment.id,
                    "project_id": comment.project_id,
                    "content": comment.content,
                    "created_at": comment.created_at.isoformat(),
                    "updated_at": comment.updated_at.isoformat(),
                }
                for comment in comments
            ], 200

        # Fetch all comments
        comments = Comment.query.all()
        return [
            {
                "id": comment.id,
                "user_id": comment.user_id,
                "project_id": comment.project_id,
                "content": comment.content,
                "created_at": comment.created_at.isoformat(),
                "updated_at": comment.updated_at.isoformat(),
            }
            for comment in comments
        ], 200

    def post(self):
        # Create a new comment
        data = request.json

        # Extract user_id, project_id, and content from the request body
        user_id = data.get('user_id')
        project_id = data.get('project_id')
        content = data.get('content')

        # Validate input
        if not user_id or not project_id or not content:
            return {"message": "'user_id', 'project_id', and 'content' are required"}, 400

        # Create a new comment
        new_comment = Comment(user_id=user_id, project_id=project_id, content=content)
        db.session.add(new_comment)

        try:
            db.session.commit()
            return {"message": f"Comment added to project {project_id} by user {user_id}"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating comment"}, 500

    def delete(self):
        # Delete a comment by user_id and project_id
        data = request.json

        # Extract user_id, project_id, and comment_id from the request body
        user_id = data.get('user_id')
        project_id = data.get('project_id')
        comment_id = data.get('comment_id')

        # Validate input
        if not user_id or not project_id or not comment_id:
            return {"message": "'user_id', 'project_id', and 'comment_id' are required"}, 400

        # Check if the comment exists
        comment = Comment.query.filter_by(id=comment_id, user_id=user_id, project_id=project_id).first()
        if not comment:
            return {"message": "Comment not found"}, 404

        # Delete the comment
        try:
            db.session.delete(comment)
            db.session.commit()
            return {"message": f"Comment for project {project_id} by user {user_id} deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting comment"}, 500
        

class SkillData(Resource):

    def get(self, skill_id=None):
        # Fetch a specific skill or all skills
        if skill_id:
            skill = Skill.query.get(skill_id)
            if not skill:
                return {"message": "Skill not found"}, 404
            return {
                "id": skill.id,
                "name": skill.name,
                "details": skill.details,
                "created_at": skill.created_at,
                "updated_at": skill.updated_at,
            }, 200
        else:
            skills = Skill.query.all()
            return [
                {
                    "id": skill.id,
                    "name": skill.name,
                    "details": skill.details,
                    "created_at": skill.created_at.isoformat(),
                    "updated_at": skill.updated_at.isoformat(),
                }
                for skill in skills
            ], 200

    def post(self):
        # Create a new skill
        data = request.json
        name = data.get('name')
        details = data.get('details')

        # Validate input
        if not name or not details:
            return {"message": "'name' and 'details' are required"}, 400

        # Create a new skill
        new_skill = Skill(name=name, details=details)
        db.session.add(new_skill)

        try:
            db.session.commit()
            return {"message": f"Skill '{new_skill.name}' created"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating skill"}, 500

    def put(self, skill_id):
        # Update an existing skill
        skill = Skill.query.get(skill_id)
        if not skill:
            return {"message": "Skill not found"}, 404

        data = request.json
        if 'name' in data:
            skill.name = data['name']
        if 'details' in data:
            skill.details = data['details']

        try:
            db.session.commit()
            return {"message": f"Skill '{skill.name}' updated"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating skill"}, 500

    def delete(self, skill_id):
        # Delete a skill
        skill = Skill.query.get(skill_id)
        if not skill:
            return {"message": "Skill not found"}, 404

        try:
            db.session.delete(skill)
            db.session.commit()
            return {"message": f"Skill '{skill.name}' deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting skill"}, 500

class ProjectSkillData(Resource):
    
    # Add a skill to a project (create a new project-skill relationship)
    def get(self):
        project_id = request.args.get('project_id')
        skill_id = request.args.get('skill_id')

        if project_id:
            # Get all skills for a specific project
            project_skills = ProjectSkill.query.filter_by(project_id=project_id).all()
            if not project_skills:
                return {"message": "No skills found for this project"}, 404
            return [
                {
                    "id": project_skill.id,
                    "project_id": project_skill.project_id,
                    "skill_id": project_skill.skill_id,
                    "skill_name": project_skill.skill.name,  # Access skill name dynamically
                }
                for project_skill in project_skills
            ], 200
        
        if skill_id:
            # Get all projects for a specific skill
            project_skills = ProjectSkill.query.filter_by(skill_id=skill_id).all()
            if not project_skills:
                return {"message": "No projects found for this skill"}, 404
            return [
                {
                    "id": project_skill.id,
                    "project_id": project_skill.project_id,
                    "skill_id": project_skill.skill_id,
                    "project_title": project_skill.project.title,  # Access project title dynamically
                }
                for project_skill in project_skills
            ], 200

        # Get all project-skill relationships
        project_skills = ProjectSkill.query.all()
        return [
            {
                "id": project_skill.id,
                "project_id": project_skill.project_id,
                "skill_id": project_skill.skill_id,
                "project_title": project_skill.project.title,  # Access project title dynamically
                "skill_name": project_skill.skill.name,  # Access skill name dynamically
            }
            for project_skill in project_skills
        ], 200

    def post(self):
        data = request.json
        project_id = data.get("project_id")
        skill_id = data.get("skill_id")

        if not project_id or not skill_id:
            return {"message": "Project ID and Skill ID are required."}, 400
        
        # Check if the combination already exists
        existing_project_skill = ProjectSkill.query.filter_by(project_id=project_id, skill_id=skill_id).first()
        if existing_project_skill:
            return {"message": "This project already has this skill."}, 400
        
        new_project_skill = ProjectSkill(project_id=project_id, skill_id=skill_id)
        db.session.add(new_project_skill)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error adding skill to project: {str(e)}"}, 500
        
        return {"message": f"Skill added to project successfully!"}, 201

    

    # Remove a skill from a project
    def delete(self, project_skill_id):
        project_skill = ProjectSkill.query.get(project_skill_id)
        if not project_skill:
            return {"message": "Project-Skill relationship not found"}, 404
        
        try:
            db.session.delete(project_skill)
            db.session.commit()
            return {"message": f"Skill removed from project successfully!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error removing skill from project: {str(e)}"}, 500




api.add_resource(UserData, '/user', '/user/<int:user_id>')
api.add_resource(ProjectData, '/projects', '/projects/<int:project_id>')
api.add_resource(BookmarkData, '/bookmark')
api.add_resource(CommentData, '/comment')
api.add_resource(SkillData, '/skill', '/skill/<int:skill_id>')
api.add_resource(ProjectSkillData, '/projectskill', '/projectskill/<int:project_skill_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)


