from django.db import models


class File(models.Model):
    file = models.FileField(upload_to='files/')  # Поле для зберігання файлу
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Дата завантаження файлу

    def __str__(self):
        return self.file.name

    def get_file_type(self):
        """Метод для отримання типу файлу."""
        return self.file.url.split('.')[-1]

    def get_file_size(self):
        """Метод для отримання розміру файлу в байтах."""
        return self.file.size


class Encryption(models.Model):
    class LangChoices(models.TextChoices):
        UKRAINIAN = ('uk', 'Ukrainian')
        ENGLISH = ('en', 'English')

    file = models.ForeignKey(File, on_delete=models.CASCADE)
    encrypted_content = models.TextField(blank=True)
    decrypted_content = models.TextField(blank=True)
    language = models.CharField(max_length=10, choices=LangChoices)
    key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
