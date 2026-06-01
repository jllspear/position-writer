"""create generic_payload

Revision ID: 001
Revises:
Create Date: 2026-05-29
"""

from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    op.execute("CREATE SCHEMA IF NOT EXISTS writer")

    op.create_table(
        "generic_payload",
        sa.Column("id",
                  sa.BigInteger(),
                  primary_key=True,
        ),
        sa.Column(
            "topic",
            sa.String(length=512),
            nullable=False,
        ),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="writer",
    )

    op.create_index(
        "ix_generic_payload_topic",
        "generic_payload",
        ["topic"],
        unique=False,
        schema="writer",
    )

    op.execute("""
        CREATE INDEX ix_generic_payload_payload_gin
        ON writer.generic_payload
        USING GIN (payload)
    """)


def downgrade():

    op.drop_index(
        "ix_generic_payload_payload_gin",
        table_name="generic_payload",
        schema="writer",
    )

    op.drop_index(
        "ix_generic_payload_topic",
        table_name="generic_payload",
        schema="writer",
    )

    op.drop_table(
        "generic_payload",
        schema="writer",
    )

    op.execute("DROP SCHEMA IF EXISTS writer")
