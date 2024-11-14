# Загрузка видео с файла.
# Добавить переметоку.
# Добавить разные элементы управления на панель инструментов.
import cv2
import os
import base64
import flet as ft
import threading
from time import sleep
from typing import List 
from datetime import datetime, timedelta, timezone
from flet_core.file_picker import FilePickerFile
import flet.canvas as cv
import numpy as np
from image_viewer import ImageViewer

current_frame = 0
capture = None
latency = None
current_time = None
total_time = None
frame_count = None
is_video_play = False
is_change_position = False
files_list_opened = False
video_window_width = 0

# TODO: Реализовать в виде отдельного класса.
def main(page: ft.Page):
    page.padding = 5
    page.window.left = page.window.left + 100
    page.theme_mode = ft.ThemeMode.LIGHT

    def on_file_list_click(e): # 8ec182
        print(e.control.title.value)
        print(e.control.parent.item_extent)

        # Метод для заполнения списка файлов.
    def read_files_list(files: List[FilePickerFile]):
        dt_files.rows = []
        dt_files.rows = list(map(lambda x: ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(x[0])),
                                    ft.DataCell(ft.Text(x[1].name))
                                ],
                    selected=True,
                    on_select_changed=on_file_list_click, #lambda e: print(f"row select changed: {e.data}"),
                ), enumerate(files) ))
        

        dt_files.update()

    def pick_files_result(e: ft.FilePickerResultEvent):
        # print(e.files) # Список файлов.
        global current_frame
        global capture
        global latency
        global frame_count
        global is_video_play
        global total_time

        page.title  = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        if e.files:
            read_files_list(e.files)
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
            btn_play.icon = ft.icons.PAUSE
            sldr_time_bar.max = int(frame_count)
            sldr_time_bar.divisions = int(frame_count)
            total_time = time_to_str(frame_count * latency) 
            print(total_time)
            if is_new:
                thread = threading.Thread(target=update_frame, args=(), daemon=True)
                thread.start()
        page.update()

    def time_to_str(seconds: float):
        dtime = timedelta(seconds = seconds)
        mm, ss = divmod(dtime.seconds, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss) if hh > 0 else "%02d:%02d" % (mm, ss)
    
    def on_image_viewer_mouse_move(x, y):
        tf_page_size.value = f'{x}/{y}'
        tf_page_size.update()

    def on_click(e):
        pick_files_dialog.pick_files(allow_multiple=True)

    def update_frame():
        # TODO: https://all-python.ru/osnovy/threading.html
        global current_frame
        global latency
        global frame_count
        global capture
        global is_change_position
        # Реализовать просмотр и перемотку.
        while current_frame < frame_count:
            if capture: # Проверка что открыт новый файл.
                if is_video_play:
                    if is_change_position:
                        capture.set(cv2.CAP_PROP_POS_FRAMES, int(current_frame))
                        is_change_position = False
                    retval, frame = capture.read()
                    img_viewer.read_image(frame)
                    sldr_time_bar.value = current_frame
                    ft_time_line_value.value = f'{time_to_str(current_frame*latency)}/{total_time}'
                    ft_time_line_value.update()
                    tf_page_size.value = str(int(capture.get(cv2.CAP_PROP_POS_FRAMES)))
                    tf_page_size.update() 
                    current_frame += 1
                    sldr_time_bar.update()
                sleep(latency)
            else:
                break
        if capture:
            capture.release()
    
    def on_page_resize(e):
        tf_page_size.value = f'{page.width}/{page.height}'
        page.update()

    def slider_changed(e):
        global capture
        global latency
        global current_frame
        global is_change_position
        current_frame = int(e.control.value)
        is_change_position = True
        # capture.set(cv2.CAP_PROP_POS_FRAMES, int(e.control.value))
        sldr_time_bar.label = time_to_str(e.control.value * latency)

    def play_button_clicked(e):
        global is_video_play
        if btn_play.icon == ft.icons.PAUSE:
            btn_play.icon = ft.icons.PLAY_ARROW
            is_video_play = False
        else:
            btn_play.icon = ft.icons.PAUSE
            is_video_play = True
        btn_play.update()

    def move_vertical_divider(e: ft.DragUpdateEvent):
        # if (e.delta_x > 0 and ft_row.width < 300) or (e.delta_x < 0 and ft_row.width > 100):
        ft_row.width += e.delta_x
        ft_row.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    def show_playlist(e):
        global files_list_opened
        global video_window_width

        if video_window_width == 0:
            video_window_width = page.width - 200

        if not files_list_opened:
            files_list_opened = True
            ft_row.expand = False
            ft_row.width = video_window_width
            gd.visible =True
            cnt.visible = True
        else:
            files_list_opened = False
            video_window_width = ft_row.width
            ft_row.expand = True
            gd.visible =False
            cnt.visible = False
        page.update()

    # Настекать кнопки.
    #================================================================
    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        controls=[
            # Выбор файла с моделью.
            ft.Row([ 
                ft.ElevatedButton('Load model'),
                ft.ListTile(
                        leading=ft.Icon(ft.icons.ALBUM),
                        title=ft.Text("Model Name"),
                        # subtitle=ft.Text(
                        #     "Music by Julie Gable. Lyrics by Sidney Stein."
                        )]
                    ),
            # предсказывать или нет вообще.
            ft.Switch('Show predicts'),       
            # использовать или нет динамический порог.
            ft.Divider(),
            ft.Switch('Dinamic Confidence'),
            
            # движок для установки порога.
            ft.Slider(min=0, max=100,
                        divisions=100,
                        label="{value}", 
                        active_color=ft.colors.PURPLE,
                        secondary_active_color=ft.colors.RED,
                        thumb_color=ft.colors.PURPLE,
                        expand=True, 
                        # on_change=slider_changed
                        ),
            ft.Divider(),
            # отображать или нет рамку.
            ft.Switch('View crop border'),

            # Отображать или нет курсор.

            # Настройка яркости и контрастности.
            # предсказывать или нет вообще.
            # ft.NavigationDrawerDestination(icon=ft.icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"),
            # ft.NavigationDrawerDestination(icon=ft.icons.ADD_COMMENT, label="Item 2"),
            # ft.ElevatedButton('Hello'),
        ],
    )

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
    btn_next_video=ft.IconButton(
        icon=ft.icons.SKIP_NEXT_ROUNDED,  # on_click=play_button_clicked, data=0
    )
    btn_prev_video = ft.IconButton(
        icon=ft.icons.SKIP_PREVIOUS_ROUNDED,  # on_click=play_button_clicked, data=0
    )
    btn_settings = ft.IconButton(
        icon=ft.icons.SETTINGS, on_click=lambda e: page.open(end_drawer)
    )
    btn_play_list = ft.IconButton(
        icon=ft.icons.MENU, on_click=show_playlist
    )    
    btn_open_video = ft.IconButton(
                            icon=ft.icons.FILE_UPLOAD_OUTLINED,
                            on_click=on_click,  # lambda _: pick_files_dialog.pick_files(allow_multiple=True)
                            tooltip='Open File'  # ft.Tooltip..TooltipValue 
                        )
    ft_time_line_value = ft.Text(value='00:00:00/00:00:00')  
    ft_play_track_coontainer = ft.Container(content=ft.Row(
        controls=[btn_prev_video, btn_play, btn_next_video, sldr_time_bar, ft_time_line_value, btn_open_video, btn_play_list, btn_settings], 
        expand=True, 
        alignment=ft.alignment.center_right
        ),
        # bgcolor=ft.colors.RED
        )
    #====================================================================
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    img_viewer = ImageViewer(on_mouse_move=on_image_viewer_mouse_move)
    tf_page_size = ft.TextField(value='', expand=True)

    ft_row = ft.Column([img_viewer, ft.Row([tf_page_size]), ft_play_track_coontainer],
                        # width = page.width-10
                        expand=True
                        )
    # Перенос видео через drug & drop.
    #====================================================================
    dt_files = ft.DataTable(
                  columns=[
                        ft.DataColumn(ft.Text("id")),
                        ft.DataColumn(ft.Text("Name"))
                      ],
                  rows=[
                    # ft.DataRow(
                    #     cells=[
                    #         ft.DataCell(ft.Text("1")),
                    #         ft.DataCell(ft.Text("dhdhfhfbbvhjfdfhjfdbfSmith"))
                    #         ],
                    #         selected=True,
                    #         on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    #     ),
                    # ft.DataRow(
                    #     cells=[
                    #         ft.DataCell(ft.Text("2")),
                    #         ft.DataCell(ft.Text("Brown"))
                    #     ],
                    #     selected=True,
                    #     on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    # ),
                    # ft.DataRow(
                    #     cells=[
                    #         ft.DataCell(ft.Text("3")),
                    #         ft.DataCell(ft.Text("Wong"))
                    #     ],
                    #     selected=True,
                    #     on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    #     ),
                    ],

#                     on_select_changed
#                     selected
# Выбрана ли строка.

# Если on_select_changed не равно нулю для какой-либо строки в таблице, то в начале каждой строки отображается флажок. Если строка выбрана (True), флажок будет установлен, а строка выделена.

# В противном случае флажок, если он присутствует, не будет установлен.
                )

    gd = ft.GestureDetector(
                content=ft.VerticalDivider(),
                drag_interval=10,
                on_pan_update=move_vertical_divider,
                on_hover=show_draggable_cursor,
                visible=False
            )
    cnt = ft.Container(
                content=dt_files,
                # bgcolor='#53765f',
                alignment=ft.alignment.top_left,
                expand=True,
                visible=False
            )
    x_row = ft.Row(
            controls=[
                    ft_row,
                    gd,
                    cnt
            ],
        spacing=0,
        expand=True
    )
    #====================================================================
    page.add(x_row)
    page.on_resized = on_page_resize
    

if __name__ == '__main__':
    ft.app(target=main)

# Циклическое воспроизведение видео.
    