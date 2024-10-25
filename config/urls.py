from django.urls import path
from crypto_app import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('about/', views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='exit'), name='logout'),
    path('exit/', views.exit_system, name='exit'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('upload/', views.upload_file, name='upload_file'),
    path('process-caesar/', views.caesar_cipher_view, name='process_file_caesar'),
    path('process-trithemius/', views.trithemius_cipher_view, name='process_file_trithemius'),
    path('process-book/', views.book_cipher_view, name='process_book'),
    path('files/', views.file_list, name='file_list'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('print/<int:file_id>/', views.print_file, name='print_file'),
    path('decrypt/<int:file_id>/', views.decrypt_file, name='decrypt_file'),
]
