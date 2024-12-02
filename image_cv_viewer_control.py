import cv2
import os
import base64
import flet as ft
import flet.canvas as cv
import numpy as np
from controls.image_viewer import ImageViewer


class MainControl(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.files_directory = ''
        self.files_list = []
        self.current_image_index = 0
        self.number_of_items = 0
        self.expand = True

    def build(self) -> ft.Control:
        self.btn = ft.ElevatedButton('Open', on_click=self.on_click, icon=ft.icons.UPLOAD_FILE,)

        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result,
                                        #   allow_multiple=False,
                                        #   file_type=
                                        )
        # .get_directory_path()
        self.page.overlay.append(self.pick_files_dialog)

        # Сделать так чтобы компонент занял всю область.
        self.container = ImageViewer(on_mouse_move=self.on_image_viewer_mouse_move)
        self.tf_page_size = ft.TextField(value='', expand=True)   
        self.ft_row = ft.Column([
            ft.Row([
                ft.Container(
                    ft.FloatingActionButton(icon=ft.icons.NAVIGATE_BEFORE_ROUNDED, bgcolor=ft.colors.TRANSPARENT, shape=ft.CircleBorder(),
                                on_click=self.prev_image
                            ),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center_right,
                    border_radius=10,
                    visible = True,
                    disabled=False
                ),
                    self.container,
                ft.Container(
                        ft.FloatingActionButton(icon=ft.icons.NAVIGATE_NEXT_ROUNDED, bgcolor=ft.colors.TRANSPARENT, shape=ft.CircleBorder(),
                                on_click=self.next_image
                            ),
                        margin=5,
                        padding=10,
                        alignment=ft.alignment.center_left,
                        border_radius=10,
                        visible = True,
                        disabled=False
                    ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        ), 
        ft.Row([self.btn, self.tf_page_size]),
        ],
        expand=True
        )

        return self.ft_row
        # page.update()   
        # page.on_resized = on_page_resize


    def pick_files_result(self, e: ft.FilePickerResultEvent):
        # page.title  = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # )
        
        if e.path:
            self.tf_page_size.value = e.path
            self.files_directory = e.path
            self.files_list = []
            for f_name in os.listdir(e.path):
                if (os.path.isfile(os.path.join(self.files_directory, f_name)) 
                and os.path.splitext(f_name)[-1].lower() in ['.jpg', '.jpeg ', '.png']):
                    self.files_list.append(f_name)
            # print(self.files_list)
            self.number_of_items = len(self.files_list) - 1
            self.update_image()
        self.update()

    def update_image(self):
        self.page.title  = self.files_list[self.current_image_index]
        img_path = os.path.join(self.files_directory, self.files_list[self.current_image_index]) # r"C:\Users\eveli\Pictures\5890633989_a359c1662b_b.jpg"
        img = cv2.imread(img_path)
        self.container.read_image(img)
        self.update()

    def next_image(self, e):
        # global current_image_index
        # global number_of_items
        self.current_image_index = (self.current_image_index + 1) if self.current_image_index < self.number_of_items else 0
        self.update_image()

    def prev_image(self, e):
        # global current_image_index
        # global number_of_items
        self.current_image_index = (self.current_image_index - 1) if self.current_image_index > 0 else self.number_of_items
        self.update_image()

    def on_image_viewer_mouse_move(self, x, y):
        self.tf_page_size.value = f'{x}/{y}'
        self.tf_page_size.update()

    def on_click(self, e):
        self.pick_files_dialog.get_directory_path()
    
    # def on_page_resize(self, e):
    #     self.tf_page_size.value = f'{page.width}/{page.height}'
    #     # print( f'{page.width}/{page.height}')
    #     self.update()


def main(page: ft.Page):
    page.padding = 5
    page.window.left = page.window.left + 100
    # page.theme_mode = ft.ThemeMode.LIGHT
    page.add(MainControl()) # Вызов события и параметров контрола.

if __name__ == '__main__':
    ft.app(target=main)

