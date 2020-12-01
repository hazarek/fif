from PIL import Image
from PIL.PngImagePlugin import PngInfo
import os
import sys
from fif.tools import *


def encode(filename, verbose=False):

    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except IOError as e:
        print(e)
        sys.exit()

    output_filename = change_ext(filename, "png")
    INPUT_BYTES_LENGHT = len(data)
    extra_bytes_lenght = 0

    # pngsize boyutunu burada hesapla 1 bayt 8 bit (256) gri pixel
    w = get_w(INPUT_BYTES_LENGHT)
    output_size = (w, w)
    OUTPUT_BYTES_LENGHT = w * w
    extra_bytes_lenght = OUTPUT_BYTES_LENGHT - INPUT_BYTES_LENGHT
    data += (b'\0' * extra_bytes_lenght)

    if os.path.isfile(output_filename):
        output_filename = get_unique_filename(output_filename)
        if verbose:
            print(
                f"file has been renamed to: '{output_filename}'")

    metadata = PngInfo()
    metadata.add_text("filename", str(os.path.basename(filename)))
    metadata.add_text("extra_bytes", str(extra_bytes_lenght))
    
    if verbose:
        print(metadata.chunks)
        print(f"File ->  {output_filename}")
        print(f"Image size ->  {output_size}")
    im = Image.frombytes("L", output_size, data)
    im.save(output_filename, pnginfo=metadata)
    sys.exit()


def decode(filename, verbose=False):
    im = Image.open(filename)
    dir_name = os.path.dirname(filename)
    output_filename = os.path.join(dir_name, im.text["filename"])
    extra_bytes_lenght = int(im.text["extra_bytes"])
    hidden_data = im.tobytes()
    print(len(hidden_data))
    hidden_data = hidden_data[:-extra_bytes_lenght]
    
    if os.path.isfile(output_filename):
        output_filename = get_unique_filename(output_filename)
        if verbose:
            print(f"file has been renamed to {output_filename}")
    if verbose:
        print(f"'{output_filename}' extracted from '{filename}'")
        print(f"Saved file ----> {output_filename}")
    try:
        with open(output_filename, "wb") as file:
            file.write(hidden_data)
    except IOError as e:
        print(e)
        sys.exit()
