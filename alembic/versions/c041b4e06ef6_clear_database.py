"""Clear database

Revision ID: c041b4e06ef6
Revises: e20c8be2aed0
Create Date: 2023-09-01 01:33:46.159407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c041b4e06ef6'
down_revision = 'e20c8be2aed0'
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