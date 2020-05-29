"""empty message

Revision ID: cb0988c0faca
Revises: bf7ad3081ec7
Create Date: 2020-02-08 11:33:43.154144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0988c0faca'
down_revision = 'bf7ad3081ec7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('Venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website_link')
    op.drop_column('Venue', 'upcoming_shows_count')
    op.drop_column('Venue', 'past_shows_count')
    op.drop_column('Artist', 'website_link')
    op.drop_column('Artist', 'upcoming_shows_count')
    op.drop_column('Artist', 'past_shows_count')
    # ### end Alembic commands ###