import uuid
import base64
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import File
from .forms import FileForm
from crypto_app.services.cipher import CaesarCipher
from crypto_app.forms import CipherForm
from crypto_app.models import Encryption
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from crypto_app.services.brute_force import BruteForceDecryption
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html')


def exit_system(request):
    return render(request, 'exit.html')


@login_required(login_url='login')
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            if form.cleaned_data['text_content']:
                text_content = form.cleaned_data['text_content']
                file_name = form.cleaned_data['file_name'] if form.cleaned_data['file_name'] else uuid.uuid4()
                file_instance.file.save(f'{file_name}.txt', ContentFile(text_content))
                file_instance.save()
            else:
                file_instance.save()

            return redirect('file_list')
    else:
        form = FileForm()

    return render(request, 'upload.html', {'form': form})


@login_required(login_url='login')
def cipher_view(request):
    result = None
    action = 'encrypt'
    if request.method == 'POST':
        form = CipherForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            language = form.cleaned_data['language']
            file_instance = form.cleaned_data['file']
            action = form.cleaned_data['action']

            cipher = CaesarCipher(key=key, language=language)
            brute_forcer = BruteForceDecryption(cipher)

            file_data = file_instance.file.read()

            if action == 'encrypt':
                processed_data = cipher.encrypt_file(file_data)
                encrypted_file_instance = Encryption(
                    file=file_instance,
                    encrypted_content=processed_data,
                    language=language,
                    key=key
                )
                encrypted_file_instance.save()
                result = processed_data
            elif action == 'decrypt':
                decrypted_data = cipher.decrypt_file(file_data.decode('utf-8'))
                result = decrypted_data.decode('utf-8')
            elif action == 'bruteforce':
                possible_texts = brute_forcer.brute_force_decrypt(cipher_text=file_data.decode('utf-8'), language=language)
                result = possible_texts
    else:
        form = CipherForm()

    return render(request, 'process.html', {'form': form, 'result': result, 'action': action})


@login_required(login_url='login')
def file_list(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})


@login_required(login_url='login')
def download_file(request, file_id):
    file_instance = File.objects.get(id=file_id)
    response = HttpResponse(file_instance.file.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    return response


@login_required(login_url='login')
def decrypt_file(request, file_id):
    file_instance = File.objects.get(id=file_id)
    cipher = CaesarCipher(key=3, language='en')
    with open(file_instance.file.path, 'rb') as file:
        encrypted_data = file.read()
        encrypted_data_str = base64.b64encode(encrypted_data).decode('utf-8')
        decrypted_data_str = cipher.decrypt_file(encrypted_data_str)

        decrypted_data = base64.b64decode(decrypted_data_str)

        response = HttpResponse(decrypted_data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="decrypted_{file_instance.filename}"'
        return response


@login_required(login_url='login')
def print_file(request, file_id):
    encryption_instance = Encryption.objects.filter(file_id=file_id).last()
    content_to_print = encryption_instance.encrypted_content if encryption_instance else ""

    html_content = render_to_string('print_template.html', {'content': content_to_print})
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="file_{file_id}.pdf"'
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
