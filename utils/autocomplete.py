import flet as ft


def crear_autocomplete(page,lado, ingredientes, lado1, lado2, actualizar_ui_lado1, actualizar_ui_lado2):
    input_field = ft.TextField(label="Agregar ingrediente", label_style=ft.TextStyle(color="black"))

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
                    on_click=lambda e, val=r: seleccionar(val)))

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