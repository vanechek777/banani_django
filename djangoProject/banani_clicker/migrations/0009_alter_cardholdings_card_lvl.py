# Generated by Django 5.1.3 on 2024-11-18 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banani_clicker', '0008_delete_level_cards_card_lvl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardholdings',
            name='card_lvl',
            field=models.IntegerField(default=0),
        ),
    ]
