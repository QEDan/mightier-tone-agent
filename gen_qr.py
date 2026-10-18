#!/usr/bin/env python3
"""
gen_qr.py - generate a Mighty Amp-compatible preset QR code from JSON.

Usage:
  python gen_qr.py input.json output.png
  python gen_qr.py -i preset.json -o preset.png --box-size 10 --border 4

Dependencies:
  pip install qrcode[pil] pillow

What the Mighty Amp app expects (from the repository):
  - QR content is a string that starts with: "nux://MightyAmp:"
  - The rest is base64 of a byte array where:
      byte[0] = deviceQRId (int 0..255)
      byte[1] = deviceQRVersion (int 0..255)
      byte[2:] = device-specific payload bytes (created by the app from the preset)

This script accepts JSON in any of these forms:

1) Raw combined nux_data (list of integers)
{
  "nux_data": [11, 1, 0, 23, 255, 10, ...]
}

2) nux_data as base64 string
{
  "nux_data_b64": "CwEAA..."

}

3) Device id + payload (convenience)
{
  "device": { "id": 11, "version": 1 },
  "payload": [0, 23, 255, 10, ...]
}

Notes:
  - The integers in lists must be 0..255.
  - The script will validate basic constraints and fail if it can't construct a valid byte array.
  - If you have a preset inside the app you can get the exact byte array by calling Preset.createNuxDataFromPreset()
    (that method returns a List<int> representing the bytes; put that list into "nux_data").

Examples:

  # Example: simple PlugAir-style (device id 11, version 1) with empty payload of length 40:
  {
    "device": { "id": 11, "version": 1 },
    "payload": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  }

  # Equivalent using nux_data:
  {
    "nux_data": [11, 1, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  }

Output:
  - A PNG image file (output path argument) containing the QR code. The QR payload will be:
      "nux://MightyAmp:" + base64(<bytes>)

Implementation details:
  - Uses qrcode (Python) with high error correction for robust scanning.
  - Validates the integer ranges and minimal length (>=2 bytes needed for id+version).
  - Accepts pretty-printed JSON.

Author:
  - Generated based on the mightier_amp repository's QR handling (QrUtils.nuxQRPrefix and Preset.setupPresetFromQRData).
"""

import argparse
import base64
import json
import sys
from typing import List, Union

try:
    import qrcode
    from PIL import Image
except Exception as e:
    print("Missing dependency: please run 'pip install qrcode[pil] pillow'")
    raise

NUX_PREFIX = "nux://MightyAmp:"

def validate_byte_list(lst: List[int]) -> None:
    if not isinstance(lst, list):
        raise ValueError("byte list must be a JSON array")
    for i, v in enumerate(lst):
        if not isinstance(v, int):
            raise ValueError(f"nux data element at index {i} is not an integer")
        if v < 0 or v > 255:
            raise ValueError(f"nux data element at index {i} is out of byte range (0..255): {v}")

def build_nux_bytes_from_json(obj: dict) -> bytes:
    # Priority: nux_data (list) -> nux_data_b64 -> device+payload
    if "nux_data" in obj:
        lst = obj["nux_data"]
        validate_byte_list(lst)
        return bytes(lst)
    if "nux_data_b64" in obj:
        if not isinstance(obj["nux_data_b64"], str):
            raise ValueError("nux_data_b64 must be a base64 string")
        try:
            data = base64.b64decode(obj["nux_data_b64"], validate=True)
            return data
        except Exception as e:
            raise ValueError("invalid base64 in nux_data_b64: " + str(e))
    if "device" in obj and "payload" in obj:
        dev = obj["device"]
        if not isinstance(dev, dict):
            raise ValueError("device must be an object with 'id' and 'version'")
        if "id" not in dev or "version" not in dev:
            raise ValueError("device object must contain 'id' and 'version'")
        did = dev["id"]
        ver = dev["version"]
        if not (isinstance(did, int) and isinstance(ver, int)):
            raise ValueError("device.id and device.version must be integers")
        payload = obj["payload"]
        validate_byte_list(payload)
        return bytes([did & 0xFF, ver & 0xFF] + payload)
    raise ValueError("JSON must contain one of: 'nux_data' (list), 'nux_data_b64' (string), or 'device' + 'payload'")

def generate_qr_bytes(data_bytes: bytes, box_size: int = 10, border: int = 4) -> Image.Image:
    """
    Generate a PIL Image (QR code) for the given bytes.
    The QR payload is NUX_PREFIX + base64(data_bytes).
    """
    b64 = base64.b64encode(data_bits := data_bytes).decode("ascii")
    content = NUX_PREFIX + b64

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=box_size,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img

def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a Mighty Amp preset QR code PNG from JSON.")
    parser.add_argument("input", nargs="?", help="Input JSON file (see docstring for format). Use '-' for stdin.")
    parser.add_argument("output", nargs="?", help="Output PNG file. If omitted writes to stdout (not recommended).")
    parser.add_argument("--box-size", type=int, default=10, help="QR box size (pixel size of one box). Default 10.")
    parser.add_argument("--border", type=int, default=4, help="QR border (boxes). Default 4.")
    args = parser.parse_args(argv)

    if not args.input or not args.output:
        parser.print_help()
        sys.exit(2)

    # Load JSON
    if args.input == "-":
        txt = sys.stdin.read()
        obj = json.loads(txt)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            obj = json.load(f)

    try:
        nux_bytes = build_nux_bytes_from_json(obj)
    except Exception as e:
        print("Error building nux bytes from JSON:", e, file=sys.stderr)
        sys.exit(1)

    if len(nux_bytes) < 2:
        print("Error: nux bytes must contain at least device id and version (2 bytes).", file=sys.stderr)
        sys.exit(1)

    img = generate_qr_bytes(nux_bytes, box_size=args.box_size, border=args.border)
    img.save(args.output)
    print(f"Wrote QR to {args.output} (payload {len(nux_bytes)} bytes)")

if __name__ == "__main__":
    main()