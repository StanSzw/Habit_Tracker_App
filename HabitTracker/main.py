from HabitTrackerApp import HabitTrackerApp

app = HabitTrackerApp()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()