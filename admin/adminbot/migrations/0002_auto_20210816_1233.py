# Generated by Django 3.1.8 on 2021-08-16 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('question', models.CharField(max_length=255, verbose_name='Вопрос')),
                ('answer_options', models.TextField(blank=True, verbose_name='Варианты ответа. Каждая строка - новый вариант ответа (точно так же будет выглядеть инлайн меню). Слово НЕ должно быть больше 32 символов. Для заполнения НЕ обязательно')),
            ],
            options={
                'verbose_name': 'Вопрос для опросника для поиска',
                'verbose_name_plural': 'Вопросы для опросника для поиска',
                'ordering': ['created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='userquestions',
            options={'ordering': ['created_at'], 'verbose_name': 'Вопрос для опросника о пользователе', 'verbose_name_plural': 'Вопросы для опросника о пользователе'},
        ),
        migrations.AlterField(
            model_name='userquestions',
            name='answer_options',
            field=models.TextField(blank=True, verbose_name='Варианты ответа. Каждая строка - новый вариант ответа (точно так же будет выглядеть инлайн меню). Слово НЕ должно быть больше 32 символов. Для заполнения НЕ обязательно'),
        ),
    ]
