# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-14 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('deposit', 'Deposito'), ('pagseguro', 'PagSeguro'), ('paypal', 'Paypal')], default='deposit', max_length=20, verbose_name='Opcao de Pagamento'),
        ),
    ]
