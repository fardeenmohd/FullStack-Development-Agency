CREATE TABLE notifications_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, event_type)
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
