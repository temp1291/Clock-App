from tkinter import *
from tkinter import ttk
import json
import time
from singleton import Singleton


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


    def load_data_from_json(self):
        with open('config.json', 'r') as file:
            data = json.load(file)

        self.window_width, self.window_height = data['window_size']


class Stopwatch(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        for c in range(3): self.columnconfigure(index=c, weight=1)
        for r in range(7): self.rowconfigure(index=r, weight=1)

        self.running = False
        self.start_time = 0
        self.previous_mark_time = 0
        self.mark_time_number = 1

        self.put_widgets()


    def put_widgets(self):
        label_title = ttk.Label(self, text='Stopwatch', font=('Arial', 18))
        label_title.grid(column=0, row=0, sticky=W)

        self.label_time = ttk.Label(self, text='0:00.00.000', font=('Arial', 30), justify=CENTER, anchor=CENTER)
        self.label_time.grid(column=0, row=1, columnspan=3, sticky=NSEW)

        self.button_toggle = ttk.Button(self, text='Start', command=self.start)
        self.button_toggle.grid(column=0, row=6)

        self.button_reset = ttk.Button(self, text='Reset', command=self.reset, state='disabled')
        self.button_reset.grid(column=1, row=6)

        self.button_mark = ttk.Button(self, text='Mark', command=self.mark, state='disabled')
        self.button_mark.grid(column=2, row=6)

        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(column=0, row=2, columnspan=3, rowspan=4, sticky=NSEW)

        self.table = ttk.Treeview(self.table_frame, column=('number', 'time', 'delta_time'), show='headings')
        self.table.pack(fill=BOTH, expand=True)

        self.table.heading('number', text='Number')
        self.table.column('number', width=100, anchor='center')

        self.table.heading('time', text='Time')
        self.table.column('time', width=120, anchor='center')

        self.table.heading('delta_time', text='Time Delta')
        self.table.column('delta_time', width=150, anchor='center')


    def start(self):
        self.button_mark.config(state='normal')
        if not self.start_time:
            self.start_time = time.time()

        self.button_toggle.config(text='Pause', command=self.pause)
        self.running = True
        self.update_time()


    def pause(self):
        self.elapsed_time = time.time() - self.start_time
        self.button_reset.config(state='normal')
        self.button_mark.config(state='disabled')
        self.button_toggle.config(text='Resume', command=self.resume)
        self.running = False

    
    def resume(self):
        current_time = time.time()
        self.start_time = current_time - self.elapsed_time
        self.button_reset.config(state='disabled')
        self.button_mark.config(state='normal')
        self.start()


    def reset(self):
        self.start_time = 0
        self.label_time.config(text='0:00.00.000')
        self.button_toggle.config(text='Start', command=self.start)
        self.button_reset.config(state='disabled')
        self.button_mark.config(state='disabled')


    def mark(self):
        current_time = time.time()
        if self.previous_mark_time:
            delta_time = round(current_time - self.previous_mark_time, 4)
        else:
            delta_time = round(current_time - self.start_time, 4)

        self.table.insert('', 0, values=(f'{self.mark_time_number:02}', self.label_time['text'], f'+ {delta_time}'))
        self.previous_mark_time = current_time
        self.mark_time_number += 1


    def update_time(self):
        if self.running:
            elapsed_seconds = time.time() - self.start_time
            hours, minutes, seconds, miliseconds = self.convert_seconds_to_time(elapsed_seconds)

            self.label_time.config(text=f'{hours:01}:{minutes:02}.{seconds:02}.{miliseconds:03}')
            self.parent.after(10, self.update_time)


    def convert_seconds_to_time(self, seconds_to_convert):
        hours = int(seconds_to_convert / 3600)
        seconds_to_convert -= hours * 3600
        minutes = int(seconds_to_convert / 60)
        seconds_to_convert -= minutes * 60
        seconds = int(seconds_to_convert)
        seconds_to_convert -= seconds
        miliseconds = int(seconds_to_convert * 1000)

        return hours, minutes, seconds, miliseconds
