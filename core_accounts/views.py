from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}!')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    """
    View para a pagina inicial do restaurante.
    Renderiza a homepage com informacoes sobre rifas ativas e dados do contexto.
    """
    context = {
        'rifas_ativas': [
            {
                'titulo': 'Rifa do Mes - Almoco Especial',
                'descricao': 'Concorra a um almoco completo para 4 pessoas!',
                'preco': 'R$ 10,00',
                'data_limite': '2025-08-15'
            },
            {
                'titulo': 'Rifa da Semana - Sobremesa Premium',
                'descricao': 'Torta especial da casa + bebidas',
                'preco': 'R$ 5,00',
                'data_limite': '2025-07-20'
            }
        ],
        'servicos': [
            {
                'nome': 'Presencial',
                'descricao': 'Ambiente acolhedor com vista para o lago',
                'icone': 'restaurant'
            },
            {
                'nome': 'Delivery',
                'descricao': 'Entrega rapida na sua casa',
                'icone': 'delivery_dining'
            },
            {
                'nome': 'Festinhas',
                'descricao': 'Eventos especiais e comemoracoes',
                'icone': 'celebration'
            }
        ],
        'info_contato': {
            'telefone': '(11) 99999-9999',
            'email': 'contato@pescaria.com.br',
            'endereco': 'Rua das Aguas, 123 - Sao Roque, SP'
        }
    }
    
    return render(request, 'registration/home.html', context)