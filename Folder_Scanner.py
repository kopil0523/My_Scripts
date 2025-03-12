import os
import shutil
import logging

# Define directories to avoid (like system files, temp, etc.)
SYSTEM_DIRECTORIES = [
    "Program Files", "Program Files (x86)", "Windows", "AppData", "System32",
    "Temp", "Microsoft", "ProgramData", "Documents and Settings", "C:\\$Recycle.Bin"
]

# Define output base directory where files will be categorized
output_base_dir = os.getcwd()

# Define file type categories
file_categories = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.flv'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Other': []  # For any other files that don't match the categories
}

# Create logging for tracking
logging.basicConfig(filename="file_organizer.log", level=logging.INFO)

# Function to check if a directory is a system directory
def is_system_directory(path):
    for sys_dir in SYSTEM_DIRECTORIES:
        if sys_dir.lower() in path.lower():
            return True
    return False

# Function to categorize and move files
def categorize_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        # Skip system directories
        if is_system_directory(root):
            continue

        # Process each file in the current directory
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()

            # Determine the category of the file based on its extension
            file_moved = False
            for category, extensions in file_categories.items():
                if file_ext in extensions:
                    # Create output directory if it doesn't exist
                    category_folder = os.path.join(output_base_dir, category)
                    os.makedirs(category_folder, exist_ok=True)

                    # Define destination path for the file
                    dest_path = os.path.join(category_folder, file)
                    source_path = os.path.join(root, file)

                    # Move the file to the respective folder
                    try:
                        shutil.move(source_path, dest_path)
                        logging.info(f"Moved {file} from {root} to {category_folder}")
                        print(f"Moved {file} to {category_folder}")
                        file_moved = True
                        break
                    except Exception as e:
                        logging.error(f"Error moving {file}: {e}")
                        print(f"Error moving {file}: {e}")

            # If the file doesn't match any category, move it to 'Other'
            if not file_moved and file_ext:
                other_folder = os.path.join(output_base_dir, 'Other')
                os.makedirs(other_folder, exist_ok=True)
                dest_path = os.path.join(other_folder, file)
                source_path = os.path.join(root, file)

                try:
                    shutil.move(source_path, dest_path)
                    logging.info(f"Moved {file} from {root} to {other_folder}")
                    print(f"Moved {file} to {other_folder}")
                except Exception as e:
                    logging.error(f"Error moving {file}: {e}")
                    print(f"Error moving {file}: {e}")

# Main function to start the file categorization
if __name__ == "__main__":
    # Start from the root of the D: drive
    categorize_files(output_base_dir)  # Modify this to your desired directory path
