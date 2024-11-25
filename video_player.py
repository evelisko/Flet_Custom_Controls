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
from video_viewer import VideoViewer
from setting_panel import SettingsPanelNavigationDrawer


class MainControl(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()
        self.is_video_play = False
        self.files_list_opened = False
        self.video_window_width = 0
        self.expand = True

    def build(self) -> ft.Control:
        self.end_drawer = SettingsPanelNavigationDrawer()

        self.sldr_time_bar = ft.Slider(
                            min=0, max=1000,
                            divisions=1000,
                            label="{value}", 
                            active_color=ft.colors.PURPLE,
                            secondary_active_color=ft.colors.RED,
                            thumb_color=ft.colors.PURPLE,
                            expand=True, 
                            on_change=self.slider_changed)

        self.btn_play = ft.IconButton(
            icon=ft.icons.PLAY_ARROW, on_click=self.play_button_clicked, data=0
        )
        self.btn_next_video=ft.IconButton(
            icon=ft.icons.SKIP_NEXT_ROUNDED,  # on_click=play_button_clicked, data=0
        )
        self.btn_prev_video = ft.IconButton(
            icon=ft.icons.SKIP_PREVIOUS_ROUNDED,  # on_click=play_button_clicked, data=0
        )
        self.btn_settings = ft.IconButton(
            icon=ft.icons.SETTINGS, on_click=lambda e: self.page.open(self.end_drawer)  # ^_^
        )
        self.btn_play_list = ft.IconButton(
            icon=ft.icons.MENU, on_click=self.show_playlist
        )    
        self.btn_open_video = ft.IconButton(
                                icon=ft.icons.FILE_UPLOAD_OUTLINED,
                                on_click=self.on_click,  # lambda _: pick_files_dialog.pick_files(allow_multiple=True)
                                tooltip='Open File'  # ft.Tooltip..TooltipValue 
                            )
        self.ft_time_line_value = ft.Text(value='00:00:00/00:00:00')  
        self.ft_play_track_coontainer = ft.Container(content=ft.Row(
            controls=[self.btn_prev_video, self.btn_play, self.btn_next_video, self.sldr_time_bar, self.ft_time_line_value, self.btn_open_video, self.btn_play_list, self.btn_settings], 
            expand=True, 
            alignment=ft.alignment.center_right
            ),
            # bgcolor=ft.colors.RED
            )
        #====================================================================
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)
        self.video_viewer = VideoViewer(update_frame_index=self.on_update_frame_index)
        self.tf_page_size = ft.TextField(value='', expand=True)

        self.ft_row = ft.Column([self.video_viewer, ft.Row([self.tf_page_size]), self.ft_play_track_coontainer],
                            # width = page.width-10
                            expand=True
                            )
        # Перенос видео через drug & drop.
        #====================================================================
        self.dt_files = ft.DataTable(
                    columns=[
                            ft.DataColumn(ft.Text("id")),
                            ft.DataColumn(ft.Text("Name"))
                        ],
                    rows=[],
                    )
        self.gd = ft.GestureDetector(
                    content=ft.VerticalDivider(),
                    drag_interval=10,
                    on_pan_update=self.move_vertical_divider,
                    on_hover=self.show_draggable_cursor,
                    visible=False
                )
        self.cnt = ft.Container(
                    content=self.dt_files,
                    # bgcolor='#53765f',
                    alignment=ft.alignment.top_left,
                    expand=True,
                    visible=False
                )
        x_row = ft.Row(
                controls=[
                        self.ft_row,
                        self.gd,
                        self.cnt
                ],
            spacing=0,
            expand=True
        )
        return x_row


    def on_file_list_click(self, e): # 8ec182
        print(e.control.title.value)
        print(e.control.parent.item_extent)

        # Метод для заполнения списка файлов.
    def read_files_list(self, files: List[FilePickerFile]):
        self.dt_files.rows = []
        self.dt_files.rows = list(map(lambda x: ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(x[0])),
                                    ft.DataCell(ft.Text(x[1].name))
                                ],
                    selected=True,
                    on_select_changed=self.on_file_list_click, #lambda e: print(f"row select changed: {e.data}"),
                ), enumerate(files) ))
        self.dt_files.update()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        #--------------------------------------------------------------------------
        # page.title  = (
        #     ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # ) #Здесь сделаем вызов события потому передающего запись в заголовок окна.
        #--------------------------------------------------------------------------
        if e.files:
            self.read_files_list(e.files)
            file_name = e.files[0].path
            self.video_viewer.open_file(file_name=file_name) # Возвращает к-во кадров в видео или статус открытия видео.
            frame_count = self.video_viewer.get_frames_count()
            self.sldr_time_bar.max = frame_count
            self.sldr_time_bar.divisions = frame_count
            self.is_video_play = True
            self.btn_play.icon = ft.icons.PAUSE
        self.update()

    def time_to_str(self, seconds: float):
        dtime = timedelta(seconds = seconds)
        mm, ss = divmod(dtime.seconds, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss) if hh > 0 else "%02d:%02d" % (mm, ss)
    
    def on_update_frame_index(self, value):
        self.sldr_time_bar.value = value
        self.ft_time_line_value.value = f'{self.video_viewer.get_current_time()}/{self.video_viewer.get_total_time()}'
        self.update()


    def on_click(self, e):
        self.pick_files_dialog.pick_files(allow_multiple=True)

    def slider_changed(self, e):
        self.sldr_time_bar.label = self.time_to_str(e.control.value * self.video_viewer.get_frame_rate())
        self.video_viewer.set_current_frame_index(int(e.control.value))

    def play_button_clicked(self, e):
        if self.btn_play.icon == ft.icons.PAUSE:
            self.btn_play.icon = ft.icons.PLAY_ARROW
            self.is_video_play = False
        else:
            self.btn_play.icon = ft.icons.PAUSE
            self.is_video_play = True
        self.video_viewer.change_play_status(self.is_video_play)
        self.btn_play.update()

    def move_vertical_divider(self, e: ft.DragUpdateEvent):
        self.ft_row.width += e.delta_x
        self.ft_row.update()

    def show_draggable_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    def show_playlist(self, e):
        if self.video_window_width == 0:
            self.video_window_width = self.page.width - 200
        if not self.files_list_opened:
            self.files_list_opened = True
            self.ft_row.expand = False
            self.ft_row.width = self.video_window_width
            self.gd.visible =True
            self.cnt.visible = True
        else:
            self.files_list_opened = False
            self.video_window_width = self.ft_row.width
            self.ft_row.expand = True
            self.gd.visible =False
            self.cnt.visible = False
        self.update()


# TODO: Реализовать в виде отдельного класса.
def main(page: ft.Page):
    page.add(MainControl()) # Вызов события и параметров контрола.
    # page.on_resized = on_page_resize
    page.padding = 5
    page.window.left = page.window.left + 100
    page.theme_mode = ft.ThemeMode.LIGHT
    

if __name__ == '__main__':
    ft.app(target=main)
    