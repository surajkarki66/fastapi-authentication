"""create post table

Revision ID: 8412fbd402b8
Revises: 
Create Date: 2022-03-08 21:37:34.643987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8412fbd402b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True),
                    sa.Column('title', sa.String(256), nullable=False),
                    sa.Column('content', sa.String(100), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    )


def downgrade():
    op.drop_table('posts')
