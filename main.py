import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import shutil
import webbrowser
from datetime import datetime

# Define the status texts
status_texts = [
    "Unlocking All Tunes✅",
    "Making the trucks go free✅",
    "Making Damage Zero✅",
    "Changing Money & Rank✅"
]

class FileChangerApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x400")
        self.master.title("DerpyStudios SR File Changer")
        self.master.resizable(False, False)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Button to change save files
        self.change_button = ctk.CTkButton(self.master, text="Change Save Files", command=self.change_save_files, width=200)
        self.change_button.place(relx=0.5, rely=0.4, anchor='center')

        # Button to load backup
        self.load_backup_button = ctk.CTkButton(self.master, text="Load Backup", command=self.load_backup, width=150)
        self.load_backup_button.place(relx=0.5, rely=0.55, anchor='center')

        # Loading bar
        self.loading_bar = ctk.CTkProgressBar(self.master, mode="determinate", width=300)
        self.loading_bar.place_forget()

        # Status label
        self.status_label = ctk.CTkLabel(self.master, text="", font=("Arial", 12), text_color="red")
        self.status_label.place_forget()

        # QUIT button
        self.quit_button = ctk.CTkButton(self.master, text="QUIT", command=self.quit_app, width=100, fg_color="red")
        self.quit_button.place(relx=0.1, rely=0.9, anchor='center')  # Bottom left

        # GITHUB button
        self.github_button = ctk.CTkButton(self.master, text="GITHUB", command=self.open_github, width=100)
        self.github_button.place(relx=0.9, rely=0.9, anchor='center')  # Bottom right

    def update_loading_bar(self):
        start_time = datetime.now()

        def update():
            elapsed = (datetime.now() - start_time).total_seconds()
            progress = min(elapsed / self.duration, 1.0)
            self.loading_bar.set(progress)

            if progress < 1.0:
                self.status_label.configure(text=status_texts[int(progress * len(status_texts))])
                self.master.after(50, update)
            else:
                self.loading_bar.place_forget()
                self.status_label.configure(text="Files Changed, Enjoy!")

        update()

    def change_save_files(self):
        directory = filedialog.askdirectory(title="Select Directory Containing initial.pak")
        if not directory:
            messagebox.showwarning("Warning", "No directory selected. Exiting.")
            return

        file_path = os.path.join(directory, 'initial.pak')
        if not os.path.isfile(file_path):
            messagebox.showerror("Error", "initial.pak not found in the selected directory.")
            return

        backup_dir = os.path.join(os.path.dirname(__file__), 'backup')
        os.makedirs(backup_dir, exist_ok=True)

        backup_file = os.path.join(backup_dir, 'initial.pak')
        shutil.copy(file_path, backup_file)

        xml_pak_file = os.path.join('XML', 'initial.pak')
        if os.path.isfile(xml_pak_file):
            shutil.copy(xml_pak_file, file_path)
            self.duration = random.uniform(5, 13)
            self.loading_bar.place(relx=0.5, rely=0.9, anchor='center')
            self.status_label.place(relx=0.5, rely=0.95, anchor='center')
            self.update_loading_bar()
            messagebox.showinfo("Success", "File replaced and backup created.")
        else:
            messagebox.showerror("Error", "Replacement file not found in 'XML' folder.")

    def load_backup(self):
        backup_file = os.path.join(os.path.dirname(__file__), 'backup', 'initial.pak')
        if not os.path.isfile(backup_file):
            messagebox.showerror("Error", "No backup file found.")
            return

        restore_dir = filedialog.askdirectory(title="Select Directory to Restore initial.pak")
        if not restore_dir:
            messagebox.showwarning("Warning", "No directory selected.")
            return
        
        original_file = os.path.join(restore_dir, 'initial.pak')
        shutil.copy(backup_file, original_file)
        messagebox.showinfo("Success", "Backup restored successfully.")

    def quit_app(self):
        self.master.quit()  # self destroy lol 

    def open_github(self):
        webbrowser.open("https://github.com/Pokieiscool/Snowrunner-Editor")  # opens github 

if __name__ == "__main__":
    app = ctk.CTk()
    file_changer_app = FileChangerApp(app)
    app.mainloop()
