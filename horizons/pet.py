import tkinter as tk
from PIL import Image, ImageTk
import os
from pygame import mixer

class VirtualPet(tk.Tk):

    def __init__(self):
        super().__init__()

        current_directory = os.path.dirname(__file__)
        self.isSmore = False

        mixer.init()
        sound_path = os.path.join(current_directory, "Sounds", "Happy.mp3")
        self.pet_sound = mixer.Sound(sound_path)

        self.cursor_image = os.path.join(current_directory, "animation_frames", "smores.cur")
        # self.custom_cursor_image = tk.PhotoImage(file=cursor_image)

        # Remove window decorations
        self.overrideredirect(True)

        # Set window size to cover the desktop screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))

        # Set the window to be transparent
        self.attributes("-transparentcolor", "white")
        self.attributes("-topmost", True)

        # Load the image for the pet
        self.state = "idle"
        self.pet_images = self.load_pet_images(self.state)
        self.current_image_index = 0
        self.pet_image = self.pet_images[self.current_image_index]
        self.curr_anim_speed = 200

        # 20min: 1,200,000
        # # self.hunger_timer = 1200000
        # self.hunger_timer = 10000
        self.hunger_timer = 40000

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
        self.after(self.hunger_timer, self.update_hunger)

        # Create right-click pop-up menu
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Food", command=self.food)
        self.menu.add_command(label="Sleep/Wake", command=self.sleep)
        self.menu.add_command(label="Exit", command=self.quit)
        self.bind("<Button-3>", self.popup)
        self.grab_set()
        
    def food(self):
        self.isSmore = True
        self.configure(cursor="star")
        pass

    def sleep(self):
        if (self.state == "sleep"):
            self.return_to_idle()
        else:
            self.state = "sleep"
            self.pet_images = self.load_pet_images(self.state)
            self.current_image_index = 0
            self.curr_anim_speed = 300

    def popup(self, e):
        self.menu.tk_popup(e.x, e.y)   

    def interact_with_pet(self, event):
        if (self.state == "sleep"):
            self.start_x = event.x
            self.start_y = event.y
            return
        
        if (self.isSmore):
            self.state = "eat"
            self.pet_images = self.load_pet_images(self.state)
            self.current_image_index = 0
            self.curr_anim_speed = 120
            self.isSmore = False
            self.configure(cursor='arrow')
            # self.pet_sound.play()

        elif (self.state == "idle"):
            self.state = "happy"
            self.pet_images = self.load_pet_images(self.state)
            self.current_image_index = 0
            self.curr_anim_speed = 90
            self.pet_sound.play()

        self.start_x = event.x
        self.start_y = event.y

    def load_pet_images(self, name):
        pet_images = []
        # Navigate to the images folder using the relative path
        current_directory = os.path.dirname(__file__)
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
        elif (self.state == "eat" and self.current_image_index == 0):
            self.state = "happy"
            self.pet_images = self.load_pet_images(self.state)
            self.current_image_index = 0
            self.curr_anim_speed = 90
            self.pet_sound.play()

        # Schedule the next update after a certain delay (in milliseconds)
        self.after(self.curr_anim_speed, self.update_pet_image)

    def update_hunger(self):
        self.state = "hungry"
        self.pet_images = self.load_pet_images(self.state)
        self.current_image_index = 0
        self.curr_anim_speed = 90
        self.after(self.hunger_timer, self.update_hunger)

    def return_to_idle(self):
        self.state = "idle"
        self.curr_anim_speed = 200
        self.pet_images = self.load_pet_images(self.state)

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