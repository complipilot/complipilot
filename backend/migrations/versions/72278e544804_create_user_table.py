"""create user table

Revision ID: 72278e544804
Revises: 
Create Date: 2025-04-30 14:42:22.032214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '72278e544804'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)

    op.create_table(
        'policy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('title',    sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('file_path', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'gap',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('policy_id', sa.Integer(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('severity',    sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at',  sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['policy_id'], ['policy.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('gap_id', sa.Integer(), nullable=False),
        sa.Column('assigned_to', sa.Integer(), nullable=True),
        sa.Column('title',   sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('status',  sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['assigned_to'], ['user.id']),
        sa.ForeignKeyConstraint(['gap_id'], ['gap.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'evidence',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('file_path',    sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('uploaded_at',  sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['task.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('evidence')
    op.drop_table('task')
    op.drop_table('gap')
    op.drop_table('policy')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
