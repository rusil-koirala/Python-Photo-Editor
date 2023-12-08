import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance


# main class ***
class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Editor")
        self.root.configure(bg="#f0f0f0")  # Set background color**

        self.root.iconbitmap('images/app.ico') #iconn

        self.image_path = None
        self.original_image = None
        self.modified_image = None
        self.photo = None

        # Set maximum values for adjustments
        self.max_blur_radius = 10
        self.max_sharpen_factor = 10
        self.max_contrast_factor = 2.0

        # Create UI elements
        self.create_widgets()

        # Bind keyboard shortcuts
        self.root.bind("<Control-o>", self.open_image)
        self.root.bind("<Control-s>", self.save_image)

    def create_widgets(self):
        # Menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # Canvas to display the image
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="#ffffff")  # Set canvas background color
        self.canvas.pack()

        # Blur slider
        blur_label = tk.Label(self.root, text="Blur", bg="#f0f0f0")  # Set label background color
        blur_label.pack(side=tk.LEFT, padx=10)
        self.blur_slider = ttk.Scale(self.root, from_=0, to=self.max_blur_radius, orient=tk.HORIZONTAL)
        self.blur_slider.pack(side=tk.LEFT, padx=10)
        self.blur_value_label = tk.Label(self.root, text="0", bg="#f0f0f0")
        self.blur_value_label.pack(side=tk.LEFT)

        # Sharpen slider
        sharpen_label = tk.Label(self.root, text="Sharpen", bg="#f0f0f0")  # Set label background color
        sharpen_label.pack(side=tk.LEFT, padx=10)
        self.sharpen_slider = ttk.Scale(self.root, from_=0, to=self.max_sharpen_factor, orient=tk.HORIZONTAL)
        self.sharpen_slider.pack(side=tk.LEFT, padx=10)
        self.sharpen_value_label = tk.Label(self.root, text="0", bg="#f0f0f0")
        self.sharpen_value_label.pack(side=tk.LEFT)

        # Contrast slider
        contrast_label = tk.Label(self.root, text="Contrast", bg="#f0f0f0")  # Set label background color
        contrast_label.pack(side=tk.LEFT, padx=10)
        self.contrast_slider = ttk.Scale(self.root, from_=0, to=self.max_contrast_factor, orient=tk.HORIZONTAL)
        self.contrast_slider.pack(side=tk.LEFT, padx=10)
        self.contrast_value_label = tk.Label(self.root, text="1.0", bg="#f0f0f0")
        self.contrast_value_label.pack(side=tk.LEFT)

        # Apply Changes button
        apply_button = tk.Button(self.root, text="Apply Changes", command=self.apply_changes, bg="#008CBA", fg="white")  # Set button colors
        apply_button.pack(side=tk.LEFT, padx=10)

        # Open image button
        open_button = tk.Button(self.root, text="Open Image", command=self.open_image, bg="#4CAF50", fg="white")  # Set button colors
        open_button.pack(side=tk.LEFT, padx=10)

        # Save image button
        save_button = tk.Button(self.root, text="Save Image", command=self.save_image, bg="#FFD700", fg="black")  # Set button colors
        save_button.pack(side=tk.LEFT, padx=10)

        # Reset button
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_image, bg="#FF5733", fg="white")  # Set button colors
        reset_button.pack(side=tk.LEFT, padx=10)

    def open_image(self, event=None):
        file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(self.image_path)
            self.modified_image = self.original_image.copy()  # Make a copy to preserve the original
            self.display_image()

    def save_image(self, event=None):
        if self.modified_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.modified_image.save(file_path)

    def display_image(self):
        if self.modified_image:
            # Resize the image to fit the canvas
            img_width, img_height = self.modified_image.size
            canvas_width, canvas_height = 500, 500
            scale = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Resize and convert the image to PhotoImage
            resized_image = self.modified_image.resize((new_width, new_height))
            self.photo = ImageTk.PhotoImage(resized_image)

            # Clear existing image on the canvas
            self.canvas.delete("all")

            # Display the new image on the canvas
            self.canvas.create_image(canvas_width / 2, canvas_height / 2, image=self.photo)

    def apply_changes(self):
        if self.modified_image:
            blur_radius = int(self.blur_slider.get())
            sharpen_factor = int(self.sharpen_slider.get())
            contrast_factor = float(self.contrast_slider.get())

            # Apply blur with limit
            blur_radius = min(blur_radius, self.max_blur_radius)
            self.modified_image = self.modified_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

            # Apply sharpen with limit
            sharpen_factor = min(sharpen_factor, self.max_sharpen_factor)
            self.modified_image = self.modified_image.filter(
                ImageFilter.UnsharpMask(radius=sharpen_factor, percent=150, threshold=3)
            )

            # Apply contrast with limit
            contrast_factor = max(contrast_factor, 0.1)  # Ensure contrast_factor is not zero
            enhancer = ImageEnhance.Contrast(self.modified_image)
            self.modified_image = enhancer.enhance(contrast_factor)

            # Update the displayed image
            self.display_image()
            # Update slider labels
            self.update_slider_labels()

    def reset_image(self):
        if self.image_path:
            self.modified_image = self.original_image.copy()  # Reset to the original image
            self.display_image()
            self.blur_slider.set(0)
            self.sharpen_slider.set(0)
            self.contrast_slider.set(1.0)
            self.update_slider_labels()

    def update_slider_labels(self):
        self.blur_value_label.config(text=str(self.blur_slider.get()))
        self.sharpen_value_label.config(text=str(self.sharpen_slider.get()))
        self.contrast_value_label.config(text="{:.1f}".format(self.contrast_slider.get()))

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoEditor(root)
    root.mainloop()
