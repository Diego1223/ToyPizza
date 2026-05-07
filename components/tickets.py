import win32print
import time
def generar_ticket(folio, fecha, orden, total):
    for x in range(2):
        ticket = "\n"

        ticket += "Toy pizza & Mas\n"
        ticket += f"Folio: {folio}\n"
        ticket += f"Fecha: {fecha}\n"
        ticket += "Telefono: 8123594433\n"
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
        ticket += "Atendido por: Fili Toy\n"
        ticket += "Vuelva pronto\n\n\n"


        printer_name = "POS58 V9"

        handle = win32print.OpenPrinter(printer_name)
        job = win32print.StartDocPrinter(handle, 1, ("Ticket", None, "RAW"))
        win32print.StartPagePrinter(handle)

        abrir_cajon = b'\x1b\x70\x00\x19\xfa'

        # Enviar primero el comando
        win32print.WritePrinter(handle, abrir_cajon)

        # Luego el ticket
        win32print.WritePrinter(handle, ticket.encode("utf-8"))

        win32print.EndPagePrinter(handle)
        win32print.EndDocPrinter(handle)
        win32print.ClosePrinter(handle)
        time.sleep(5)