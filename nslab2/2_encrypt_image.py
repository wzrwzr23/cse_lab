# Encrypt Image
import numpy as np
import shutil
import os
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Prepare output destination
try:
    shutil.rmtree("output")
except:
    pass
os.mkdir("output")


def image_to_cols(image):
    """
    Helper function to convert a 2D image into an array of columns
    """
    arr = np.asarray(image)
    return list(zip(*arr))


def cols_to_image(cols):
    """
    Helper function to convert an array of columns back to 2D image so we can save it back to file
    """
    rows = list(zip(*cols))
    return Image.fromarray(np.array(rows, dtype=np.uint8))


def col_to_bytes(col, top_down=False):
    """
    Helper function to convert each pixel tuple to bytes. Iterate the column top-down or bottom-up
    """
    out = []
    for pixel in col[:: (1, -1)[top_down]]:
        out.insert(0, tuple_to_bytes(pixel))
    return b"".join(out)


def tuple_to_bytes(x):
    """
    Helper function to convert a tuple of integers into bytes
    """
    return int.from_bytes(list(x), byteorder="big").to_bytes(
        4, byteorder="big"
    )


def bytes_to_col(x, length, top_down=False):
    """
    Helper function to convert each pixel value in bytes back to tuple. Iterate the column top-down or bottom-up
    """
    out = []

    x = int.from_bytes(x[::-1], byteorder="big")
    for _ in range(length):
        pixel = []
        # Discard fake alpha value
        x >>= 8
        for _ in range(3):
            if top_down:
                pixel.append(x & 0xFF)
            else:
                pixel.insert(0, x & 0xFF)
            x >>= 8
        if top_down:
            out.append(pixel)
        else:
            out.insert(0, pixel)
    return out


def enc_img(input_filename, output_filename, cbc, top_down=False):
    """
    Encrypt [input_filename] image with 3DES and save it as [output_filename]

    :param cbc: whether CBC mode is used
    :type cbc: Bool
    """
    # Key for 3DES
    key = b"\xb6\x11\xd5\xd7\x83\xb2,m"

    # Initialisation Vector CBC mode
    iv = b"\x94k\xae\x83@D\xfcc"

    # Create the encryption mode instance
    mode = modes.CBC(iv) if cbc else modes.ECB()

    # Create and configure Cipher object
    # TODO: Task 2-1
    cipher = Cipher(algorithms.TripleDES(key), mode)

    # Load the image
    im = Image.open(input_filename)

    # Prepare an array to hold encrypted column values
    encrypted_cols = []

    # Iterate through all columns in the image
    for col in image_to_cols(im):

        # Create a CipherContext instance for encryption
        # TODO: Task 2-2
        encryptor = cipher.encryptor()
        #raw_bytes = b"abcdefghijklmnop"  # 16 bytes
        #print("raw_bytes", raw_bytes)
        #encrypted_bytes = (encryptor.update(raw_bytes) + encryptor.finalize())  # 16 bytes
        #print("encrypted_bytes", encrypted_bytes)
        # Prepare a padding scheme
        # TODO: Task 2-3
        padder = padding.PKCS7(64).padder() 
        #test_bytes = b"Lorem" # 5 bytes
        #padded_test_bytes = padder.update(test_bytes) + padder.finalize() # 8 bytes
        #print("padded_test_bytes", padded_test_bytes)
        # Convert each column value into bytes
        column_bytes = col_to_bytes(col, top_down)

        # Pad each column bytes
        # TODO: Task 2-4
        padded_col_bytes = padder.update(column_bytes)+padder.finalize()
        # Encrypt each padded column bytes
        # TODO: Task 2-5
        encrypted_bytes = encryptor.update(padded_col_bytes) + encryptor.finalize()

        try:
            # Convert back the encrypted column bytes to tuple of int
            encrypted_col = bytes_to_col(encrypted_bytes, im.height, top_down)

            # Append the result to the array
            encrypted_cols.append(encrypted_col)
        except:
            print("Task 2-1 to 2-5 not implemented")
            exit()

    # Construct the image back from encrypted column bytes
    encrypted_image = cols_to_image(encrypted_cols)

    # Save the image to file
    encrypted_image.save(output_filename)


if __name__ == "__main__":
    ##### SUTD #####
    # ECB
    enc_img(
        "original_files/SUTD.bmp",
        "output/enc_bottom_up_ecb_SUTD.bmp",
        False,
        False,
    )
    enc_img(
        "original_files/SUTD.bmp",
        "output/enc_top_down_ecb_SUTD.bmp",
        False,
        True,
    )

    # # CBC
    enc_img(
        "original_files/SUTD.bmp",
        "output/enc_bottom_up_cbc_SUTD.bmp",
        True,
        False,
    )
    enc_img(
        "original_files/SUTD.bmp",
        "output/enc_top_down_cbc_SUTD.bmp",
        True,
        True,
    )
    # ################

    # ### TODO: TRIANGLE ###
    # # ECB
    enc_img(
        "original_files/triangle.bmp",
        "output/enc_bottom_up_ecb_triangle.bmp",
        False,
        False,
    )
    enc_img(
        "original_files/triangle.bmp",
        "output/enc_top_down_ecb_triangle.bmp",
        False,
        True,
    )

    # # CBC
    enc_img(
        "original_files/triangle.bmp",
        "output/enc_bottom_up_cbc_triangle.bmp",
        True,
        False,
    )
    enc_img(
        "original_files/triangle.bmp",
        "output/enc_top_down_cbc_triangle.bmp",
        True,
        True,
    )
    ################
