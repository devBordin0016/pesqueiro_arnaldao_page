from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .forms import CustomUserCreationForm, ContatoForm
from .models import Rifa, NumeroRifa
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import json


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
    View principal da home page do restaurante.
    Renderiza a homepage com rifas ativas do banco de dados e informacoes do restaurante.
    """
    # Processar formulario de contato se for POST
    contato_form = ContatoForm()
    print(f"DEBUG: contato_form criado = {contato_form}")
    if request.method == 'POST' and 'contato_submit' in request.POST:
        contato_form = ContatoForm(request.POST)
        if contato_form.is_valid():
            # Dados do formulario
            nome = contato_form.cleaned_data['nome']
            email = contato_form.cleaned_data['email']
            telefone = contato_form.cleaned_data['telefone']
            assunto = contato_form.cleaned_data['assunto']
            mensagem = contato_form.cleaned_data['mensagem']
            
            # Enviar email
            try:
                send_mail(
                    subject=f'Contato - {assunto}',
                    message=f'Nome: {nome}\nEmail: {email}\nTelefone: {telefone}\n\nMensagem:\n{mensagem}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['contato@pescaria.com.br'],  # Seu email
                    fail_silently=False,
                )
                messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'Erro ao enviar mensagem. Tente novamente.')

    # Buscar rifas ativas (limitando a 6 para nao sobrecarregar)
    rifas_ativas = Rifa.objects.filter(
        situacao='ativa',
        data_sorteio__gt=timezone.now()
    ).order_by('data_sorteio')[:6]
    
    # Estatisticas gerais
    total_rifas = Rifa.objects.filter(situacao='ativa').count()
    
    # Para a primeira rifa, calcular numeros disponiveis
    rifa_destaque = None
    if rifas_ativas.exists():
        rifa_destaque = rifas_ativas.first()
        numeros_vendidos = list(NumeroRifa.objects.filter(rifa=rifa_destaque).values_list('numero', flat=True))
        numeros_disponiveis = [i for i in range(1, rifa_destaque.total_numeros + 1) if i not in numeros_vendidos]
        # Adicionar aos rifas_ativas para usar no template
        rifa_destaque.numeros_disponiveis = numeros_disponiveis
    
    # Dados estaticos do restaurante
    servicos = [
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
    ]
    
    info_contato = {
        'telefone': '(11) 99999-9999',
        'email': 'contato@pescaria.com.br',
        'endereco': 'Rua das Aguas, 123 - Sao Roque, SP'
    }
    
    context = {
        'rifas_ativas': rifas_ativas,
        'rifa_destaque': rifa_destaque,
        'total_rifas': total_rifas,
        'has_rifas': rifas_ativas.exists(),
        'servicos': servicos,
        'info_contato': info_contato,
        'contato_form': contato_form,  # Adicionar o form
    }
    
    return render(request, 'home.html', context)


def rifa_detail(request, rifa_id):
    """
    View para exibir detalhes de uma rifa especifica
    """
    rifa = get_object_or_404(Rifa, id=rifa_id)
    
    # Verificar se a rifa esta ativa
    if not rifa.is_ativa:
        messages.warning(request, 'Esta rifa nao esta mais disponivel.')
        return redirect('home')
    
    # Buscar numeros ja vendidos
    numeros_vendidos = NumeroRifa.objects.filter(rifa=rifa).values_list('numero', flat=True)
    
    context = {
        'rifa': rifa,
        'numeros_vendidos': list(numeros_vendidos),
        'numeros_disponiveis': [i for i in range(1, rifa.total_numeros + 1) if i not in numeros_vendidos],
    }
    
    return render(request, 'rifa_detail.html', context)


def todas_rifas(request):
    """
    View para exibir todas as rifas ativas
    """
    rifas = Rifa.objects.filter(situacao='ativa').order_by('-created_at')
    
    context = {
        'rifas': rifas,
        'total_rifas': rifas.count(),
    }
    
    return render(request, 'todas_rifas.html', context)


def contato(request):
    """
    View para pagina de contato
    """
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            # Processar o formulario
            # Aqui voce pode enviar email, salvar no banco, etc.
            messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
            return redirect('contato')
    else:
        form = ContatoForm()
    
    return render(request, 'contato.html', {'form': form})

def cardapio_view(request):
    # Dados do cardapio - pode ser movido para models futuramente
    cardapio_data = {
        "Feijoada": [
            {"tamanho": "Individual (executivo)  1 pessoa", "preco": 50.00},
            {"tamanho": "Mini  2 pessoas", "preco": 95.00},
            {"tamanho": "Pequena  3 pessoas", "preco": 130.00},
            {"tamanho": "Media  4 pessoas", "preco": 165.00},
            {"tamanho": "Grande  5 pessoas", "preco": 195.00}
        ],
        "Bacalhau": [
            {"tamanho": "Individual  1 pessoa", "preco": 90.00},
            {"tamanho": "Pequeno  2 pessoas", "preco": 175.00},
            {"tamanho": "Medio  3 pessoas", "preco": 260.00},
            {"tamanho": "Grande  4 pessoas", "preco": 340.00}
        ],
        "Carnes": [
            {"tamanho": "Contra File Acebolado", "preco": 115.00, "preco3": 160.00},
            {"tamanho": "Contra File a Parmegiana", "preco": 140.00, "preco3": 200.00},
            {"tamanho": "Contra File na Chapa", "preco": 120.00, "preco3": 160.00},
            {"tamanho": "Contra File com Legumes", "preco": 120.00, "preco3": 160.00},
            {"tamanho": "Picanha c/ Batata, Brocolis e Alho", "preco": 145.00, "preco3": 200.00},
            {"tamanho": "Costela c/ Mandioca", "preco": 95.00, "preco3": 135.00},
            {"tamanho": "Virado a Paulista", "preco": 120.00, "preco3": 165.00}
        ],
        "Peixes": [
            {"tamanho": "File de Pescada", "preco": 95.00, "preco3": 140.00},
            {"tamanho": "File de Tilapia", "preco": 110.00, "preco3": 145.00},
            {"tamanho": "File de Tilapia a Parmegiana", "preco": 120.00, "preco3": 170.00},
            {"tamanho": "Tilapia Fresca (peixe)", "preco": 110.00, "preco3": 165.00},
            {"tamanho": "Cacao ao Molho c/ Leite de Coco", "preco": 100.00, "preco3": 155.00}
        ],
        "Aves": [
            {"tamanho": "File de Frango Grelhado", "preco": 95.00, "preco3": 140.00},
            {"tamanho": "File de Frango a Milanesa", "preco": 100.00, "preco3": 145.00},
            {"tamanho": "File de Frango a Parmegiana", "preco": 120.00, "preco3": 165.00}
        ],
        "Guarnicoes": [
            {"tamanho": "Arroz Porcao", "preco": 25.00},
            {"tamanho": "Feijao Porcao", "preco": 25.00},
            {"tamanho": "Couve Porcao", "preco": 25.00},
            {"tamanho": "Bisteca Unidade", "preco": 12.00}
        ],
        "Massas": [
            {"tamanho": "Spaghetti (Molho Bolonhesa)  1 pessoa", "preco": 45.00},
            {"tamanho": "Lasanha (Molho Bolonhesa)  1 pessoa", "preco": 50.00}
        ]
    }
    
    # Context para o template
    context = {
        'cardapio': cardapio_data,
        'page_title': 'Cardapio - Pesqueiro Arnaldao',
        'page_description': 'Confira nosso delicioso cardapio com pratos tradicionais e sabores unicos do Pesqueiro Arnaldao.'
    }
    
    return render(request, 'cardapio.html', context)

def cardapio_api_view(request):
    
    # Mesmos dados da view principal
    cardapio_data = {
        "Feijoada": [
            {"tamanho": "Individual (executivo)  1 pessoa", "preco": 50.00},
            {"tamanho": "Mini  2 pessoas", "preco": 95.00},
            {"tamanho": "Pequena  3 pessoas", "preco": 130.00},
            {"tamanho": "Media  4 pessoas", "preco": 165.00},
            {"tamanho": "Grande  5 pessoas", "preco": 195.00}
        ],
        "Bacalhau": [
            {"tamanho": "Individual  1 pessoa", "preco": 90.00},
            {"tamanho": "Pequeno  2 pessoas", "preco": 175.00},
            {"tamanho": "Medio  3 pessoas", "preco": 260.00},
            {"tamanho": "Grande  4 pessoas", "preco": 340.00}
        ],
        "Carnes": [
            {"tamanho": "Contra File Acebolado (2?pessoas)", "preco": 115.00, "preco3": 160.00},
            {"tamanho": "Contra File a Parmegiana", "preco": 140.00, "preco3": 200.00},
            {"tamanho": "Contra File na Chapa", "preco": 120.00, "preco3": 160.00},
            {"tamanho": "Contra File com Legumes", "preco": 120.00, "preco3": 160.00},
            {"tamanho": "Picanha c/ Batata, Brocolis e Alho", "preco": 145.00, "preco3": 200.00},
            {"tamanho": "Costela c/ Mandioca", "preco": 95.00, "preco3": 135.00},
            {"tamanho": "Virado a Paulista", "preco": 120.00, "preco3": 165.00}
        ],
        "Peixes": [
            {"tamanho": "File de Pescada", "preco": 95.00, "preco3": 140.00},
            {"tamanho": "File de Tilapia", "preco": 110.00, "preco3": 145.00},
            {"tamanho": "File de Tilapia a Parmegiana", "preco": 120.00, "preco3": 170.00},
            {"tamanho": "Tilapia Fresca (peixe)", "preco": 110.00, "preco3": 165.00},
            {"tamanho": "Cacao ao Molho c/ Leite de Coco", "preco": 100.00, "preco3": 155.00}
        ],
        "Aves": [
            {"tamanho": "File de Frango Grelhado", "preco": 95.00, "preco3": 140.00},
            {"tamanho": "File de Frango a Milanesa", "preco": 100.00, "preco3": 145.00},
            {"tamanho": "File de Frango a Parmegiana", "preco": 120.00, "preco3": 165.00}
        ],
        "Guarnicoes": [
            {"tamanho": "Arroz Porcao", "preco": 25.00},
            {"tamanho": "Feijao Porcao", "preco": 25.00},
            {"tamanho": "Couve Porcao", "preco": 25.00},
            {"tamanho": "Bisteca Unidade", "preco": 12.00}
        ],
        "Massas": [
            {"tamanho": "Spaghetti (Molho Bolonhesa) 1 pessoa", "preco": 45.00},
            {"tamanho": "Lasanha (Molho Bolonhesa) 1 pessoa", "preco": 50.00}
        ]
    }
    
    return JsonResponse({
        'status': 'success',
        'data': cardapio_data,
        'total_categorias': len(cardapio_data),
        'timestamp': '2024-01-01T00:00:00Z'  # Pode usar timezone.now()
    })