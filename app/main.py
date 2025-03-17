import flet as ft
import App
def main(page: ft.Page):
    # ph = ft.PermissionHandler()
    # page.overlay.append(ph)
    #
    # def request_permission(e):
    #     o = ph.request_permission(e.control.data)
    #     page.add(ft.Text(f"Requested {e.control.data.name}: {o}"))
    #
    # page.add(ft.OutlinedButton(
    #         "Request file Permission",
    #         data=ft.PermissionType.MANAGE_EXTERNAL_STORAGE,
    #         on_click=request_permission,
    #     ))
    page.add(App.Page(page))

ft.app(target=main)