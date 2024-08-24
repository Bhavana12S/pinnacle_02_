pip install playsound
pip install pygame
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
import time
import threading
from playsound import playsound

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.alarm_time = None
        self.alarm_tone = None
        self.snooze_duration = 5  # Default snooze for 5 minutes
        self.create_widgets()
        self.check_alarm_thread = threading.Thread(target=self.check_alarm)
        self.check_alarm_thread.start()

    def create_widgets(self):
        tk.Label(self.root, text="Set Alarm Time (HH:MM:SS):").pack(pady=10)
        
        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack(pady=5)
        
        self.snooze_label = tk.Label(self.root, text=f"Snooze Duration: {self.snooze_duration} minutes")
        self.snooze_label.pack(pady=5)
        
        tk.Button(self.root, text="Set Alarm", command=self.set_alarm).pack(pady=5)
        tk.Button(self.root, text="Choose Alarm Tone", command=self.choose_tone).pack(pady=5)
        tk.Button(self.root, text="Snooze", command=self.snooze).pack(pady=5)

    def set_alarm(self):
        alarm_time_str = self.time_entry.get()
        try:
            self.alarm_time = datetime.strptime(alarm_time_str, "%H:%M:%S").time()
            messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time.strftime('%H:%M:%S')}")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM:SS format.")
    
    def choose_tone(self):
        self.alarm_tone = filedialog.askopenfilename(title="Choose Alarm Tone", filetypes=(("MP3 files", "*.mp3"), ("WAV files", "*.wav")))
        if self.alarm_tone:
            messagebox.showinfo("Tone Selected", f"Tone selected: {self.alarm_tone}")

    def snooze(self):
        if self.alarm_time:
            snooze_time = datetime.combine(datetime.today(), self.alarm_time) + timedelta(minutes=self.snooze_duration)
            self.alarm_time = snooze_time.time()
            messagebox.showinfo("Snooze", f"Alarm snoozed until {self.alarm_time.strftime('%H:%M:%S')}")

    def check_alarm(self):
        while True:
            if self.alarm_time and datetime.now().time() >= self.alarm_time:
                self.ring_alarm()
                break
            time.sleep(1)
    
    def ring_alarm(self):
        if self.alarm_tone:
            playsound(self.alarm_tone)
        else:
            messagebox.showinfo("Alarm!", "Time to wake up!")
        self.alarm_time = None

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
