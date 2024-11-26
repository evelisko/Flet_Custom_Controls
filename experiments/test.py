import flet as ft

def main(page: ft.Page):
    container = ft.canvas.Canvas(
        content=ft.Stack([ft.ElevatedButton("Search")], expand=True),
        expand=True,
        on_resize=lambda e: print(e.width, e.height),
    )
    page.add(container)

ft.app(main)