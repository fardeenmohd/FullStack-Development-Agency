CREATE TABLE conversion_rates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    exporter_id INT NOT NULL,
    conversion_rate DECIMAL(5, 4) NOT NULL,
    CONSTRAINT fk_exporter_id FOREIGN KEY (exporter_id) REFERENCES exporters(id)
);
