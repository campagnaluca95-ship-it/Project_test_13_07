from db import get_connection


def add_product(nome, categoria, prezzo, quantita):
    if not nome or not nome.strip():
        raise ValueError("Il nome del prodotto non puo essere vuoto")
    if prezzo <= 0:
        raise ValueError("Il prezzo deve essere maggiore di zero")
    if quantita < 0:
        raise ValueError("La quantita non puo essere negativa")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO products (nome, categoria, prezzo, quantita)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (nome, categoria, prezzo, quantita),
            )
            product_id = cur.fetchone()[0]
        conn.commit()
        return product_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_quantity(product_id, nuova_quantita):
    if nuova_quantita < 0:
        raise ValueError("La quantita non puo essere negativa")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE products SET quantita = %s WHERE id = %s",
                (nuova_quantita, product_id),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Prodotto con id {product_id} non trovato")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def list_inventory():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nome, categoria, prezzo, quantita FROM products ORDER BY id"
            )
            return cur.fetchall()
    finally:
        conn.close()
