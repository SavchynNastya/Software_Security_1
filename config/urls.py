from django.urls import path
from crypto_app import views


urlpatterns = [
    # # path('encrypt/', views.encrypt_file, name='encrypt_file'),
    # # path('decrypt/', views.decrypt_file, name='decrypt_file'),
    path('about/', views.about, name='about'),
    path('exit/', views.exit_system, name='exit'),
    # # path('brute_force/', views.brute_force_attack, name='brute_force'),
    # path('cipher/', views.cipher_view, name='cipher'),

    path('upload/', views.upload_file, name='upload_file'),
    path('process/', views.cipher_view, name='process_file'),
    path('files/', views.file_list, name='file_list'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('print/<int:file_id>/', views.print_file, name='print_file'),
    path('decrypt/<int:file_id>/', views.decrypt_file, name='decrypt_file'),
]
