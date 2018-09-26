"""create comments table

Revision ID: 68760f62b701
Revises: 5cb3bd9a1d0e
Create Date: 2018-09-26 14:21:05.339908

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '68760f62b701'
down_revision = '5cb3bd9a1d0e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('article_id', sa.Integer, index=True),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('text', sa.Text(), server_default=''),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )
    op.create_foreign_key('article_id_key', 'comments', 'articles', ['article_id'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('article_id_key', 'comments', type_='foreignkey')
    op.drop_table('comments')
