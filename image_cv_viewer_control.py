import cv2
import os
import base64
import flet as ft
import flet.canvas as cv
import numpy as np
from controls.play_list import PlayList
from controls.image_viewer import ImageViewer


class MainControl(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.files_list_opened = False
        self.main_window_width = 0
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
        self.image_control = ImageViewer(on_mouse_move=self.on_image_viewer_mouse_move)
        self.tf_page_size = ft.TextField(value='', expand=True)
        self.play_list = PlayList(self.on_file_list_click) 
        self.play_list.visible = False
        self.btn_play_list = ft.IconButton(icon=ft.icons.MENU, on_click=self.show_playlist)   
        self.main_window = ft.Column([
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
                    self.image_control,
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
        ft.Row([self.btn, self.tf_page_size, self.btn_play_list]),
        ],
        expand=True
        )
        self.vertical_split = ft.GestureDetector(
                    content=ft.VerticalDivider(),
                    drag_interval=10,
                    on_pan_update=self.move_vertical_divider,
                    on_hover=self.show_draggable_cursor,
                    visible=False
                )
        x_row = ft.Row(
                controls=[
                        self.main_window,
                        self.vertical_split,
                        self.play_list
                ],
            spacing=0,
            expand=True
        )
        return x_row

    def on_file_list_click(self, value): # 8ec182
        print(value)
        self.tf_page_size.value = value
        self.update_image(value)


    def move_vertical_divider(self, e: ft.DragUpdateEvent):
        self.main_window.width += e.delta_x
        self.main_window.update()
        self.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()


    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            self.tf_page_size.value = e.path
            self.files_directory = e.path
            files_list = []
            for f_name in os.listdir(e.path):  # Можно добавить индикатор загрузки.
                if (os.path.isfile(os.path.join(self.files_directory, f_name)) 
                and os.path.splitext(f_name)[-1].lower() in ['.jpg', '.jpeg ', '.png']):
                    files_list.append([f_name, e.path])
            if files_list:
                self.play_list.load_playlist(files_list)
                self.update_image(os.path.join(files_list[0][1], files_list[0][0]))
        self.update()

    def update_image(self, image_name: str):
        img = cv2.imread(image_name)
        if img is not None:
            self.image_control.read_image(img)
            self.update()

    def next_image(self, e):
        value = self.play_list.next_file()
        if value:
            self.tf_page_size.value = value
        self.update_image(value)

    def prev_image(self, e):
        value = self.play_list.prev_file()
        if value:
            self.tf_page_size.value = value
            self.update_image(value)

    def on_image_viewer_mouse_move(self, x, y):
        self.tf_page_size.value = f'{x}/{y}'
        self.tf_page_size.update()

    def on_click(self, e):
        self.pick_files_dialog.get_directory_path()

    def show_playlist(self, e):
        if self.main_window_width == 0:
            self.main_window_width = self.page.width - 200
        if not self.files_list_opened:
            self.files_list_opened = True
            self.main_window.expand = False
            self.main_window.width = self.main_window_width
            self.vertical_split.visible =True
            self.play_list.visible = True
        else:
            self.files_list_opened = False
            self.video_window_width = self.main_window_width
            self.main_window.expand = True
            self.vertical_split.visible =False
            self.play_list.visible = False
        self.update()
    
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

