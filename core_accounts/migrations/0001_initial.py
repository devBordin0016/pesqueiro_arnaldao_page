# Generated by Django 5.2.4 on 2025-07-12 03:37

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contato",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100, verbose_name="Nome")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                (
                    "telefone",
                    models.CharField(
                        blank=True, max_length=20, verbose_name="Telefone"
                    ),
                ),
                ("assunto", models.CharField(max_length=200, verbose_name="Assunto")),
                ("mensagem", models.TextField(verbose_name="Mensagem")),
                (
                    "data_envio",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data de envio"
                    ),
                ),
                (
                    "respondido",
                    models.BooleanField(default=False, verbose_name="Respondido"),
                ),
            ],
            options={
                "verbose_name": "Contato",
                "verbose_name_plural": "Contatos",
                "ordering": ["-data_envio"],
            },
        ),
        migrations.CreateModel(
            name="Rifa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=200, verbose_name="Titulo")),
                ("descricao", models.TextField(verbose_name="Descricao")),
                (
                    "preco",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Preco por numero"
                    ),
                ),
                (
                    "total_numeros",
                    models.IntegerField(
                        default=100,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10000),
                        ],
                        verbose_name="Total de numeros",
                    ),
                ),
                ("data_sorteio", models.DateTimeField(verbose_name="Data do sorteio")),
                (
                    "situacao",
                    models.CharField(
                        choices=[
                            ("ativa", "Ativa"),
                            ("finalizada", "Finalizada"),
                            ("cancelada", "Cancelada"),
                        ],
                        default="ativa",
                        max_length=20,
                        verbose_name="Situacao",
                    ),
                ),
                (
                    "premio",
                    models.CharField(blank=True, max_length=500, verbose_name="Premio"),
                ),
                (
                    "imagem",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="rifas/",
                        verbose_name="Imagem da rifa",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criado em"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Atualizado em"),
                ),
            ],
            options={
                "verbose_name": "Rifa",
                "verbose_name_plural": "Rifas",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="NumeroRifa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero", models.IntegerField(verbose_name="Numero")),
                (
                    "comprador_nome",
                    models.CharField(max_length=100, verbose_name="Nome do comprador"),
                ),
                (
                    "comprador_telefone",
                    models.CharField(
                        max_length=20, verbose_name="Telefone do comprador"
                    ),
                ),
                (
                    "comprador_email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        verbose_name="Email do comprador",
                    ),
                ),
                (
                    "data_compra",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data da compra"
                    ),
                ),
                ("pago", models.BooleanField(default=False, verbose_name="Pago")),
                (
                    "usuario",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuario (se logado)",
                    ),
                ),
                (
                    "rifa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="numerorifas",
                        to="core_accounts.rifa",
                        verbose_name="Rifa",
                    ),
                ),
            ],
            options={
                "verbose_name": "Numero da Rifa",
                "verbose_name_plural": "Numeros das Rifas",
                "ordering": ["numero"],
                "unique_together": {("rifa", "numero")},
            },
        ),
    ]
