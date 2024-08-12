from tkinter import *
from tkinter import ttk
import json
from singleton import Singleton
from stopwatch import Stopwatch
from timer import Timer


class Window(Tk, Singleton):
    def __init__(self):
        pass


    def init(self):
        super().__init__()
        self.load_data_from_json()
        self.title('Clock')
        self.geometry(f'{self.window_width}x{self.window_height}+{self.winfo_screenwidth() // 2 - self.window_width // 2}+{self.winfo_screenheight() // 2 - self.window_height // 2}')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        stopwatch_frame = Stopwatch(self)
        stopwatch_frame.grid(row=0, column=0, sticky="nsew")
        self.notebook.add(stopwatch_frame, text='Stopwatch')

        timer_frame = Timer(self)
        timer_frame.grid(row=0, column=0, sticky="nsew")
        self.notebook.add(timer_frame, text='Timer')


    def load_data_from_json(self):
        with open('config.json', 'r') as file:
            data = json.load(file)

        self.window_width, self.window_height = data['window_size']


    def convert_seconds_to_time(self, seconds_to_convert):
        hours = int(seconds_to_convert / 3600)
        seconds_to_convert -= hours * 3600
        minutes = int(seconds_to_convert / 60)
        seconds_to_convert -= minutes * 60
        seconds = int(seconds_to_convert)
        seconds_to_convert -= seconds
        miliseconds = int(seconds_to_convert * 1000)

        return hours, minutes, seconds, miliseconds
    








