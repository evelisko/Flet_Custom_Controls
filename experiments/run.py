import flet as ft
from experiments.capture_control import CameraCaptureControl

def main(page: ft.Page):
    page.padding = 50
    page.window_left = page.window_left + 100
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(CameraCaptureControl())

if __name__ == '__main__':
    ft.app(target=main)