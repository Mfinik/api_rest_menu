"""clear base 05

Revision ID: f0eacbc3e47a
Revises: f493da1afd90
Create Date: 2023-09-04 20:45:27.587158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0eacbc3e47a'
down_revision = 'f493da1afd90'
branch_labels = None
depends_on = None


# Очистка таблиц
def clear_database():
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM dishes"))
    conn.execute(sa.text("DELETE FROM submenus"))
    conn.execute(sa.text("DELETE FROM menus"))


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    clear_database()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
