# Generated by Django 4.1.3 on 2022-11-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_remove_feedback_user_id_feedback_user_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='user_mail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
