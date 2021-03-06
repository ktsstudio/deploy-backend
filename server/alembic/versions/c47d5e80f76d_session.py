"""session

Revision ID: c47d5e80f76d
Revises: b904fa6a38f9
Create Date: 2021-08-25 18:22:47.636687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c47d5e80f76d"
down_revision = "b904fa6a38f9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "session",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("session")
    # ### end Alembic commands ###
