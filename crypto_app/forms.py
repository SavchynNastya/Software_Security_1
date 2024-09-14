from django import forms
from crypto_app.models import Encryption, File

#
# class FileForm(forms.ModelForm):
#     file_name = forms.CharField(
#         label="File Name",
#         required=False,
#         help_text="Enter a name for the created file (leave blank to upload a file)."
#     )
#     text_content = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 5}),
#         required=False,
#         label="Text Content",
#         help_text="Enter text content to create a new text file (leave blank to upload a file)."
#     )
#     file = forms.FileField(label="File", required=False)
#
#     class Meta:
#         model = File
#         fields = ['file', 'text_content']


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


# class CipherForm(forms.Form):
#     ACTION_CHOICES = [
#         ('encrypt', 'Зашифрувати'),
#         ('decrypt', 'Розшифрувати'),
#         ('bruteforce', 'Атака грубої сили'),
#     ]
#
#     key = forms.IntegerField(label='Ключ', required=True, min_value=0, help_text="Введіть ключ для шифрування/розшифрування.")
#     language = forms.ChoiceField(choices=[('uk', 'Українська'), ('en', 'Англійська')], label="Мова")
#     file = forms.ModelChoiceField(queryset=File.objects.all(), label="Оберіть файл")
#     action = forms.ChoiceField(choices=ACTION_CHOICES, label="Дія")

class CipherForm(forms.Form):
    ACTION_CHOICES = [
        ('encrypt', 'Зашифрувати'),
        ('decrypt', 'Розшифрувати'),
        ('bruteforce', 'Атака грубої сили'),
    ]

    key = forms.IntegerField(
        label='Ключ',
        required=True,
        min_value=0,
        help_text="Введіть ключ для шифрування/розшифрування.",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
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