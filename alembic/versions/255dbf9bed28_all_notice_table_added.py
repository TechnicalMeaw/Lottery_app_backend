"""all_notice table added

Revision ID: 255dbf9bed28
Revises: 5a12961a6468
Create Date: 2023-07-16 00:08:07.033571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255dbf9bed28'
down_revision = '5a12961a6468'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('all_notice',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('notice_text', sa.String(), nullable=False),
    sa.Column('notice_type', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('Now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('all_notice')
    # ### end Alembic commands ###