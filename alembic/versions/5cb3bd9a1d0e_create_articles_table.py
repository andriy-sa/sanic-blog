"""create articles table

Revision ID: 5cb3bd9a1d0e
Revises: 
Create Date: 2018-09-06 15:52:10.164071

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5cb3bd9a1d0e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), server_default=''),
        sa.Column('is_published', sa.Boolean(), sa.schema.DefaultClause("1"), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('account')
