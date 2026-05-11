import flet as ft
from database.complementos_db import complementos_db

def crear_dialogo_complementos(page,orden, actualizar_lista):
    contenido = ft.Column()
    #recibir una lista
    complementos_catalogo = complementos_db()
    complementos_temp = {}
    editando_complemento = {"index": None}

    def cerrar_modal():
        dialog.open = False
        page.update()
 
    
    def confirmar_complementos():
        items_nuevos = []

        for nombre, cantidad in list(complementos_temp.items()):
            if cantidad == 0:
                continue

            comp = next(
                c for c in complementos_catalogo
                if c["nombre"] == nombre
            )

            nuevo_item = {
                "tipo_item": "complemento",
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": comp["precio"] * cantidad
            }

            items_nuevos.append(nuevo_item)

        if editando_complemento["index"] is not None:
            if items_nuevos:
                orden[editando_complemento["index"]] = items_nuevos[0]

            editando_complemento["index"] = None
        else:
            orden.extend(items_nuevos)

        complementos_temp.clear()
        cerrar_modal()
        actualizar_lista()
        page.update()

    def abrir_complementos(e=None):
        contenido.controls.clear()
        
        nombre_editando = None
        #Si estamos editando, detectamos cual complemento es
        if editando_complemento["index"] is not None:
            item = orden[editando_complemento["index"]]
            nombre_editando = item["nombre"]


        for comp in complementos_catalogo:
            nombre = comp["nombre"]

            cantidad_text = ft.Text(
                str(complementos_temp.get(nombre, 0)),
                text_align=ft.TextAlign.CENTER
            )
            
            #Si estamos editando detectamos cual complemento es

            bloqueado = (
                nombre_editando is not None
                and nombre != nombre_editando
            )

            def sumar(e, n=nombre, txt=cantidad_text):
                complementos_temp[n] = complementos_temp.get(n, 0) + 1
                txt.value = str(complementos_temp[n])
                page.update()

            def restar(e, n=nombre, txt=cantidad_text):
                if complementos_temp.get(n, 0) > 0:
                    complementos_temp[n] -= 1
                    txt.value = str(complementos_temp[n])
                    page.update()

            fila = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                nombre,
                                size=15,
                                weight=ft.FontWeight.W_500
                            ),
                            width=320
                        ),

                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            on_click=restar,
                            disabled=bloqueado
                        ),

                        ft.Container(
                            content=cantidad_text,
                            width=40,
                        ),

                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            on_click=sumar,
                            disabled=bloqueado
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10,
                border_radius=10,
                bgcolor="#f8f8f8",
                margin=ft.margin.only(bottom=8)
            )
            contenido.controls.append(fila)

        dialog.open = True
        page.update()

    def cargar_complementos(item, index):
        complementos_temp.clear()
        complementos_temp[item["nombre"]] = item["cantidad"]
        editando_complemento["index"] = index

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Complementos"),
        content=ft.Container(
            content=contenido,
            width=700,
            height=450,
            padding=10
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: cerrar_modal()
            ),
            ft.TextButton(
                "Agregar",
                on_click=lambda e: confirmar_complementos()
            )
        ]
    )

    page.overlay.append(dialog)

    return (
        dialog,
        abrir_complementos,
        cargar_complementos
    )
    
