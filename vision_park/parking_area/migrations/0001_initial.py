# Generated by Django 5.0.4 on 2024-05-09 11:02

from string import ascii_uppercase
from django.db import migrations, models


def create_parking_spaces(apps, schema_editor):
    ParkingSpace = apps.get_model('parking_area', 'ParkingSpace')
    for letter in ascii_uppercase[:2]:  # Вибираємо перші дві літери "A" та "B"
        for i in range(1, 11):
            number = f"{letter}{i:02}"  # Форматуємо номер у потрібний формат
            ParkingSpace.objects.create(number=number)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, unique=True)),
                ('is_occupied', models.BooleanField(default=False)),
            ],
        ),
        migrations.RunPython(create_parking_spaces),
    ]