import flet as ft
import App
def main(page: ft.Page):

    page.add(App.Page(page))

ft.app(target=main)