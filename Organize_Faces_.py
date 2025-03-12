import os
import shutil

# Path to the specific folder (D:\My files)
base_dir = r"D:\"  # Use raw string or double backslashes for Windows paths

# Define the file types and their corresponding folder names
file_types = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'pdfs': ['.pdf'],
    'text_files': ['.txt', '.docx', '.doc', '.rtf'],
    'videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'audios': ['.mp3', '.wav', '.flac'],
    'spreadsheets': ['.xls', '.xlsx', '.csv'],
    'archives': ['.zip', '.rar', '.tar', '.gz']
}

# Function to organize files
def organize_files(base_dir):
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()  # Get file extension
            
            # Check each file type category
            for folder, extensions in file_types.items():
                if file_ext in extensions:
                    folder_path = os.path.join(base_dir, folder)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)  # Create the folder if it doesn't exist
                    
                    # Move the file to the respective folder
                    try:
                        shutil.move(file_path, os.path.join(folder_path, file))
                        print(f"Moved {file} to {folder_path}")
                    except Exception as e:
                        print(f"Error moving {file}: {e}")
                    break  # No need to check other file types once we've found the correct folder

# Run the function
if __name__ == "__main__":
    organize_files(base_dir)
