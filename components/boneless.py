import flet as ft
from database.boneless_db import get_boneless, get_salsas


def crear_dialogo_boneless(page, orden, actualizar_lista):
    contenido = ft.Column()

    boneless_catalogo = get_boneless()
    salsas_catalogo = get_salsas()

    boneless_temp = {}
    salsas_temp = {}

    editando_boneless = {"index": None}

    def cerrar_modal():
        dialog.open = False
        page.update()

    def calcular_precio_boneless():
        """
        Boneless:
        - precio base
        - 2 salsas gratis
        - desde la 3ra: $15 c/u
        """

        boneless_info = boneless_catalogo[0]

        precio_base = boneless_info["precio_base"]
        salsas_gratis = boneless_info["salsas_gratis"]
        precio_extra = boneless_info["precio_extra_salsa"]

        total_salsas = sum(salsas_temp.values())

        extras = max(0, total_salsas - salsas_gratis)

        return precio_base + (extras * precio_extra)

    def confirmar_boneless():
        items_nuevos = []

        for nombre, cantidad in boneless_temp.items():
            if cantidad == 0:
                continue

            precio_final = calcular_precio_boneless() * cantidad

            nuevo_item = {
                "tipo_item": "boneless",
                "nombre": nombre,
                "cantidad": cantidad,
                "salsas": salsas_temp.copy(),
                "precio": precio_final
            }

            items_nuevos.append(nuevo_item)

        if editando_boneless["index"] is not None:
            if items_nuevos:
                orden[editando_boneless["index"]] = items_nuevos[0]

            editando_boneless["index"] = None
        else:
            orden.extend(items_nuevos)

        boneless_temp.clear()
        salsas_temp.clear()

        cerrar_modal()
        actualizar_lista()
        page.update()

    def abrir_boneless(e=None):
        contenido.controls.clear()

        # ======================
        # BONeless principal
        # ======================

        for item in boneless_catalogo:
            nombre = item["nombre"]

            cantidad_text = ft.Text(
                str(boneless_temp.get(nombre, 0)),
                text_align=ft.TextAlign.CENTER
            )

            def sumar(e, n=nombre, txt=cantidad_text):
                boneless_temp[n] = boneless_temp.get(n, 0) + 1
                txt.value = str(boneless_temp[n])
                page.update()

            def restar(e, n=nombre, txt=cantidad_text):
                if boneless_temp.get(n, 0) > 0:
                    boneless_temp[n] -= 1
                    txt.value = str(boneless_temp[n])
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
                            width=300
                        ),

                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            on_click=restar
                        ),

                        ft.Container(
                            content=cantidad_text,
                            width=40,
                        ),

                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            on_click=sumar
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

        # ======================
        # SALSAS
        # ======================

        contenido.controls.append(ft.Divider())

        contenido.controls.append(
            ft.Text(
                "Seleccionar salsas (2 gratis)",
                size=16,
                weight=ft.FontWeight.BOLD
            )
        )

        for salsa in salsas_catalogo:
            nombre_salsa = salsa["nombre"]

            cantidad_salsa_text = ft.Text(
                str(salsas_temp.get(nombre_salsa, 0)),
                text_align=ft.TextAlign.CENTER
            )

            def sumar_salsa(e, n=nombre_salsa, txt=cantidad_salsa_text):
                salsas_temp[n] = salsas_temp.get(n, 0) + 1
                txt.value = str(salsas_temp[n])
                page.update()

            def restar_salsa(e, n=nombre_salsa, txt=cantidad_salsa_text):
                if salsas_temp.get(n, 0) > 0:
                    salsas_temp[n] -= 1
                    txt.value = str(salsas_temp[n])
                    page.update()

            fila_salsa = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(nombre_salsa),
                            width=250
                        ),

                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            on_click=restar_salsa
                        ),

                        ft.Container(
                            content=cantidad_salsa_text,
                            width=40
                        ),

                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            on_click=sumar_salsa
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=8,
                border_radius=8,
                bgcolor="#f8f8f8",
                margin=ft.margin.only(bottom=5)
            )

            contenido.controls.append(fila_salsa)

        dialog.open = True
        page.update()

    def cargar_boneless(item, index):
        boneless_temp.clear()
        salsas_temp.clear()

        boneless_temp[item["nombre"]] = item["cantidad"]

        for nombre_salsa, cantidad in item.get("salsas", {}).items():
            salsas_temp[nombre_salsa] = cantidad

        editando_boneless["index"] = index

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Boneless"),
        content=ft.Container(
            content=contenido,
            width=700,
            height=500,
            padding=10
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: cerrar_modal()
            ),
            ft.TextButton(
                "Agregar",
                on_click=lambda e: confirmar_boneless()
            )
        ]
    )

    page.overlay.append(dialog)

    return (
        dialog,
        abrir_boneless,
        cargar_boneless
    )