import binascii
from typing import Literal
import base64


class CaesarCipher:
    def __init__(self, key: int, language: Literal['uk', 'en'] = 'en'):
        self.language = language
        # Base64 alphabet includes a-z, A-Z, 0-9, +, /
        self.base64_alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='
        if language == 'en':
            self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        elif language == 'uk':
            self.alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
        else:
            raise ValueError("Unsupported language")
        self.n = len(self.alphabet)
        self.key = self.validate_key(key)

    def validate_key(self, key: int) -> int:
        if not isinstance(key, int):
            raise ValueError("Key must be an integer")
        return key % self.n

    def encrypt(self, text: str) -> str:
        result = []
        for char in text.lower():
            if char in self.alphabet:
                x = self.alphabet.index(char)
                y = (x + self.key) % self.n
                result.append(self.alphabet[y])
            else:
                result.append(char)  # Keep non-alphabetic characters as is
        return ''.join(result)

    def decrypt(self, cipher_text: str) -> str:
        result = []
        for char in cipher_text.lower():
            if char in self.alphabet:
                y = self.alphabet.index(char)
                x = (y - self.key) % self.n
                result.append(self.alphabet[x])
            else:
                result.append(char)  # Keep non-alphabetic characters as is
        return ''.join(result)

    def encrypt_file(self, file_data: bytes) -> str:
        """Encrypt a binary file by first converting it to Base64 and then applying Caesar cipher."""
        base64_encoded = base64.b64encode(file_data).decode('utf-8')
        # Encrypt the Base64 string using the Base64 alphabet
        return self._encrypt_base64(base64_encoded)

    def decrypt_file(self, encrypted_data: str) -> bytes | None:
        """Decrypt a file by first decrypting the Caesar cipher and then decoding from Base64."""
        try:
            # Decrypt the Caesar cipher text
            decrypted_base64 = self._decrypt_base64(encrypted_data)
            # Decode from Base64 to get the original binary data
            return base64.b64decode(decrypted_base64)
        except binascii.Error:
            return None

    def _encrypt_base64(self, text: str) -> str:
        """Encrypts a string with the full Base64 alphabet."""
        result = []
        for char in text:
            if char in self.base64_alphabet:
                x = self.base64_alphabet.index(char)
                y = (x + self.key) % len(self.base64_alphabet)
                result.append(self.base64_alphabet[y])
            else:
                result.append(char)
        return ''.join(result)

    def _decrypt_base64(self, cipher_text: str) -> str:
        """Decrypts a Base64-encoded Caesar cipher text."""
        result = []
        for char in cipher_text:
            if char in self.base64_alphabet:
                y = self.base64_alphabet.index(char)
                x = (y - self.key) % len(self.base64_alphabet)
                result.append(self.base64_alphabet[x])
            else:
                result.append(char)
        return ''.join(result)
