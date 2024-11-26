import flet as ft

name = "CupertinoListTile example"


def main(page: ft.Page):
    # def open_pagelet_end_drawer(e):
    #     pagelet.end_drawer.open = True
    #     pagelet.end_drawer.update()

    name = "Draggable VerticalDivider"


    def move_vertical_divider(e: ft.DragUpdateEvent):
        # if (e.delta_x > 0 and c.width < 300) or (e.delta_x < 0 and c.width > 100):
        c.width += e.delta_x
        c.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    c = ft.Container(
        bgcolor=ft.colors.ORANGE_300,
        alignment=ft.alignment.center,
        width = page.width - 200,
        # expand=True,
    )

    r= ft.Row(
        controls=[
            c,
            ft.GestureDetector(
                content=ft.VerticalDivider(),
                drag_interval=10,
                on_pan_update=move_vertical_divider,
                on_hover=show_draggable_cursor,
            ),
            ft.Container(
                bgcolor=ft.colors.BROWN_400,
                alignment=ft.alignment.center,
                expand=1,
                # width=200,
            ),
        ],
        spacing=0,
        expand=True,
        # width=400,
        # height=400,
    )
    # return pagelet
    page.add(r)

if __name__ == '__main__':
    ft.app(target=main)