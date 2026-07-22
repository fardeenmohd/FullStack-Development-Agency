CREATE TABLE segment_leads (
    id SERIAL PRIMARY KEY,
    lead_id INT NOT NULL,
    country VARCHAR(255) NOT NULL,
    industry VARCHAR(255) NOT NULL,
    product_interest VARCHAR(255) NOT NULL
);
