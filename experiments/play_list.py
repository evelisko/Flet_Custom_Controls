
import flet as ft

def main(page: ft.Page):
    page.padding = 5
    page.window.left = page.window.left + 100
    # page.width = 300
    page.theme_mode = ft.ThemeMode.DARK

    def on_file_list_click( e): # 8ec182
        tf_selected_value.value = f'{e.control.cells[0].data} | {e.control.cells[1].data}'
        # e.control.selected = 
        page.update()
        # print(e.control.parent.item_extent) # Еще но так - e.control._DataRow__cells[1].content.value

    # Поиск.
    # Перелистывание следующе.
    # Выбор.  

    def on_prev_click(e):
        pass

    def on_next_click(e):
        pass

    files_list = [
            'Hellboj.Geroj.iz.Pekla.2004.D.BDRip.1.46Gb_ExKinoRay_by_Twi7ter.avi',
            'Hellboj.II.Zolotaja.Armija.2008.D.BDRip.1.46Gb_ExKinoRay_by_Twi7ter.avi',
            'report_october_2024.mp4',
            'Snowden.2016.HDRip-AVC 1.46 .OlLanDGroup..mkv',
            'Snowden_2016_HDRip__[scarabey.org].avi'
    ]
    dt_files = ft.DataTable(
                    columns=[
                            ft.DataColumn(ft.Text("id"), visible=False),
                            ft.DataColumn(ft.Text("Name"))
                        ],
                    rows=[],
                    )
    
    dt_files.rows = list(map(lambda x: ft.DataRow(
                            cells=[
                                ft.DataCell( 
                                    ft.Text(x[0]),
                                    data=x[0],
                                    visible=False
                                    ),
                                ft.DataCell(
                                    ft.Text(x[1]),
                                     data=x[1]
                                     )
                            ],
                selected=True,
                on_select_changed=on_file_list_click, #lambda e: print(f"row select changed: {e.data}"),
            ), enumerate(files_list) ))
    
    tf_selected_value = ft.TextField(value='')

    next_prev = ft.Row([
        ft.IconButton(icon=ft.icons.NAVIGATE_BEFORE,
                      on_click=on_prev_click
                      ),
        ft.IconButton(icon=ft.icons.NAVIGATE_NEXT,
                      on_click=on_next_click
                      )
                ])


    page.add(ft.Column([dt_files, tf_selected_value, next_prev]))


if __name__ == '__main__':
    ft.app(target=main)



# https://github.com/flet-dev/flet/discussions/1220
# https://davy.ai/how-to-get-data-table-rows-value-in-flet-python/
#  def recive_btn(self, e):

#         # data = self.my_table.rows[0].cells
#         # print(data)

#         save = []
#         for r in self.my_table.rows:
#             j = []
#             data = r.cells
#             j.append(data[2]._DataCell__content.value)
#             j.append(data[1]._DataCell__content.value)
#             j.append(data[0]._DataCell__content.value)
#             save.append(j)
#         print(save)  # [['6', 'aa', 'bb'], ['3', 'nn', 'zz']]
    

# class PlayList(ft.UserControl):
#     def __init__(self):
#         super().__init__()
#         dt_files = ft.DataTable(
#                   columns=[
#                         ft.DataColumn(ft.Text("id"), visible=False),
#                         ft.DataColumn(ft.Text("Name"))
#                       ],
#                   rows=[],
#                 )

#         cnt = ft.Container(
#                 content=dt_files,
#                 # bgcolor='#53765f',
#                 alignment=ft.alignment.top_left,
#                 expand=True,
#                 visible=False
#             )


#     def on_file_list_click(e): # 8ec182
#             print(e.control.title.value)
#             print(e.control.parent.item_extent)

#         # Метод для заполнения списка файлов.
#     def read_files_list(files: List[FilePickerFile]):
#         dt_files.rows = []
#         dt_files.rows = list(map(lambda x: ft.DataRow(
#                                 cells=[
#                                     ft.DataCell(ft.Text(x[0])),
#                                     ft.DataCell(ft.Text(x[1].name))
#                                 ],
#                     selected=True,
#                     on_select_changed=on_file_list_click, #lambda e: print(f"row select changed: {e.data}"),
#                 ), enumerate(files) ))
        

#         dt_files.update()





#     def pick_files_result(e: ft.FilePickerResultEvent):
#             # print(e.files) # Список файлов.
#             global current_frame
#             global capture
#             global latency
#             global frame_count
#             global is_video_play
#             global total_time

#             page.title  = (
#                 ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
#             )
#             if e.files:
#                 read_files_list(e.files)
#                 file_name = e.files[0].path
#                 current_frame = 0
#                 is_new = True
#                 if capture:
#                     if capture.isOpened():
#                         capture.release()
#                         capture=None
#                         is_new = False
#                         # thread.stop()
#                 capture = cv2.VideoCapture(file_name)
#                 latency = 1 / capture.get(cv2.CAP_PROP_FPS)
#                 frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
#                 # capture.set(cv2.CAP_PROP_POS_FRAMES, 100)
#                 is_video_play = True
#                 btn_play.icon = ft.icons.PAUSE
#                 sldr_time_bar.max = int(frame_count)
#                 sldr_time_bar.divisions = int(frame_count)
#                 total_time = time_to_str(frame_count * latency) 
#                 print(total_time)
#                 if is_new:
#                     thread = threading.Thread(target=update_frame, args=(), daemon=True)
#                     thread.start()
#             page.update()