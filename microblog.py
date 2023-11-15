import os
import json
from datetime import datetime
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image

# ASCII characters used to build the ASCII art
ASCII_CHARS = "@%#*+=-:. "
# Template for ANSI color formatting
ANSI_COLOR_TEMPLATE = '\x1b[48;2;{};{};{}m \x1b[0m'
# Directory to store ANSI images
ANSI_IMAGE_DIR = "ansi_images"

def image_to_ascii_art(image_path):
    """
    Convert an image to ASCII art.
    """
    image = Image.open(image_path)
    image = image.convert('L').resize((80, 30))
    pixels = image.getdata()
    ascii_str = ''.join(ASCII_CHARS[pixel // 25] for pixel in pixels)
    return '\n'.join(ascii_str[i:i+80] for i in range(0, len(ascii_str), 80))

def image_to_ansi_art(image_path):
    """
    Convert an image to ANSI art.
    """
    image = Image.open(image_path)
    image = image.resize((80, 30))
    art = ''
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            art += ANSI_COLOR_TEMPLATE.format(*pixel)
        art += '\n'
    return art

def save_ansi_image(art, file_name):
    """
    Save the ANSI art as a text file in a specific directory.
    """
    if not os.path.exists(ANSI_IMAGE_DIR):
        os.makedirs(ANSI_IMAGE_DIR)
    path = os.path.join(ANSI_IMAGE_DIR, file_name + '.txt')
    with open(path, 'w') as file:
        file.write(art)
    return path

def save_post(art, type, text=''):
    """
    Save the art and text as a post with a timestamp.
    """
    timestamp = datetime.now().isoformat()
    post = {'timestamp': timestamp, 'art': art, 'type': type, 'text': text}
    with open('posts.json', 'a') as file:
        file.write(json.dumps(post) + '\n')

def display_post(art, text):
    """
    Display the art and text as it would appear in the terminal.
    """
    print("\n--- Post Start ---\n")
    print(art)
    print("\n" + text)
    print("\n--- Post End ---\n")

def process_image(file_path, text=''):
    """
    Process the image and text, then save and display them.
    """
    ascii_art = image_to_ascii_art(file_path)
    ansi_art = image_to_ansi_art(file_path)
    ansi_image_path = save_ansi_image(ansi_art, os.path.basename(file_path).split('.')[0])
    save_post(ascii_art, 'ascii', text)
    save_post(ansi_image_path, 'ansi', text)
    display_post(ascii_art, text)  # Display ASCII art version

def select_image():
    """
    Handle image and text file selection.
    """
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not file_path:
        messagebox.showinfo("No Image Selected", "You did not select an image file.")
        return

    text_file = filedialog.askopenfilename(title="Select Text Document (optional)", filetypes=[("Text files", "*.txt")])
    text_content = ''
    if text_file:
        with open(text_file, 'r') as file:
            text_content = file.read()

    process_image(file_path, text_content)
    status_label.config(text="Image and text processed and saved.")

# Setting up the GUI
root = Tk()
root.title("Micro-Blogging Platform")

select_button = Button(root, text="Select Image and Text", command=select_image)
select_button.pack()

status_label = Label(root, text="")
status_label.pack()

# Run the GUI application
root.mainloop()

