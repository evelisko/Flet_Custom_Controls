import flet as ft
import flet.canvas as cv


class State:
    x: float
    y: float


state = State()


def main(page: ft.Page):
    page.title = "Flet Brush"

    def pan_start(e: ft.DragStartEvent):
        state.x = e.local_x
        state.y = e.local_y

    def pan_update(e: ft.DragUpdateEvent):
        cp.shapes.append(
            cv.Line(
                state.x, state.y, e.local_x, e.local_y, paint=ft.Paint(stroke_width=3)
            )
        )
        cp.update()
        state.x = e.local_x
        state.y = e.local_y

    cp = cv.Canvas(
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
        ),
        expand=False,
    )

    page.add(
        ft.Container(
            ft.Stack(
                [
                    ft.Image(
                        src= r"C:\Users\eveli\Pictures\5890633989_a359c1662b_b.jpg",
                        fit=ft.ImageFit.FILL,
                        width=float("inf"),
                    ),
                    cp,
                ]
            ),
            border_radius=5,
            width=float("inf"),
            expand=True,
        )
    )


ft.app(main)