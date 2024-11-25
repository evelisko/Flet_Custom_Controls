import cv2
import os
import base64
import flet as ft
import flet.canvas as cv
import numpy as np
from image_viewer import ImageViewer


files_directory = ''
files_list = []
current_image_index = 0
number_of_items = 0

def main(page: ft.Page):
    page.padding = 5
    page.window.left = page.window.left + 100
    page.theme_mode = ft.ThemeMode.DARK

    def pick_files_result(e: ft.FilePickerResultEvent):
        global files_list
        global files_directory
        global number_of_items
        # page.title  = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # )
        if e.path:
            tf_page_size.value = e.path
            files_directory = e.path
            for f_name in os.listdir(e.path):
                if (os.path.isfile(os.path.join(files_directory, f_name)) 
                and os.path.splitext(f_name)[-1].lower() in ['.jpg', '.jpeg ', '.png']):
                    files_list.append(f_name)
            print(files_list)
            number_of_items = len(files_list) - 1
            update_image()
        page.update()

    def update_image():
        global current_image_index
        global number_of_items
        global files_directory
        global files_list
        page.title  = files_list[current_image_index]
        img_path = os.path.join(files_directory, files_list[current_image_index]) # r"C:\Users\eveli\Pictures\5890633989_a359c1662b_b.jpg"
        img = cv2.imread(img_path)
        container.read_image(img)
        page.update()

    def next_image(e):
        global current_image_index
        global number_of_items
        current_image_index = (current_image_index + 1) if current_image_index < number_of_items else 0
        update_image()

    def prev_image(e):
        global current_image_index
        global number_of_items
        current_image_index = (current_image_index - 1) if current_image_index > 0 else number_of_items
        update_image()

    def on_image_viewer_mouse_move(x, y):
        tf_page_size.value = f'{x}/{y}'
        tf_page_size.update()

    def on_click(e):
        pick_files_dialog.get_directory_path()


    btn = ft.ElevatedButton('Open', on_click=on_click, icon=ft.icons.UPLOAD_FILE,)
    
    def on_page_resize(e):
        tf_page_size.value = f'{page.width}/{page.height}'
        # print( f'{page.width}/{page.height}')
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result,
                                    #   allow_multiple=False,
                                    #   file_type=
                                      )
    # .get_directory_path()
    page.overlay.append(pick_files_dialog)

    # Сделать так чтобы компонент занял всю область.
    container = ImageViewer(on_mouse_move=on_image_viewer_mouse_move)
    tf_page_size = ft.TextField(value='', expand=True)   
    ft_row = ft.Column([
        ft.Row([
            ft.Container(
				ft.FloatingActionButton(icon=ft.icons.NAVIGATE_BEFORE_ROUNDED, bgcolor=ft.colors.TRANSPARENT, shape=ft.CircleBorder(),
                             on_click=prev_image
                        ),
				margin=10,
				padding=10,
				alignment=ft.alignment.center_right,
				border_radius=10,
				visible = True,
				disabled=False
			),
                container,
            ft.Container(
					ft.FloatingActionButton(icon=ft.icons.NAVIGATE_NEXT_ROUNDED, bgcolor=ft.colors.TRANSPARENT, shape=ft.CircleBorder(),
                            on_click=next_image
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
       ft.Row([btn, tf_page_size]),
      ],
      expand=True
    )

    page.add(ft_row)
    page.update()   
    page.on_resized = on_page_resize

if __name__ == '__main__':
    ft.app(target=main)

