from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Rifa(models.Model):
    """
    Modelo para representar uma rifa do restaurante/pesqueiro
    """
    SITUACAO_CHOICES = [
        ('ativa', 'Ativa'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Titulo')
    descricao = models.TextField(verbose_name='Descricao')
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Preco por numero'
    )
    total_numeros = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        verbose_name='Total de numeros'
    )
    data_sorteio = models.DateTimeField(verbose_name='Data do sorteio')
    situacao = models.CharField(
        max_length=20,
        choices=SITUACAO_CHOICES,
        default='ativa',
        verbose_name='Situacao'
    )
    premio = models.CharField(max_length=500, verbose_name='Premio', blank=True)
    imagem = models.ImageField(
        upload_to='rifas/',
        blank=True,
        null=True,
        verbose_name='Imagem da rifa'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Rifa'
        verbose_name_plural = 'Rifas'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.titulo
    
    @property
    def is_ativa(self):
        """Verifica se a rifa esta ativa e nao passou da data de sorteio"""
        return self.situacao == 'ativa' and self.data_sorteio > timezone.now()
    
    @property
    def numeros_vendidos_count(self):
        """Retorna a quantidade de numeros vendidos"""
        return self.numerorifas.count()
    
    @property
    def numeros_disponiveis_count(self):
        """Retorna a quantidade de numeros disponiveis"""
        return self.total_numeros - self.numeros_vendidos_count
    
    @property
    def percentual_vendido(self):
        """Retorna o percentual de numeros vendidos"""
        if self.total_numeros == 0:
            return 0
        return (self.numeros_vendidos_count / self.total_numeros) * 100


class NumeroRifa(models.Model):
    """
    Modelo para representar a compra de um numero especifico de uma rifa
    """
    rifa = models.ForeignKey(
        Rifa,
        on_delete=models.CASCADE,
        related_name='numerorifas',
        verbose_name='Rifa'
    )
    numero = models.IntegerField(verbose_name='Numero')
    comprador_nome = models.CharField(max_length=100, verbose_name='Nome do comprador')
    comprador_telefone = models.CharField(
        max_length=20, 
        verbose_name='Telefone do comprador'
    )
    comprador_email = models.EmailField(
        blank=True, 
        null=True, 
        verbose_name='Email do comprador'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario (se logado)'
    )
    data_compra = models.DateTimeField(auto_now_add=True, verbose_name='Data da compra')
    pago = models.BooleanField(default=False, verbose_name='Pago')
    
    class Meta:
        verbose_name = 'Numero da Rifa'
        verbose_name_plural = 'Numeros das Rifas'
        unique_together = ['rifa', 'numero']  # Garante que o mesmo numero nao seja vendido duas vezes
        ordering = ['numero']
    
    def __str__(self):
        return f'Numero {self.numero} - {self.rifa.titulo}'
    
    def clean(self):
        """Validacao personalizada"""
        from django.core.exceptions import ValidationError
        
        if self.numero < 1 or self.numero > self.rifa.total_numeros:
            raise ValidationError(
                f'Numero deve estar entre 1 e {self.rifa.total_numeros}'
            )


class Contato(models.Model):
    """
    Modelo para armazenar mensagens de contato
    """
    nome = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='Email')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    assunto = models.CharField(max_length=200, verbose_name='Assunto')
    mensagem = models.TextField(verbose_name='Mensagem')
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name='Data de envio')
    respondido = models.BooleanField(default=False, verbose_name='Respondido')
    
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['-data_envio']
    
    def __str__(self):
        return f'{self.nome} - {self.assunto}'