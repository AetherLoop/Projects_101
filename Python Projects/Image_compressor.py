"""
Simple Image Compressor GUI - Basic Version
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os

class SimpleImageCompressor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Image Compressor")
        self.root.geometry("600x500")
        
        # Variables
        self.input_files = []
        self.output_dir = ""
        self.quality = tk.IntVar(value=85)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Simple Image Compressor", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # File selection frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(file_frame, text="Select Images:", font=("Arial", 12, "bold")).pack()
        
        # Buttons
        button_frame = tk.Frame(file_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Select Images", 
                 command=self.select_files, width=15).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Select Folder", 
                 command=self.select_folder, width=15).pack(side="left", padx=5)
        
        # File list
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.pack(fill="x", pady=10)
        
        # Quality setting
        quality_frame = tk.Frame(self.root)
        quality_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(quality_frame, text="Quality:", font=("Arial", 12, "bold")).pack()
        
        quality_control = tk.Frame(quality_frame)
        quality_control.pack(pady=5)
        
        self.quality_slider = tk.Scale(quality_control, from_=1, to=100, 
                                      orient="horizontal", variable=self.quality,
                                      command=self.update_quality_label)
        self.quality_slider.pack(side="left")
        
        self.quality_label = tk.Label(quality_control, text="85")
        self.quality_label.pack(side="left", padx=10)
        
        # Output directory
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(output_frame, text="Output Directory:", font=("Arial", 12, "bold")).pack()
        
        output_button_frame = tk.Frame(output_frame)
        output_button_frame.pack(pady=10)
        
        tk.Button(output_button_frame, text="Select Output Folder", 
                 command=self.select_output_dir, width=20).pack(side="left", padx=5)
        
        self.output_label = tk.Label(output_button_frame, text="No output directory selected")
        self.output_label.pack(side="left", padx=10)
        
        # Compress button
        self.compress_btn = tk.Button(self.root, text="Start Compression", 
                                     command=self.compress_images, 
                                     font=("Arial", 14, "bold"),
                                     bg="blue", fg="white", width=20)
        self.compress_btn.pack(pady=20)
        
        # Results text area
        self.results_text = tk.Text(self.root, height=8, width=70)
        self.results_text.pack(fill="both", expand=True, padx=20, pady=10)
    
    def update_quality_label(self, value):
        self.quality_label.configure(text=str(int(float(value))))
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
        )
        if files:
            self.input_files = list(files)
            self.update_file_list()
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            self.input_files = []
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']):
                        self.input_files.append(os.path.join(root, file))
            self.update_file_list()
    
    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.input_files:
            filename = os.path.basename(file)
            self.file_listbox.insert(tk.END, filename)
    
    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_label.configure(text=f"Output: {os.path.basename(directory)}")
    
    def compress_images(self):
        if not self.input_files:
            messagebox.showerror("Error", "Please select at least one image file.")
            return
        
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Starting compression...\n\n")
        
        successful = 0
        failed = 0
        total_original_size = 0
        total_compressed_size = 0
        
        for input_path in self.input_files:
            try:
                # Generate output filename
                filename = os.path.basename(input_path)
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_compressed.jpg"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Compress image
                with Image.open(input_path) as img:
                    original_size = os.path.getsize(input_path)
                    
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Save with compression
                    img.save(output_path, 'JPEG', quality=self.quality.get(), optimize=True)
                    compressed_size = os.path.getsize(output_path)
                    
                    # Calculate compression ratio
                    compression_ratio = (1 - compressed_size / original_size) * 100
                    
                    successful += 1
                    total_original_size += original_size
                    total_compressed_size += compressed_size
                    
                    # Add result to text area
                    result_text = f"✓ {filename}\n"
                    result_text += f"  Original: {self.format_size(original_size)}\n"
                    result_text += f"  Compressed: {self.format_size(compressed_size)}\n"
                    result_text += f"  Compression: {compression_ratio:.1f}%\n\n"
                    
                    self.results_text.insert(tk.END, result_text)
                    self.root.update()  # Update the GUI
                
            except Exception as e:
                failed += 1
                error_text = f"✗ {filename} - Error: {str(e)}\n\n"
                self.results_text.insert(tk.END, error_text)
                self.root.update()
        
        # Final results
        total_compression_ratio = 0
        if total_original_size > 0:
            total_compression_ratio = (1 - total_compressed_size / total_original_size) * 100
        
        final_text = f"\n=== COMPRESSION COMPLETE ===\n"
        final_text += f"Successful: {successful}\n"
        final_text += f"Failed: {failed}\n"
        final_text += f"Total original size: {self.format_size(total_original_size)}\n"
        final_text += f"Total compressed size: {self.format_size(total_compressed_size)}\n"
        final_text += f"Overall compression: {total_compression_ratio:.1f}%\n"
        
        self.results_text.insert(tk.END, final_text)
    
    def format_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def run(self):
        self.root.mainloop()

def main():
    app = SimpleImageCompressor()
    app.run()

if __name__ == "__main__":
    main()
