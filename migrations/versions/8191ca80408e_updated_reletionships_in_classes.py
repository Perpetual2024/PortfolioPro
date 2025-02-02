"""Updated reletionships in classes

Revision ID: 8191ca80408e
Revises: f9e8468f03de
Create Date: 2025-01-27 14:26:11.257873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8191ca80408e'
down_revision = 'f9e8468f03de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project_skills', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_project_skill', ['project_id', 'skill_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project_skills', schema=None) as batch_op:
        batch_op.drop_constraint('unique_project_skill', type_='unique')

    # ### end Alembic commands ###
