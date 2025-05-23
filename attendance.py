import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3
import threading
import queue

# Project modules
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Initialize text-to-speech engine
def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# Paths
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# Create necessary directories if they don't exist
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)
if not os.path.exists("TrainingImageLabel"):
    os.makedirs("TrainingImageLabel")
if not os.path.exists("StudentDetails"):
    os.makedirs("StudentDetails")
if not os.path.exists(attendance_path):
    os.makedirs(attendance_path)

# Create a queue for thread-safe communication
message_queue = queue.Queue()

# Main application window
window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
window.configure(background="#1c1c1c")  # Dark theme

# Function to destroy error screen
def del_sc1():
    sc1.destroy()

# Error message for missing enrollment and name
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

# Validation for enrollment number
def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Title
titl = tk.Label(
    window, text="BIG STEPS", bg="#1c1c1c", fg="yellow", font=("Verdana", 27, "bold")
)
titl.pack(pady=20)

# Center frame for buttons
center_frame = Frame(window, bg="#1c1c1c")
center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Function to process messages from the queue
def process_queue():
    try:
        while True:
            # Get the latest message from the queue
            msg_type, msg = message_queue.get_nowait()
            if msg_type == "success":
                message.configure(text=msg)
                text_to_speech(msg)
            elif msg_type == "error":
                message.configure(text=msg)
                text_to_speech(msg)
    except queue.Empty:
        # No more messages in the queue
        pass

    # Check the queue again after 100ms
    window.after(100, process_queue)

# Function to take images
def take_image(txt1, txt2):
    l1 = txt1.get()
    l2 = txt2.get()
    threading.Thread(
        target=takeImage.TakeImage,
        args=(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech, message_queue),
    ).start()
    txt1.delete(0, "end")
    txt2.delete(0, "end")

    # Check the queue periodically for updates
    window.after(100, process_queue)

# Buttons
def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#1c1c1c", fg="green", font=("Verdana", 30, "bold"),
    )
    titl.place(x=270, y=12)

    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",
        fg="yellow",
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(x=280, y=75)

    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    global message
    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 14, "bold"),
    )
    message.place(x=250, y=270)

    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=lambda: take_image(txt1, txt2),  # Pass txt1 and txt2 as arguments
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)

# Register button
r = tk.Button(
    center_frame,
    text="Register a new student",
    command=TakeImageUI,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=20,
)
r.pack(pady=10)

# Take Attendance button
def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)

r = tk.Button(
    center_frame,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=20,
)
r.pack(pady=10)

# View Attendance button
def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

r = tk.Button(
    center_frame,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=20,
)
r.pack(pady=10)

# Exit button
r = tk.Button(
    center_frame,
    text="EXIT",
    bd=10,
    command=window.quit,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=20,
)
r.pack(pady=10)

window.mainloop()