# Mobile Shop Inventory — Design

## Scopo

Repository didattico, semplice da leggere e studiare, per esercitarsi con:
- un workflow Git a due branch (`main` e `feat`)
- gestione di un piccolo inventario per un centro di telefonia mobile, con database PostgreSQL

Non è un progetto di produzione: niente framework web, niente ORM, niente autenticazione.

## Stack

- Python 3 (nessuna dipendenza da versioni specifiche avanzate)
- PostgreSQL
- `psycopg2-binary` per la connessione al DB (SQL parametrizzato, nessun ORM)
- `python-dotenv` per leggere le credenziali da `.env`
- `pytest` per i test

## Struttura repo

```
mobile-shop-inventory/
├── README.md              # setup, comandi, spiegazione branch main/feat
├── requirements.txt
├── .env.example            # DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
├── .gitignore
├── schema.sql               # DDL tabelle
├── db.py                     # get_connection()
├── inventory.py               # funzioni su tabella products
├── main.py                     # menu CLI
└── tests/
    └── test_inventory.py
```

## Modello dati

### Branch `main`

Tabella `products`:

| colonna    | tipo          | note                  |
|------------|---------------|-----------------------|
| id         | SERIAL PK     |                       |
| nome       | TEXT          | es. "iPhone 13"       |
| categoria  | TEXT          | testo libero, es. "Smartphone", "Accessorio", "SIM" |
| prezzo     | NUMERIC(10,2) |                       |
| quantita   | INTEGER       | quantità a magazzino  |

Funzioni in `inventory.py`:
- `add_product(nome, categoria, prezzo, quantita)` → inserisce riga
- `update_quantity(product_id, nuova_quantita)` → aggiorna quantità
- `list_inventory()` → ritorna tutte le righe di `products`

`main.py`: menu CLI con 3 opzioni (aggiungi prodotto, aggiorna quantità, elenca inventario) + uscita.

`tests/test_inventory.py`: test pytest che verificano le 3 funzioni contro un DB Postgres di test (connessione da `.env` di test), con setup/teardown che pulisce la tabella tra i test.

### Branch `feat` (a partire da `main`)

Aggiunge tabella `sales`:

| colonna     | tipo      | note                          |
|-------------|-----------|-------------------------------|
| id          | SERIAL PK |                               |
| product_id  | INTEGER   | FK → products.id              |
| quantita    | INTEGER   | quantità venduta               |
| data_vendita| TIMESTAMP | default `now()`                |

Nuovo file `sales.py`:
- `register_sale(product_id, quantita)` → inserisce riga in `sales` e decrementa `products.quantita` della stessa quantità, in una singola transazione. Se la quantità richiesta supera la disponibilità, solleva un errore e non modifica nulla.

`main.py` aggiornato con una 4ª opzione "Registra vendita".

`tests/test_sales.py`: test pytest per `register_sale`, incluso il caso di quantità insufficiente.

## Gestione errori

Errori applicativi semplici (es. prodotto inesistente, quantità insufficiente) vengono segnalati con eccezioni Python standard (`ValueError`) e un messaggio leggibile stampato dal menu CLI — nessun framework di gestione errori, per restare aderenti allo scopo didattico.

## Non in scope

- Autenticazione/utenti
- API HTTP
- ORM
- Categorie come tabella separata o fornitori (rimandati a un eventuale sviluppo futuro)
