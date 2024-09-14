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

    # def brute_force_decrypt(self, cipher_text: str, language: Literal['uk', 'en', 'base64']) -> Optional[Tuple[bytes, int]]:
    #     """
    #     Brute-force attack:
    #         Try all possible keys and return the decrypted binary data
    #         that matches the original file.
    #     """
    #     max_key = len(self.alphabet) if language in ['uk', 'en'] else len(self.base64_alphabet)
    #
    #     for key in range(max_key):
    #         self.key = key
    #         decrypted_text = self.decrypt(cipher_text) if language in ['uk', 'en'] else self._decrypt_base64(cipher_text)
    #
    #         # For Base64, check if it's a valid Base64 encoding (optional)
    #         if language == 'base64':
    #             try:
    #                 # Try to decode the Base64; if it's valid, return the decrypted binary data
    #                 decrypted_data = base64.b64decode(decrypted_text)
    #                 return decrypted_data, key
    #             except Exception:
    #                 continue
    #
    #         # If decrypted text is valid or matches the known substring
    #         if language in ['uk', 'en']:
    #             return decrypted_text.encode(), key  # Convert to bytes
    #
    #     return None


# def brute_force_decrypt(self, cipher_text: str, language: Literal['uk', 'en'], known_substring: Optional[str] = None) -> Optional[int]:
    #     """
    #     Brute-force attack:
    #         Try all possible keys and return the one that
    #         produces readable text or matches a known substring.
    #     """
    #     max_key = len(self.alphabet) if language != 'base64' else len(self.base64_alphabet)
    #
    #     for key in range(max_key):
    #         self.key = key
    #         decrypted_text = self.decrypt(cipher_text) if language in ['uk', 'en'] else self._decrypt_base64(cipher_text)
    #
    #         # If a known substring is provided, return the key if it matches
    #         if known_substring and known_substring.lower() in decrypted_text:
    #             return key
    #
    #         # For Base64, check if it's a valid Base64 encoding (optional)
    #         if language == 'base64':
    #             try:
    #                 # Try to decode the Base64; if it's valid, return the key
    #                 base64.b64decode(decrypted_text)
    #                 return key
    #             except Exception:
    #                 continue
    #     return None
    #

# class CaesarCipher:
#     def __init__(self, key: int, language: Literal['uk', 'en'] = 'en'):
#         self.language = language
#         if language == 'en':
#             self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
#         elif language == 'uk':
#             self.alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
#         else:
#             raise ValueError("Unsupported language")
#         self.n = len(self.alphabet)
#         self.key = self.validate_key(key)
#
#     def validate_key(self, key: int) -> int:
#         """Валідує ключ, щоб він знаходився в допустимому діапазоні."""
#         if not isinstance(key, int):
#             raise ValueError("Ключ має бути цілим числом")
#         return key % self.n
#
#     def encrypt(self, text: str) -> str:
#         result = []
#         for char in text.lower():
#             if char in self.alphabet:
#                 x = self.alphabet.index(char)
#                 y = (x + self.key) % self.n
#                 result.append(self.alphabet[y])
#             else:
#                 result.append(char)  # Якщо символ не в алфавіті, залишаємо як є
#         return ''.join(result)
#
#     def decrypt(self, cipher_text: str) -> str:
#         # Ensure cipher_text is a string, and handle bytes input gracefully
#         if isinstance(cipher_text, bytes):
#             cipher_text = cipher_text.decode('utf-8')  # Decode bytes to string
#
#         result = []
#         for char in cipher_text.lower():
#             if isinstance(char, str) and char in self.alphabet:  # Ensure char is a string and in alphabet
#                 y = self.alphabet.index(char)
#                 x = (y - self.key) % self.n
#                 result.append(self.alphabet[x])
#             else:
#                 result.append(char)  # Keep non-alphabetic characters as is
#         return ''.join(result)
#
#     def brute_force(self, cipher_text: str) -> list[str]:
#         possibilities = []
#         for k in range(self.n):
#             self.key = k
#             possibilities.append(self.decrypt(cipher_text))
#         return possibilities
#
#     def encrypt_file(self, file_data: bytes) -> str:
#         base64_encoded = base64.b64encode(file_data).decode('utf-8')
#         return self.encrypt(base64_encoded)
#
#     def decrypt_file(self, encrypted_data: str) -> bytes:
#         decrypted_data = self.decrypt(encrypted_data)
#         # # return decrypted_data
#         # print(decrypted_data)
#         return base64.b64decode(decrypted_data)
