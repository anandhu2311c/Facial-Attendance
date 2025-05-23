
# Facial Recognition Attendance System using Tkinter

A simple GUI-based automatic attendance system using facial recognition powered by OpenCV and Tkinter.

---

## 🔧 Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/anandhu2311c/Facial-Attendance.git
   cd Facial-Attendance


2. **Install Dependencies**
   Make sure you have Python installed. Then, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the Environment**

   * Create a folder named `TrainingImage` inside the project directory.
   * Update all hardcoded file paths in `attendance.py` and `automaticAttedance.py` to match your system's path.

4. **Run the Application**

   ```bash
   python attendance.py
   ```

---

## 📌 Project Workflow & Features

### 👤 1. Register New Student

* Click **"Register New Student"**
* Enter Student ID and Name
* Click **"Take Image"**
* Webcam will open and capture 50 images (you can modify the count in code)
* Images are saved in the `TrainingImage/` folder

### 🧠 2. Train the Model

* Click **"Train Image"**
* Converts images into numeric data using OpenCV
* Prepares the model for face recognition

### 🎓 3. Automatic Attendance

* Click **"Automatic Attendance"**
* Enter the subject name
* System captures face from webcam and marks attendance using the trained model
* Attendance is saved in CSV format (one per subject)

### 📊 4. View Attendance

* Click **"View Attendance"**
* Opens a window showing attendance records in tabular format

---

## 📷 Screenshots

### 🏠 Home Page

![Home Page](https://github.com/anandhu2311c/Facial-Attendance/blob/177a91348a3c74ad07a1689232ce04f620e6589a/Project%20Snap/1.png)

### 📝 Register Your Face

![Register Face](https://github.com/anandhu2311c/Facial-Attendance/blob/177a91348a3c74ad07a1689232ce04f620e6589a/Project%20Snap/2.png)

### 📸 Capturing 50 Images for Training

![Training Images](https://github.com/anandhu2311c/Facial-Attendance/blob/177a91348a3c74ad07a1689232ce04f620e6589a/Project%20Snap/3.png)

### 🤖 Filling Attendance Using Face Recognition

![Filling Attendance](https://github.com/anandhu2311c/Facial-Attendance/blob/177a91348a3c74ad07a1689232ce04f620e6589a/Project%20Snap/4.png)

### 📄 Attendance Records View

![Attendance Records](https://github.com/anandhu2311c/Facial-Attendance/blob/177a91348a3c74ad07a1689232ce04f620e6589a/Project%20Snap/5.png)

---

## 📁 Project Structure

```
Facial-Attendance/
│
├── attendance.py              # Main GUI application
├── automaticAttedance.py      # Script for face recognition-based attendance
├── trainImage.py              # Training the model with captured images
├── takeImage.py               # Image capture for new students
├── show_attendance.py         # Display attendance records
├── requirements.txt           # Python dependencies
├── haarcascade_frontalface_*.xml # Face detection classifiers
├── TrainingImage/             # Folder to store captured images
├── StudentDetails/            # Contains CSVs of student info and attendance
├── Project Snap/              # Screenshots of UI (for documentation)
└── README.md
```

---

## 💡 Notes

* Make sure your webcam is enabled and accessible.
* The more images you provide during registration, the better the accuracy.
* Each attendance session is saved separately per subject.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## ✨ Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

````


