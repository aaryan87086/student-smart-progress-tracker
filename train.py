import face_recognition
import os
import pickle

known_faces = []
known_names = []

path = "C:\VSCODE\student-smart-progress-tracker\images"

for file in os.listdir(path):
    img_path = os.path.join(path,file)

    image = face_recognition.load_image_file(img_path)

    encodings = face_recognition.face_encodings(image)

    if len(encodings) > 0:
        known_faces.append(encodings[0])

        known_names.append(os.path.splitext(file)[0])


data = {
    "faces": known_faces,
    "names": known_names
}

with open("face_data.pkl", "wb") as f:
    pickle.dump(data,f)

print("Training Complete")