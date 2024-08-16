from tkinter import *
from tkinter import ttk
from time import time, sleep
from pygame import init, mixer
from threading import Thread
from time_picker_window import TimePickerWindow


class Timer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        for c in range(2): self.columnconfigure(index=c, weight=1)
        for r in range(7): self.rowconfigure(index=r, weight=1)

        init()
        mixer.init()

        self.alarm_sound = mixer.Sound('alarm_sounds\\alarm_1.mp3')
        self.alarm_sound.set_volume(0.3)

        self.running = False

        self.put_widgets()


    def put_widgets(self):
        label_title = ttk.Label(self, text='Timer', font=('Arial', 18))
        label_title.grid(column=0, row=0, sticky=W)

        self.label_time = ttk.Label(self, text='00:00.00', font=('Arial', 30), justify=CENTER, anchor=CENTER)
        self.label_time.grid(column=0, row=1, columnspan=2, sticky=NSEW)
        self.label_time.bind('<ButtonPress-1>', self.open_time_picker)

        self.button_toggle = ttk.Button(self, text='Start', command=self.start, state=DISABLED)
        self.button_toggle.grid(column=0, row=6)

        self.button_reset = ttk.Button(self, text='Reset', command=self.reset, state=DISABLED)
        self.button_reset.grid(column=1, row=6)


    def start(self):
        self.target_time = time() + self.selected_time

        self.button_reset.config(state='normal')
        self.button_toggle.config(text='Pause', command=self.pause)
        self.running = True
        self.update_time()


    def reset(self):
        self.selected_time = 0
        self.running = False
        self.label_time.config(text='00:00.00')
        self.button_toggle.config(text='Start', command=self.start, state=DISABLED)
        self.button_reset.config(state=DISABLED)


    def pause(self):
        self.pause_start_time = time()
        self.button_toggle.config(text='Resume', command=self.resume)
        self.running = False


    def resume(self):
        self.button_toggle.config(text='Pause', command=self.pause)

        pause_elapsed_time = time() - self.pause_start_time
        self.target_time += pause_elapsed_time
        self.running = True
        self.update_time()


    def update_time(self):
        if self.running:
            remaining_time = self.target_time - time()

            if remaining_time <= 0:
                self.timer_done()
                self.running = False

            hours, minutes, seconds, miliseconds = self.parent.convert_seconds_to_time(remaining_time)
            self.label_time.config(text=f'{hours:01}:{minutes:02}.{seconds:02}')
            self.parent.after(17, self.update_time)


    def open_time_picker(self, event:Event=None):
        window = TimePickerWindow()
        window.grab_set()
        self.parent.wait_window(window)

        self.selected_time = window.get_selected_time()
        hours, minutes, seconds, miliseconds = self.parent.convert_seconds_to_time(self.selected_time)
        self.label_time.config(text=f'{hours:01}:{minutes:02}.{seconds:02}')
        self.button_toggle.config(state=NORMAL)
        self.button_reset.config(state=NORMAL)


    def timer_done(self):
        self.reset()
        self.button_alarm_off = ttk.Button(self, text='Turn off the alarm', command=self.turn_off_alarm)
        self.button_alarm_off.grid(column=0, row=2, columnspan=2)

        self.alarm_played = True

        alarm_thread = Thread(target=self.play_alarm)
        alarm_thread.start()

    
    def play_alarm(self):
        while self.alarm_played:
            self.alarm_sound.play()
            sleep(self.alarm_sound.get_length())


    def turn_off_alarm(self):
        self.alarm_played = False
        self.button_alarm_off.destroy()
