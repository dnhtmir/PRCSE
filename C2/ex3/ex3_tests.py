import unittest
from ex3 import extract_hidden_message  # Importing the function from ex3.py
import os

class TestSteganography(unittest.TestCase):
    """Test suite for steganography message extraction"""
    
    def setUp(self):
        """Initialize test paths and create corrupted test image"""
        self.image_path = "images/PRCSE-C2.png"
        self.image_not_found = "images/image.png"
        self.image_without_msg = "images/isep.png"
        self.corrupted_image_path = self._create_corrupted_image()

    def _create_corrupted_image(self):
        """Create a corrupted version of the test image"""
        with open(self.image_path, "rb") as file:
            data = file.read()

        corrupted_data = data[:100] + b"CORRUPTED" + data[200:]
        new_img_path = "images/image_corrupted.png"

        with open(new_img_path, "wb") as file:
            file.write(corrupted_data)
            
        return new_img_path

    def test_1_valid_image(self):
        """Test extraction from valid image with hidden message"""
        print('\n------- TEST 1 : Success test (Valid Image) ---------')
        result = extract_hidden_message(self.image_path)
        if result:
            print("::: Hidden message found :::")
            print(f"{result}")
        self.assertIsNotNone(result)
        self.assertIn("CONGRATULATIONSTHISISPRCSEHIDDENMESSAGE", result)

    def test_2_image_not_found(self):
        """Test handling of non-existent image"""
        print('\n------- TEST 2 : Image not found ---------')
        try:
            extract_hidden_message(self.image_not_found)
        except Exception as e:
            print(f"Error processing the image: {e}")

    def test_3_corrupted_image(self):
        """Test handling of corrupted image"""
        print('\n------- TEST 3 : Corrupted image ---------')
        try:
            extract_hidden_message(self.corrupted_image_path)
        except Exception as e:
            print(f"Error processing the image: {e}")

    def test_4_image_without_message(self):
        """Test image without hidden message"""
        print('\n------- TEST 4 : Image with no hidden message ---------')
        try:
            result = extract_hidden_message(self.image_without_msg)
            if not result:
                print("No hidden message found.")
            self.assertIn("No hidden message found", result)
        except Exception:
            print(f"No hidden message found.")

    def test_5_encryption_decryption(self):
        """Test if re-encryption matches original message"""
        print('\n------- TEST 5 : Check if the re-encrypted message is same than original message ---------')
        original_message = "CONGRATULATIONSTHISISPRCSEHIDDENMESSAGE"
        result = extract_hidden_message(self.image_path)
        
        self.assertIn("Encripted message:", result)
        self.assertIn(f"Re-encrypt (apply ROT13 again): {original_message}", result)
        self.assertIn(original_message, result)
        print("The re-encripted message (using ROT13) is equal than the original message\n")

    def tearDown(self):
        """Clean up corrupted test image"""
        if os.path.exists(self.corrupted_image_path):
            os.remove(self.corrupted_image_path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
