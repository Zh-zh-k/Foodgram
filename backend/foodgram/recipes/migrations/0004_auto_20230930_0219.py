# Generated by Django 2.2.16 on 2023-09-29 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Тэг'),
        ),
    ]
