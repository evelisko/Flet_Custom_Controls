import typing as t

import flet as ft


class MyControl(ft.UserControl):
    def __init__(self, on_stuff: t.Callable[[str], None]) -> None:
        super().__init__()
        self._count = 0
        self._on_stuff = on_stuff

    def build(self) -> ft.Control:
        return ft.TextButton("Fire on_stuff event", on_click=self._handle_stuff_event)

    def _handle_stuff_event(self, e: ft.ControlEvent) -> None:
        self._count += 1
        self._on_stuff(f"Stuff has been fired {self._count} times!")


def main(page: ft.Page) -> None:
    def do_stuff(message: str) -> None:
        page.add(ft.Text(message))

    page.add(MyControl())#@(on_stuff=do_stuff))


ft.app(target=main)