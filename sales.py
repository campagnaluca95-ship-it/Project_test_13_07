from db import get_connection


def register_sale(product_id, quantita):
    if quantita <= 0:
        raise ValueError("La quantita venduta deve essere maggiore di zero")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT quantita FROM products WHERE id = %s FOR UPDATE",
                (product_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Prodotto con id {product_id} non trovato")

            disponibile = row[0]
            if quantita > disponibile:
                raise ValueError(
                    f"Quantita richiesta ({quantita}) superiore alla disponibilita ({disponibile})"
                )

            cur.execute(
                "UPDATE products SET quantita = quantita - %s WHERE id = %s",
                (quantita, product_id),
            )
            cur.execute(
                """
                INSERT INTO sales (product_id, quantita)
                VALUES (%s, %s)
                RETURNING id
                """,
                (product_id, quantita),
            )
            sale_id = cur.fetchone()[0]
        conn.commit()
        return sale_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
