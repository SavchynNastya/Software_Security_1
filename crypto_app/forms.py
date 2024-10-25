from django import forms
from crypto_app.models import File


class FileForm(forms.ModelForm):
    file_name = forms.CharField(
        label="File Name",
        required=False,
        help_text="Enter a name for the created file (leave blank to upload a file).",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter file name'
        })
    )
    text_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter text content'
        }),
        required=False,
        label="Text Content",
        help_text="Enter text content to create a new text file (leave blank to upload a file)."
    )
    file = forms.FileField(
        label="File",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = File
        fields = ['file', 'text_content', 'file_name']


class CipherForm(forms.Form):
    ACTION_CHOICES = [
        ('encrypt', 'Зашифрувати'),
        ('decrypt', 'Розшифрувати'),
        ('bruteforce', 'Атака грубої сили'),
    ]

    key = forms.CharField(
        label='Ключ',
        required=False,
        help_text="Введіть ключ для шифрування/розшифрування. Можна ввести ціле число, рядок або список (наприклад, '[1, 2]')",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    language = forms.ChoiceField(
        choices=[('uk', 'Українська'), ('en', 'Англійська')],
        label="Мова",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    file = forms.ModelChoiceField(
        queryset=File.objects.all(),
        label="Оберіть файл",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        label="Дія",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_key(self):
        key_input = self.cleaned_data['key']

        try:
            return int(key_input)
        except ValueError:
            pass

        if key_input.startswith('[') and key_input.endswith(']'):
            try:
                key_list = eval(key_input)
                if isinstance(key_list, list) and len(key_list) in [2, 3]:
                    return key_list
            except (SyntaxError, ValueError):
                raise forms.ValidationError("Invalid list format.")

        return key_input


class TrithemiusCipherForm(forms.Form):
    ACTION_CHOICES = [
        ('encrypt', 'Зашифрувати'),
        ('decrypt', 'Розшифрувати'),
        ('attack', 'Brute Force Атака')
    ]

    key = forms.CharField(
        label="Ключ",
        required=False,
        max_length=100,
        help_text="Введіть ключ для шифру Тритеміуса. Для 2D/3D вектора — через кому (a,b або a,b,c). Для текстового гасла — звичайний текст."
    )
    language = forms.ChoiceField(
        choices=[('ua', 'Українська'), ('en', 'Англійська')],
        label="Мова",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    file = forms.ModelChoiceField(
        queryset=File.objects.all(),
        label="Оберіть файл",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    action = forms.ChoiceField(
        label="Дія",
        choices=ACTION_CHOICES
    )


class BookCipherForm(forms.Form):
    action = forms.ChoiceField(choices=[
        ('encrypt', 'Encrypt'),
        ('decrypt', 'Decrypt'),
    ])
    key = forms.CharField(widget=forms.Textarea, label='Key Text')
    plaintext = forms.CharField(widget=forms.Textarea, required=False, label='Plaintext (for encryption)')
    ciphertext = forms.CharField(widget=forms.Textarea, required=False, label='Ciphertext (for decryption)')
    rows = forms.IntegerField(label='Rows', min_value=1, initial=3)
    cols = forms.IntegerField(label='Cols', min_value=1, initial=10)
