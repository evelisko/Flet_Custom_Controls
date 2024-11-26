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
from controls.image_viewer import ImageViewer


class SettingsPanelNavigationDrawer(ft.NavigationDrawer):
    def __init__(self, 
                  on_change_confidence = None,
                  on_load_model = None
                ):
        super().__init__()
        self.on_change_confidence = on_change_confidence
        self.on_load_model = on_load_model

        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)

        self.btn_open_model = ft.ElevatedButton('Load model',
                                                on_click=lambda _: self.pick_files_dialog.pick_files(
                                                    allow_multiple=False,
                                                    file_type='.pt'
                                                ))
        self.lst_model_name = ft.ListTile(
                                leading=ft.Icon(ft.icons.ALBUM),
                                title=ft.Text("Model Name"),
                            )
        self.swh_show_predicts = ft.Switch('Show predicts', # on_change=self.use_show_predicts
                                           )
        self.swh_use_dinamic_confidence = ft.Switch('Dinamic Confidence')
        self.sldr_confidence_value = ft.Slider(min=0, max=100,
                                divisions=100,
                                label="{value}", 
                                active_color=ft.colors.PURPLE,
                                secondary_active_color=ft.colors.RED,
                                thumb_color=ft.colors.PURPLE,
                                expand=True, 
                                on_change=self.slider_changed  # Что-то надо делать с обработкой событий.
                            )
        self.swh_view_crop_border = ft.Switch('View crop border', on_change=self.show_crop_border)


        # self.overlay.append(self.pick_files_dialog)

        self.position=ft.NavigationDrawerPosition.END
        self.controls=[
                ft.Row([ 
                        self.btn_open_model,
                        self.lst_model_name
                    ]),
                    self.swh_show_predicts,
                    self.sldr_confidence_value,
                    ft.Divider(),
                    self.swh_use_dinamic_confidence,
                    ft.Divider(),
                    self.swh_view_crop_border
            ]
        # self.   

    # .get_directory_path()
    
    def build(self):
        self.page.overlay.append(self.pick_files_dialog)


    # def did_mount(self):
    #     self.update()

    def slider_changed(self, e):
        # if self.on_change_confidence
        self.on_change_confidence(e.value/100)
        # Получаем значение confidence value.
        # Ызов события с отображением значения
 
    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.lst_model_name.title = e.files[0].name
            self.update()

    # def use_show_predicts(self, e):
    #     return self.swh_show_predicts.value
    # Показывать предсказания модели.

    def show_crop_border(self, e):
        return self.show_crop_border.value
    # Показывать или отключать отображение границ кропа.

    def set_confidence(self, value):
        self.sldr_confidence_value = value
        self.update()

    def get_dinamic_confidence_status(self):
        return self.swh_use_dinamic_confidence.value
    
    def get_show_predicts_status(self):
        return self.swh_show_predicts.value
    
    def get_crop_border_visible_status(self):
        return self.swh_view_crop_border.value

    # def on_load_model(self, e):
    #     self.pick_files_dialog..get_directory_path()
        # pass
        # Загрузка модели.
        # Вызывать событие загрузки модели. 

    # При реализации событий используется переопредеелние.
    # Если объекта нет то используется объет взятый внутри класса, если есть то берется внешний объект.
