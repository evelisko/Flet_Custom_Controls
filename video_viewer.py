import os
import base64
import cv2
import flet as ft
import threading
from time import sleep
from typing import List 
from datetime import datetime, timedelta, timezone
from flet_core.file_picker import FilePickerFile
import flet.canvas as cv
import numpy as np
from image_viewer import ImageViewer
from setting_panel import SettingsPanelNavigationDrawer

# current_frame = 0
# capture = None
# latency = None
# current_time = None
# total_time = None
# frame_count = None
# is_video_play = False
# is_change_position = False
# files_list_opened = False
# video_window_width = 0

# TODO: Реализовать в виде отдельного класса.
class VideoViewer(ImageViewer): # Унаследовать компонент от image_viewer
    def __init__(self, update_frame_index=None):
        super().__init__()
        self.current_frame = 0
        self.capture = None
        self.latency = None
        self.current_time = None
        self.total_time = None
        self.frame_count = None
        self.is_video_play = False
        self.is_change_position = False
        self.files_list_opened = False
        self.video_window_width = 0
        # self.img_viewer = ImageViewer()
        self._on_update_frame_index = update_frame_index
        # self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        # необходимые параметры.
        # Характеристики видео. frame_rate, total_time frames_count, frame_index, current_time  
        # 
        #on_mouse_move=self.on_image_viewer_mouse_move)

    # def build(self):img_viewer
    #     # self.page.overlay.append(self.pick_files_dialog)
    #     return self.


    # def update_frame_index(self): # это событие.
    #     # Получаем значение нового индекса кадра.
    #     pass 

    def get_frames_count(self):
        return self.frame_count

    def get_current_frame_index(self):
        return self.current_frame
    
    def set_current_frame_index(self, value):
        self.is_change_position = True
        self.current_frame = value

    def get_total_time(self):
        return self.total_time

    def get_current_time(self):
        return self.current_time

    def get_frame_rate(self):
        return self.latency

    def play_video_status(self):
        # Возвращаем статус видео. воспроизведение или пауза.
        pass

    def get_video_status(self):
        self.is_video_play

    def change_play_status(self, status: bool):
        self.is_video_play = status

    def time_to_str(self, seconds: float):
        dtime = timedelta(seconds = seconds)
        mm, ss = divmod(dtime.seconds, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss) if hh > 0 else "%02d:%02d" % (mm, ss)
    
    # def on_image_viewer_mouse_move(x, y):
    #     tf_page_size.value = f'{x}/{y}'
    #     tf_page_size.update()

        # def set_position(self, value):
        # self.current_frame = int(e.control.value)
        # self.is_change_position = True
        # # return self.time_to_str(e.control.value * latency)

    # def show_draggable_cursor(e: ft.HoverEvent):
    #     e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
    #     e.control.update()

    def open_file(self, file_name: str):
        if file_name:
            self.current_frame = 0
            is_new = True
            if self.capture:
                if self.capture.isOpened():
                    self.capture.release()
                    self.capture=None
                    self.is_new = False
                    # thread.stop()
            self.capture = cv2.VideoCapture(file_name)
            self.latency = 1 / self.capture.get(cv2.CAP_PROP_FPS)
            self.frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            # capture.set(cv2.CAP_PROP_POS_FRAMES, 100)
            self.is_video_play = True
            # btn_play.icon = ft.icons.PAUSE
            # if self.sldr_time_bar:
            #     self.sldr_time_bar.max = int(self.frame_count)
            #     self.sldr_time_bar.divisions = int(self.frame_count)
            self.total_time = self.time_to_str(self.frame_count * self.latency) 
            # print(total_time)
            if is_new:
                thread = threading.Thread(target=self.update_frame, args=(), daemon=True)
                thread.start()
        self.update()
        # page.update()

    # def on_click(e):
    #     pick_files_dialog.pick_files(allow_multiple=True)

    def time_to_str(self, seconds: float):
        dtime = timedelta(seconds = seconds)
        mm, ss = divmod(dtime.seconds, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss) if hh > 0 else "%02d:%02d" % (mm, ss)

    def update_frame(self):
        # TODO: https://all-python.ru/osnovy/threading.html
        # Реализовать просмотр и перемотку.
        while self.current_frame < self.frame_count:
            if self.capture: # Проверка что открыт новый файл.
                if self.is_video_play:
                    start_time = datetime.now()
                    if self.is_change_position:
                        self.capture.set(cv2.CAP_PROP_POS_FRAMES, int(self.current_frame))
                        self.is_change_position = False
                    retval, frame = self.capture.read()
                    self.read_image(frame)
                    if self._on_update_frame_index is not None:
                        self._on_update_frame_index(self.current_frame)
                    self.current_time = self.time_to_str(self.current_frame*self.latency)
                    self.current_frame += 1
                    d_time = datetime.now() - start_time
                if d_time.microseconds/1000000 < self.latency and d_time.microseconds > 0.0:
                   sleep(self.latency - d_time.microseconds/1000000) # Здесь необходимо замерять время между вызовами, и если и ожидать только разницу.
                # sleep(self.latency)
            else:
                break
        if self.capture:
            self.capture.release()
