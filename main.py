from inventory import add_product, list_inventory, update_quantity

MENU = """
--- Mobile Shop Inventory ---
1. Aggiungi prodotto
2. Aggiorna quantita
3. Elenca inventario
4. Esci
"""


def menu_add_product():
    nome = input("Nome: ")
    categoria = input("Categoria: ")
    prezzo = float(input("Prezzo: "))
    quantita = int(input("Quantita: "))
    product_id = add_product(nome, categoria, prezzo, quantita)
    print(f"Prodotto aggiunto con id {product_id}")


def menu_update_quantity():
    product_id = int(input("ID prodotto: "))
    nuova_quantita = int(input("Nuova quantita: "))
    update_quantity(product_id, nuova_quantita)
    print("Quantita aggiornata")


def menu_list_inventory():
    rows = list_inventory()
    if not rows:
        print("Nessun prodotto in inventario")
        return
    for row in rows:
        product_id, nome, categoria, prezzo, quantita = row
        print(f"[{product_id}] {nome} - {categoria} - {prezzo} EUR - qta: {quantita}")


def main():
    while True:
        print(MENU)
        scelta = input("Scelta: ")
        try:
            if scelta == "1":
                menu_add_product()
            elif scelta == "2":
                menu_update_quantity()
            elif scelta == "3":
                menu_list_inventory()
            elif scelta == "4":
                break
            else:
                print("Scelta non valida")
        except ValueError as e:
            print(f"Errore: {e}")


if __name__ == "__main__":
    main()
