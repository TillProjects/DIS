-- Estate Agents
INSERT INTO estate_agent (name, address, login_name, login_password)
VALUES 
('Max Mustermann', 'Main Street 1, 12345 Sampletown', 'max', '123456789'),
('Lisa Müller', 'Agentenstraße 5, 98765 Musterstadt', 'lisa', 'passwort456'),
('Tom Schmidt', 'Immoallee 7, 54321 Häuserdorf', 'tom', 'haus123');

-- Persons
INSERT INTO person (first_name, surname, address)
VALUES 
('John', 'Doe', 'Sample Street 2, 12345 Sampletown'),
('Anna', 'Meier', 'Lindenweg 4, 23456 Neuburg'),
('Peter', 'Parker', 'Webstraße 8, 11111 Spinnenstadt');

-- Apartments
INSERT INTO apartment (city, postal_code, street, street_number, square_area, floor, rent, rooms, has_balcony, has_built_in_kitchen, manager)
VALUES 
('Berlin', '10115', 'Invalidenstrasse', '98', 85.00, 3, 950.00, 3, true, true, 1),
('Hamburg', '20095', 'Mönckebergstraße', '12A', 60.00, 2, 750.00, 2, false, true, 2),
('München', '80331', 'Leopoldstraße', '22', 120.00, 5, 1500.00, 4, true, true, 3);

-- Houses
INSERT INTO house (city, postal_code, street, street_number, square_area, floors, price, has_garden, manager)
VALUES 
('Berlin', '10115', 'Schwartzkopffstrasse', '12', 250.00, 2, 550000.00, true, 1),
('Köln', '50667', 'Domstraße', '5', 180.00, 1, 420000.00, false, 2),
('Frankfurt', '60311', 'Mainkai', '3', 300.00, 3, 750000.00, true, 3);

-- Tenancy Contracts
INSERT INTO tenancy_contract (date, place, start_date, duration, additional_costs, person, apartment)
VALUES 
('2025-04-01', 'Berlin', '2025-04-15', 12, 150.00, 1, 1),
('2025-03-20', 'Hamburg', '2025-04-01', 24, 100.00, 2, 2);

-- Purchase Contracts
INSERT INTO purchase_contract (date, place, no_of_installments, interest_rate, person, house)
VALUES 
('2025-04-10', 'Berlin', 24, 2.50, 1, 1),
('2025-03-15', 'Frankfurt', 36, 3.20, 3, 3);
