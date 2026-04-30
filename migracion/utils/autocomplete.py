import flet as ft

class Autocomplete(ft.Column):
    def __init__(self, page, opciones, on_select):
        self.page = page
        self.opciones = opciones
        self.on_select = on_select

        self.input_field = ft.TextField(
            label="Agregar ingrediente",
            label_style=ft.TextStyle(color="black")
        )

        self.sugerencias = ft.Column()

        self.container = ft.Container(
            content=self.sugerencias,
            visible=False,
            bgcolor="#eee",
            padding=5
        )

        self.input_field.on_change = self.filtrar

        self.controls = [
            self.input_field,
            self.container
        ]

    def filtrar(self, e):
        texto = self.input_field.value.lower()
        self.sugerencias.controls.clear()

        if texto == "":
            self.container.visible = False
            self.page.update()
            return

        resultados = [
            i for i in self.opciones
            if texto in i.lower()
        ]

        self.container.visible = bool(resultados)

        for r in resultados:
            self.sugerencias.controls.append(
                ft.ListTile(
                    title=ft.Text(r),
                    on_click=lambda e, val=r: self.seleccionar(val)
                )
            )

        self.page.update()

    def seleccionar(self, valor):
        self.on_select(valor)

        self.input_field.value = ""
        self.container.visible = False

        self.page.update()

        