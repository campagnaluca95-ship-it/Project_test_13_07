CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    prezzo NUMERIC(10, 2) NOT NULL,
    quantita INTEGER NOT NULL
);
