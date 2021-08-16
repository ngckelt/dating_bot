from django.db import models


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        abstract = True


class Questions(TimeBasedModel):
    question = models.CharField(verbose_name="Вопрос", max_length=255)
    answer_options = models.TextField(verbose_name="Варианты ответа. Каждая строка - новый вариант ответа "
                                                   "(точно так же будет выглядеть инлайн меню). "
                                                   "Слово НЕ должно быть больше 32 символов. "
                                                   "Для заполнения НЕ обязательно", blank=True)

    class Meta:
        abstract = True


class UserQuestions(Questions):

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['created_at']
        verbose_name = "Вопрос для опросника о пользователе"
        verbose_name_plural = "Вопросы для опросника о пользователе"


class SearchQuestions(Questions):

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['created_at']
        verbose_name = "Вопрос для опросника для поиска"
        verbose_name_plural = "Вопросы для опросника для поиска"


