import tempfile
import json
from PIL import Image
from pytesseract import pytesseract

global image_counter

with open('config.json', 'r') as f:
    data = json.load(f)

pytesseract.tesseract_cmd = data['executable_path']

def get_image(image, calls=0):
    with tempfile.TemporaryFile() as fp:
        image.save(f'{fp.name}.png')
        text = pytesseract.image_to_string(Image.open(f'{fp.name}.png'))
        print(text)
