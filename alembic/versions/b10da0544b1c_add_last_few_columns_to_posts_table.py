"""add last few columns to posts table

Revision ID: b10da0544b1c
Revises: 4292a10d4ea8
Create Date: 2023-12-09 19:24:26.862616

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b10da0544b1c'
down_revision: Union[str, None] = '4292a10d4ea8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at',
                            sa.TIMESTAMP(timezone=True),
                            nullable=False,
                            server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
