from tkinter import *
from tkinter import ttk
from time import time


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
        self.button_toggle.config(text='Pause', command=self.pause)

        if not self.start_time:
            self.start_time = time()

        self.running = True
        self.update_time()


    def pause(self):
        self.elapsed_time = time() - self.start_time
        self.button_reset.config(state='normal')
        self.button_mark.config(state='disabled')
        self.button_toggle.config(text='Resume', command=self.resume)
        self.running = False

    
    def resume(self):
        current_time = time()
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
        self.clear_table()
        self.mark_time_number = 1


    def mark(self):
        current_time = time()
        if self.previous_mark_time:
            delta_time = round(current_time - self.previous_mark_time, 4)
        else:
            delta_time = round(current_time - self.start_time, 4)

        self.table.insert('', 0, values=(f'{self.mark_time_number:02}', self.label_time['text'], f'+ {delta_time}'))
        self.previous_mark_time = current_time
        self.mark_time_number += 1


    def update_time(self):
        if self.running:
            elapsed_seconds = time() - self.start_time
            hours, minutes, seconds, miliseconds = self.parent.convert_seconds_to_time(elapsed_seconds)
            self.label_time.config(text=f'{hours:01}:{minutes:02}.{seconds:02}.{miliseconds:03}')
            self.parent.after(17, self.update_time)


    def clear_table(self):
        for item in self.table.get_children():
            self.table.delete(item)



    