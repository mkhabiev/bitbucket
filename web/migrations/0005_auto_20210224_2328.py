# Generated by Django 3.1.5 on 2021-02-24 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0004_auto_20210224_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='group',
            field=models.CharField(choices=[('pc', 'PersonalComputer'), ('phone', 'Phone'), ('laptop', 'Laptop'), ('acc', 'Accessory')], default='phone', max_length=20),
        ),
        migrations.CreateModel(
            name='ConfirmationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('valid_until', models.DateTimeField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
