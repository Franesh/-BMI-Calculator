import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import matplotlib.pyplot as plt


class BMICalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        self.weight_label = tk.Label(master, text="Weight (kg):")
        self.weight_label.grid(row=0, column=0, padx=10, pady=10)
        self.weight_entry = tk.Entry(master)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)

        self.height_label = tk.Label(master, text="Height (m):")
        self.height_label.grid(row=1, column=0, padx=10, pady=10)
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.save_button = tk.Button(master, text="Save Data", command=self.save_data)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.plot_button = tk.Button(master, text="Plot BMI History", command=self.plot_data)
        self.plot_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Create database connection
        self.conn = sqlite3.connect('bmi_data.db')
        self.create_table()

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive numbers.")
                return

            bmi = weight / (height ** 2)
            category = self.get_category(bmi)
            self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

    def get_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           weight REAL,
                           height REAL,
                           bmi REAL,
                           date TEXT)''')
        self.conn.commit()

    def save_data(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = weight / (height ** 2)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = self.conn.cursor()
            cursor.execute('''INSERT INTO bmi_records (weight, height, bmi, date) VALUES (?, ?, ?, ?)''',
                           (weight, height, bmi, date))
            self.conn.commit()
            messagebox.showinfo("Success", "Data saved successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

    def plot_data(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT date, bmi FROM bmi_records''')
        data = cursor.fetchall()
        dates = [row[0] for row in data]
        bmis = [row[1] for row in data]

        plt.figure(figsize=(8, 6))
        plt.plot(dates, bmis, marker='o', color='blue', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.title('BMI History')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot
        plt.show()


def main():
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
