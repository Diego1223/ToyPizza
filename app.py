import flet as ft
from database.generar_folio import obtener_folio_diario
from database.guardar_venta import guardar_venta_folio
import ssl
import certifi
from database.ingredientes import obtener_ingredientes
from database.calcular_precios import calcular_precio
from database.obtener_tipos_pizza import obtener_tipos_pizza
from database.obtener_tamanos import obtener_tamanos
from components.complementos import crear_dialogo_complementos
from utils.autocomplete import crear_autocomplete
#from components.tickets import generar_ticket
from datetime import datetime
import sqlite3

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)
def main(page: ft.Page):
    page.title = "POS Pizzería"
    page.theme = ft.Theme(
        text_theme=ft.TextTheme(body_medium=ft.TextStyle(color="black"))
    )

    tipos = obtener_tipos_pizza()

    tipo_base = ft.Dropdown(
        label="Tipo de pizza",
        label_style=ft.TextStyle(color="black"),
        options=[ft.dropdown.Option(t) for t in tipos],
        color=ft.Colors.BLACK
    )


    ingredientes = obtener_ingredientes()

    orden = []
    editando_index = None

    # LISTAS SEPARADAS
    lado1 = []
    lado2 = []

    lado1_ui = ft.Column()
    lado2_ui = ft.Column()

    lista_pedidos = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    total_text = ft.Text("Total: $0")



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
    tamanos_pizza = obtener_tamanos()
    tamano = ft.Dropdown(
        label="Tamaño",
        label_style=ft.TextStyle(color="black"),
        options= [ft.dropdown.Option(t) for t in tamanos_pizza],
        color=ft.Colors.BLACK
    )


    auto1 = crear_autocomplete(page,1, ingredientes, lado1, lado2, actualizar_ui_lado1, actualizar_ui_lado2)
    auto2 = crear_autocomplete(page,2, ingredientes, lado1, lado2, actualizar_ui_lado1, actualizar_ui_lado2)

    # -----------------------
    # FUNCIONES
    # -----------------------


    def agregar_pizza(e):
        nonlocal editando_index

        if not tamano.value or not tipo_base.value:
            return

        if tipo.value == "mitad":
            pizza = {
                "tamano": tamano.value,
                "tipo": "mitad",
                "tipo_base": tipo_base.value,
                "lado1": lado1.copy(),
                "lado2": lado2.copy(),
            }
        else:
            pizza = {
                "tamano": tamano.value,
                "tipo": "completa",
                "tipo_base": tipo_base.value,
                "ingredientes": lado1.copy(),
            }

        pizza["precio"] = calcular_precio(pizza)

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
                item = orden[index] 

                if p.get("tipo_item") == "complemento":
                    cargar_complementos(item, index)
                    abrir_complementos(e)
                else:
                    boton_agregar.content = "Guardar cambios"
                    boton_agregar.update()
                    nonlocal editando_index

                    pizza = orden[index]

                    tamano.value = pizza["tamano"]
                    tipo.value = pizza["tipo"]
                    actualizar_tipo()

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
            
            
            if p.get("tipo_item") == "complemento":
                titulo = f"Complemento #{i+1}"
                desc = f"{p['nombre']} x {p['cantidad']}"

            else:
                titulo = f"Pizza #{i + 1}"
                if p.get("tipo") == "mitad":
  
                  desc = f"{', '.join(p['lado1'])}  |  {', '.join(p['lado2'])}"
                else:
                    desc = ", ".join(p["ingredientes"])

            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(titulo, weight="bold"),
                        ft.Text(f"${p['precio']}", weight="bold")
                    ], alignment="spaceBetween"),

                    ft.Text(p.get("tamano"), size=12, color="gray"),
                    ft.Text(p.get("tipo_base"), size=12, color="gray"),
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

    dialog, abrir_complementos, cargar_complementos = crear_dialogo_complementos(
        page,
        orden,
        actualizar_lista
    )

    def obtener_total():
        return sum(item["precio"] for item in orden)
    
    def calcular_cambio(e):
        total = obtener_total()
        efectivo = 0
        transferencia = 0

        try:
            if monto_efectivo.value:
                efectivo = float(monto_efectivo.value.strip()) if monto_efectivo.value else 0
            if monto_transferencia.value:
                transferencia = float(monto_transferencia.value.strip()) if monto_transferencia.value else 0
            
            recibido = efectivo + transferencia

            if recibido < total:
                texto_cambio.value = "Pago insuficiente"
                page.update
                return
            
            cambio = recibido - total

            if cambio < 0:
                cambio = 0
            texto_cambio.value = f"Cambio: ${cambio}"
        except ValueError:
            texto_cambio.value = "Monto invalido"

        page.update()
    

    monto_efectivo = ft.TextField(
        label="Monto efectivo",
        visible=False,
        width=300
    )
    monto_transferencia = ft.TextField(
        label="Monto transferencia",
        visible=False,
        width=300
    )

    texto_cambio = ft.Text(
        "Cambio: $0",
        size=16,
        weight="bold"
    )

    monto_efectivo.on_change = calcular_cambio
    monto_transferencia.on_change = calcular_cambio

    dropdown_cobro = ft.DropdownM2(
        width=200,
        options=[
            ft.dropdownm2.Option("Efectivo"),
            ft.dropdownm2.Option("Transferencia"),
            ft.dropdownm2.Option("Mixto")
        ]
    )
    def cambiar_metodo_pago(e):
        metodo = dropdown_cobro.value

        #ocultar todo al principio
        monto_efectivo.visible = False
        monto_transferencia.visible = False

        #Limpiar valores
        monto_efectivo.value = ""
        monto_transferencia.value = ""

        texto_cambio.value = "Cambio: $0"

        if metodo == "Efectivo":
            monto_efectivo.visible = True
        elif metodo == "Transferencia":
            monto_transferencia.visible = True
        elif metodo == "Mixto":
            monto_efectivo.visible = True
            monto_transferencia.visible = True
        
        page.update()

    #Conectar el dropDown
    dropdown_cobro.on_change = cambiar_metodo_pago

    alert_cobro = ft.AlertDialog(
        modal=True,
        title=ft.Text("Metodo de pago"),
        content=ft.Column([
            ft.Row(
                [dropdown_cobro], 
                alignment=ft.MainAxisAlignment.CENTER
            ),
            monto_efectivo,
            monto_transferencia,
            texto_cambio
        ], width=400, height=400),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
            ft.TextButton("Confirmar", on_click=lambda e: page.pop_dialog())
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

        
    def cobrar(e):
        ahora = datetime.now()
        fecha_dia = ahora.strftime("%Y-%m-%d") 
        conexion = sqlite3.connect("ventas.db")
        cursor = conexion.cursor()

        metodo_de_pago = dropdown_cobro.value
        efectivo = 0
        transferencia = 0

        total = sum(item["precio"] for item in orden)

        try:
            if monto_efectivo.value:
                efectivo = float(monto_efectivo.value)
            if monto_transferencia.value:
                transferencia = float(monto_transferencia.value)
            recibido  = efectivo + transferencia

            if recibido < total:
                texto_cambio.value = "Pago insuficiente"
                page.update()
                return

            cambio = recibido - total


            folio = obtener_folio_diario()
            for item in orden:
                #agregar ,cursor aqui en guardar_venta_folio
                guardar_venta_folio(
                    item=item, 
                    folio=folio,
                    metodo_de_pago=metodo_de_pago,
                    monto_efectivo=efectivo,
                    monto_transferencia=transferencia,
                    cambio=cambio
                )
            texto_cambio.value = f"Pago confirmado | Cambio: ${cambio}"

            #Limpiar orden
            orden.clear()
            actualizar_lista()

            dialog.open = False

            monto_efectivo.value = ""
            monto_transferencia.value = ""
            texto_cambio.value = "Cambio: $0"
            dropdown_cobro.value = "Efectivo"

            conexion.commit()
            conexion.close()

            page.update()
        except ValueError:
            texto_cambio.value = "Monto invalido"
            page.update()

    # -----------------------
    # UI
    # -----------------------

    def actualizar_tipo(e=None):
        if tipo.value == "completa":
            mitad2_container.visible = False

            lado2.clear()
            actualizar_ui_lado2()
        else:
            mitad2_container.visible = True

        page.update()


    tipo = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(
                value="completa",
                label="Completa",
                label_style=ft.TextStyle(color="black"),
                fill_color="black"
            ),
            ft.Radio(
                value="mitad",
                label="Mitades",
                label_style=ft.TextStyle(color="black"),
                fill_color="black"
            )
        ])
    )


    mitad2_container = ft.Column(
        controls=[
            ft.Text("Mitad 2"),
            auto2,
            lado2_ui
        ]
    )


    tipo.on_change = actualizar_tipo

    boton_agregar = ft.ElevatedButton("Agregar", on_click=agregar_pizza, color=ft.Colors.WHITE, bgcolor=ft.Colors.BLACK)

    panel_izq = ft.Container(
        content=ft.Column([
            ft.Text("Armar Pizza", size=18, weight="bold", color=ft.Colors.BLACK),

            tipo_base,
            tamano,
            tipo,

            ft.Divider(),

            ft.Text("Mitad 1"),
            auto1,        # 👈 INPUT
            lado1_ui,     # 👈 LISTA VISUAL

            mitad2_container,
            ft.Row(controls=[
                boton_agregar,
                ft.ElevatedButton("Complementos",on_click=abrir_complementos, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

            ], alignment="spaceBetween", spacing=10),
        ], scroll=ft.ScrollMode.AUTO,),

        width=400,
        padding=15,
        bgcolor="#f9f9f9",
        border_radius=10,
    )

    panel_der = ft.Container(
        content=ft.Column([
            ft.Text("Pedido", size=18, weight="bold"),
            ft.Divider(),
            ft.Container(
                content=lista_pedidos,
                expand=True
            ),
        ], alignment=ft.MainAxisAlignment.START, expand=True
        ),

        expand=2,
        padding=15,
    ) 

    footer = ft.Container(
        content=ft.Row([
            total_text,
            ft.Row([
                ft.Button("Cobrar", on_click=lambda e: page.show_dialog(alert_cobro), color=ft.Colors.WHITE, bgcolor=ft.Colors.BLACK),
                ft.PopupMenuButton(
                    icon=ft.Icons.PRINT,
                    items=[
                        ft.PopupMenuItem(content="Ticket Cliente"),
                        ft.PopupMenuItem(content="Ticket Cocina")
                    ]
                )
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
                ft.Text("POS Pizzería", size=24, weight="bold", color=ft.Colors.BLACK),

                ft.Row([
                    panel_izq,
                    ft.VerticalDivider(width=1),
                    panel_der
                ], expand=True, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),

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