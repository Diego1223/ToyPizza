import flet as ft
import ssl
import certifi
from migracion.views.main_view import PizzaApp

ssl._create_default_https_context = lambda: ssl.create_default_context(
    cafile=certifi.where()
)

def main(page: ft.Page):
    PizzaApp(page)

ft.app(target=main)

