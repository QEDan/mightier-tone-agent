import sys
from pyzbar.pyzbar import decode
from PIL import Image

target = sys.argv[1] if len(sys.argv) > 1 else 'nitro.png'
img = Image.open(target)
results = decode(img)
if not results:
    print(f"No QR code found in {target}")
else:
    decoded = results[0].data.decode('utf-8')
    print(decoded)
