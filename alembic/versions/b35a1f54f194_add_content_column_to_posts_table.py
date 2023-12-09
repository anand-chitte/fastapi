"""add content column to  posts table

Revision ID: b35a1f54f194
Revises: 4e43ca3cc18e
Create Date: 2023-12-09 13:26:52.623187

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b35a1f54f194'
down_revision: Union[str, None] = '4e43ca3cc18e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
