"""empty message

Revision ID: 17bbeb91a244
Revises: 5924973acdc5
Create Date: 2024-10-18 15:39:50.225004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17bbeb91a244'
down_revision = '5924973acdc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bakery',
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('nid', sa.String(length=10), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('bakery_id', sa.String(length=30), nullable=True),
    sa.Column('ownership_status', sa.String(length=30), nullable=True),
    sa.Column('number_violations', sa.Integer(), nullable=True),
    sa.Column('second_fuel', sa.String(length=30), nullable=True),
    sa.Column('city', sa.String(length=30), nullable=True),
    sa.Column('region', sa.Integer(), nullable=True),
    sa.Column('district', sa.Integer(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('household_risk', sa.String(length=30), nullable=True),
    sa.Column('bakers_risk', sa.String(length=30), nullable=True),
    sa.Column('type_flour', sa.Integer(), nullable=True),
    sa.Column('type_bread', sa.String(length=30), nullable=True),
    sa.Column('bread_rations', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bakery')
    # ### end Alembic commands ###