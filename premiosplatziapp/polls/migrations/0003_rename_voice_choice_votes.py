# Generated by Django 4.2.2 on 2023-06-21 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_choices_choice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='voice',
            new_name='votes',
        ),
    ]
