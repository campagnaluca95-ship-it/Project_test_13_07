# Mobile Shop Inventory

Repository didattico per esercitarsi con un workflow Git a due branch (`main` e `feat`) e con la gestione di un piccolo inventario per un centro di telefonia mobile, usando PostgreSQL puro (nessun ORM, nessun framework web).

## Branch

- `main`: gestione prodotti (tabella `products`) — aggiungi prodotto, aggiorna quantita, elenca inventario.
- `feat`: parte da `main` e aggiunge la registrazione vendite (tabella `sales`), con decremento automatico della quantita in `products`.

## Setup

1. Crea un virtualenv e installa le dipendenze:

   ```bash
   python -m venv venv
   source venv/bin/activate  # su Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copia `.env.example` in `.env` e imposta le credenziali del tuo database PostgreSQL:

   ```bash
   cp .env.example .env
   ```

3. Crea il database e applica lo schema:

   ```bash
   psql -U <utente> -d <database> -f schema.sql
   ```

## Uso

```bash
python main.py
```

Il menu CLI permette di:
1. Aggiungere un prodotto
2. Aggiornare la quantita di un prodotto
3. Elencare l'inventario
4. Uscire

(Sul branch `feat` è disponibile anche l'opzione "Registra vendita".)

## Test

I test usano un database Postgres di test (connessione letta da `.env`) e puliscono le tabelle coinvolte prima/dopo ogni test.

```bash
pytest
```

## CI Pipeline

La pipeline definita in `.github/workflows/ci.yml` gira su push/PR verso `main` e `feat`:

| Step | Descrizione |
|------|-------------|
| Checkout | Scarica il codice del repository |
| Setup Python | Installa Python 3.12 |
| Install dependencies | Installa le dipendenze da `requirements.txt` |
| Servizio Postgres | Avvia un container Postgres 16 di supporto |
| Apply database schema | Applica `schema.sql` al database di test |
| Run tests | Esegue `pytest` |
