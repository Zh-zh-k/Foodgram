# Generated by Django 2.2.16 on 2023-09-29 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Breakfast', 'Завтрак'), ('Lunch', 'Обед'), ('Dinner', 'Ужин')], max_length=15)),
                ('slug', models.SlugField(unique=True)),
                ('color', models.CharField(default='#ffffff', max_length=7, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(verbose_name='Описание рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.TextField(verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time',
            field=models.DurationField(verbose_name='Время приготовления'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='recipes', to='recipes.Tag', verbose_name='Тэг'),
        ),
    ]