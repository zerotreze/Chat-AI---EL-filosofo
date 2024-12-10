from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # URLs padrão para autenticação
    path('chat/', include('chatbot03.urls')),  # Rotas do chatbot
]
