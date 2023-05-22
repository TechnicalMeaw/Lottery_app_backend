"""create user table

Revision ID: 3ef111f6b12d
Revises: 
Create Date: 2023-05-13 18:27:00.642249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ef111f6b12d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default = sa.TextClause("Now()")),
                    sa.UniqueConstraint('email'),
                    sa.PrimaryKeyConstraint('id'),
                    )



def downgrade() -> None:
    op.drop_table('users')
