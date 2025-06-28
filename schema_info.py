dvdrental_schema = """
CREATE TABLE actor (
  actor_id INTEGER PRIMARY KEY, -- Unique ID for each actor
  first_name VARCHAR(45),
  last_name VARCHAR(45),
  last_update TIMESTAMP
);

CREATE TABLE address (
  address_id INTEGER PRIMARY KEY,
  address VARCHAR(50),
  address2 VARCHAR(50),
  district VARCHAR(20),
  city_id INTEGER, -- FK to city
  postal_code VARCHAR(10),
  phone VARCHAR(20),
  last_update TIMESTAMP
);

CREATE TABLE category (
  category_id INTEGER PRIMARY KEY,
  name VARCHAR(25),
  last_update TIMESTAMP
);

CREATE TABLE city (
  city_id INTEGER PRIMARY KEY,
  city VARCHAR(50),
  country_id INTEGER, -- FK to country
  last_update TIMESTAMP
);

CREATE TABLE country (
  country_id INTEGER PRIMARY KEY,
  country VARCHAR(50),
  last_update TIMESTAMP
);

CREATE TABLE customer (
  customer_id INTEGER PRIMARY KEY,
  store_id INTEGER, -- FK to store
  first_name VARCHAR(45),
  last_name VARCHAR(45),
  email VARCHAR(50),
  address_id INTEGER, -- FK to address
  activebool BOOLEAN,
  create_date DATE,
  last_update TIMESTAMP,
  active INTEGER
);

CREATE TABLE film (
  film_id INTEGER PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  release_year INTEGER,
  language_id INTEGER, -- FK to language
  rental_duration INTEGER,
  rental_rate NUMERIC(4,2),
  length INTEGER,
  replacement_cost NUMERIC(5,2),
  rating VARCHAR(10),
  last_update TIMESTAMP,
  special_features TEXT[],
  fulltext TSVECTOR
);

CREATE TABLE film_actor (
  actor_id INTEGER, -- FK to actor
  film_id INTEGER, -- FK to film
  last_update TIMESTAMP,
  PRIMARY KEY (actor_id, film_id)
);

CREATE TABLE film_category (
  film_id INTEGER, -- FK to film
  category_id INTEGER, -- FK to category
  last_update TIMESTAMP,
  PRIMARY KEY (film_id, category_id)
);

CREATE TABLE inventory (
  inventory_id INTEGER PRIMARY KEY,
  film_id INTEGER, -- FK to film
  store_id INTEGER, -- FK to store
  last_update TIMESTAMP
);

CREATE TABLE language (
  language_id INTEGER PRIMARY KEY,
  name VARCHAR(20),
  last_update TIMESTAMP
);

CREATE TABLE payment (
  payment_id INTEGER PRIMARY KEY,
  customer_id INTEGER, -- FK to customer
  staff_id INTEGER, -- FK to staff
  rental_id INTEGER, -- FK to rental
  amount NUMERIC(5,2),
  payment_date TIMESTAMP
);

CREATE TABLE rental (
  rental_id INTEGER PRIMARY KEY,
  rental_date TIMESTAMP,
  inventory_id INTEGER, -- FK to inventory
  customer_id INTEGER, -- FK to customer
  return_date TIMESTAMP,
  staff_id INTEGER, -- FK to staff
  last_update TIMESTAMP
);

CREATE TABLE staff (
  staff_id INTEGER PRIMARY KEY,
  first_name VARCHAR(45),
  last_name VARCHAR(45),
  address_id INTEGER, -- FK to address
  email VARCHAR(50),
  store_id INTEGER, -- FK to store
  active BOOLEAN,
  username VARCHAR(16),
  password VARCHAR(40),
  last_update TIMESTAMP,
  picture BYTEA
);

CREATE TABLE store (
  store_id INTEGER PRIMARY KEY,
  manager_staff_id INTEGER, -- FK to staff
  address_id INTEGER, -- FK to address
  last_update TIMESTAMP
);

-- Foreign Key Relationships (not enforced in CREATE TABLEs for brevity)
-- address.city_id → city.city_id
-- city.country_id → country.country_id
-- customer.address_id → address.address_id
-- customer.store_id → store.store_id
-- film.language_id → language.language_id
-- film_actor.actor_id → actor.actor_id
-- film_actor.film_id → film.film_id
-- film_category.film_id → film.film_id
-- film_category.category_id → category.category_id
-- inventory.film_id → film.film_id
-- inventory.store_id → store.store_id
-- rental.inventory_id → inventory.inventory_id
-- rental.customer_id → customer.customer_id
-- rental.staff_id → staff.staff_id
-- payment.customer_id → customer.customer_id
-- payment.staff_id → staff.staff_id
-- payment.rental_id → rental.rental_id
-- staff.address_id → address.address_id
-- staff.store_id → store.store_id
-- store.address_id → address.address_id
-- store.manager_staff_id → staff.staff_id
"""