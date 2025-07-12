from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .forms import CustomUserCreationForm, ContatoForm
from .models import Rifa, NumeroRifa


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
    }
    
    return render(request, 'registration/home.html', context)


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