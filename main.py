from App import App
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter

customtkinter.set_appearance_mode("Dark")

app = App()
app.mainloop()

# class TicTacToeGrid:
#     def __init__(self, root, size=3):
#         self.root = root
#         self.root.title("Number Tic-Tac-Toe Grid")
#         self.size = size  # Grid size (3x3 by default)
#         self.cells = {}  # To store cell entries
        
#         # Create main frame
#         self.main_frame = tk.Frame(root, padx=20, pady=20)
#         self.main_frame.pack()
        
#         # Grid size selection
#         self.size_frame = tk.Frame(self.main_frame)
#         self.size_frame.pack(pady=10)
        
#         tk.Label(self.size_frame, text="Grid Size:").pack(side=tk.LEFT)
#         self.size_var = tk.StringVar(value=str(self.size))
#         self.size_entry = tk.Entry(self.size_frame, textvariable=self.size_var, width=3)
#         self.size_entry.pack(side=tk.LEFT, padx=5)
        
#         self.update_btn = tk.Button(
#             self.size_frame, 
#             text="Update Grid", 
#             command=self.update_grid_size
#         )
#         self.update_btn.pack(side=tk.LEFT)
        
#         # Create grid frame
#         self.grid_frame = tk.Frame(self.main_frame)
#         self.grid_frame.pack()
        
#         # Create initial grid
#         self.create_grid()
        
#         # Add clear button
#         self.clear_btn = tk.Button(
#             self.main_frame, 
#             text="Clear All", 
#             command=self.clear_grid,
#             bg="#ff9999"
#         )
#         self.clear_btn.pack(pady=10)
    
#     def create_grid(self):
#         # Clear existing grid if any
#         for widget in self.grid_frame.winfo_children():
#             widget.destroy()
        
#         self.cells = {}  # Reset cell storage
        
#         # Create grid of Entry widgets
#         for row in range(self.size):
#             for col in range(self.size):
#                 # Create entry widget
#                 entry = tk.Entry(
#                     self.grid_frame,
#                     width=3,
#                     font=('Arial', 24),
#                     justify='center',
#                     bd=2,
#                     relief="ridge"
#                 )
#                 entry.grid(row=row, column=col, padx=2, pady=2)
                
#                 # Validate to allow only numbers
#                 entry['validate'] = 'key'
#                 entry['validatecommand'] = (entry.register(self.validate_number), '%P')
                
#                 # Store reference
#                 self.cells[(row, col)] = entry
    
#     def validate_number(self, text):
#         """Allow only empty string or numbers"""
#         if text == "":
#             return True
#         try:
#             int(text)
#             return True
#         except ValueError:
#             return False
    
#     def update_grid_size(self):
#         """Update grid size based on user input"""
#         try:
#             new_size = int(self.size_var.get())
#             if new_size < 1 or new_size > 10:  # Reasonable limits
#                 messagebox.showerror("Error", "Please enter size between 1 and 10")
#                 return
                
#             self.size = new_size
#             self.create_grid()
#         except ValueError:
#             messagebox.showerror("Error", "Please enter a valid number")
    
#     def clear_grid(self):
#         """Clear all cells"""
#         for entry in self.cells.values():
#             entry.delete(0, tk.END)

# class SingleImageViewer:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Single Image Viewer")
#         self.root.geometry("600x500")
        
#         ctk.set_appearance_mode("System")
#         ctk.set_default_color_theme("blue")
        
#         # Main container
#         self.main_frame = ctk.CTkFrame(root)
#         self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
#         # Widgets
#         self.create_widgets()
        
#         # Image reference storage
#         self.current_image = None
    
#     def create_widgets(self):
#         # Instruction label
#         self.instruction_label = ctk.CTkLabel(
#             self.main_frame,
#             text="Select an image to display",
#             font=("Arial", 14)
#         )
#         self.instruction_label.pack(pady=10)
        
#         # Select button
#         self.select_button = ctk.CTkButton(
#             self.main_frame,
#             text="Choose Image",
#             command=self.load_single_image,
#             width=200,
#             height=40
#         )
#         self.select_button.pack(pady=10)
        
#         # Image display area
#         self.image_label = ctk.CTkLabel(
#             self.main_frame,
#             text="No image selected",
#             width=400,
#             height=300,
#             fg_color=("gray85", "gray25"),  # Light gray in light mode, dark gray in dark mode
#             corner_radius=10
#         )
#         self.image_label.pack(pady=20, padx=20, fill="both", expand=True)
        
#         # Filename label
#         self.filename_label = ctk.CTkLabel(
#             self.main_frame,
#             text="",
#             font=("Arial", 12)
#         )
#         self.filename_label.pack()
    
#     def load_single_image(self):
#         # Supported file types
#         filetypes = (
#             ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
#             ("All files", "*.*")
#         )
        
#         # Open file dialog
#         image_path = filedialog.askopenfilename(
#             title="Select an image",
#             initialdir=os.path.expanduser("~"),
#             filetypes=filetypes
#         )
        
#         if not image_path:
#             return  # User cancelled
        
#         try:
#             # Open and resize the image
#             img = Image.open(image_path)
            
#             # Calculate new size while maintaining aspect ratio
#             label_width = self.image_label.winfo_width() - 20
#             label_height = self.image_label.winfo_height() - 20
#             img.thumbnail((label_width, label_height))
            
#             # Convert to CTkImage
#             ctk_image = ctk.CTkImage(
#                 light_image=img,
#                 dark_image=img,
#                 size=img.size
#             )
            
#             # Update the display
#             self.image_label.configure(image=ctk_image, text="")
#             self.filename_label.configure(text=os.path.basename(image_path))
            
#             # Keep reference to prevent garbage collection
#             self.current_image = ctk_image
            
#         except Exception as e:
#             self.image_label.configure(
#                 text=f"Error loading image\n{str(e)}",
#                 image=None
#             )
#             self.filename_label.configure(text="")

# if __name__ == "__main__":
#     root = ctk.CTk()
#     app = SingleImageViewer(root)
#     root.mainloop()