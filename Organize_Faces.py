import os
import cv2
import shutil

# Path to the folder where images are stored
base_dir = r"D:\My files\images"  # Update this to the directory you want to scan

# Define the output folders
faces_folder = os.path.join(base_dir, "With_Faces")
no_faces_folder = os.path.join(base_dir, "Without_Faces")

# Ensure the output folders exist
os.makedirs(faces_folder, exist_ok=True)
os.makedirs(no_faces_folder, exist_ok=True)

# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Function to check if a photo contains a face
def contains_face(image_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    # Convert the image to grayscale (face detection works better on grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Return True if faces are detected, False otherwise
    return len(faces) > 0

# Function to organize images based on whether they contain faces
def organize_photos(base_dir):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            # Process only image files (e.g., jpg, jpeg)
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in ['.jpg', '.jpeg', '.png']:
                file_path = os.path.join(root, file)

                # Check if the image contains a face
                if contains_face(file_path):
                    target_folder = faces_folder
                else:
                    target_folder = no_faces_folder

                # Move the file to the appropriate folder
                try:
                    shutil.move(file_path, os.path.join(target_folder, file))
                    print(f"Moved {file} to {target_folder}")
                except Exception as e:
                    print(f"Error moving {file}: {e}")

# Run the function
if __name__ == "__main__":
    organize_photos(base_dir)
