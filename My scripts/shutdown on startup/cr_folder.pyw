import os
import time
import shutil

# Define the desktop path and folder name
desktop_path = r"C:\Users\kopil\OneDrive\Desktop"
folder_name = "itsmekopil"
folder_path = os.path.join(desktop_path, folder_name)

# Create the folder
os.makedirs(folder_path, exist_ok=True)
print(f"Folder created at: {folder_path}")

# Wait for 10 seconds
time.sleep(10)

# Delete the folder
shutil.rmtree(folder_path)
print(f"Folder deleted at: {folder_path}")

# Close the script
print("Script closed.")
