from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

# Verificar se o usuário é superusuário


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'



@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()

            # Validações básicas
            if not name or not email or not password:
                return JsonResponse({'error': 'Todos os campos são obrigatórios.'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Este e-mail já está em uso.'}, status=400)

            # Criar o usuário
            user = User.objects.create_user(
                username=email,  # Usando o e-mail como username
                email=email,
                password=password,
                first_name=name
            )
            user.save()

            return JsonResponse({'message': 'Usuário cadastrado com sucesso!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': f'Erro ao processar o cadastro: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método não permitido.'}, status=405)


