import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def page_resize(e):  # <<< new
        # Pops up a message from page bottom side.
        page.snack_bar = ft.SnackBar(ft.Text(f'New page size => width: {page.width}, height: {page.height}'))
        page.snack_bar.open = True

        # Adjust the control width depending on the page width.
        # It worked for both desktop and web.
        txt_number.width = min(100, max(50, page.width * 0.1))
        page.update()

    page.on_resize = page_resize  # <<< new

    txt_number = ft.TextField(value="0", text_align="right")

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)        
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main)