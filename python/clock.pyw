import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import winsound

class DigitalClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")
        self.root.geometry("550x300")
        self.root.configure(bg='#282c34')
        self.time_label = tk.Label(root, font=('Helvetica', 48, 'bold'), bg='#282c34', fg='#61dafb')
        self.time_label.pack(pady=20)
        self.date_label = tk.Label(root, font=('Helvetica', 24, 'bold'), bg='#282c34', fg='#61dafb')
        self.date_label.pack(pady=10)
        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p") 
        current_date = now.strftime("%A, %B %d, %Y")
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_clock)

    def run(self):
        self.root.mainloop()

class AlarmTimerApp(DigitalClockApp):
    def __init__(self, root):
        super().__init__(root)
        self.alarm_time = None
        self.timer_seconds = 0

        alarm_frame = tk.Frame(root, bg='#282c34')
        alarm_frame.pack(pady=10)
        tk.Label(alarm_frame, text="Set Alarm (HH:MM AM/PM):", font=('Helvetica', 12), bg='#282c34', fg='#61dafb').grid(row=0, column=0, padx=5)
        self.alarm_entry = ttk.Entry(alarm_frame, font=('Helvetica', 14))
        self.alarm_entry.grid(row=0, column=1, padx=5)
        alarm_button = ttk.Button(alarm_frame, text="Set Alarm", command=self.set_alarm)
        alarm_button.grid(row=0, column=2, padx=5)

        timer_frame = tk.Frame(root, bg='#282c34')
        timer_frame.pack(pady=10)
        tk.Label(timer_frame, text="Set Timer (minutes):", font=('Helvetica', 12), bg='#282c34', fg='#61dafb').grid(row=0, column=0, padx=5)
        self.timer_entry = ttk.Entry(timer_frame, font=('Helvetica', 14))
        self.timer_entry.grid(row=0, column=1, padx=5)
        timer_button = ttk.Button(timer_frame, text="Start Timer", command=self.start_timer)
        timer_button.grid(row=0, column=2, padx=5)

        self.check_alarm()
        self.check_timer()

    def set_alarm(self):
        self.alarm_time = self.alarm_entry.get()
        self.alarm_entry.delete(0, tk.END)
        messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time}")

    def start_timer(self):
        try:
            minutes = int(self.timer_entry.get())
            self.timer_seconds = minutes * 60
            self.timer_entry.delete(0, tk.END)
            messagebox.showinfo("Timer Set", f"Timer set for {minutes} minutes")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    def check_alarm(self):
        if self.alarm_time:
            now = datetime.now().strftime("%I:%M %p")
            if now == self.alarm_time:
                winsound.Beep(1000, 1000)
                messagebox.showinfo("Alarm", "Time to wake up!")
                self.alarm_time = None
        self.root.after(1000, self.check_alarm)

    def check_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            if self.timer_seconds == 0:
                winsound.Beep(1000, 1000)
                messagebox.showinfo("Timer", "Time's up!")
        self.root.after(1000, self.check_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmTimerApp(root)
    app.run()
