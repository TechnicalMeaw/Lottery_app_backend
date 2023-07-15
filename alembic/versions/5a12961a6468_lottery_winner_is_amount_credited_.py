"""lottery winner is_amount_credited column added

Revision ID: 5a12961a6468
Revises: 902ffb098930
Create Date: 2023-07-15 23:30:25.549311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a12961a6468'
down_revision = '902ffb098930'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lottery_winners', sa.Column('is_amount_credited', sa.Boolean(), server_default=sa.text('False'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lottery_winners', 'is_amount_credited')
    # ### end Alembic commands ###
