"""empty message

Revision ID: 67fd89eafcf5
Revises: cf5e1b673a2c
Create Date: 2020-02-13 15:40:59.025651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67fd89eafcf5'
down_revision = 'cf5e1b673a2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(length=25), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'artist_id')
    )
    op.drop_table('show')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('Artist_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Venue_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('start_time', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['Artist_id'], ['Artist.id'], name='show_Artist_id_fkey'),
    sa.ForeignKeyConstraint(['Venue_id'], ['Venue.id'], name='show_Venue_id_fkey')
    )
    op.drop_table('Show')
    # ### end Alembic commands ###
