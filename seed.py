from app import app, db
from models import User, Project, Comment, Bookmark, Skill, ProjectSkill
from faker import Faker

fake = Faker()

with app.app_context():
   
   for _ in range(10):
      user = User(
         username= fake.user_name(),
         email=fake.email(),
         role= fake.random_element(elements=('admin','user')),
         
      )
      db.session.add(user)
      db.session.commit()

   for  _ in range (10) : 
      project = Project(
         title = fake.word(),
         description = fake.text(),
         image =fake.image_url(),
         user_id = fake.random_element(elements=(1,2,3,4,5,6))

      )
      db.session.add(project)
      db.session.commit()

   for _ in range (10):
      comment = Comment(
         content = fake.text(),
         user_id = fake.random_element(elements= (1,2,3,4,5,6)),
         project_id = fake.random_element(elements=(1,2,3,4,5,6))
      )
      db.session.add(comment)
      db.session.commit()


         