import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import random
import shutil
import os
from PIL import Image, ImageTk
import json

# Define the status texts
status_texts = [
    "Unlocking All Tunes✅",
    "Making the trucks go free✅",
    "Making Damage Zero✅",
    "Changing Money & Rank✅"
]

# Initialize duration and status index variables
duration = 0
status_index = 0

# Function to update the loading bar and status text
def update_loading_bar():
    global duration, status_index
    start_time = datetime.now()
    
    def update():
        elapsed = (datetime.now() - start_time).total_seconds()
        progress = min(elapsed / duration, 1.0)
        loading_bar.set(progress)
        
        # Update status text based on progress
        if progress < 1.0:
            status_index = int(progress * 4)  # 4 statuses
            if status_index < len(status_texts):
                status_label.configure(text=status_texts[status_index])
        else:
            # Loading complete
            loading_bar.place_forget()  # Hide the loading bar
            status_label.configure(text="Files Changed, Enjoy!")
            print("Loading complete!")

        if progress < 1.0:
            app.after(50, update)  # Update every 50ms

    update()

# Function that will be called when the main button is clicked
def change_save_files():
    global duration, status_index
    print("Change Save Files button clicked")

    # Ask for the directory containing initial.pak
    directory = filedialog.askdirectory(
        title="Select Directory Containing initial.pak"
    )
    
    if not directory:
        messagebox.showwarning("Warning", "No directory selected. Exiting.")
        return

    # Check for the initial.pak file in the selected directory
    file_path = os.path.join(directory, 'initial.pak')
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", "initial.pak not found in the selected directory.")
        return
    
    # Define backup and replacement paths
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory where the script is located
    backup_dir = os.path.join(script_dir, 'backup')
    backup_file = os.path.join(backup_dir, 'initial.pak')
    xml_pak_file = os.path.join('XML', 'initial.pak')
    
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Make a backup of the original file
    shutil.copy(file_path, backup_file)
    
    # Replace the initial.pak file with the one in the XML folder
    if os.path.isfile(xml_pak_file):
        shutil.copy(xml_pak_file, file_path)
        # Start the loading bar and status text
        duration = random.uniform(5, 13)  # Random duration between 5 and 13 seconds
        loading_bar.place(relx=0.5, rely=0.9, anchor='center')  # Show the loading bar at the bottom
        status_label.place(relx=0.5, rely=0.95, anchor='center')  # Show the status text below the loading bar
        update_loading_bar()  # Start updating the loading bar and status text
        messagebox.showinfo("Success", "File replaced and backup created.")
    else:
        messagebox.showerror("Error", "Replacement file not found in 'XML' folder.")

# Function that will be called when the smaller button is clicked
def load_backup():
    print("Load Backup button clicked")
    
    # Define paths for backup and original file
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory where the script is located
    backup_dir = os.path.join(script_dir, 'backup')
    backup_file = os.path.join(backup_dir, 'initial.pak')
    original_file = os.path.join(filedialog.askdirectory(title="Select Directory to Restore initial.pak"), 'initial.pak')
    
    if not os.path.isfile(backup_file):
        messagebox.showerror("Error", "No backup file found.")
        return

    if not os.path.isfile(original_file):
        messagebox.showerror("Error", "Target location does not contain initial.pak.")
        return

    # Restore the backup to the original location
    shutil.copy(backup_file, original_file)
    messagebox.showinfo("Success", "Backup restored successfully.")

# Function to toggle between light and dark mode
def toggle_mode():
    global is_dark_mode
    if is_dark_mode:
        ctk.set_appearance_mode("Light")
        is_dark_mode = False
    else:
        ctk.set_appearance_mode("Dark")
        is_dark_mode = True

# Setup the main application window with your default settings
app = ctk.CTk()
app.geometry("700x400")  # Set the size of the window
app.title("DerpyStudios SR File Changer")  # Set the window title
app.resizable(False, False)  # Make the window non-resizable

# Initialize the mode tracker
is_dark_mode = False  # Start in light mode by default

# Create the main button in the center of the window
change_button = ctk.CTkButton(app, text="Change Save Files", command=change_save_files, width=200)
change_button.place(relx=0.5, rely=0.4, anchor='center')  # Position the main button

# Create the smaller button below the main button
load_backup_button = ctk.CTkButton(app, text="Load Backup", command=load_backup, width=150)
load_backup_button.place(relx=0.5, rely=0.55, anchor='center')  # Position the smaller button

# Create a switch in the top right corner to toggle between light and dark mode
mode_switch = ctk.CTkSwitch(app, text="Light/Dark Mode", command=toggle_mode)
mode_switch.place(relx=0.9, rely=0.1, anchor='center')  # Position the switch in the top right

# Create a loading bar
loading_bar = ctk.CTkProgressBar(app, mode="determinate", width=300)
loading_bar.place_forget()  # Hide the loading bar initially

# Create a label to show the status text
status_label = ctk.CTkLabel(app, text="", font=("Arial", 12), text_color="red")
status_label.place_forget()  # Hide the status label initially

app.mainloop()
