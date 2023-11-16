import os
import json
from datetime import datetime
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
    ascii_str = ''.join(ASCII_CHARS[min(pixel // 28, len(ASCII_CHARS) - 1)] for pixel in pixels)
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
    Save the ANSI art as a text file in the ANSI_IMAGE_DIR directory.
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

def read_text_file(file_path):
    """
    Read text from a .txt file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def get_file_path(prompt, file_types):
    """
    Get file path from the user.
    """
    path = input(f"{prompt} (Supported types: {', '.join(file_types)}): ")
    if not os.path.exists(path) or not path.lower().endswith(tuple(file_types)):
        print("Invalid file path or file type. Please try again.")
        return get_file_path(prompt, file_types)
    return path

def process_image(image_path, text_file=''):
    """
    Process the image and text file, then save them.
    """
    ascii_art = image_to_ascii_art(image_path)
    ansi_art = image_to_ansi_art(image_path)
    ansi_image_path = save_ansi_image(ansi_art, os.path.basename(image_path).split('.')[0])
    text_content = read_text_file(text_file) if text_file else ''
    save_post(ascii_art, 'ascii', text_content)
    save_post(os.path.join(ANSI_IMAGE_DIR, os.path.basename(ansi_image_path)), 'ansi', text_content)
    print("\n--- ASCII Art ---\n")
    print(ascii_art)
    print("\nANSI Art saved at:", ansi_image_path)
    if text_file:
        print("\nText from the blog post:")
        print(text_content)

def main():
    print("Welcome to the Microblog Creator")
    include_image = input("Do you want to include an image in your post? (yes/no): ").lower()
    text_file_path = get_file_path("Enter the path to the text file", ['.txt'])

    if include_image == 'yes':
        image_path = get_file_path("Enter the path to the image file", ['.jpg', '.jpeg', '.png', '.bmp'])
        process_image(image_path, text_file_path)
    else:
        text_content = read_text_file(text_file_path)
        save_post('', 'text', text_content)
        print("\nText from the blog post:")
        print(text_content)

if __name__ == "__main__":
