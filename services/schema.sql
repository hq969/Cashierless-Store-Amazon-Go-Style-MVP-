CREATE TABLE IF NOT EXISTS person_session (
    id SERIAL PRIMARY KEY,
    person_id VARCHAR(50),
    entry_time TIMESTAMP,
    exit_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shelf (
    id SERIAL PRIMARY KEY,
    shelf_id VARCHAR(20),
    sku VARCHAR(20),
    unit_price FLOAT,
    item_weight_g FLOAT
);

CREATE TABLE IF NOT EXISTS vision_event (
    id SERIAL PRIMARY KEY,
    person_id VARCHAR(50),
    shelf_id VARCHAR(20),
    ts TIMESTAMP,
    event_type VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS sensor_event (
    id SERIAL PRIMARY KEY,
    shelf_id VARCHAR(20),
    ts TIMESTAMP,
    delta_g FLOAT
);

CREATE TABLE IF NOT EXISTS cart_line (
    id SERIAL PRIMARY KEY,
    person_id VARCHAR(50),
    sku VARCHAR(20),
    qty INT,
    unit_price FLOAT,
    ts TIMESTAMP
);

CREATE TABLE IF NOT EXISTS receipt (
    id SERIAL PRIMARY KEY,
    person_id VARCHAR(50),
    total FLOAT,
    ts TIMESTAMP,
    pay_ref VARCHAR(50),
    status VARCHAR(20)
);
