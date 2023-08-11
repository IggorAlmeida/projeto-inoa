# Generated by Django 4.2.4 on 2023-08-11 03:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('bolsa', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preco_maximo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('preco_minimo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tempo_check', models.IntegerField()),
                ('deleteted_at', models.DateTimeField(null=True)),
                ('asset', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='assets.assetlist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]