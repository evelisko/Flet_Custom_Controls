
import flet as ft


class PlayList(ft.UserControl):
    def __init__(self):
        super().__init__()
        dt_files = ft.DataTable(
                  columns=[
                        ft.DataColumn(ft.Text("id")),
                        ft.DataColumn(ft.Text("Name"))
                      ],
                  rows=[],
                )

        cnt = ft.Container(
                content=dt_files,
                # bgcolor='#53765f',
                alignment=ft.alignment.top_left,
                expand=True,
                visible=False
            )


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