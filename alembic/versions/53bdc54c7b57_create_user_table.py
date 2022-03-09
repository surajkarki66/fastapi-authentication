"""create user table

Revision ID: 53bdc54c7b57
Revises: 8412fbd402b8
Create Date: 2022-03-08 22:16:47.165099

"""
from alembic import op
import sqlalchemy as sa

from app.models import Role


# revision identifiers, used by Alembic.
revision = '53bdc54c7b57'
down_revision = '8412fbd402b8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(32), nullable=False),
                    sa.Column('last_name', sa.String(32), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('isActive', sa.Boolean(),
                              server_default="FALSE"),
                    sa.Column('role', sa.Enum(Role),
                              server_default="subscriber"),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')
