import os
import cv2
import json
import base64
import flet as ft
import flet.canvas as cv
from flet_core.event_handler import EventHandler
from flet_core.control_event import ControlEvent
from flet_core.types import OptionalEventCallable
import numpy as np


# TODO: Передаются не правилные пропорции для изображения.
# добавить возможность передвавать любой shape на экран
# или сделать так чтобы никакой шейп не рисовался.
# сделать так чтобы события можно было подключать и отключать через handle.
class Size():
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height

class ImageViewer(ft.UserControl):
    def __init__(self,
                  on_mouse_move = None,
                #   canvas_shape = None
                  ):
        super().__init__()
        self.cursor_position_x = 0
        self.cursor_position_y = 0
        self.img_pos_y = 0
        self.img_pos_x = 0
        self.scale_factor = 1
        self.img_size = Size(0, 0)
        self.size = Size(0, 0)
        self.ft_img = None
        self.expand = True
        self.img = None

        # self.cursor_shape = None

        # Докинуть еще каких-нибудь 
        self.__on_mouse_move = on_mouse_move

    def did_mount(self):
        self.update()

    def draw_looking_window(self, cursor_x, cursor_y):
        # if self.cursor_shape:
        # При перемещении возвраать позицию в координатах изображения.
        # Подписать событие на перемещение курсора по окну.
        self.ft_canvas.shapes.clear()
        self.ft_canvas.shapes.append(
            cv.Rect(cursor_x - 25, cursor_y - 25, 50, 50,
                    paint=ft.Paint(
                        color=ft.colors.YELLOW,
                        stroke_width=2,
                        style=ft.PaintingStyle.STROKE,
                    ))
                    )
        self.ft_canvas.update()
        self.update()

    def calc_image_cursor_position(self, x:float, y:float):
        self.cursor_position_x = int((x - self.img_pos_x) / self.scale_factor)
        self.cursor_position_y = int((y - self.img_pos_y) / self.scale_factor)
        if self.__on_mouse_move is not None:
            self.__on_mouse_move(x=self.cursor_position_x, y=self.cursor_position_y)
        # передаем также размеры окна в параметрах изображения.
        # его можно как задать так и получить.

    def pan_start(self, e: ft.DragStartEvent):
        self.calc_image_cursor_position(e.local_x, e.local_y)
        self.draw_looking_window(e.local_x, e.local_y)

    def pan_update(self, e: ft.DragUpdateEvent):
        self.calc_image_cursor_position(e.local_x, e.local_y)
        self.draw_looking_window(e.local_x, e.local_y)

    def update_image(self):
        background = np.zeros((int(self.size.height), int(self.size.width), 3))
        scale_y = self.size.height / self.img_size.height
        scale_x = self.size.width / self.img_size.width
        self.scale_factor = scale_x if scale_x < scale_y else scale_y
        new_width = int(self.img_size.width * self.scale_factor)
        new_height = int(self.img_size.height * self.scale_factor)

        new_img = cv2.resize(self.img, (new_width, new_height))
        self.img_pos_y = int((self.size.height - new_height) / 2)
        self.img_pos_x = int((self.size.width - new_width) / 2)
        background[self.img_pos_y:self.img_pos_y + new_img.shape[0],
        self.img_pos_x:self.img_pos_x + new_img.shape[1]] = new_img
        _, im_arr = cv2.imencode('.jpg', background)
        im_b64 = base64.b64encode(im_arr).decode('utf-8')
        self.ft_img.src_base64 = im_b64
        self.ft_canvas.update()
        self.update()

    def read_image(self, image: np.ndarray):
        self.img = image
        self.img_size.height, self.img_size.width = image.shape[:2]
        self.update_image()

    def on_canvas_resize(self, e: cv.CanvasResizeEvent):
        if e.height > 0 and e.width > 0:
            self.size.height = e.height
            self.size.width = e.width
            self.update_image()

    def build(self):
        background = np.zeros((int(600), int(1200), 3))
        self.img_size.height, self.img_size.width = background.shape[:2]
        self.img = background.copy()
        _, im_arr = cv2.imencode('.jpg', background)
        self.im_b64 = base64.b64encode(im_arr).decode('utf-8')
        self.ft_img = ft.Image(src_base64=self.im_b64,
                               fit=ft.ImageFit.FILL,
                               width=float("inf")
                               )
        self.ft_canvas = ft.canvas.Canvas(
            expand=False,
            content=ft.GestureDetector(
                on_pan_start=self.pan_start,
                on_pan_update=self.pan_update,
                drag_interval=10,
            ),
            on_resize=self.on_canvas_resize,
        )

        return ft.Container(
            ft.Stack([self.ft_img,
                      self.ft_canvas
                      ]),
            border_radius=5,
            width=float("inf"),
            expand=True,
            # bgcolor=ft.colors.RED
        )
