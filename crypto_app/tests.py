import os
from django.test import TestCase
from crypto_app.services.cipher import CaesarCipher
from crypto_app.services.brute_force import BruteForceDecryption


class CaesarCipherFileTest(TestCase):
    def setUp(self):
        """Set up the file paths and the cipher instance."""
        self.input_file = os.path.join(os.path.dirname(__file__), 'test_files', 'test_file1.jpg')
        self.input_file2 = os.path.join(os.path.dirname(__file__), 'test_files', 'test_file2.txt')
        self.encrypted_file = os.path.join(os.path.dirname(__file__), 'test_files', 'encrypted_file.txt')
        self.decrypted_file = os.path.join(os.path.dirname(__file__), 'test_files', 'decrypted_file.jpg')

        # Initialize the CaesarCipher with a key (e.g., 3) and English alphabet
        self.cipher = CaesarCipher(key=3, language='en')

    def _read_file(self, file_path: str) -> bytes:
        """Read the file as binary data."""
        with open(file_path, 'rb') as file:
            return file.read()

    def _write_file(self, file_path: str, data: bytes):
        """Write binary data to a file."""
        with open(file_path, 'wb') as file:
            file.write(data)

    def test_encrypt_decrypt_file_img(self):
        """Test the encryption and decryption of a file."""
        original_file_data = self._read_file(self.input_file)
        self.assertTrue(original_file_data)  # Ensure the file is not empty

        encrypted_data = self.cipher.encrypt_file(original_file_data)
        self.assertTrue(encrypted_data)  # Ensure encryption happened

        decrypted_file_data = self.cipher.decrypt_file(encrypted_data)

        self._write_file(self.decrypted_file, decrypted_file_data)

        self.assertEqual(original_file_data, decrypted_file_data, "Decrypted data does not match the original file")

    def test_encrypt_decrypt_file_txt(self):
        """Test the encryption and decryption of a file."""
        original_file_data = self._read_file(self.input_file2)
        self.assertTrue(original_file_data)  # Ensure the file is not empty

        encrypted_data = self.cipher.encrypt_file(original_file_data)
        self.assertTrue(encrypted_data)  # Ensure encryption happened

        decrypted_file_data = self.cipher.decrypt_file(encrypted_data)

        self._write_file(self.decrypted_file, decrypted_file_data)

        self.assertEqual(original_file_data, decrypted_file_data, "Decrypted data does not match the original file")

    def test_brute_force_decrypt_img(self):
        brute_forcer = BruteForceDecryption(self.cipher)
        original_file_data = self._read_file(self.input_file)
        print(f"ORIGINAL: {original_file_data[:100]}")

        encrypted_data = self.cipher.encrypt_file(original_file_data)
        print(f"ENCR: {encrypted_data[:100]}")
        possibilities = brute_forcer.brute_force_decrypt(encrypted_data, language='base64')

        key_found = None
        for decrypted_data, key in possibilities:
            if decrypted_data == original_file_data:
                key_found = key
                break

        print(f"Correct key found: {key_found}")
        self.assertTrue(bool(key_found), "Brute force decryption did not find the correct solution with the correct key")

    def test_brute_force_decrypt_txt(self):
        brute_forcer = BruteForceDecryption(self.cipher)
        original_file_data = self._read_file(self.input_file2)
        print(f"ORIGINAL: {original_file_data}")

        encrypted_data = self.cipher.encrypt_file(original_file_data)
        print(f"ENCR: {encrypted_data}")
        possibilities = brute_forcer.brute_force_decrypt(encrypted_data, language='en')

        key_found = None
        for decrypted_data, key in possibilities:
            if decrypted_data == original_file_data:
                key_found = key
                break

        print(f"Correct key found: {key_found}")
        self.assertTrue(bool(key_found), "Brute force decryption did not find the correct solution with the correct key")
