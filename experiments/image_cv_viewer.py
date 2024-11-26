import cv2
import os
import base64
import flet as ft
import flet.canvas as cv
import numpy as np


img_path = r"C:\Users\eveli\Pictures\5890633989_a359c1662b_b.jpg"
img = cv2.imread(img_path)
_, im_arr = cv2.imencode('.jpg', img)
im_b64 = base64.b64encode(im_arr).decode('utf-8')
img_height, img_width = img.shape[:2]

cursor_position_x = 0
cursor_position_y = 0
scale_factor = 1
img_pos_y = 0
img_pos_x = 0


def main(page: ft.Page):

    def pan_start(e: ft.DragStartEvent):
        ft_canvas.shapes.clear()
        ft_canvas.shapes.append(
        cv.Rect(e.local_x-25, e.local_y-25, 50, 50, 
                            paint= ft.Paint(
                            color=ft.colors.YELLOW,  
                            stroke_width=2,  
                            style=ft.PaintingStyle.STROKE,
                        )))
        ft_canvas.update()

    def pan_update(e: ft.DragUpdateEvent):
        ft_canvas.shapes.clear()
        ft_canvas.shapes.append(
            cv.Rect(e.local_x-25, e.local_y-25, 50, 50, 
                    paint= ft.Paint(
                    color=ft.colors.YELLOW,  
                    stroke_width=2,  
                    style=ft.PaintingStyle.STROKE,
                )))
        tf_page_size.value = f'{int((e.local_x-img_pos_x))}/{int((e.local_y-img_pos_y))}'
        print(img_pos_y, img_pos_x)
        ft_canvas.update()
        page.update()

    def on_canvas_resize(e: cv.CanvasResizeEvent):
        tf_canvas_size.value = f'{e.width}/{e.height}'
        background = np.zeros((int(e.height),int(e.width),3))
        scale_y = e.height/img_height
        scale_x = e.width/img_width 
        scale_factor = scale_x if scale_x < scale_y else scale_y
        print(scale_factor)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        new_img = cv2.resize(img, (new_width, new_height))
        print(img.shape)
        print(new_img.shape)
        print(background.shape)
        img_pos_y = int((e.height-new_height)/2)
        img_pos_x = int((e.width-new_width)/2)
        # print(img_pos_y, img_pos_x)
        # print(img_pos_y,img_pos_y+new_img.shape[0],  img_pos_x,img_pos_x+new_img.shape[1])
        background[img_pos_y:img_pos_y+new_img.shape[0], img_pos_x:img_pos_x+new_img.shape[1]] = new_img
        _, im_arr = cv2.imencode('.jpg', background)
        im_b64 = base64.b64encode(im_arr).decode('utf-8')
        ft_img.src_base64=im_b64
        page.update()

    tf_page_size = ft.TextField(value='')
    tf_canvas_size = ft.TextField(value='')

    def on_page_resize(e):
       tf_page_size.value = f'{page.width}/{page.height}'
       print( f'{page.width}/{page.height}')
       page.update()

    page.padding = 50
    page.window_left = page.window_left + 100
    page.theme_mode = ft.ThemeMode.LIGHT

    ft_img = ft.Image(
        src_base64=im_b64,
        fit=ft.ImageFit.FILL,
        width=float("inf"),
    )

    ft_canvas = ft.canvas.Canvas(
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            # on_secondary_tap=None,
            # mouse_cursor=None,
            # on_page_resize = None,
            drag_interval=10,
        ),
        on_resize=on_canvas_resize,
        expand=False,
    )

    container = ft.Container(
            ft.Stack(
                [
                  ft_img,
                  ft_canvas,
                ]
            ),
            border_radius=5,
            width=float("inf"),
            expand=True,
        )

    ft_row = ft.Column([container, tf_page_size, tf_canvas_size], expand=True)
  
    page.add(ft_row)
    page.on_resize =on_page_resize

if __name__ == '__main__':
    ft.app(target=main)
    