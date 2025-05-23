import cv2
import os
import csv
import threading
import queue

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech, queue):
    def capture_images():
        try:
            # Create TrainingImage folder if it doesn't exist
            if not os.path.exists(trainimage_path):
                os.makedirs(trainimage_path)

            # Initialize camera
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                queue.put(("error", "Error: Camera not accessible!"))
                return

            detector = cv2.CascadeClassifier(haarcasecade_path)
            if detector.empty():
                queue.put(("error", "Error: Haar cascade file not found!"))
                return

            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = f"{Enrollment}_{Name}"
            path = os.path.join(trainimage_path, directory)

            # Create directory for the student
            if not os.path.exists(path):
                os.makedirs(path)

            while True:
                ret, img = cam.read()
                if not ret:
                    queue.put(("error", "Error: Failed to capture image."))
                    break

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum += 1
                    cv2.imwrite(
                        os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                        gray[y:y + h, x:x + w],
                    )
                    cv2.imshow("Frame", img)

                if cv2.waitKey(1) & 0xFF == ord("q") or sampleNum > 50:
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Save student details to CSV
            with open("StudentDetails/studentdetails.csv", "a+", newline="") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([Enrollment, Name])

            res = f"Images saved for ER No: {Enrollment}, Name: {Name}"
            queue.put(("success", res))

        except Exception as e:
            queue.put(("error", f"Error: {str(e)}"))

    # Start the image capture in a separate thread
    threading.Thread(target=capture_images).start()