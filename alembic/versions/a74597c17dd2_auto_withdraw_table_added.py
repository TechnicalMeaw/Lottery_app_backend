"""auto withdraw table added

Revision ID: a74597c17dd2
Revises: fd115c0e6278
Create Date: 2023-05-28 19:14:54.107171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a74597c17dd2'
down_revision = 'fd115c0e6278'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lottery_winners',
    sa.Column('lottery_token_no', sa.Integer(), nullable=False),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['position'], ['lottery_prize.rank_no'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('lottery_token_no'),
    sa.UniqueConstraint('lottery_token_no'),
    sa.UniqueConstraint('position'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('withdrawals',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('phone_no', sa.String(), nullable=False),
    sa.Column('transaction_medium', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), server_default=sa.text('False'), nullable=False),
    sa.Column('is_rejected_by_admin', sa.Boolean(), server_default=sa.text('False'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('Now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('country_code', sa.String(), nullable=True))
    op.drop_column('users', 'country')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('country', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'country_code')
    op.drop_table('withdrawals')
    op.drop_table('lottery_winners')
    # ### end Alembic commands ###
