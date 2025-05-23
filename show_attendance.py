import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
import csv

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if not Subject:
            text_to_speech("Please enter the subject name.")
            return

        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
        if not filenames:
            text_to_speech(f"No attendance records found for {Subject}.")
            return

        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)

        # Calculate attendance percentage
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            attendance_percentage = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
            newdf.at[newdf.index[i], "Attendance"] = attendance_percentage

        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        # Display attendance in a new window
        root = tk.Tk()
        root.title(f"Attendance of {Subject}")
        root.configure(background="black")

        with open(f"Attendance\\{Subject}\\attendance.csv") as file:
            reader = csv.reader(file)
            for r, col in enumerate(reader):
                for c, row in enumerate(col):
                    label = tk.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, "bold"),
                        bg="black",
                        text=row,
                        relief=tk.RIDGE,
                    )
                    label.grid(row=r, column=c)

        root.mainloop()

    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=tk.RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    global tx
    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=tk.RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=tk.RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()