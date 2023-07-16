import unittest
import tkinter as tk
from tkinter import messagebox
from HabitTrackerApp import HabitTrackerApp

class TestHabitTrackerApp(unittest.TestCase):
    def setUp(self):
        self.app = HabitTrackerApp()
        self.app.title("Test Habit Tracker")
        self.app.geometry("300x200")

    def test_add_habit(self):
        self.app.add_habit("test_add_habit", 7)
        self.assertIn("test_add_habit", self.app.habits)
        self.assertEqual(self.app.habits["test_add_habit"]["periodicity"], 7)       
    
    def tearDown(self):
        self.app.destroy()

if __name__ == "__main__":
    unittest.main()
