CREATE TABLE "RolesUsers" (
	id INTEGER NOT NULL,
	user_id INTEGER,
	role_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES "User" (id),
	FOREIGN KEY(role_id) REFERENCES "Role" (id)
);

CREATE TABLE "Role" (
	id INTEGER NOT NULL,
	name VARCHAR(80) NOT NULL,
	description VARCHAR(255),
	PRIMARY KEY (id),
	UNIQUE (name)
);

CREATE TABLE "User" (
	id INTEGER NOT NULL,
	email VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	last_login_at DATETIME,
	current_login_at DATETIME,
	last_login_ip VARCHAR(100),
	current_login_ip VARCHAR(100),
	login_count INTEGER,
	active BOOLEAN,
	fs_uniquifier VARCHAR(255) NOT NULL,
	confirmed_at DATETIME,
	account_id INTEGER,
	PRIMARY KEY (id),
	UNIQUE (email),
	UNIQUE (name),
	UNIQUE (fs_uniquifier),
	FOREIGN KEY(account_id) REFERENCES "Account" (id)
);

CREATE TABLE "Currency" (
	id INTEGER NOT NULL,
	name VARCHAR(50) NOT NULL,
	exchange_rate REAL NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE "SubAccount" (
	id INTEGER NOT NULL,
	balance REAL,
	account_id INTEGER NOT NULL,
	currency_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(account_id) REFERENCES "Account" (id),
	FOREIGN KEY(currency_id) REFERENCES "Currency" (id)
);

CREATE TABLE "InternalTransaction" (
	id INTEGER NOT NULL,
	transaction_from INTEGER NOT NULL,
	transaction_to INTEGER NOT NULL,
	currency_id INTEGER NOT NULL,
	value REAL NOT NULL,
	transaction_date DATETIME NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY (id),
	FOREIGN KEY(transaction_from) REFERENCES "User" (id),
	FOREIGN KEY(transaction_to) REFERENCES "User" (id),
	FOREIGN KEY(currency_id) REFERENCES "Currency" (id)
);

CREATE TABLE "ExternalTransaction" (
	id INTEGER NOT NULL,
	transaction_from VARCHAR(500),
	transaction_to INTEGER NOT NULL,
	currency_id INTEGER NOT NULL,
	value REAL NOT NULL,
	transaction_date DATETIME NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY (id),
	FOREIGN KEY(transaction_to) REFERENCES "User" (id),
	FOREIGN KEY(currency_id) REFERENCES "Currency" (id)
);

CREATE TABLE "CurrencyExchange" (
	id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	currency_from INTEGER NOT NULL,
	currency_to INTEGER NOT NULL,
	value_old REAL NOT NULL,
	value_new REAL NOT NULL,
	exchange_date DATETIME NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES "User" (id),
	FOREIGN KEY(currency_from) REFERENCES "Currency" (id),
	FOREIGN KEY(currency_to) REFERENCES "Currency" (id)
);

CREATE TABLE "Account" (
	id INTEGER NOT NULL,
	active BOOLEAN NOT NULL,
	created_at DATETIME,
	PRIMARY KEY (id)
);