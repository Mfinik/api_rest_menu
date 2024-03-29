"""Initial migration

Revision ID: e20c8be2aed0
Revises: 
Create Date: 2023-08-31 23:16:27.965717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e20c8be2aed0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menus_id'), 'menus', ['id'], unique=False)
    op.create_index(op.f('ix_menus_title'), 'menus', ['title'], unique=False)
    op.create_table('submenus',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_submenus_id'), 'submenus', ['id'], unique=False)
    op.create_index(op.f('ix_submenus_title'), 'submenus', ['title'], unique=False)
    op.create_table('dishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('submenu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dishes_description'), 'dishes', ['description'], unique=False)
    op.create_index(op.f('ix_dishes_id'), 'dishes', ['id'], unique=False)
    op.create_index(op.f('ix_dishes_price'), 'dishes', ['price'], unique=False)
    op.create_index(op.f('ix_dishes_title'), 'dishes', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dishes_title'), table_name='dishes')
    op.drop_index(op.f('ix_dishes_price'), table_name='dishes')
    op.drop_index(op.f('ix_dishes_id'), table_name='dishes')
    op.drop_index(op.f('ix_dishes_description'), table_name='dishes')
    op.drop_table('dishes')
    op.drop_index(op.f('ix_submenus_title'), table_name='submenus')
    op.drop_index(op.f('ix_submenus_id'), table_name='submenus')
    op.drop_table('submenus')
    op.drop_index(op.f('ix_menus_title'), table_name='menus')
    op.drop_index(op.f('ix_menus_id'), table_name='menus')
    op.drop_table('menus')
    # ### end Alembic commands ###
