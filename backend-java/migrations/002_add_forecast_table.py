from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table named 'forecast' with specified columns and constraints
    op.create_table(
        'forecast',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('historical_data', sa.JSON, nullable=True),
        sa.Column('market_trends', sa.JSON, nullable=True),
        sa.Column('predicted_conversion_rate', sa.Float, nullable=True)
    )

def downgrade():
    # Drop the 'forecast' table
    op.drop_table('forecast')
