DROP TABLE IF EXISTS contract;
DROP TABLE IF EXISTS tenancy_contract;
DROP TABLE IF EXISTS purchase_contract;
DROP TABLE IF EXISTS estate;
DROP TABLE IF EXISTS house;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS apartment;
DROP TABLE IF EXISTS estate_agent;


CREATE TABLE IF NOT EXISTS estate_agent (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    login_name TEXT UNIQUE,
    login_password TEXT NOT NULL
);

--- is estate necessary? ---
CREATE TABLE IF NOT EXISTS estate (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    street TEXT NOT NULL,
    street_number TEXT NOT NULL,
    square_area NUMERIC(10,2) NOT NULL,
    manager INTEGER NOT NULL,
    CONSTRAINT fk_manager_estate FOREIGN KEY (manager) REFERENCES estate_agent(id)
);

CREATE TABLE IF NOT EXISTS apartment (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    street TEXT NOT NULL,
    street_number TEXT NOT NULL,
    square_area NUMERIC(10,2) NOT NULL,
    floor SMALLINT,
    rent NUMERIC(10,2),
    rooms SMALLINT,
    has_balcony BOOLEAN,
    has_built_in_kitchen BOOLEAN,
    manager INTEGER NOT NULL,
    CONSTRAINT fk_manager_apartment FOREIGN KEY (manager) REFERENCES estate_agent(id)
);

CREATE TABLE IF NOT EXISTS house (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    street TEXT NOT NULL,
    street_number TEXT NOT NULL,
    square_area NUMERIC(10,2) NOT NULL,
    floors SMALLINT,
    price NUMERIC(12,2),
    has_garden BOOLEAN,
    manager INTEGER NOT NULL,
    CONSTRAINT fk_manager_house FOREIGN KEY (manager) REFERENCES estate_agent(id)
);

CREATE TABLE IF NOT EXISTS person (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    address TEXT
);

--- is contract necessary? ---
CREATE TABLE IF NOT EXISTS contract (
    contract_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    place TEXT NOT NULL,
    person_id INTEGER NOT NULL,
    CONSTRAINT fk_person_id_contract FOREIGN KEY (person_id) REFERENCES person(id)
);

--- are the relationships correct here? Own table? ---
CREATE TABLE IF NOT EXISTS tenancy_contract (
    contract_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    place TEXT NOT NULL,
    start_date DATE NOT NULL,
    duration INTEGER NOT NULL,
    additional_costs NUMERIC(10,2),
    person INTEGER NOT NULL,
    apartment INTEGER NOT NULL,
    CONSTRAINT fk_person_tenancy_contract FOREIGN KEY (person) REFERENCES person(id),
    CONSTRAINT fk_apartment_tenancy_contract FOREIGN KEY (apartment) REFERENCES apartment(id)
);

CREATE TABLE IF NOT EXISTS purchase_contract (
    contract_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    place TEXT NOT NULL,
    no_of_installments SMALLINT,
    interest_rate NUMERIC(5,2),
    person INTEGER NOT NULL,
    house INTEGER NOT NULL,
    CONSTRAINT fk_person_purchase_contract FOREIGN KEY (person) REFERENCES person(id),
    CONSTRAINT fk_house_purchase_contract FOREIGN KEY (house) REFERENCES house(id)
);
