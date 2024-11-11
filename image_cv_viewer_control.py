import cv2
import os
import base64
import flet as ft
import flet.canvas as cv
import numpy as np
from image_viewer import ImageViewer

img_path = r"C:\Users\eveli\Pictures\5890633989_a359c1662b_b.jpg"
img = cv2.imread(img_path)


def main(page: ft.Page):
    page.padding = 50
    page.window.left = page.window.left + 100
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # container.
    # container.read_image(img)
    # ft_row = ft.Column([container], expand=True)  
    

    def on_image_viewer_mouse_move(x, y):
        tf_page_size.value = f'{x}/{y}'
        tf_page_size.update()

    def on_click(e):
        img_path = r"C:\Users\eveli\Pictures\5890633989_a359c1662b_b.jpg"
        img = cv2.imread(img_path)
        container.read_image(img)


    btn = ft.ElevatedButton('helo', on_click=on_click)
    
    def on_page_resize(e):
        tf_page_size.value = f'{page.width}/{page.height}'
        # print( f'{page.width}/{page.height}')
        page.update()
    
    container = ImageViewer(on_mouse_move=on_image_viewer_mouse_move)
    tf_page_size = ft.TextField(value='')   
    ft_row = ft.Column([container, tf_page_size, btn], expand=True)

    page.add(ft_row)
    page.on_resized = on_page_resize

if __name__ == '__main__':
    ft.app(target=main)
    