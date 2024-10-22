# Generated by Django 5.1.1 on 2024-10-22 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_manual_imagem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manual',
            name='imagem',
        ),
        migrations.CreateModel(
            name='ImagemManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='manuais/')),
                ('descricao', models.CharField(blank=True, max_length=200, null=True)),
                ('manual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='chat.manual')),
            ],
        ),
    ]