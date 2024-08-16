from tkinter import BooleanVar


class AlarmDetails:
    def __init__(self, is_on:bool, hour:int, minute:int):
        self.is_on = BooleanVar(value=is_on)
        self.hour = hour
        self.minute = minute
        self.sound_played = False
        self.has_rung = False


    def is_time_to_ring(self, current_hour:int, current_minute:int) -> bool:
        return self.is_on.get() and not self.has_rung and self.hour == current_hour and self.minute == current_minute
