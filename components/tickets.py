import win32print

def generar_ticket(folio, fecha, orden, total):
    ticket = ""

    ticket += "Toy pizza"
    ticket += "-" * 30 + "\n"
    ticket += f"Folio: {folio}\n"
    ticket += f"Fecha: {fecha}\n"
    ticket += "Telefono: "
    ticket += "-" * 30 + "\n"

    for item in orden:
        if item.get("tipo_item") == "complemento":
            ticket += f"{item['nombre']} x {item['cantidad']}\n"
            ticket += f"${item['precio']}\n\n"

        else:
            ticket += f"Pizza {item['tamano']} - {item['tipo_base']}\n"

            if item["tipo"] == "mitad":
                ingredientes = (
                    f"{', '.join(item['lado1'])} / "
                    f"{', '.join(item['lado2'])}"
                )
            else:
                ingredientes = ", ".join(item["ingredientes"])

            ticket += f"{ingredientes}\n"
            ticket += f"${item['precio']}\n\n"

    ticket += "-" * 30 + "\n"
    ticket += f"TOTAL: ${total}\n"
    ticket += "-" * 30 + "\n"
    ticket += "Gracias por su compra\n"

    return ticket

