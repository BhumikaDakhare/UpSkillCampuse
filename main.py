import customtkinter as ctk
from tkinter import filedialog, messagebox
from organizer.engine import organize_directory, undo_changes

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python File Organizer")
        self.root.geometry("600x500")
        
        self.root.grid_columnconfigure(0, weight=1)
        self.selected_path = None
        self.move_history = []

        # UI Elements
        self.title_label = ctk.CTkLabel(root, text="File Organizer", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=0, column=0, pady=20)

        self.path_label = ctk.CTkLabel(root, text="No folder selected", text_color="gray")
        self.path_label.grid(row=1, column=0, pady=5)

        self.select_btn = ctk.CTkButton(root, text="Select Folder", command=self.select_folder)
        self.select_btn.grid(row=2, column=0, pady=10)

        self.recursive_var = ctk.BooleanVar()
        self.recursive_check = ctk.CTkCheckBox(root, text="Include Subfolders", variable=self.recursive_var)
        self.recursive_check.grid(row=3, column=0, pady=5)

        # Progress Bar (New - Week 2/4 Requirement)
        self.progress_bar = ctk.CTkProgressBar(root, width=400)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, pady=20)

        self.organize_btn = ctk.CTkButton(root, text="Organize Files", command=self.organize, state="disabled", fg_color="#2CC985")
        self.organize_btn.grid(row=5, column=0, pady=10)

        self.reset_btn = ctk.CTkButton(root, text="Undo Changes", command=self.undo, state="disabled", fg_color="#E53935")
        self.reset_btn.grid(row=6, column=0, pady=10)

        self.status_label = ctk.CTkLabel(root, text="Ready", font=("Roboto", 12))
        self.status_label.grid(row=7, column=0, pady=10)

    def update_progress(self, value):
        self.progress_bar.set(value)
        self.root.update_idletasks() # Ensures GUI doesn't freeze 

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_path = path
            self.path_label.configure(text=f"📂 {path}")
            self.organize_btn.configure(state="normal")
            self.progress_bar.set(0)

    def organize(self):
        if not self.selected_path: return
        self.status_label.configure(text="Organizing...", text_color="orange")
        
        # Pass the progress callback to the engine 
        self.move_history = organize_directory(
            self.selected_path, 
            recursive=self.recursive_var.get(),
            progress_callback=self.update_progress
        )
        
        if self.move_history:
            self.status_label.configure(text=f"Done! Moved {len(self.move_history)} files.", text_color="green")
            self.reset_btn.configure(state="normal")
        else:
            self.status_label.configure(text="No files moved.")

    def undo(self):
        if messagebox.askyesno("Undo", "Revert all file movements?"):
            restored, failed = undo_changes(self.move_history)
            self.status_label.configure(text=f"Undo Complete: {restored} restored.")
            self.reset_btn.configure(state="disabled")
            self.progress_bar.set(0)

if __name__ == "__main__":
    root = ctk.CTk()
    app = FileOrganizerApp(root)
    root.mainloop()