import flet as ft
from database.generar_folio import obtener_folio_diario
import sqlite3
from datetime import datetime

def main(page: ft.Page):
    page.title = "POS Pizzería"

    ingredientes = [
        "Peperoni", "Jamón", "Piña", "Salami",
        "Champiñones", "Extra queso"
    ]

    orden = []
    editando_index = None

    # LISTAS SEPARADAS
    lado1 = []
    lado2 = []

    lado1_ui = ft.Column()
    lado2_ui = ft.Column()

    lista_pedidos = ft.Column(scroll="auto")
    total_text = ft.Text("Total: $0")

    
    # -----------------------
    # AUTOCOMPLETE
    # -----------------------
    def crear_autocomplete(lado):
        input_field = ft.TextField(label="Agregar ingrediente")

        sugerencias = ft.Column()
        container = ft.Container(
            sugerencias,
            visible=False,
            bgcolor="#eee",
            padding=5
        )

        def filtrar(e):
            texto = input_field.value.lower()
            sugerencias.controls.clear()

            if texto == "":
                container.visible = False
                page.update()
                return

            resultados = [i for i in ingredientes if texto in i.lower()]

            container.visible = bool(resultados)

            for r in resultados:
                sugerencias.controls.append(
                    ft.ListTile(
                        title=ft.Text(r),
                        on_click=lambda e, val=r: seleccionar(val)
                    )
                )

            page.update()

        def seleccionar(valor):
            if lado == 1:
                lado1.append(valor)
                actualizar_ui_lado1()
            else:
                lado2.append(valor)
                actualizar_ui_lado2()

            input_field.value = ""
            container.visible = False
            page.update()

        input_field.on_change = filtrar

        return ft.Column([input_field, container])

    # -----------------------
    # UI LADOS
    # -----------------------
    def actualizar_ui_lado1():
        lado1_ui.controls.clear()
        for i, ing in enumerate(lado1):
            lado1_ui.controls.append(
                ft.Row([
                    ft.Text(ing),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, idx=i: eliminar_ing(1, idx)
                    )
                ])
            )

    def actualizar_ui_lado2():
        lado2_ui.controls.clear()
        for i, ing in enumerate(lado2):
            lado2_ui.controls.append(
                ft.Row([
                    ft.Text(ing),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, idx=i: eliminar_ing(2, idx)
                    )
                ])
            )
        

    def eliminar_ing(lado, index):
        if lado == 1:
            lado1.pop(index)
            actualizar_ui_lado1()
        else:
            lado2.pop(index)
            actualizar_ui_lado2()

    # -----------------------
    # CAMPOS
    # -----------------------
    tamano = ft.Dropdown(
        label="Tamaño",
        options=[
            ft.dropdown.Option("Chica"),
            ft.dropdown.Option("Mediana"),
            ft.dropdown.Option("Grande"),
        ]
    )

    tipo = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="completa", label="Completa"),
            ft.Radio(value="mitad", label="Mitades")
        ])
    )

    auto1 = crear_autocomplete(1)
    auto2 = crear_autocomplete(2)

    # -----------------------
    # FUNCIONES
    # -----------------------
    def agregar_pizza(e):
        nonlocal editando_index

        if not tamano.value:
            return

        precios = {"Chica": 100, "Mediana": 150, "Grande": 180}

        if tipo.value == "mitad":
            pizza = {
                "tamano": tamano.value,
                "tipo": "mitad",
                "lado1": lado1.copy(),
                "lado2": lado2.copy(),
                "precio": precios[tamano.value]
            }
        else:
            pizza = {
                "tamano": tamano.value,
                "tipo": "completa",
                "ingredientes": lado1.copy(),
                "precio": precios[tamano.value]
            }

        if editando_index is not None:
            orden[editando_index] = pizza
            editando_index = None

            boton_agregar.content = "Agregar"
        else:
            orden.append(pizza)

        limpiar()
        actualizar_lista()
        page.update()

    def limpiar():
        lado1.clear()
        lado2.clear()
        actualizar_ui_lado1()
        actualizar_ui_lado2()


    def actualizar_lista():
        lista_pedidos.controls.clear()
        total = 0

        for i, p in enumerate(orden):

            def eliminar(e, index=i):
                orden.pop(index)
                actualizar_lista()

            def editar(e, index=i):
                boton_agregar.content = "Guardar cambios"
                boton_agregar.update()
                nonlocal editando_index

                pizza = orden[index]

                tamano.value = pizza["tamano"]
                tipo.value = pizza["tipo"]

                lado1.clear()
                lado2.clear()

                if pizza["tipo"] == "mitad":
                    lado1.extend(pizza["lado1"])
                    lado2.extend(pizza["lado2"])
                else:
                    lado1.extend(pizza["ingredientes"])

                actualizar_ui_lado1()
                actualizar_ui_lado2()

                editando_index = index
                page.update()
            # descripción bonita
            if p["tipo"] == "mitad":
                desc = f"{', '.join(p['lado1'])}  |  {', '.join(p['lado2'])}"
            else:
                desc = ", ".join(p["ingredientes"])

            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Pizza #{i+1}", weight="bold"),
                        ft.Text(f"${p['precio']}", weight="bold")
                    ], alignment="spaceBetween"),

                    ft.Text(p["tamano"], size=12, color="gray"),
                    ft.Text(desc),

                    ft.Row([
                        ft.TextButton("Editar", on_click=editar),
                        ft.TextButton("Eliminar", on_click=eliminar, style=ft.ButtonStyle(color=ft.Colors.RED))
                    ])
                ]),
                padding=12,
                border_radius=12,
                bgcolor="#ffffff",
                shadow=ft.BoxShadow(
                    blur_radius=8,
                    color=ft.Colors.BLACK12
                )
            )

            lista_pedidos.controls.append(card)
            total += p["precio"]

        total_text.value = f"Total: ${total}"
        page.update()

    def guardar_venta_folio(pizza, folio):
        conexion = sqlite3.connect("ventas.db")
        cursor = conexion.cursor()

        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d %H:%M:%S")
        fecha_dia = ahora.strftime("%Y-%m-%d")

        if pizza["tipo"] == "mitad":
            ingredientes = f"{','.join(pizza['lado1'])} / {','.join(pizza['lado2'])}"
        else:
            ingredientes = ",".join(pizza["ingredientes"])

        cursor.execute("""
            INSERT INTO ventas (folio, fecha, fecha_dia, tamano, tipo, ingredientes, precio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            folio,
            fecha,
            fecha_dia,
            pizza["tamano"],
            pizza["tipo"],
            ingredientes,
            pizza["precio"]
        ))

        conexion.commit()
        conexion.close()
    
    def cobrar(e):
        folio = obtener_folio_diario()

        for pizza in orden:
            guardar_venta_folio(pizza, folio)
        orden.clear()
        actualizar_lista()


    # -----------------------
    # UI
    # -----------------------
    boton_agregar = ft.ElevatedButton("Agregar", on_click=agregar_pizza)
    panel_izq = ft.Container(
        content=ft.Column([
            ft.Text("Armar Pizza", size=18, weight="bold"),

            tamano,
            tipo,

            ft.Divider(),

            ft.Text("Mitad 1"),
            auto1,        # 👈 INPUT
            lado1_ui,     # 👈 LISTA VISUAL

            ft.Text("Mitad 2"),
            auto2,
            lado2_ui,

            boton_agregar
        ], spacing=10),

        width=300,
        padding=15,
        bgcolor="#f9f9f9",
        border_radius=10
    
    )

    panel_der = ft.Container(
        content=ft.Column([
            ft.Text("Pedido", size=18, weight="bold"),
            ft.Divider(),
            lista_pedidos
        ], alignment=ft.MainAxisAlignment.START, expand=True
        ),

        expand=True,
        padding=15,
    ) 

    footer = ft.Container(
        content=ft.Row([
            total_text,
            ft.Row([
                ft.Button("Cobrar", on_click=cobrar),
                ft.IconButton(ft.Icons.PRINT)
            ])
        ], alignment="spaceBetween"),
        padding=10,
        bgcolor="#f1f1f1",
        border_radius=10
    )
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("POS Pizzería", size=24, weight="bold"),

                ft.Row([
                    panel_izq,
                    ft.VerticalDivider(width=1),
                    panel_der
                ], expand=True),

                footer
            ]),
            padding=20,
            border_radius=12,
            bgcolor="#ffffff",
            shadow=ft.BoxShadow(
                blur_radius=15,
                spread_radius=1,
                color=ft.Colors.BLACK12
            ),
            expand=True
        )
    )
ft.app(target=main)