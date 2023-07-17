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
        self.load_data_from_json()



    def create_widgets(self):
        self.add_button = tk.Button(self, text="Add New Habit", command=self.show_add_habit_dialog)
        self.add_button.pack()

        self.see_habits_button = tk.Button(self, text="See My Habits", command=self.see_my_habits)
        self.see_habits_button.pack()

        self.check_off_button = tk.Button(self, text="Check off habit", command=self.check_off_habit)
        self.check_off_button.pack()

        self.statistics_button = tk.Button(self, text="Statistics", command=self.open_statistics_window)
        self.statistics_button.pack()

        self.remove_habit_button = tk.Button(self, text="Remove Habit", command=self.remove_habit)
        self.remove_habit_button.pack()
        
        
        
    def open_statistics_window(self):
        statistics_window = tk.Toplevel(self)
        statistics_window.title("Statistics")
        statistics_window.geometry("200x200")

        self.current_streak_button = tk.Button(statistics_window, text="Current Streaks", command=self.display_habit_streaks)
        self.current_streak_button.pack()

        self.longest_streak_button = tk.Button(statistics_window, text="Longest Streak", command=self.get_longest_streak)
        self.longest_streak_button.pack()

        self.show_missing_button = tk.Button(statistics_window, text="Missing Check-offs", command=self.show_broken_streaks)
        self.show_missing_button.pack()
        
        self.show_missing_button = tk.Button(statistics_window, text="Sort habits by periodicity", command=self.get_habits_by_periodicity)
        self.show_missing_button.pack()
        
        self.statistics_button = tk.Button(statistics_window, text="Periodicities", command=self.List_of_periodicities)
        self.statistics_button.pack()


    def List_of_periodicities(self):
        periodicities_window = tk.Toplevel(self)
        periodicities_window.title("Periodicities")
        periodicities_window.geometry("200x200")
        
        for periodicity in set(habit_data['periodicity'] for habit_data in self.habits.values()):
            periodicity_button = tk.Button(periodicities_window, text=f"Periodicity: {periodicity} days", command=lambda p=periodicity: self.show_habits_by_periodicity(p))
            periodicity_button.pack()

        

    def show_habits_by_periodicity(self, periodicity):
        habits_with_periodicity = self.get_habits_by_periodicity(periodicity)

        habits_list_window = tk.Toplevel(self)
        habits_list_window.title(f"Habits with Periodicity: {periodicity} days")
        habits_list_window.geometry("300x200")

        if not habits_with_periodicity:
            no_habits_label = tk.Label(habits_list_window, text="No habits with this periodicity.")
            no_habits_label.pack()
            return

        listbox = tk.Listbox(habits_list_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        for habit in habits_with_periodicity:
            listbox.insert(tk.END, habit)



    def get_habits_by_periodicity(self, periodicity):
        habits_with_periodicity = []
        for habit, data in self.habits.items():
            if data['periodicity'] == periodicity:
                habits_with_periodicity.append(habit)
        return habits_with_periodicity



    def show_add_habit_dialog(self):
        self.Enter_Habit = tk.Toplevel(self)
        self.Enter_Habit.title("Enter Habit")
        self.Enter_Habit.geometry("300x200")
        
        label = tk.Label(self.Enter_Habit, text="Enter new habit")
        label.pack()
        
        self.task_label = tk.Label(self.Enter_Habit, text="Task:")
        self.task_label.pack()
    
        self.task_entry = tk.Entry(self.Enter_Habit)
        self.task_entry.pack()
    
        self.periodicity_label = tk.Label(self.Enter_Habit, text="Periodicity \n (number of days between repeating your habit):")
        self.periodicity_label.pack()
    
        self.periodicity_entry = tk.Entry(self.Enter_Habit)
        self.periodicity_entry.pack()
        
        self.add_button = tk.Button(self.Enter_Habit, text="Add New Habit", command=self.add_new_habit)
        self.add_button.pack()



    def add_new_habit(self):
        task = self.task_entry.get()
        periodicity = int(self.periodicity_entry.get())
        created_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.add_habit(task, periodicity, created_date)
        messagebox.showinfo("Success", "Habit added!")
        self.Enter_Habit.destroy()



    def add_habit(self, task, periodicity, created_date):
        self.habits[task] = {
            'periodicity': periodicity,
            'created_day': created_date,
            'completed_dates': []
        }     
  
        
        
    def check_off_habit(self):
        self.Habit_list = tk.Toplevel(self)
        self.Habit_list.title("The list of your habits")
        self.Habit_list.geometry("200x300")

        for habit in self.habits.keys():
            button = tk.Button(self.Habit_list, text=habit, command=lambda habit=habit: self.check_off_single_habit(habit))
            button.pack()
        
        

    def check_off_single_habit(self, habit):
        if habit in self.habits.keys():
            today = datetime.date.today().isoformat()
            self.habits[habit]['completed_dates'].append(today)
            self.update_streak(habit)
            messagebox.showinfo("Check Off", f"{habit} checked off!")
            self.save_data_to_json()
        self.Habit_list.destroy()
       

        
    def update_streak(self, habit):
        completed_dates = self.habits[habit]['completed_dates']
        current_streak = 0
        
        if completed_dates:
            last_completed_date = datetime.datetime.strptime(completed_dates[-1], '%Y-%m-%d').date()
            current_date = datetime.date.today()
            delta = current_date - last_completed_date
    
            if delta.days == 0 or delta.days % self.habits[habit]['periodicity'] == 0:
                current_streak = 1
    
                for i in range(len(completed_dates) - 2, -1, -1):
                    previous_date = datetime.datetime.strptime(completed_dates[i], '%Y-%m-%d').date()
                    if (last_completed_date - previous_date).days == 1:
                        current_streak += 1
                        last_completed_date = previous_date
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

 

    def save_data_to_json(self):
        with open("habits.json", "w") as file:
            json.dump(self.habits, file)



    def load_data_from_json(self):
        try:
            with open("habits.json", "r") as file:
                self.habits = json.load(file)
        except FileNotFoundError:
            self.habits = {}



    def on_closing(self):
        self.save_data_to_json()
        self.destroy()
        
        
        
    def see_my_habits(self):
        habits_list = tk.Toplevel(self)
        habits_list.title("My Habits")
        habits_list.geometry("300x200")

        if not self.habits:
            no_habits_label = tk.Label(habits_list, text="No habits to display.")
            no_habits_label.pack()
            return

        listbox = tk.Listbox(habits_list)
        listbox.pack(fill=tk.BOTH, expand=True)

        for habit, data in self.habits.items():
            created_date = data.get('created_day', 'Unknown')
            habit_info = f"{habit} (Periodicity: {data['periodicity']})"
            listbox.insert(tk.END, habit_info, created_date)
    
    
    def remove_habit(self):
        if not self.habits:
            messagebox.showinfo("No Habits", "There are no habits to remove.")
            return

        self.habit_remove_dialog = tk.Toplevel(self)
        self.habit_remove_dialog.title("Remove Habit")
        self.habit_remove_dialog.geometry("300x200")

        for habit in self.habits.keys():
            button = tk.Button(self.habit_remove_dialog, text=habit, command=lambda h=habit: self.confirm_removal(h))
            button.pack()

    def confirm_removal(self, habit):
        confirmation = messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove the habit: {habit}?")
        if confirmation:
            del self.habits[habit]
            messagebox.showinfo("Habit Removed", f"{habit} has been removed.")
        self.habit_remove_dialog.destroy()


    
    def show_broken_streaks(self):
        if not self.habits:
            messagebox.showinfo("No Habits", "There are no habits to show.")
            return

        missing_streaks_dialog = tk.Toplevel(self)
        missing_streaks_dialog.title("Missing Check-offs")
        missing_streaks_dialog.geometry("300x200")

        for habit, data in self.habits.items():
            completed_dates = data['completed_dates']
            periodicity = data['periodicity']
            streak_break_count = 0

            if not completed_dates:
                missing_checkoff_label = tk.Label(missing_streaks_dialog, text=f"Missing check-off: {habit}")
                missing_checkoff_label.pack()

            else:
                last_completed_date = datetime.datetime.strptime(completed_dates[-1], '%Y-%m-%d').date()
                while last_completed_date < datetime.date.today():
                    next_due_date = last_completed_date + datetime.timedelta(days=periodicity)
                    if next_due_date <= datetime.date.today():
                        streak_break_count += 1
                        last_completed_date = next_due_date
                    else:
                        break

                if streak_break_count > 0:
                    broken_streak_label = tk.Label(missing_streaks_dialog, text=f"Broken streak for {habit} ({streak_break_count} times).")
                    broken_streak_label.pack()
                    
                    
 



                   
            