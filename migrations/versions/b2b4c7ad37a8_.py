"""empty message

Revision ID: b2b4c7ad37a8
Revises: 9746350942e4
Create Date: 2022-08-12 22:17:16.811585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2b4c7ad37a8'
down_revision = '9746350942e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('associate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('associate',
    sa.Column('Artist_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Venue_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['Artist_id'], ['Artist.id'], name='associate_Artist_id_fkey'),
    sa.ForeignKeyConstraint(['Venue_id'], ['Venue.id'], name='associate_Venue_id_fkey')
    )
    # ### end Alembic commands ###
