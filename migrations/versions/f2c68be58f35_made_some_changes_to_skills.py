"""made some changes to skills

Revision ID: f2c68be58f35
Revises: 8191ca80408e
Create Date: 2025-01-29 02:45:09.828703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2c68be58f35'
down_revision = '8191ca80408e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('skills', schema=None) as batch_op:
        batch_op.add_column(sa.Column('details', sa.Text(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('skills', schema=None) as batch_op:
        batch_op.drop_column('details')

    # ### end Alembic commands ###
