from tkinter import *
from tkinter import ttk
from singleton import Singleton


class SetAlarmWindow(Toplevel, Singleton):
    def __init__(self):
        pass


    def init(self):
        super().__init__()
        self.title('Set Alarm')
        self.geometry(f'{320}x{240}+{self.winfo_screenwidth() // 2 - 320 // 2}+{self.winfo_screenheight() // 2 - 240 // 2}')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.quit)

        for c in range(2): self.columnconfigure(index=c, weight=1)
        for r in range(4): self.rowconfigure(index=r, weight=1)

        # self.validate_command = (self.register(self.validate_text), '%P')
        self.hour = StringVar(value='0')
        self.minute = StringVar(value='0')

        self.put_widgets()


    def put_widgets(self):
        label_hour = ttk.Label(self, text='Hour:')
        label_hour.grid(column=0, row=0, sticky=S)

        label_minute = ttk.Label(self, text='Minute:')
        label_minute.grid(column=1, row=0, sticky=S)

        self.combobox_hour = ttk.Combobox(self, values=[num for num in range(24)], textvariable=self.hour, state='readonly')
        self.combobox_hour.grid(column=0, row=1, sticky=N, padx=10)
        
        self.combobox_minute = ttk.Combobox(self, values=[num for num in range(60)], textvariable=self.minute, state='readonly')
        self.combobox_minute.grid(column=1, row=1, sticky=N, padx=10)

        self.button_ok = ttk.Button(self, text='Ok', command=self.quit)
        self.button_ok.grid(column=0, row=3, sticky=E, padx=5)

        self.button_cancel = ttk.Button(self, text='Cancel', command=self.cancel)
        self.button_cancel.grid(column=1, row=3, sticky=W, padx=5)


    def quit(self):
        self.destroy()
        self.reset_instance()


    def get_selected_time(self):
        return int(self.hour.get()) if self.hour is not None else self.hour, int(self.minute.get()) if self.minute is not None else self.minute
    

    def cancel(self):
        self.hour = None
        self.minute = None
        self.quit()


