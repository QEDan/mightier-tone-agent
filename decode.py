from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('bib.png')  # save the image first
decoded = decode(img)[0].data.decode('utf-8')
print(decoded)
