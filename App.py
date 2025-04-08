import customtkinter
from Controller import *
from numpy import zeros, float64, clip
from PIL import Image
import os

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.title("Image Processor")

        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1)   

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.load_files_frame = LoadFilesFrame(self)
        self.load_files_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.load_files_frame.set_image_frame_ref(self.image_frame)

        self.matrix_frame = MatrixFrame(self)
        self.matrix_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.matrix_frame.set_image_frame_ref(self.image_frame)
        
        self.load_files_frame.grid_columnconfigure(0, weight=1)
        self.matrix_frame.grid_columnconfigure(0, weight=1)


class ImageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.image_label = customtkinter.CTkLabel(self, text="Image")
        self.image_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.image_display = customtkinter.CTkLabel(self, text="")
        self.image_display.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        try:
            self.set_image(Image.open("default.png"))
            self.show_image()

        except:
            self.img_to_show.thumbnail((WINDOW_WIDTH - 200, WINDOW_HEIGHT - 100))

            self.image_display.configure(image=customtkinter.CTkImage(light_image=self.img_to_show,
                                                                    dark_image=self.img_to_show,
                                                                    size=self.img_to_show.size),
                                                                    text="") 
            
    def set_image(self, img: Image):
        self.current_img = img
        self.img_to_show = img.copy()

    def update_image(self, img: Image):
        self.img_to_show = img
        
    def show_image(self):
        self.img_to_show.thumbnail((WINDOW_WIDTH - 200, WINDOW_HEIGHT - 100))
        self.image_display.configure(image=customtkinter.CTkImage(light_image=self.img_to_show,
                                                                  dark_image=self.img_to_show,
                                                                  size=self.img_to_show.size),
                                     text="")
        
    def restore_default(self):
        self.set_image(self.current_img)
        self.show_image()
        
    def get_img_toshow(self):
        return self.img_to_show


class LoadFilesFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Configure frame to expand
        self.grid_columnconfigure(0, weight=1)
        
        self.load_button = customtkinter.CTkButton(self, text="Load an Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        self.filename_label = customtkinter.CTkLabel(self, text="No image selected")
        self.filename_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    def load_image(self):
        filetypes = (
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
            ("All files", "*.*")
        )

        image_path = customtkinter.filedialog.askopenfilename(
            title="Select an image",
            initialdir=os.path.expanduser("~"),
            filetypes=filetypes
        )

        if not image_path: return

        try:
            img = Image.open(image_path)
            self.filename_label.configure(text=image_path)

            self.image_frame_ref.set_image(img)
            self.image_frame_ref.show_image()

        except Exception as e:
            customtkinter.CTkMessagebox.show_error(
                title="Error",
                message=f"Error loading image:\n{str(e)}"
            )

    def set_image_frame_ref(self, image_frame):
        self.image_frame_ref = image_frame


class MatrixFrame(customtkinter.CTkFrame):
    MATRIX_SIZE = 3

    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        for col in range(self.MATRIX_SIZE):
            self.grid_columnconfigure(col, weight=1)

        self.matrix_label = customtkinter.CTkLabel(self, text="Matrix")
        self.matrix_label.grid(row=0, column=0, 
                             columnspan=self.MATRIX_SIZE,
                             padx=10, pady=(10, 0), 
                             sticky="ew")

        self.cells = {}
        for row in range(self.MATRIX_SIZE):
            for col in range(self.MATRIX_SIZE):
                entry = customtkinter.CTkEntry(
                    self,
                    width=50,
                    justify='center'
                )

                if row == col:
                    entry.insert(0, "1")
                else:
                    entry.insert(0, "0")

                entry.grid(row=row+1, column=col, padx=5, pady=5)
                self.cells[(row, col)] = entry

        self.apply_button = customtkinter.CTkButton(self, text="Apply matrix", command=self.apply_matrix_functionality)
        self.apply_button.grid(row=self.MATRIX_SIZE+1, column=0, columnspan=self.MATRIX_SIZE, padx=10, pady=(10, 0), sticky="ew")

        self.restore_button = customtkinter.CTkButton(self, text="Restore default", command=self.restore_default)
        self.restore_button.grid(row=self.MATRIX_SIZE+2, column=0, columnspan=self.MATRIX_SIZE, padx=10, pady=(10, 10), sticky="ew")

    def set_image_frame_ref(self, image_frame):
        self.image_frame_ref = image_frame

    def apply_matrix_functionality(self):
        convolved_image = convolve_image(self.get_matrix_vals(), self.image_frame_ref.get_img_toshow())

        self.image_frame_ref.update_image(convolved_image)
        self.image_frame_ref.show_image()

    def restore_default(self):
        self.image_frame_ref.restore_default()

    def get_matrix_vals(self):
        matrix = zeros((self.MATRIX_SIZE, self.MATRIX_SIZE), dtype=float64)

        for row in range(self.MATRIX_SIZE):
            for col in range(self.MATRIX_SIZE):
                entry = self.cells[(row, col)]
                try:
                    matrix[row, col] = float64(entry.get())
                except ValueError:
                    matrix[row, col] = 0.0

        return matrix