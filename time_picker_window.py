from tkinter import *
from tkinter import ttk
from singleton import Singleton


class TimePickerWindow(Toplevel, Singleton):
    def __init__(self):
        pass


    def init(self):
        super().__init__()
        self.title('Time Picker')
        self.geometry(f'{320}x{240}+{self.winfo_screenwidth() // 2 - 320 // 2}+{self.winfo_screenheight() // 2 - 240 // 2}')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.quit)

        for c in range(3): self.columnconfigure(index=c, weight=1)
        for r in range(4): self.rowconfigure(index=r, weight=1)

        self.validate_command = (self.register(self.validate_text), '%P')
        self.selected_time = 0

        self.put_widgets()


    def put_widgets(self):
        label_hour = ttk.Label(self, text='Hour:')
        label_hour.grid(column=0, row=0, sticky=S)

        label_minute = ttk.Label(self, text='Minute:')
        label_minute.grid(column=1, row=0, sticky=S)

        label_second = ttk.Label(self, text='Second')
        label_second.grid(column=2, row=0, sticky=S)

        self.spinbox_hour = ttk.Spinbox(self, from_=0, to=24, wrap=True, validate='key', validatecommand=self.validate_command)
        self.spinbox_hour.grid(column=0, row=1, sticky=N, padx=10)
        
        self.spinbox_minute = ttk.Spinbox(self, from_=0, to=60, wrap=True, validate='key', validatecommand=self.validate_command)
        self.spinbox_minute.grid(column=1, row=1, sticky=N, padx=10)
        
        self.spinbox_second = ttk.Spinbox(self, from_=0, to=60, wrap=True, validate='key', validatecommand=self.validate_command)
        self.spinbox_second.grid(column=2, row=1, sticky=N, padx=10)

        self.button_ok = ttk.Button(self, text='Ok', command=self.confirm_time_selection)
        self.button_ok.grid(column=1, row=3, sticky=E, padx=5)

        self.button_cancel = ttk.Button(self, text='Cancel', command=self.quit)
        self.button_cancel.grid(column=2, row=3, sticky=W, padx=5)


    def confirm_time_selection(self):
        hours = 0 if (not self.spinbox_hour.get().isdigit() or not self.spinbox_hour.get()) else int(self.spinbox_hour.get())
        minutes = 0 if (not self.spinbox_minute.get().isdigit() or not self.spinbox_minute.get()) else int(self.spinbox_minute.get())
        seconds = 0 if (not self.spinbox_second.get().isdigit() or not self.spinbox_second.get()) else int(self.spinbox_second.get())
        self.selected_time = hours * 3600 + minutes * 60 + seconds

        self.quit()


    def get_selected_time(self):
        return self.selected_time
    

    def validate_text(self, text:str) -> bool:
        return text.isdigit()
        #Invalid input: Please enter a valid number.


    def quit(self):
        self.destroy()
        self.reset_instance()

        


