import os
import cv2
import numpy as np
from PIL import Image

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)

        if detector.empty():
            text_to_speech("Error: Haar cascade file not found!")
            return

        faces, Ids = getImagesAndLabels(trainimage_path)
        if not faces or not Ids:
            text_to_speech("Error: No images found for training.")
            return

        recognizer.train(faces, np.array(Ids))
        recognizer.save(trainimagelabel_path)
        res = "Image trained successfully."
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        text_to_speech(f"Error: {str(e)}")

def getImagesAndLabels(path):
    faces = []
    Ids = []

    try:
        # Get all subdirectories in the TrainingImage folder
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".jpg"):
                    imagePath = os.path.join(root, file)
                    pilImage = Image.open(imagePath).convert("L")
                    imageNp = np.array(pilImage, "uint8")
                    Id = int(os.path.split(imagePath)[-1].split("_")[1])
                    faces.append(imageNp)
                    Ids.append(Id)
    except Exception as e:
        print(f"Error loading images: {str(e)}")

    return faces, Ids