"""
Script: Steganography Hidden Message Extraction
Author: Group 4
Date: 2024-12-04
Python version: 3.10
Description:
    This script is designed to uncover a hidden message embedded in the provided PNG file 
    "PRCSE-C2.png" using steganographic techniques. The process involves decoding the image 
    and analyzing its content to retrieve the concealed information.

Steps to be performed:
1. Load the image file "PRCSE-C2.png".
2. Use steganographic decoding techniques to extract the hidden message.
3. Analyze and decode the hidden content, if necessary.
4. Provide the extracted message as output.

Notes:
- The script assumes the use of a library or method capable of handling image steganography.
- Ensure all dependencies are installed before running the script.
"""

# Importing necessary libraries
import os
from stegano import lsb  # LSB (Least Significant Bit) steganography for hiding/revealing messages
from pycipher import Caesar  # Caesar cipher for encryption and decryption using ROT13

image_path = "images\PRCSE-C2.png"

# Check if the file exists
if os.path.exists(image_path):

    # Reveal the hidden message from an image using LSB steganography
    hidden_message = lsb.reveal(image_path)
    print(f"Encrypted message: {hidden_message}")  # Display the encrypted (hidden) message

    # Decrypt the hidden message using the Caesar cipher with ROT13 (shift key = 13)
    decrypted_message = Caesar(key=13).decipher(hidden_message)
    print(f"Decrypted message: {decrypted_message}")  # Display the decrypted message

else:
    print(f"The image '{image_path}' does not exist.")



