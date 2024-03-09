import tkinter as tk
from PIL import Image, ImageTk
import os

class VirtualPet(tk.Tk):
    def __init__(self):
        super().__init__()

        # Remove window decorations
        self.overrideredirect(True)

        #set window size to cover the desktop screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))


        # Set the window to be transparent
        self.attributes("-transparentcolor", "white")

        # Load the image for the pet
        self.pet_images = self.load_pet_images()
        self.current_image_index = 0
        self.pet_image = self.pet_images[self.current_image_index]
        
        # Set the window size based on the pet image size //make window size = desktop size
        #self.geometry(f"{self.pet_image.width()}x{self.pet_image.height()}")

        # Create a canvas to hold the pet image
        self.canvas = tk.Canvas(self, width=width, height=height, bg='white', highlightthickness=0)
        self.canvas.pack()

        # Add the pet image to the canvas
        self.pet_label = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pet_image)

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.dragging)

        # Schedule updating the pet image
        self.update_pet_image()

    def load_pet_images(self):
        pet_images = []
        # Provide the directory path where your pet animation frames are located
        current_directory = os.path.dirname(__file__)

        # Navigate to the images folder using the relative path
        animation_folder = os.path.join(current_directory, "animation_frames", "idle")
        # animation_folder = "\\animation_frames"
        for filename in sorted(os.listdir(animation_folder)):
            image_path = os.path.join(animation_folder, filename)
            image = Image.open(image_path)
            new_width = 150
            new_height = 150
            resized_image = image.resize((new_width, new_height))
            image = ImageTk.PhotoImage(resized_image)
            pet_images.append(image)
        return pet_images

    def update_pet_image(self):
        # Update the pet image on the canvas
        self.pet_image = self.pet_images[self.current_image_index]
        self.canvas.itemconfig(self.pet_label, image=self.pet_image)

        # Increment the current image index
        self.current_image_index = (self.current_image_index + 1) % len(self.pet_images)

        # Schedule the next update after a certain delay (in milliseconds)
        self.after(200, self.update_pet_image)

    def start_drag(self, event):
        # Record the starting position of the mouse when dragging starts
        self.start_x = event.x
        self.start_y = event.y

    def dragging(self, event):
        # Calculate the distance moved by the mouse
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        # Move the pet image accordingly
        self.canvas.move(self.pet_label, dx, dy)

        # Update the starting position for the next movement
        self.start_x = event.x
        self.start_y = event.y

if __name__ == "__main__":
    app = VirtualPet()
    app.mainloop()
