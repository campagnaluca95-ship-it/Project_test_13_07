import pytest

from db import get_connection
from inventory import add_product, list_inventory, update_quantity


@pytest.fixture(autouse=True)
def clean_products_table():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products")
    conn.commit()
    conn.close()
    yield
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM products")
    conn.commit()
    conn.close()


def test_add_product():
    product_id = add_product("iPhone 13", "Smartphone", 699.99, 10)
    assert product_id is not None

    rows = list_inventory()
    assert len(rows) == 1
    assert rows[0][1] == "iPhone 13"
    assert rows[0][2] == "Smartphone"
    assert float(rows[0][3]) == 699.99
    assert rows[0][4] == 10


def test_update_quantity():
    product_id = add_product("Cover Silicone", "Accessorio", 9.99, 50)
    update_quantity(product_id, 40)

    rows = list_inventory()
    assert rows[0][4] == 40


def test_update_quantity_prodotto_inesistente():
    with pytest.raises(ValueError):
        update_quantity(9999, 5)


def test_list_inventory_vuoto():
    rows = list_inventory()
    assert rows == []


def test_list_inventory_piu_prodotti():
    add_product("iPhone 13", "Smartphone", 699.99, 10)
    add_product("SIM Vodafone", "SIM", 9.99, 100)

    rows = list_inventory()
    assert len(rows) == 2
