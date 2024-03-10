import tkinter as tk
from PIL import Image, ImageTk
import os
from pygame import mixer

class VirtualPet(tk.Tk):

    def __init__(self):
        super().__init__()
        
        mixer.init()
        self.pet_sound = mixer.Sound("C:\\Users\\Kelly\\OneDrive\\Documents\\ShootingStar\\shootingstar\\horizons\\Sounds\\Happy.mp3")
        

        # Remove window decorations
        self.overrideredirect(True)

        # Set window size to cover the desktop screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))

        # Set the window to be transparent
        self.attributes("-transparentcolor", "white")

        # Load the image for the pet
        self.state = "idle"
        self.pet_images = self.load_pet_images(self.state)
        self.current_image_index = 0
        self.pet_image = self.pet_images[self.current_image_index]
        self.curr_anim_speed = 200

        # Create a canvas to hold the pet image
        self.canvas = tk.Canvas(self, width=width, height=height, bg='white', highlightthickness=0)
        self.canvas.pack()

        # Add the pet image to the canvas
        self.pet_label = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.pet_image)

        # Bind mouse events to the canvas
        self.canvas.bind("<Button-1>", self.interact_with_pet)
        self.canvas.bind("<B1-Motion>", self.dragging)

        # self.interact_button = tk.Button(self, text="Interact", command=self.interact_with_pet, bg='white')
        # self.interact_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Schedule updating the pet image
        self.update_pet_image()

        # Create right-click pop-up menu
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Exit", command=self.quit)
        self.bind("<Button-3>", self.popup)

        
    def popup(self, e):
        self.menu.tk_popup(e.x, e.y)   

    def interact_with_pet(self, event):
        if (self.state == "idle"):
            self.state = "happy"
            self.pet_images = self.load_pet_images(self.state)
            self.current_image_index = 0
            self.curr_anim_speed = 90
            self.pet_sound.play()
            print("Trying to be happy...")
        return

    def load_pet_images(self, name):
        pet_images = []
        # Provide the directory path where your pet animation frames are located
        current_directory = os.path.dirname(__file__)

        # Navigate to the images folder using the relative path
        animation_folder = os.path.join(current_directory, "animation_frames", name)
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
        if (self.state == "happy" and self.current_image_index == 0):
            self.return_to_idle()

        # Schedule the next update after a certain delay (in milliseconds)
        self.after(self.curr_anim_speed, self.update_pet_image)

    def return_to_idle(self):
        self.state = "idle"
        self.curr_anim_speed = 200
        self.pet_images = self.load_pet_images(self.state)

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