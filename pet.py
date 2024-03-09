import tkinter as tk
from PIL import Image, ImageTk
import sys

class VirtualPet(tk.Tk):
    def __init__(self):
        super().__init__()

        # Remove window decorations
        self.overrideredirect(True)

        # Set the window to be transparent
        self.attributes("-transparentcolor", "white")

        #Hello

        # Load the image for the pet
        self.pet_image = Image.open("C:\\Users\\17703\\OneDrive - Georgia Institute of Technology\\Documents\\mushRush\\images\\shroom\\sparky1.png")
        self.pet_image = ImageTk.PhotoImage(self.pet_image)

        # Set the window size based on the pet image size
        self.geometry(f"{self.pet_image.width()}x{self.pet_image.height()}")

        # Create a label to display the pet image
        self.pet_label = tk.Label(self, image=self.pet_image, bg='white')
        self.pet_label.pack()

        self.interact_button = tk.Button(self, text="Interact", command=self.interact_with_pet, bg='white')
        self.interact_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def interact_with_pet(self):
        # Implement interactions with the pet here
        # For demonstration, let's change the pet image when interacted
        sys.exit()
        return

if __name__ == "__main__":
    app = VirtualPet()
    app.mainloop()
