"""create_vacation_model_and_add_timezoned_employee

Revision ID: 9ac51baae378
Revises: c782c730870f
Create Date: 2023-03-04 22:24:22.245760

"""
import sqlalchemy as sa
from alembic import op

from app.model.base import CustomUUID

# revision identifiers, used by Alembic.
revision = "9ac51baae378"
down_revision = "c782c730870f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vacation",
        sa.Column("id", CustomUUID, nullable=False),
        sa.Column("employee_id", CustomUUID, nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column(
            "type", sa.Enum("UNPAID", "PAID", name="vacationtype"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employee.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_vacation_id"), "vacation", ["id"], unique=False)
    op.add_column("employee", sa.Column("timezone", sa.String(), nullable=True))

    # add default value for timezone for existing employees
    op.execute("UPDATE employee SET timezone = 'Europe/Paris'")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("employee", "timezone")
    op.drop_index(op.f("ix_vacation_id"), table_name="vacation")
    op.drop_table("vacation")
    # ### end Alembic commands ###