from tkinter import *
from tkinter import ttk
from time import sleep
from datetime import datetime
from pygame import init, mixer
from threading import Thread
from functools import partial
from set_alarm_window import SetAlarmWindow
from alarm_details import AlarmDetails


class Alarm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        for c in range(3): self.columnconfigure(index=c, weight=1)
        for r in range(7): self.rowconfigure(index=r, weight=1)

        init()
        mixer.init()

        self.alarm_sound = mixer.Sound('alarm_sounds\\alarm_1.mp3')
        self.alarm_sound.set_volume(0.3)

        self.alarms_list = []

        self.put_widgets()
        self.update_time()


    def put_widgets(self):
        self.label_title = ttk.Label(self, text='Alarm', font=('Arial', 18))
        self.label_title.grid(column=0, row=0, columnspan=3, sticky=W)

        self.label_time = ttk.Label(self, text='', font=('Arial', 30), justify=CENTER)
        self.label_time.grid(column=0, row=1, columnspan=3)

        self.button_add = ttk.Button(self, text='Add', command=self.open_time_set_window)
        self.button_add.grid(column=1, row=6)

        self.create_frame_alarms()


    def create_frame_alarms(self):
        frame_alarms = ttk.Frame(self)
        frame_alarms.grid(column=0, row=2, columnspan=3, rowspan=4, sticky=NSEW)

        for c in range(2): frame_alarms.columnconfigure(index=c, weight=1)
        for r in range(1): frame_alarms.rowconfigure(index=r, weight=1)

        self.canvas = Canvas(frame_alarms)
        self.canvas.grid(column=0, row=0, sticky=NSEW)

        scrollbar = ttk.Scrollbar(frame_alarms, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(column=1, row=0, sticky=NS)

        self.frame_scrollable = ttk.Frame(self.canvas)
        self.frame_scrollable.bind('<Configure>', lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.canvas.create_window((0, 0), window=self.frame_scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)


    def update_time(self):
        now = datetime.now()
        self.label_time.config(text=f'{now.hour:02}:{now.minute:02}:{now.second:02}')

        for alarm in self.alarms_list:
            if alarm.is_time_to_ring(now.hour, now.minute):
                alarm.has_rung = True
                alarm.sound_played = True
                alarm_thread = Thread(target=self.play_alarm, args=(alarm,))
                alarm_thread.start()

                button_alarm_off = ttk.Button(self.frame_scrollable, text='Turn off the alarm')
                button_alarm_off.config(command=partial(self.turn_off_alarm, alarm, button_alarm_off))
                button_alarm_off.grid(column=0, row=self.alarms_list.index(alarm), columnspan=2)

        self.parent.after(1000, self.update_time)


    def open_time_set_window(self):
        window = SetAlarmWindow()
        window.grab_set()
        self.parent.wait_window(window)

        hour, minute = window.get_selected_time()
        if hour is not None and minute is not None:
            alarm = AlarmDetails(True, hour, minute)
            self.alarms_list.append(alarm)
            self.create_alarm_widget(alarm)


    def create_alarm_widget(self, alarm:AlarmDetails):
        hour = alarm.hour
        minute = alarm.minute

        row = len(self.alarms_list) - 1

        label = ttk.Label(self.frame_scrollable, text=f'{hour:02}:{minute:02}', font=('Arial', 18))
        label.grid(column=0, row=row, sticky=W)

        checkbutton = ttk.Checkbutton(self.frame_scrollable, variable=alarm.is_on)
        checkbutton.grid(column=5, row=row, sticky=E)

    
    def play_alarm(self, alarm:AlarmDetails):
        while alarm.sound_played:
            self.alarm_sound.play()
            sleep(self.alarm_sound.get_length())


    def turn_off_alarm(self, alarm:AlarmDetails, button_alarm_off:ttk.Button):
        alarm.sound_played = False
        button_alarm_off.destroy()
        self.parent.after(60_000, self.reset_has_rung, alarm)


    def reset_has_rung(self, alarm:AlarmDetails):
        alarm.has_rung = False


        
