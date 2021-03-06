"""followers

Revision ID: 9a2c61a3901a
Revises: 4392b88e428f
Create Date: 2020-03-13 21:06:17.554604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a2c61a3901a'
down_revision = '4392b88e428f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_service_id'], ['service.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
