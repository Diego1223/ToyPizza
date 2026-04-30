import flet as ft

#Actualizar UI
class PizzaManager(ft.Column):
    def __init__(self, lado ,lado1, lado2, lado1_ui, lado2_ui, eliminar_ing, index):
        super().__init__()

        self.lado = lado
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado1_ui = lado1_ui
        self.lado2_ui = lado2_ui
        self.eliminar_ing = eliminar_ing
        self.index = index

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
    
    def eliminar_ing(self):
        if self.lado == 1:
            self.lado1.pop(self.index)
            self.actualizar_ui_lado1()
        else:
            self.lado2.pop(self.index)
            self.actualizar_ui_lado2()
        
