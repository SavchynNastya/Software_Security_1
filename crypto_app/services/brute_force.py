from typing import Literal, Optional, Tuple, List
from crypto_app.services.cipher import CaesarCipher


class BruteForceDecryption:
    def __init__(self, cipher: CaesarCipher):
        self.cipher = cipher

    def brute_force_decrypt(self, cipher_text: str, language: Literal['uk', 'en', 'base64'], known_substring: Optional[str] = None) -> List[Tuple[bytes, int]]:
        """
        Brute-force attack:
            Try all possible keys and return the decrypted binary data
            that matches the original file.
        """
        possibilities = []
        max_key = len(self.cipher.alphabet) if language in ['uk', 'en'] else len(self.cipher.base64_alphabet)

        for key in range(max_key):
            self.cipher.key = key
            decrypted_text = self.cipher.decrypt_file(cipher_text)
            if decrypted_text:
                possibilities.append((decrypted_text, key))
        return possibilities
