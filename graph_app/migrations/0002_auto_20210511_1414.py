# Generated by Django 3.1.7 on 2021-05-11 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteractiveModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companycode', models.CharField(max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name='Graphs',
        ),
    ]
