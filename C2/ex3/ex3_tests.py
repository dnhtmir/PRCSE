import unittest
from ex3 import extract_hidden_message  # Importing the function from ex3.py
import os

# Paths for different test cases
image_path = "images/PRCSE-C2.png"
image_not_found = "images/image.png"
image_without_msg = "images/isep.png"

def corruptedImage():
    # This function will corrupt the image by modifying some bytes
    with open(image_path, "rb") as file:
        data = file.read()

    # Corrupt the image by changing a part of the bytes
    corrupted_data = data[:100] + b"CORRUPTED" + data[200:]
    new_img_path = "images/image_corrupted.png"

    # Save the corrupted image
    with open(new_img_path, "wb") as file:
        file.write(corrupted_data)
        
    return new_img_path

def testMultipleScenarios(image):    
    try:
        # Extract the hidden message from the image
        secret_message = extract_hidden_message(image)

        # Check if the secret message was found
        if secret_message:
            print("::: Hidden message found :::")
            print(f"{secret_message}")
        else:
            print("No hidden message found.")
    except Exception as e:
        # Catch all exceptions and print the error
        print(f"Error processing the image: {e}")

def test_encryption_and_decryption(self):
        original_message = "CONGRATULATIONSTHISISPRCSEHIDDENMESSAGE"

        result = extract_hidden_message(image_path)
        assert "Encripted message:" in result
        assert f"Re-encrypt (apply ROT13 again): {original_message}" in result

        assert original_message in result
        print("The re-encripted message (using ROT13) is equal than the original message\n")


def main():
    print('------- TEST 1 : Success test (Valid Image) ---------')
    # Test with the original image that has the hidden message
    testMultipleScenarios(image_path)

    print('\n\n------- TEST 2 : Image not found ---------')
    # Test with an image path that doesn't exist
    testMultipleScenarios(image_not_found)

    print('\n\n------- TEST 3 : Corrupted image ---------')
    # Create a corrupted version of the image and test it
    new_img_path = corruptedImage()
    testMultipleScenarios(new_img_path)

    print('\n\n------- TEST 4 : Image with no hidden message ---------')
    # Test with an image that has no hidden message (could be a valid image with no hidden content)
    testMultipleScenarios(image_without_msg)  # Example: if no message is hidden, this will print "No hidden message found."


    print('\n\n------- TEST 5 : Check if the re-encrypted message is same than original message ---------')
    test_encryption_and_decryption(new_img_path)

if __name__ == "__main__":
    main()
