from sqlalchemy import create_engine, text

# Function to execute a query and fetch results as dictionaries
def fetch_data(query):
    engine = create_engine('your_database_connection_string')
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return [dict(row) for row in result]

# Aggregate trade metrics from the database
def aggregate_trade_metrics():
    return fetch_data("SELECT * FROM trade_metrics")

# Get active leads from the database
def get_active_leads():
    return fetch_data("SELECT * FROM active_leads")

# Fetch transaction statuses from the database
def fetch_transaction_statuses():
    return fetch_data("SELECT * FROM transaction_statuses")
