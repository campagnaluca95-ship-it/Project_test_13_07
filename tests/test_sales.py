import pytest

from db import get_connection
from inventory import add_product, list_inventory
from sales import register_sale


@pytest.fixture(autouse=True)
def clean_tables():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM sales")
        cur.execute("DELETE FROM products")
    conn.commit()
    conn.close()
    yield
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM sales")
        cur.execute("DELETE FROM products")
    conn.commit()
    conn.close()


def test_register_sale_decrementa_quantita():
    product_id = add_product("iPhone 13", "Smartphone", 699.99, 10)

    sale_id = register_sale(product_id, 3)

    assert sale_id is not None
    rows = list_inventory()
    assert rows[0][4] == 7


def test_register_sale_quantita_insufficiente():
    product_id = add_product("SIM Vodafone", "SIM", 9.99, 2)

    with pytest.raises(ValueError):
        register_sale(product_id, 5)

    # la quantita non deve essere modificata in caso di errore
    rows = list_inventory()
    assert rows[0][4] == 2


def test_register_sale_prodotto_inesistente():
    with pytest.raises(ValueError):
        register_sale(9999, 1)


def test_register_sale_quantita_non_positiva():
    product_id = add_product("iPhone 13", "Smartphone", 699.99, 10)

    with pytest.raises(ValueError):
        register_sale(product_id, 0)

    rows = list_inventory()
    assert rows[0][4] == 10
