import cv2
import base64
import threading
import flet as ft
from time import sleep

class CameraCaptureControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(0)
        self.latency = 1 / self.capture.get(cv2.CAP_PROP_FPS)

    def did_mount(self):
        self.running = True
        self.thread = threading.Thread(target=self.update_frame, args=(), daemon=True)
        self.thread.start()

    def will_unmount(self):
        self.running = False

    def update_frame(self):
        while self.capture.isOpened() and self.running:
            retval, frame = self.capture.read()
            retval, frame = cv2.imencode(".jpg", frame)
            data = base64.b64encode(frame)
            self.image_control.src_base64 = data.decode()
            self.update()
            sleep(self.latency)

    def build(self):
        self.image_control = ft.Image(
            width=self.capture.get(cv2.CAP_PROP_FRAME_WIDTH),
            height=self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT),
            fit=ft.ImageFit.FIT_WIDTH,
        )
        return self.image_control
