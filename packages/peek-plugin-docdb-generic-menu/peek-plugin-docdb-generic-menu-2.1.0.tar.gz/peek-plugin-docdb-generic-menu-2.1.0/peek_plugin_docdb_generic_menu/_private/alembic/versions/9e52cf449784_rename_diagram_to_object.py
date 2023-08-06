"""rename diagram to object

Peek Plugin Database Migration Script

Revision ID: 9e52cf449784
Revises: bac1e4f7a3d9
Create Date: 2019-07-28 14:35:58.718257

"""

# revision identifiers, used by Alembic.
revision = '9e52cf449784'
down_revision = 'bac1e4f7a3d9'
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.rename_table("DiagramGenericMenu", "Menu",
                    schema='pl_docdb_generic_menu')


def downgrade():
    op.rename_table("Menu", "DiagramGenericMenu",
                    schema='pl_docdb_generic_menu')