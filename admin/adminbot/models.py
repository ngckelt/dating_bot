from django.db import models


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        abstract = True


class UserQuestions(TimeBasedModel):
    question = models.CharField(verbose_name="Вопрос", max_length=255)
    answer_options = models.TextField(verbose_name="Варианты ответа. Каждая строка - новый вариант ответа "
                                                   "(точно так же будет вышлядеть инлайн меню). "
                                                   "Слово НЕ должно быть больше 32 символов. "
                                                   "Для заполнения не обязательно", blank=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Вопросы для опросника о пользователе"




