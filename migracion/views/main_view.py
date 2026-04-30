import flet as ft
from migracion.utils.autocomplete import Autocomplete
from database.obtener_tipos_pizza import obtener_tipos_pizza
from database.ingredientes import obtener_ingredientes
from database.obtener_tamanos import obtener_tamanos
from migracion.utils.autocomplete import Autocomplete
from database.calcular_precios import calcular_precio

class PizzaApp:
    def __init__(self, page:ft.Page):
        self.page = page
        self.page.theme = ft.Theme(
                text_theme=ft.TextTheme(body_medium=ft.TextStyle(color="black"))
        )
        self.page.title = "Toy Pizza"

        #Tipos de pizza
        self.tipos = obtener_tipos_pizza()
        
        self.tipo_base = ft.Dropdown(
            label="Tipo de pizza",
            options=[ft.Dropdown.Option(t) for t in self.tipos]
        )

        #Ingredientes
        self.ingredientes = obtener_ingredientes()


        #datos
        self.orden = []
        self.lado1 = []
        self.lado2 = []
        
        self.lado1_ui = ft.Column()
        self.lado2_ui = ft.Column()

        self.editando_index = None
        
        #Tipo de pizza
        self.tipo = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="completa", label="Completa",  label_style=ft.TextStyle(color="black"), fill_color="black"),
            ft.Radio(value="mitad", label="Mitades",  label_style=ft.TextStyle(color="black"), fill_color="black")
        ]))

        self.tipo.on_change = self.actualizar_tipo

        #Tamanos de pizza
        self.tamanos_pizza = obtener_tamanos()
        self.tamano = ft.Dropdown(
            label="Tamaño",
            options= [ft.dropdown.Option(t) for t in self.tamanos_pizza],
            color= ft.Colors.BLACK
        )

        self.tipo = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="completa", label="Completa",  label_style=ft.TextStyle(color="black"), fill_color="black"),
                ft.Radio(value="mitad", label="Mitades",  label_style=ft.TextStyle(color="black"), fill_color="black")
        ]))

        #Crear los 2 inputs de autocompletado
        self.auto1 = Autocomplete(
            self.page,
            self.ingredientes,
            self.agregar_lado1
        )

        self.auto2 = Autocomplete(
            self.page,
            self.ingredientes,
            self.agregar_lado2
        )


        #Construir la UI
        self.setup_ui()
    
    def agregar_pizza(self, e):
        if self.tamano.value or not self.tipo.value:
            return
        
        if self.tipo.value == "mitad":
            #declaracion de variable pizza
            self.pizza = {
                    "tamano": self.tamano.value,
                "tipo": "mitad",
                "tipo_base": self.tipo_base.value,
                "lado1": self.lado1.copy(),
                "lado2": self.lado2.copy(),
            }
        else:
            self.pizza = {
                "tamano": self.tamano.value,
                "tipo": "completa",
                "tipo_base": self.tipo_base.value,
                "ingredientes": self.lado1.copy(),
            }

        self.pizza["precio"] = calcular_precio(self.pizza)
        
        if self.editando_index is not None:
            self.orden[self.editando_index] = self.pizza
            self.editando_index = None

            self.boton_agregar.content = "Agregar"
        else:
            self.orden.append(self.pizza)
            



    def actualizar_tipo(self, e=None):
        if self.tipo.value == "completa":
            self.mitad2_container.visible = False

            self.lado2.clear()
            self.actualizar_ui_lado2()
        else:
            self.mitad2_container.visible = True
        self.page.update()

    def actualizar_ui_lado1(self):
        self.lado1_ui.controls.clear()
        for i, ing in enumerate(self.lado1):
            self.lado1_ui.controls.append(
                ft.Row([
                    ft.Text(ing),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, idx=i: self.eliminar_ing(1, idx)
                    )
                ])
            )

    def actualizar_ui_lado2(self):
        self.lado2_ui.controls.clear()
        for i, ing in enumerate(self.lado2):
            self.lado2_ui.controls.append(
                ft.Row([
                    ft.Text(ing),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, idx=i: self.eliminar_ing(2, idx)
                    )
                ])
            )
        

    def eliminar_ing(self,lado, index):
        if lado == 1:
            self.lado1.pop(index)
            self.actualizar_ui_lado1()
        else:
            self.lado2.pop(index)
            self.actualizar_ui_lado2()

    #Esto sirve con el autocomplete
    def agregar_lado1(self, valor):
        self.lado1.append(valor)
        self.actualizar_ui_lado1()
    
    def agregar_lado2(self, valor):
        self.lado2.append(valor)
        self.actualizar_ui_lado2()

    def setup_ui(self):
        self.total_text = ft.Text("Total: $0")

        self.page.add(
            ft.Column(controls=[
                ft.Text("Toy Pizza"),
                self.total_text
            ])
        ) 

    