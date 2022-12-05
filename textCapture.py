import tempfile, os, json
from PIL import Image
from pytesseract import pytesseract

global image_counter

try:
    if os.name == 'nt':
        with open('config.json', 'r') as f:
            data = json.load(f)

    pytesseract.tesseract_cmd = data['executable_path']
except:
    print('Warning: No path found to tesseract. Proceding anyway.')
    pass

def get_image(image):
    with tempfile.TemporaryFile() as fp:
        image.save(f'{fp.name}.png')
        return pytesseract.image_to_string(Image.open(f'{fp.name}.png'))
