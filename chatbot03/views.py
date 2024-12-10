import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from langchain_groq import ChatGroq
from markdown import markdown

from chatbot03.models import Chat


# Configuração da chave de API para o modelo Groq
os.environ['GROQ_API_KEY'] = settings.GROQ_API_KEY


def get_chat_history(chats):
    """
    Recupera o histórico de mensagens no formato necessário para a IA.

    Args:
        chats: Queryset de objetos Chat.

    Returns:
        Lista de tuplas contendo as mensagens no formato ('role', 'message').
    """
    return [
        ('human', chat.message) if chat.message else ('ai', chat.response)
        for chat in chats
    ]


def save_chat_history(user, messages):
    """
    Salva o histórico de mensagens no banco de dados.

    Args:
        user: Usuário autenticado.
        messages: Lista de mensagens no formato [('role', 'message')].
    """
    for role, content in messages:
        if role == 'human':
            Chat.objects.create(user=user, message=content, response="")
        elif role == 'ai':
            Chat.objects.create(user=user, message="", response=content)


def ask_ai(context, message):
    """
    Consulta o modelo de IA com o contexto e a mensagem do usuário.

    Args:
        context: Histórico de mensagens.
        message: Mensagem atual do usuário.

    Returns:
        Resposta da IA em formato HTML (Markdown renderizado).
    """
    model = ChatGroq(model='llama-3.2-90b-vision-preview')
    messages = [
        (
            'system',
            'Simule um humano filósofo, escritor, poeta, naturalista, coerente, pensador e sensato. '
            'Tenha base nos livros de história e filosofia. Responda em formato markdown.',
        )
    ]
    messages.extend(context)
    messages.append(('human', message))
    
    print(messages)  # Para debug
    response = model.invoke(messages)
    return markdown(response.content, output_format='html')


@login_required
def chatbot(request):
    """
    Gerencia o fluxo do chatbot, incluindo salvar mensagens e exibir o histórico.

    Args:
        request: Objeto de solicitação HTTP.

    Returns:
        Resposta JSON ou renderização da página do chatbot.
    """
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        # Recupera o histórico de mensagens anteriores
        context = get_chat_history(chats)
        message = request.POST.get('message')

        # Obtém a resposta da IA
        response = ask_ai(context, message)

        # Salva a mensagem atual e a resposta no histórico
        save_chat_history(
            user=request.user,
            messages=[
                ('human', message),
                ('ai', response),
            ]
        )

        return JsonResponse({
            'message': message,
            'response': response,
        })

    # Renderiza a página inicial do chatbot com o histórico
    return render(request, 'chatbot.html', {'chats': chats})
