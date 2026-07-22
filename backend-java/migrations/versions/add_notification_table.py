from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'your_revision_id'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table named 'notification' with specified columns and constraints
    op.create_table(
        'notification',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('lead_id', sa.Integer, nullable=False),
        sa.Column('exporter_id', sa.Integer, nullable=False),
        sa.Column('notification_type', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False)
    )

def downgrade():
    # Drop the 'notification' table
    op.drop_table('notification')
