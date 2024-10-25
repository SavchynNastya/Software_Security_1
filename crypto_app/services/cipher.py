import binascii
from typing import Literal
import base64
from typing import Union, List, Tuple


class TrithemiusCipher:
    def __init__(self, key: Union[List[int], str], language: str = 'en'):
        self.key = self.validate_key(key)
        self.alphabet = self.get_alphabet(language)
        self.n = len(self.alphabet)

    def get_alphabet(self, language: str) -> str:
        """Return the alphabet based on the specified language."""
        if language == 'en':
            return 'abcdefghijklmnopqrstuvwxyz'
        elif language == 'ua':
            return 'абвгґдежзийклмнопрстуфхцчшщьюя'
        else:
            raise ValueError("Unsupported language. Available options: 'en', 'ua'.")

    def validate_key(self, key: Union[List[int], str]) -> Union[List[int], str]:
        """Validate the key provided for the cipher."""
        if isinstance(key, str):
            try:
                key_list = [int(num.strip()) for num in key.split(',')]
                if len(key_list) in [2, 3]:
                    return key_list
                else:
                    raise ValueError("List of coefficients must have 2 or 3 elements.")
            except ValueError:
                if all(char in self.get_alphabet('en') for char in key) or \
                        all(char in self.get_alphabet('ua') for char in key):
                    return key
                else:
                    raise ValueError("Key string contains characters not in the alphabet.")
        elif isinstance(key, list) and len(key) in [2, 3]:
            if all(isinstance(coef, int) for coef in key):
                return key
            else:
                raise ValueError("All coefficients in the vector key must be integers.")
        else:
            raise ValueError("Invalid key format. Use a 2D/3D vector or a string.")


    def encrypt(self, text: str) -> str:
        """Encrypt text using the Trithemius cipher."""
        result = []
        text = text.lower()
        for i, char in enumerate(text):
            if char in self.alphabet:
                x = self.alphabet.index(char)
                shift = self._calculate_shift(i)
                y = (x + shift) % self.n
                result.append(self.alphabet[y])
            else:
                result.append(char)
        return ''.join(result)

    def decrypt(self, cipher_text: str) -> str:
        """Decrypt text using the Trithemius cipher."""
        result = []
        cipher_text = cipher_text.lower()
        for i, char in enumerate(cipher_text):
            if char in self.alphabet:
                y = self.alphabet.index(char)
                shift = self._calculate_shift(i)
                x = (y - shift) % self.n
                result.append(self.alphabet[x])
            else:
                result.append(char)
        return ''.join(result)

    def encrypt_file(self, file_data: bytes) -> str:
        """Encrypt the contents of a file."""
        text = file_data.decode('utf-8')
        return self.encrypt(text)

    def decrypt_file(self, encrypted_data: str) -> bytes:
        """Decrypt the contents of a file and return as bytes."""
        decrypted_text = self.decrypt(encrypted_data)
        return decrypted_text.encode('utf-8')

    def _calculate_shift(self, position: int) -> int:
        """Calculate the shift based on the key type."""
        if isinstance(self.key, list):
            if len(self.key) == 2:
                a, b = self.key
                return a + b * position
            elif len(self.key) == 3:
                a, b, c = self.key
                return a + b * position + c * position**2
        elif isinstance(self.key, str):
            return self.alphabet.index(self.key[position % len(self.key)])
        else:
            raise ValueError("Unknown key format.")


class CaesarCipher:
    def __init__(self, key: Union[int, List[float], str], language: Literal['uk', 'en'] = 'en'):
        self.language = language
        self.base64_alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/='

        if language == 'en':
            self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        elif language == 'uk':
            self.alphabet = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
        else:
            raise ValueError("Unsupported language")

        self.n = len(self.alphabet)
        self.key = self.validate_key(key)

    def validate_key(self, key: Union[int, List[float], str]) -> Union[int, List[int]]:
        if isinstance(key, int):
            return key % self.n
        elif isinstance(key, list) and len(key) in [2, 3]:
            return [int(k) % self.n for k in key]
        elif isinstance(key, str):
            return sum(ord(char) for char in key) % self.n
        else:
            raise ValueError("Key must be an integer, list of coefficients (2D or 3D), or a string.")

    def encrypt(self, text: str) -> str:
        result = []
        for index, char in enumerate(text.lower()):
            if char in self.alphabet:
                x = self.alphabet.index(char)
                shift = self.key[index % len(self.key)] if isinstance(self.key, list) else self.key
                y = (x + shift) % self.n
                result.append(self.alphabet[y])
            else:
                result.append(char)
        return ''.join(result)

    def decrypt(self, cipher_text: str) -> str:
        result = []
        for index, char in enumerate(cipher_text.lower()):
            if char in self.alphabet:
                y = self.alphabet.index(char)
                shift = self.key[index % len(self.key)] if isinstance(self.key, list) else self.key
                x = (y - shift) % self.n
                result.append(self.alphabet[x])
            else:
                result.append(char)
        return ''.join(result)

    def encrypt_file(self, file_data: bytes) -> str:
        """Encrypt a binary file by first converting it to Base64 and then applying Caesar cipher."""
        base64_encoded = base64.b64encode(file_data).decode('utf-8')
        return self._encrypt_base64(base64_encoded)

    def decrypt_file(self, encrypted_data: str) -> bytes | None:
        """Decrypt a file by first decrypting the Caesar cipher and then decoding from Base64."""
        try:
            decrypted_base64 = self._decrypt_base64(encrypted_data)
            return base64.b64decode(decrypted_base64)
        except binascii.Error:
            return None

    def _encrypt_base64(self, text: str) -> str:
        """Encrypts a string with the full Base64 alphabet."""
        result = []
        for index, char in enumerate(text):
            if char in self.base64_alphabet:
                x = self.base64_alphabet.index(char)
                shift = self.key[index % len(self.key)] if isinstance(self.key, list) else self.key
                y = (x + shift) % len(self.base64_alphabet)
                result.append(self.base64_alphabet[y])
            else:
                result.append(char)
        return ''.join(result)

    def _decrypt_base64(self, cipher_text: str) -> str:
        """Decrypts a Base64-encoded Caesar cipher text."""
        result = []
        for index, char in enumerate(cipher_text):
            if char in self.base64_alphabet:
                y = self.base64_alphabet.index(char)
                shift = self.key[index % len(self.key)] if isinstance(self.key, list) else self.key
                x = (y - shift) % len(self.base64_alphabet)
                result.append(self.base64_alphabet[x])
            else:
                result.append(char)
        return ''.join(result)


class BookCipher:
    def __init__(self, key_text: str, rows: int, cols: int):
        self.key_text = list(key_text)
        self.rows = rows
        self.cols = cols
        self.key_grid = self.create_key_grid()

    def create_key_grid(self) -> List[List[str]]:
        """Creates a key grid based on the key text."""
        grid = []
        total_chars = len(self.key_text)

        if total_chars < self.rows * self.cols:
            raise ValueError("Not enough characters to fill the key grid.")

        for i in range(self.rows):
            start_index = i * self.cols
            row = self.key_text[start_index:start_index + self.cols]
            grid.append(row)
        return grid

    def find_coordinates(self, char: str) -> Tuple[int, int]:
        """Finds the coordinates of a character in the key grid."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.key_grid[r][c].lower() == char.lower():
                    return r, c
        return None

    def encrypt(self, plaintext: str) -> str:
        """Encrypts the input text using the key."""
        cipher_text = []
        for char in plaintext:
            coords = self.find_coordinates(char)
            if coords:
                row, col = coords
                cipher_code = f"{row+1:02}/{col+1:02}"
                cipher_text.append(cipher_code)
            else:
                cipher_text.append("??")
        return ', '.join(cipher_text)

    def decrypt(self, cipher_text: str) -> str:
        """Decrypts the encrypted text using the key."""
        decrypted_text = []
        codes = cipher_text.split(', ')
        for code in codes:
            if code == "??":
                decrypted_text.append('?')
                continue

            row, col = map(int, code.split('/'))
            char = self.key_grid[row-1][col-1]
            decrypted_text.append(char)
        return ''.join(decrypted_text)


if __name__ == "__main__":
    key = "На зорі ти не зривай, мій пісню, мій витвір"
    book_cipher = BookCipher(key, rows=3, cols=10)

    text_to_encrypt = "зерно"
    encrypted = book_cipher.encrypt(text_to_encrypt)
    print("Зашифрований текст:", encrypted)

    decrypted = book_cipher.decrypt(encrypted)
    print("Розшифрований текст:", decrypted)
