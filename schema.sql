CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    prezzo NUMERIC(10, 2) NOT NULL,
    quantita INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantita INTEGER NOT NULL,
    data_vendita TIMESTAMP NOT NULL DEFAULT now()
);
