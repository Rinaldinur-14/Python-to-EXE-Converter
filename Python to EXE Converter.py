import os
import sys
import re
import shutil
import tempfile
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
from PIL import Image  # Pillow library for image conversion

class PyToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Python to EXE Converter")
        self.root.geometry("800x600")  # Default size
        self.root.minsize(600, 450)  # Minimum size
        self.root.configure(bg="#F5F5F5")  # Light gray background
        self.apply_modern_theme()  # Apply modern theme
        self.setup_ui()
        self.processing = False

        # Make the UI responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def apply_modern_theme(self):
        # Define modern theme colors
        self.bg_color = "#F5F5F5"  # Light gray
        self.fg_color = "#333333"  # Dark gray
        self.entry_bg = "#FFFFFF"  # White
        self.entry_fg = "#333333"  # Dark gray
        self.button_bg = "#800000"  # Maroon
        self.button_fg = "#FFFFFF"  # White
        self.progress_color = "#800000"  # Maroon
        self.accent_color = "#A52A2A"  # Brown for accents

        # Apply theme to root window
        self.root.configure(bg=self.bg_color)

    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)  # Make the second column expandable

        # Title label
        title_label = ttk.Label(
            main_frame,
            text="Python to EXE Converter",
            font=("Helvetica", 24, "bold"),
            foreground=self.bg_color,  # Maroon for title
            background=self.button_bg,
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="")

        # Python file upload
        ttk.Label(
            main_frame,
            text="Python File (.py):",
            background=self.bg_color,
            foreground=self.fg_color,
            font=("Helvetica", 10),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_py_file = ttk.Entry(main_frame, width=40, font=("Helvetica", 10))
        self.entry_py_file.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(
            main_frame,
            text="Browse",
            command=self.browse_py_file,
            style="Modern.TButton",
        ).grid(row=1, column=2, padx=5, pady=5)

        # Output EXE name
        ttk.Label(
            main_frame,
            text="Output EXE Name:",
            background=self.bg_color,
            foreground=self.fg_color,
            font=("Helvetica", 10),
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_output = ttk.Entry(main_frame, width=40, font=("Helvetica", 10))
        self.entry_output.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        # Icon selection
        ttk.Label(
            main_frame,
            text="Icon (optional, PNG/JPG/SVG/ICO):",
            background=self.bg_color,
            foreground=self.fg_color,
            font=("Helvetica", 10),
        ).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_icon = ttk.Entry(main_frame, width=40, font=("Helvetica", 10))
        self.entry_icon.grid(row=3, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(
            main_frame,
            text="Browse",
            command=self.browse_icon,
            style="Modern.TButton",
        ).grid(row=3, column=2, padx=5, pady=5)

        # Output Directory
        ttk.Label(
            main_frame,
            text="Output Directory:",
            background=self.bg_color,
            foreground=self.fg_color,
            font=("Helvetica", 10),
        ).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_output_dir = ttk.Entry(main_frame, width=40, font=("Helvetica", 10))
        self.entry_output_dir.grid(row=4, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(
            main_frame,
            text="Browse",
            command=self.browse_output_dir,
            style="Modern.TButton",
        ).grid(row=4, column=2, padx=5, pady=5)

        # Options
        options_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        options_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="w")
        
        self.uac_admin_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Require Admin Privileges",
            variable=self.uac_admin_var,
            style="Modern.TCheckbutton",
        ).pack(side=tk.LEFT, padx=5)

        self.open_folder_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Open Output Folder",
            variable=self.open_folder_var,
            style="Modern.TCheckbutton",
        ).pack(side=tk.LEFT, padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            orient=tk.HORIZONTAL,
            mode="indeterminate",
            style="Modern.Horizontal.TProgressbar",
        )
        self.progress.grid(row=6, column=0, columnspan=3, pady=10, sticky="we")

        # Create button
        self.create_btn = ttk.Button(
            main_frame,
            text="Convert to EXE",
            command=self.on_submit,
            style="Modern.TButton",
        )
        self.create_btn.grid(row=7, column=0, columnspan=3, pady=20, sticky="ew")

        # Footer
        footer_frame = ttk.Frame(self.root, style="Modern.TFrame")
        footer_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        footer_frame.grid_columnconfigure(0, weight=1)
        ttk.Label(
            footer_frame,
            text="© 2025 Rinaldi Nurhardiansyah. All rights reserved.",
            font=("Helvetica", 8),
            background=self.bg_color,
            foreground=self.fg_color,
        ).pack(side=tk.BOTTOM)

        # Configure styles
        self.configure_styles()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")  # Use a theme that allows customization

        # Configure frame style
        style.configure(
            "Modern.TFrame",
            background=self.bg_color,
        )

        # Configure button style
        style.configure(
            "Modern.TButton",
            background=self.button_bg,
            foreground=self.button_fg,
            font=("Helvetica", 10, "bold"),
            padding=10,
            borderwidth=0,
            focusthickness=0,
            focuscolor=self.bg_color,
            relief="flat",
        )
        style.map(
            "Modern.TButton",
            background=[("active", self.accent_color), ("disabled", "#CCCCCC")],
        )

        # Configure checkbutton style
        style.configure(
            "Modern.TCheckbutton",
            background=self.bg_color,
            foreground=self.fg_color,
            font=("Helvetica", 10),
        )

        # Configure progressbar style
        style.configure(
            "Modern.Horizontal.TProgressbar",
            background=self.progress_color,
            thickness=20,
        )

    def browse_py_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if path:
            self.entry_py_file.delete(0, tk.END)
            self.entry_py_file.insert(0, path)

    def browse_icon(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.svg *.ico")]
        )
        if path:
            self.entry_icon.delete(0, tk.END)
            self.entry_icon.insert(0, path)

    def browse_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.entry_output_dir.delete(0, tk.END)
            self.entry_output_dir.insert(0, path)

    def validate_inputs(self, py_file, exe_name):
        invalid_chars = r'[\\/:*?"<>|]'
        
        if not py_file:
            return "Please select a Python file"
        
        if not py_file.endswith(".py"):
            return "Selected file must be a Python script (.py)"

        if not exe_name:
            return "Please enter an output EXE name"
        
        if re.search(invalid_chars, exe_name):
            return "Output name contains invalid characters"

        return None

    def convert_image_to_ico(self, image_path):
        """Convert PNG/JPG/SVG to ICO format using Pillow."""
        try:
            img = Image.open(image_path)
            ico_path = os.path.join(tempfile.gettempdir(), "temp_icon.ico")
            img.save(ico_path, format="ICO")
            return ico_path
        except Exception as e:
            print(f"Image conversion error: {str(e)}")
            return None

    def on_submit(self):
        if self.processing:
            return

        # Get and validate inputs
        py_file = self.entry_py_file.get().strip()
        exe_name = self.entry_output.get().strip()
        error = self.validate_inputs(py_file, exe_name)

        if error:
            messagebox.showwarning("Input Error", error)
            return

        # Prepare parameters
        icon_path = self.entry_icon.get().strip()
        if icon_path and not icon_path.endswith(".ico"):
            icon_path = self.convert_image_to_ico(icon_path)
            if not icon_path:
                messagebox.showwarning(
                    "Icon Error",
                    "Failed to convert image to ICO format. Using default icon."
                )
                icon_path = ""

        params = {
            "py_file": py_file,
            "exe_name": exe_name.split(".exe")[0],
            "icon_path": icon_path,
            "uac_admin": self.uac_admin_var.get(),
            "open_folder": self.open_folder_var.get(),
        }

        # Start processing in background
        self.processing = True
        self.create_btn.config(state=tk.DISABLED)
        self.progress.start()
        threading.Thread(target=self.convert_to_exe, args=(params,)).start()

    def convert_to_exe(self, params):
        try:
            # Get the output directory
            output_dir = self.entry_output_dir.get().strip()
            if not output_dir:
                output_dir = "dist"  # Default to 'dist' if no directory is specified

            # Build PyInstaller command
            cmd = [
                "pyinstaller",
                "--onefile",
                "--noconsole",
                "--name",
                params["exe_name"],
                "--distpath",
                output_dir,  # Use the custom output directory
                params["py_file"],
            ]

            if params["uac_admin"]:
                cmd.insert(1, "--uac-admin")
            
            if params["icon_path"] and os.path.exists(params["icon_path"]):
                cmd += ["--icon", params["icon_path"]]

            # Run PyInstaller
            subprocess.run(cmd, check=True, capture_output=True, text=True)

            # Show success and open folder
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Successfully created '{params['exe_name']}.exe'\n"
                f"Location: {output_dir}"
            ))
            
            if params["open_folder"] and os.path.exists(output_dir):
                os.startfile(output_dir)

        except subprocess.CalledProcessError as e:
            error_msg = f"PyInstaller Error: {e.stderr or e.stdout}"
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Unexpected error: {str(e)}"
            ))
        finally:
            # Cleanup operations
            self.cleanup_residual_files(params["exe_name"])
            self.root.after(0, self.reset_ui)

    def cleanup_residual_files(self, exe_name):
        try:
            if os.path.exists(f"{exe_name}.spec"):
                os.remove(f"{exe_name}.spec")
            if os.path.exists("build"):
                shutil.rmtree("build")
        except Exception as e:
            print(f"Cleanup error: {str(e)}")

    def reset_ui(self):
        self.progress.stop()
        self.create_btn.config(state=tk.NORMAL)
        self.processing = False

if __name__ == "__main__":
    root = tk.Tk()
    app = PyToExeConverter(root)
    root.mainloop()