# Загрузка видео с файла.
# Добавить переметоку.
# Добавить разные элементы управления на панель инструментов.
import cv2
import os
import base64
import flet as ft
import threading
from time import sleep
from datetime import datetime, timedelta, timezone
import flet.canvas as cv
import numpy as np
from controls.image_viewer import ImageViewer

class VideoPlayer(ft.UserControl):
    def __init__(self, on_mouse_move):
        self.current_frame = 0
        self.capture = None
        self.latency = None
        self.current_time = None
        self.total_time = None
        self.frame_count = None
        self.is_video_play = False
        self.is_change_position = False
        # Добавить трек-бар. Выполняется проброс компонентов. Если они есть, то их можно рисовать.

    # TODO: Реализовать в виде отдельного класса.

    # def main(page: ft.Page):
    #     page.padding = 50
    #     page.window.left = page.window.left + 100
    #     page.theme_mode = ft.ThemeMode.LIGHT

    # def open_file(file_name: str):
    #     pass

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        print(e.files) # Список файлов.
        # global current_frame
        # global capture
        # global latency
        # global frame_count
        # global is_video_play
        # global total_time
        # page.title  = (", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!")
        if e.files:
            file_name = e.files[0].path
            current_frame = 0
            is_new = True
            if capture:
                if capture.isOpened():
                    capture.release()
                    capture=None
                    is_new = False
                    # thread.stop()
            capture = cv2.VideoCapture(file_name)
            latency = 1 / capture.get(cv2.CAP_PROP_FPS)
            frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
            # capture.set(cv2.CAP_PROP_POS_FRAMES, 100)
            is_video_play = True
            self.btn_play.icon = ft.icons.PAUSE
            self.sldr_time_bar.max = int(frame_count)
            self.sldr_time_bar.divisions = int(frame_count)
            total_time = time_to_str(frame_count * latency) 
            print(total_time)
            if is_new:
                thread = threading.Thread(target=update_frame, args=(), daemon=True)
                thread.start()
        self.update()

    def time_to_str(self, seconds: float):
        dtime = timedelta(seconds = seconds)
        mm, ss = divmod(dtime.seconds, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss) if hh > 0 else "%02d:%02d" % (mm, ss)
    
    def on_image_viewer_mouse_move(self, x, y):
        self.tf_page_size.value = f'{x}/{y}'
        self.tf_page_size.update()

    def on_click(self, e):
        pick_files_dialog.pick_files(allow_multiple=True)

    def update_frame(self):
        # # TODO: https://all-python.ru/osnovy/threading.html
        # global current_frame
        # global latency
        # global frame_count
        # global capture
        # global is_change_position
        # Реализовать просмотр и перемотку.
        while current_frame < self.frame_count:
            if self.capture: # Проверка что открыт новый файл.
                if is_video_play:
                    if is_change_position:
                        self.capture.set(cv2.CAP_PROP_POS_FRAMES, int(current_frame))
                        is_change_position = False
                    retval, frame = self.capture.read()
                    self.img_viewer.read_image(frame)
                    self.sldr_time_bar.value = current_frame
                    self.ft_time_line_value.value = f'{self.time_to_str(current_frame*self.latency)}/{self.total_time}'
                    self.ft_time_line_value.update()
                    self.tf_page_size.value = str(int(self.capture.get(cv2.CAP_PROP_POS_FRAMES)))
                    self.tf_page_size.update() 
                    current_frame += 1
                    self.sldr_time_bar.update()
                sleep(self.latency)
            else:
                break
        if self.capture:
            self.capture.release()
    
    def on_page_resize(self, e): # Измененение размеров.
        #tf_page_size.value = f'{page.width}/{page.height}'
        self.update()

    def slider_changed(self, e):
        # global capture
        # global latency
        # global current_frame
        # global is_change_position
        current_frame = int(e.control.value)
        is_change_position = True
        # capture.set(cv2.CAP_PROP_POS_FRAMES, int(e.control.value))
        self.sldr_time_bar.label = self.time_to_str(e.control.value * self.latency)

    def play_button_clicked(self, e):
        global is_video_play
        if self.btn_play.icon == ft.icons.PAUSE:
            self.btn_play.icon = ft.icons.PLAY_ARROW
            is_video_play = False
        else:
            self.btn_play.icon = ft.icons.PAUSE
            is_video_play = True
        self.btn_play.update()

    # Настекать кнопки.
    #================================================================
    sldr_time_bar = ft.Slider(
                        min=0, max=1000,
                        divisions=1000,
                        label="{value}", 
                        active_color=ft.colors.PURPLE,
                        secondary_active_color=ft.colors.RED,
                        thumb_color=ft.colors.PURPLE,
                        expand=True, 
                        on_change=slider_changed)
    btn_play = ft.IconButton(
        icon=ft.icons.PLAY_ARROW, on_click=play_button_clicked, data=0
    )
    btn_play_list = ft.IconButton(
        icon=ft.icons.MENU  # on_click=play_button_clicked, data=0
    )
    ft_time_line_value = ft.Text(value='00:00:00/00:00:00')  
    ft_play_track_coontainer = ft.Container(content=ft.Row(
        controls=[btn_play, sldr_time_bar, ft_time_line_value, btn_play_list], 
        expand=True, 
        alignment=ft.alignment.center_right
        ),
        bgcolor=ft.colors.RED
        )
    #================================================================
    self.pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    self.overlay.append(self.pick_files_dialog)
    self.img_viewer = ImageViewer(on_mouse_move=on_image_viewer_mouse_move)
    self.tf_page_size = ft.TextField(value='')
    btn = ft.ElevatedButton('Open File',
                            icon=ft.icons.UPLOAD_FILE,
                            on_click=on_click  # lambda _: pick_files_dialog.pick_files(allow_multiple=True)
                        )
    ft_row = ft.Column([img_viewer, tf_page_size, btn, ft_play_track_coontainer], expand=True)

    # Перенос видео через drug & drop.
    # page.add(ft_row)
    # page.on_resized = on_page_resize

# if __name__ == '__main__':
#     ft.app(target=main)

# Циклическое воспроизведение видео.
    