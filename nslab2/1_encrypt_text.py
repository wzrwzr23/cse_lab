# Encrypt and Decrypt Text File
import base64
from email.contentmanager import raw_data_manager
import shutil
import os
from cryptography.fernet import Fernet

# Generate a Fernet key
# TODO: Task 1-1
symmetric_key = Fernet.generate_key()
print("---------1.1------------")
print(symmetric_key)
print("---------1.1------------")
# Prepare output destination
try:
    shutil.rmtree("output")
except:
    pass
os.mkdir("output")


def enc_text(input_filename, output_filename):
    """
    Encrypt [input_filename] with the symmetric key above, save it as [output_filename]
    """
    # Generate a cipher
    # TODO: Task 1-2
    #symmetric_key = Fernet.generate_key()
    cipher = Fernet(symmetric_key)
    # Open the file, read as bytes
    with open(input_filename, "rb") as fp:
        raw_bytes = fp.read()

    # Encrypt the raw bytes
    # TODO: Task 1-3
    encrypted_bytes = cipher.encrypt(raw_bytes) #input must be bytes

    try:
        # Convert the ciphertext output to a printable string
        encrypted_base64_bytes = base64.b64encode(encrypted_bytes)
        encrypted_text = encrypted_base64_bytes.decode("utf8")

        # Save the printable string back to file
        with open(output_filename, "w") as fp:
            fp.write(encrypted_text)

        print(f"Original byte length: {len(raw_bytes)}")
        print(f"Encrypted byte length: {len(encrypted_bytes)}")
        print()
    except:
        print("Task 1-1 to 1-5 not implemented")


def dec_text(input_filename, output_filename):
    """
    Decrypt [output_filename] with the symmetric key above, save it as [output_filename]
    """
    # Generate a cipher from key (same as above in enc_text)
    # TODO: Task 1-2
    #symmetric_key = Fernet.generate_key()
    cipher = Fernet(symmetric_key)

    try:
        # Open the file containing the cyphertext, read as string
        with open(input_filename, "r") as fp:
            encrypted_text = fp.read()

        # Convert the printable string back to bytes
        encrypted_bytes = base64.b64decode(encrypted_text.encode("utf8"))
    except Exception as e:
        print(
            f"You didn't implement the encryption and save the encrypted file back correctly."
        )
        print(e)

    # Decrypt the cipher bytes
    # TODO: Task 1-4
    decrypted_bytes = cipher.decrypt(encrypted_bytes)

    try:
        # Convert the decrypted bytes to printable text
        decrypted_text = decrypted_bytes.decode("utf8")
        message_bytes = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna'
        encrypted_message_bytes = cipher.encrypt(message_bytes)
        decrypted_message_bytes = cipher.decrypt(encrypted_message_bytes)
        assert message_bytes == decrypted_message_bytes
        # Save the printable text back to file
        with open(output_filename, "w") as fp:
            fp.write(decrypted_text)

        print(f"Original byte length: {len(encrypted_bytes)}")
        print(f"Decrypted byte length: {len(decrypted_text)}")
        print()
    except:
        print("Task 1-1, 1-2, 1-6 to 1-8 not implemented")


if __name__ == "__main__":
    enc_text("original_files/shorttext.txt", "output/enc_shorttext.txt")
    dec_text("output/enc_shorttext.txt", "output/dec_shorttext.txt")

    enc_text("original_files/longtext.txt", "output/enc_longtext.txt")
    dec_text("output/enc_longtext.txt", "output/dec_longtext.txt")

