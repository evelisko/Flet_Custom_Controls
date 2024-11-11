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

    def pick_files_result(e: ft.FilePickerResultEvent):
        print(e.files) # Список файлов.
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
            ft.NavigationDrawerDestination(icon=ft.icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"),
            ft.NavigationDrawerDestination(icon=ft.icons.ADD_COMMENT, label="Item 2"),
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
        icon=ft.icons.SKIP_NEXT_ROUNDED,# on_click=play_button_clicked, data=0
    )
    btn_prev_video = ft.IconButton(
        icon=ft.icons.SKIP_PREVIOUS_ROUNDED, #on_click=play_button_clicked, data=0
    )
    btn_play_model_config = ft.IconButton(
        icon=ft.icons.MENU, on_click=lambda e: page.open(end_drawer)
    )
    btn_play_list = ft.IconButton(
        icon=ft.icons.MENU, on_click=show_playlist
    )    
    btn_open_video = ft.IconButton(
                            icon=ft.icons.FILE_UPLOAD_OUTLINED,
                            on_click=on_click,  # lambda _: pick_files_dialog.pick_files(allow_multiple=True)
                            tooltip='Open File'# ft.Tooltip..TooltipValue 
                        )
    ft_time_line_value = ft.Text(value='00:00:00/00:00:00')  
    ft_play_track_coontainer = ft.Container(content=ft.Row(
        controls=[btn_prev_video, btn_play, btn_next_video, sldr_time_bar, ft_time_line_value, btn_play_list, btn_open_video], 
        expand=True, 
        alignment=ft.alignment.center_right
        ),
        # bgcolor=ft.colors.RED
        )
    #================================================================
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
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    count = 1
    for i in range(0, 5):
        lv.controls.append(ft.Text(f"Line {count}"))
        count += 1

    gd = ft.GestureDetector(
                content=ft.VerticalDivider(),
                drag_interval=10,
                on_pan_update=move_vertical_divider,
                on_hover=show_draggable_cursor,
                visible=False
            )
    cnt = ft.Container(
                content=lv,
                bgcolor=ft.colors.BROWN_400,
                alignment=ft.alignment.center,
                expand=1,
                visible= False
            )
    x_row = ft.Row(
        controls=[
           ft_row,
           gd,
           cnt
        ],
        spacing=0,
        expand=True
        # width=400,
        # height=400,
    )
    #====================================================================
    page.add(x_row)
    page.on_resized = on_page_resize
    

if __name__ == '__main__':
    ft.app(target=main)

# Циклическое воспроизведение видео.
    