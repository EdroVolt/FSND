"""empty message

Revision ID: 2e815655138e
Revises: cb0988c0faca
Create Date: 2020-02-08 12:21:37.354441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e815655138e'
down_revision = 'cb0988c0faca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('Artist_id', sa.Integer(), nullable=True),
    sa.Column('Venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['Venue_id'], ['Venue.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    # ### end Alembic commands ###
