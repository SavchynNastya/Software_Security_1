class TrithemiusAttack:
    def __init__(self, language='en'):
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz' if language == 'en' else 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
        self.n = len(self.alphabet)

    def validate_key(self, key: list) -> bool:
        """
        Перевірка валідності ключа.
        :param key: Список зсувів ключа.
        :return: True, якщо ключ валідний, інакше False.
        """
        return all(isinstance(shift, int) and 0 <= shift < self.n for shift in key)

    def validate_text(self, text: str) -> bool:
        """
        Перевірка тексту на наявність символів з алфавіту.
        :param text: Текст для перевірки.
        :return: True, якщо текст валідний, інакше False.
        """
        return all(char.lower() in self.alphabet for char in text if char.isalpha())

    def find_key(self, plaintext: str, ciphertext: str) -> list:
        """
        Find shifts for each pair of characters.
        :param plaintext: The plaintext.
        :param ciphertext: The ciphertext.
        :return: A list of shifts for each character pair.
        """
        if not (self.validate_text(plaintext) and self.validate_text(ciphertext)):
            raise ValueError("Plaintext and ciphertext must only contain valid alphabet characters.")

        shifts = []
        for pt_char, ct_char in zip(plaintext, ciphertext):
            if pt_char.lower() in self.alphabet and ct_char.lower() in self.alphabet:
                pt_index = self.alphabet.index(pt_char.lower())
                ct_index = self.alphabet.index(ct_char.lower())

                shift = (ct_index - pt_index) % self.n
                shifts.append(shift)
            else:
                shifts.append(None)

        return shifts

    def reconstruct_text(self, shifts: list, ciphertext: str) -> str:
        """
        Reconstruct the decrypted text using the found shifts and ciphertext.
        :param shifts: List of shifts.
        :param ciphertext: The ciphertext to decrypt.
        :return: The decrypted text.
        """
        decrypted_text = []
        shift_idx = 0

        for char in ciphertext:
            if char.lower() in self.alphabet:
                if shift_idx < len(shifts) and shifts[shift_idx] is not None:
                    shift_value = shifts[shift_idx]
                    ct_index = self.alphabet.index(char.lower())

                    shifted_index = (ct_index - shift_value) % self.n
                    decrypted_char = self.alphabet[shifted_index]
                    decrypted_text.append(decrypted_char if char.islower() else decrypted_char.upper())

                    shift_idx += 1
                else:
                    decrypted_text.append(char)
                    shift_idx += 1
            else:
                decrypted_text.append(char)
                shift_idx += 1

        return ''.join(decrypted_text)
