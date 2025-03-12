import asyncio
import random
from itertools import product
import keyboard
import pygetwindow as gw
from pynput.mouse import Button, Controller
from PIL import ImageGrab
import tkinter as tk


class BlumClicker:
    def __init__(self):
        self.mouse: Controller = Controller()
        self.paused: bool = True
        self.running: bool = False

    async def click(self, x: int, y: int) -> None:
        """Click the mouse at specified coordinates."""
        self.mouse.position = (x, y)  # Remove random vertical offset for faster clicks
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)

    @staticmethod
    async def activate_window(window) -> None:
        """Activate the specified window."""
        if window:
            window.activate()
            await asyncio.sleep(1)  # Ensure activation completes

    @staticmethod
    def get_window_rect(window) -> tuple:
        """Get the rectangle area of the window."""
        return (window.left, window.top, window.width, window.height)

    @staticmethod
    def capture_screenshot(rect) -> ImageGrab.Image:
        """Capture a screenshot of the given rectangle area."""
        return ImageGrab.grab(bbox=rect)

    async def find_and_click(self, screen, rect) -> None:
        """Find and click on detected green objects while ignoring all other colors."""
        width, height = screen.size
        click_positions = []

        step_size = 10  # Check more pixels by decreasing the step size
        for x, y in product(range(0, width, step_size), range(0, height, step_size)):
            r, g, b = screen.getpixel((x, y))

            # Broaden the green color detection range
            is_green = (r > 150) and (g > 100) and (b < 100)


            if is_green:
                screen_x = rect[0] + x
                screen_y = rect[1] + y
                click_positions.append((screen_x, screen_y))  # No offset for faster clicking

        # Click all detected positions without skipping
        for pos in click_positions:
            await self.click(*pos)

    async def run(self) -> None:
        """Runs the clicker."""
        print("You have 5 seconds to switch to the game screen...")
        await asyncio.sleep(5)  # Give the user 5 seconds to switch to the game

        try:
            window_list = gw.getWindowsWithTitle("LDPlayer")

            if not window_list:
                print("Window not found!")
                return

            window = window_list[0]  # Get the first window from the list
            print(f"Initialized blum-clicker! Found window: {window.title}")

            self.running = True

            while self.running:
                if self.paused:
                    await asyncio.sleep(0.1)
                    continue

                rect = self.get_window_rect(window)

                # Limit the size of the rectangle to prevent huge screenshots
                max_width, max_height = 1920, 1080  # Example limits
                rect = (
                    rect[0],
                    rect[1],
                    min(rect[2], max_width),
                    min(rect[3], max_height)
                )

                await self.activate_window(window)

                # Check if window is active
                if not window.isActive:
                    print("Window is not active, retrying...")
                    await asyncio.sleep(1)
                    continue

                print(f"Capturing screenshot with rect: {rect}")
                screenshot = self.capture_screenshot(rect)

                await self.find_and_click(screenshot, rect)
                await asyncio.sleep(0.01)  # Decrease delay between captures for faster processing

        except Exception as error:
            print(f"An error occurred: {str(error)}")

    def start(self):
        """Start the clicker."""
        self.running = True
        self.paused = False
        asyncio.run(self.run())

    def pause(self):
        """Pause the clicker."""
        self.paused = True

    def resume(self):
        """Resume the clicker."""
        self.paused = False


def create_gui(clicker):
    """Create a simple GUI with buttons to control the clicker."""
    root = tk.Tk()
    root.title("Blum Clicker Control")

    status_label = tk.Label(root, text="Status: Stopped")
    status_label.pack(pady=10)

    def update_status():
        if clicker.running:
            status_label.config(text="Status: Running" if not clicker.paused else "Status: Paused")
        else:
            status_label.config(text="Status: Stopped")
        root.after(100, update_status)

    start_button = tk.Button(root, text="Start", command=lambda: (clicker.start(), update_status()))
    start_button.pack(pady=10)

    pause_button = tk.Button(root, text="Pause", command=lambda: (clicker.pause(), update_status()))
    pause_button.pack(pady=10)

    resume_button = tk.Button(root, text="Resume", command=lambda: (clicker.resume(), update_status()))
    resume_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: (setattr(clicker, 'running', False), root.quit()))  # Handle window closing
    update_status()  # Start updating status
    root.mainloop()


def toggle_pause(clicker):
    """Toggle pause on F6 key press."""
    if clicker.paused:
        clicker.resume()
    else:
        clicker.pause()


if __name__ == "__main__":
    clicker = BlumClicker()
    keyboard.add_hotkey('f6', lambda: toggle_pause(clicker))  # Bind F6 key to toggle pause
    create_gui(clicker)