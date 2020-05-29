"""empty message

Revision ID: 1f1a02c3ee9e
Revises: 4e0bb6b445c8
Create Date: 2020-02-13 20:48:16.951242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f1a02c3ee9e'
down_revision = '4e0bb6b445c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###
