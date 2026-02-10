import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import shutil

try:
    from metadata_remover import remove_metadata
    METADATA_REMOVAL_AVAILABLE = True
except ImportError:
    METADATA_REMOVAL_AVAILABLE = False
    print("Warning: metadata_remover.py not found. Metadata removal will not work.")


class MetadataWiperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MDWipe")
        self.root.geometry("500x400")
        self.root.attributes('-fullscreen', False)
        self.root.resizable(False, False)
        
        self.setup_windows_theme()
        
        self.selected_files = []
        
        self.create_main_screen()
    
    def setup_windows_theme(self):
        try:
            import sys
            
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
                icon_path = os.path.join(base_path, 'MDWipe.ico')
            else:
                icon_path = 'MDWipe.ico'
            
            if os.path.exists(icon_path):
                self.root.iconbitmap(default=icon_path)
            elif os.path.exists('MDWipe.ico'):
                self.root.iconbitmap(default='MDWipe.ico')
        except Exception as e:
            pass
        
        try:
            style = ttk.Style()
            available_themes = style.theme_names()
            if 'vista' in available_themes:
                style.theme_use('vista')
            elif 'winnative' in available_themes:
                style.theme_use('winnative')
            elif 'xpnative' in available_themes:
                style.theme_use('xpnative')
        except:
            pass
    
    def create_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        title_label = ttk.Label(
            main_frame,
            text="Metadata Wiper",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=(0, 5))
        
        desc_label = ttk.Label(
            main_frame,
            text="Locally remove metadata from images, PDFs, and media files without spending a dime.",
            font=("Segoe UI", 9)
        )
        desc_label.pack(pady=(0, 20))
        
        select_btn = ttk.Button(
            main_frame,
            text="Select files...",
            command=self.select_files,
            width=20
        )
        select_btn.pack(pady=(0, 10))
        
        list_frame = ttk.LabelFrame(main_frame, text="Selected Files", padding="5")
        list_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")
        
        self.file_listbox = tk.Listbox(
            list_container,
            yscrollcommand=scrollbar.set,
            height=8
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.bind('<Double-Button-1>', lambda e: self.remove_selected_file())
        self.file_listbox.bind('<Delete>', lambda e: self.remove_selected_file())
        
        remove_btn = ttk.Button(
            list_frame,
            text="Remove selected files...",
            command=self.remove_selected_file,
            width=30
        )
        remove_btn.pack(pady=(5, 0))
        
        wipe_btn = ttk.Button(
            main_frame,
            text="Wipe metadata",
            command=self.wipe_metadata,
            width=20
        )
        wipe_btn.pack(pady=(10, 0))
    
    def select_files(self):
        filetypes = (
            ("All supported files", "*.jpg *.jpeg *.png *.gif *.pdf *.mp3 *.mp4 *.heic"),
            ("Images", "*.jpg *.jpeg *.png *.gif *.heic"),
            ("PDFs", "*.pdf"),
            ("Audio/Video", "*.mp3 *.mp4"),
            ("All files", "*.*")
        )
        
        files = filedialog.askopenfilenames(
            title="Select files to clean",
            filetypes=filetypes
        )
        
        if files:
            self.selected_files = list(files)
            self.update_file_list()
    
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            filename = os.path.basename(file_path)
            self.file_listbox.insert(tk.END, filename)
    
    def remove_selected_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_files.pop(index)
            self.update_file_list()
    
    def wipe_metadata(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return
        
        if not METADATA_REMOVAL_AVAILABLE:
            messagebox.showerror("Error", "metadata_remover.py not found. Please ensure it's in the same folder.")
            return
        
        self.create_processing_screen()
    
    def create_processing_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        self.status_label = ttk.Label(
            main_frame,
            text="Processing files...",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(
            main_frame,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(pady=(0, 10))
        
        log_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        log_frame.pack(fill="both", expand=True, pady=(0, 10))

        log_container = ttk.Frame(log_frame)
        log_container.pack(fill="both", expand=True)
        
        log_scroll = ttk.Scrollbar(log_container)
        log_scroll.pack(side="right", fill="y")
        
        self.log_text = tk.Text(
            log_container,
            height=10,
            width=50,
            yscrollcommand=log_scroll.set,
            wrap="word"
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        self.root.after(100, lambda: self.process_files())
    
    def process_files(self):
        total_files = len(self.selected_files)
        successful = 0
        failed = 0
        
        for i, file_path in enumerate(self.selected_files):
            filename = os.path.basename(file_path)
            file_dir = os.path.dirname(file_path)
            base_name = Path(filename).stem
            extension = Path(filename).suffix
            
            progress = ((i + 1) / total_files) * 100
            self.progress_bar['value'] = progress
            self.status_label.config(text=f"Processing {i + 1} of {total_files}: {filename}")
            
            try:
                original_backup = os.path.join(file_dir, f"{base_name}_original{extension}")
                
                counter = 1
                while os.path.exists(original_backup):
                    original_backup = os.path.join(file_dir, f"{base_name}_original_{counter}{extension}")
                    counter += 1
                
                os.rename(file_path, original_backup)
                
                success = remove_metadata(original_backup, file_path)
                
                if success:
                    self.log_text.insert(tk.END, f"{filename} - cleaned (original saved as {os.path.basename(original_backup)})\n")
                    successful += 1
                else:
                    os.rename(original_backup, file_path)
                    self.log_text.insert(tk.END, f"{filename} - ERROR (original restored)\n")
                    failed += 1
                    
            except Exception as e:
                self.log_text.insert(tk.END, f"{filename} - ERROR: {str(e)}\n")
                failed += 1

                try:
                    if os.path.exists(original_backup):
                        os.rename(original_backup, file_path)
                except:
                    pass
            
            self.log_text.see(tk.END)
            self.root.update()
        
        self.create_completion_screen(successful, failed)
    
    def create_completion_screen(self, successful=0, failed=0):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        success_label = ttk.Label(
            main_frame,
            text="Process Complete!",
            font=("Segoe UI", 14, "bold")
        )
        success_label.pack(pady=(20, 10))
        
        message = f"{successful} files cleaned successfully"
        if failed > 0:
            message += f"\n{failed} files failed"
        message += "\n\nOriginal files saved with '_original' suffix"
        
        msg_label = ttk.Label(
            main_frame,
            text=message,
            font=("Segoe UI", 9),
            justify="center"
        )
        msg_label.pack(pady=(0, 20))
        
        wipe_more_btn = ttk.Button(
            main_frame,
            text="Wipe more files",
            command=self.create_main_screen,
            width=15
        )
        wipe_more_btn.pack()


def main():
    root = tk.Tk()
    app = MetadataWiperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()