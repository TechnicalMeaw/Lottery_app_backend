"""added country field to users table

Revision ID: c81fefb1c6c4
Revises: f1fcc424342a
Create Date: 2023-05-27 21:36:33.407510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c81fefb1c6c4'
down_revision = 'f1fcc424342a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'coins', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_unique_constraint(None, 'lottery', ['lottery_token'])
    op.create_unique_constraint(None, 'lottery_prize', ['rank_no'])
    op.create_foreign_key(None, 'transactions', 'users', ['user_id'], ['id'])
    # op.add_column('users', sa.Column('is_verified', sa.Boolean(), server_default=sa.text('False'), nullable=False))
    # op.add_column('users', sa.Column('role', sa.Integer(), server_default=sa.text('1'), nullable=True))
    op.add_column('users', sa.Column('country', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'country')
    # op.drop_column('users', 'role')
    # op.drop_column('users', 'is_verified')
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_constraint(None, 'lottery_prize', type_='unique')
    op.drop_constraint(None, 'lottery', type_='unique')
    op.drop_constraint(None, 'coins', type_='foreignkey')
    # ### end Alembic commands ###
