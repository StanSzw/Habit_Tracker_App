import tkinter as tk
from tkinter import messagebox
import datetime
import json

class HabitTrackerApp(tk.Tk):
    
    
    def __init__(self):
        
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("300x200")
      
        self.create_widgets()
        self.habits = {}


    def create_widgets(self):
        
      
        self.add_button = tk.Button(self, text="Add New Habit", command=self.add_habit)
        self.add_button.pack()

        self.check_off_button = tk.Button(self, text="Check off habit", command=self.check_off_habit)
        self.check_off_button.pack()

        self.current_streak_button = tk.Button(self, text="Current Streaks", command=self.display_habit_streaks)
        self.current_streak_button.pack()

        self.longest_streak_button = tk.Button(self, text="Longest Streak", command=self.get_longest_streak)
        self.longest_streak_button.pack()

        #self.missed_periods_button = tk.Button(self, text="Missed Periods", command=self.get_missed_periods)
        #self.missed_periods_button.pack()


    def add_habit(self):
        
        
        self.Enter_Habit = tk.Toplevel(self)
        self.Enter_Habit.title("Enter Habit")
        self.Enter_Habit.geometry("200x200")
        
        label = tk.Label(self.Enter_Habit, text="Enter new habit")
        label.pack()
        
        self.task_label = tk.Label(self.Enter_Habit, text="Task:")
        self.task_label.pack()
    
        self.task_entry = tk.Entry(self.Enter_Habit)
        self.task_entry.pack()
    
        self.periodicity_label = tk.Label(self.Enter_Habit, text="Periodicity:")
        self.periodicity_label.pack()
    
        self.periodicity_entry = tk.Entry(self.Enter_Habit)
        self.periodicity_entry.pack()
        
        self.add_button = tk.Button(self.Enter_Habit, text="Add New Habit", command=self.confirm_habit)
        self.add_button.pack()
        
        
    def confirm_habit(self):
        
               
        task = self.task_entry.get()
        periodicity = int(self.periodicity_entry.get())
        self.habits[task] = {
          'periodicity': periodicity,
          'completed_dates': []
          }
        messagebox.showinfo("Success", "Habit added!")
        self.Enter_Habit.destroy()
        
        
        
    def check_off_habit(self):
        Habit_list = tk.Toplevel(self)
        Habit_list.title("The list of your habits")
        Habit_list.geometry("200x300")

        for habit in self.habits.keys():
            button = tk.Button(Habit_list, text=habit, command=lambda habit=habit: self.check_off_single_habit(habit))
            button.pack()
        
        

    def check_off_single_habit(self, habit):
        if habit in self.habits.keys():
            today = datetime.date.today().isoformat()
            self.habits[habit]['completed_dates'].append(today)
            self.update_streak(habit, today)
            messagebox.showinfo("Check Off", f"{habit} checked off!")
            self.display_habit_streaks()
        
      
  
        
    def update_streak(self, habit, today):
        completed_dates = self.habits[habit]['completed_dates']
        current_streak = 0
    
        last_completed_date = None
        if completed_dates:
            last_completed_date = completed_dates[-1]
    
        if last_completed_date:
            last_completed_date = datetime.datetime.strptime(last_completed_date, '%Y-%m-%d').date()
    
        while last_completed_date and last_completed_date <= datetime.date.today():
            next_due_date = last_completed_date + datetime.timedelta(days=self.habits[habit]['periodicity'])
            if next_due_date <= datetime.date.today():
                current_streak += 1
                last_completed_date = next_due_date
            else:
                break
    
        self.habits[habit]['current_streak'] = current_streak

        

    def get_habit_streaks(self):
        habit_streaks = {}
        for habit, data in self.habits.items():
            if 'current_streak' in data:
                current_streak = data['current_streak']
            else:
                current_streak = 0
            habit_streaks[habit] = current_streak
        return habit_streaks
   
    
   
    def display_habit_streaks(self):
        habit_streaks = self.get_habit_streaks()
    
        habit_list = tk.Toplevel(self)
        habit_list.title("Habit Streaks")
        habit_list.geometry("200x300")
    
        listbox = tk.Listbox(habit_list)
        listbox.pack(fill=tk.BOTH, expand=True)
    
        for habit, streak in habit_streaks.items():
            listbox.insert(tk.END, f"{habit}: {streak}")
    
        
     
        
        
    def get_longest_streak(self):
         longest_streak = 0
         for habit in self.habits.values():
             if 'current_streak' in habit:
                 current_streak = habit['current_streak']
                 if current_streak > longest_streak:
                     longest_streak = current_streak
         messagebox.showinfo("Longest Streak", f"The longest streak is {longest_streak}.")

    #
 
        
        
        
        
        
        
        
app = HabitTrackerApp()
app.mainloop()    
        
        
        
  