import os
import time
import sys
import platform
from pathlib import Path
from datetime import datetime

# Function to check if folder exists
def check_folder():
    # Get the current user's Desktop path (OneDrive Desktop)
    if platform.system() == "Windows":
        # Check OneDrive Desktop path
        desktop_path = str(Path.home() / "OneDrive" / "Desktop")
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        desktop_path = str(Path.home() / "Desktop")  # Assumes standard Desktop folder location
    else:
        raise Exception("Unsupported OS")

    # Folder path for 'itsmekopil' on the Desktop
    folder_path = Path(desktop_path) / "itsmekopil"
    
    # Debugging print to see the exact folder path
    print(f"Checking for folder at: {folder_path}")

    # Using pathlib to check if folder exists
    folder_exists = folder_path.is_dir()

    # Print additional info for debugging
    if folder_exists:
        print(f"The folder '{folder_path}' exists and is a valid directory.")
        # Log the time when the folder is found
        log_time(folder_path)
    else:
        print(f"Folder '{folder_path}' does not exist or is not a valid directory.")
    
    return folder_exists

# Function to log the folder found event with timestamp
def log_time(folder_path):
    # Get the current time and format it as a string
    folder_found_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Define the log folder and log file path (inside Documents\Shutdown_Logs)
    log_folder = Path.home() / "OneDrive" / "Documents" / "Shutdown_Logs"
    
    # Make sure the log folder exists, create it if it doesn't
    log_folder.mkdir(parents=True, exist_ok=True)

    # Log file path
    log_file_path = log_folder / "folder_check_log.txt"

    # Get the script start time from the global variable
    global script_start_time, script_start_time_str
    elapsed_time = time.time() - script_start_time
    elapsed_time_str = format_elapsed_time(elapsed_time)

    # Log entry for folder found event
    with open(log_file_path, "a") as log_file:
        log_file.write(f"Script started at: {script_start_time_str}\n")
        log_file.write(f"Folder '{folder_path}' found at {folder_found_time}\n")
        log_file.write(f"Elapsed time: {elapsed_time_str}\n\n")

    # Print the log message to the console (optional)
    print(f"Content found. Exiting Now. Log saved at: {log_file_path}")

# Function to format the elapsed time
def format_elapsed_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)} minutes, {int(seconds)} seconds"

# Function to shut down the computer
def shutdown():
    # Depending on the platform (Windows, Linux, or macOS), the shutdown command varies
    if platform.system() == "Windows":
        os.system("shutdown /s /f /t 1")  # Shutdown immediately
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        os.system("shutdown -h now")  # Shutdown immediately
    else:
        print("Unsupported OS for shutdown.")
        sys.exit(1)

# Main logic
def main():
    global script_start_time, script_start_time_str
    script_start_time = time.time()  # Record the start time of the script
    script_start_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format it for logging

    print("Script started. Waiting for folder 'itsmekopil' to appear on the Desktop...")

    start_time = time.time()

    while time.time() - start_time < 30:
        if check_folder():
            print("Folder 'itsmekopil' found. System will not shut down.")
            return  # Exit if the folder is found before 30 seconds
        time.sleep(1)

    print("Folder not found. Shutting down the system...")
    shutdown()

if __name__ == "__main__":
    main()
