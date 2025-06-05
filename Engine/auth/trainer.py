import cv2
import numpy as np
from PIL import Image  #---------------- Pillow package ----------------#
import os

#---------------- Path for samples already taken ----------------#
path = "Savi\\Engine\\auth\\samples"

#---------------- Local Binary Patterns Histograms ----------------#
recognizer = cv2.face.LBPHFaceRecognizer_create()

#---------------- Haar Cascade classifier is an effective object detection approach ----------------#
detector = cv2.CascadeClassifier(
    'Savi\\Engine\\auth\\haarcascade_frontalface_default.xml'
)

def Images_And_Labels(path):  #---------------- Function to fetch the images and labels ----------------#
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:  #---------------- To iterate particular image path ----------------#
        gray_img = Image.open(imagePath).convert('L')  #---------------- Convert it to grayscale ----------------#
        img_arr = np.array(gray_img, 'uint8')  #---------------- Creating an array of the image ----------------#

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x, y, w, h) in faces:
            faceSamples.append(img_arr[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait ...")

faces, ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

#---------------- Ensure the directory for saving the trained model exists ----------------#
output_dir = "Savi\\Engine\\auth\\trainer"
os.makedirs(output_dir, exist_ok=True)

#---------------- Save the trained model as trainer.yml ----------------#
output_file = os.path.join(output_dir, "trainer.yml")
recognizer.write(output_file)

print("Model trained, Now we can recognize your face.")