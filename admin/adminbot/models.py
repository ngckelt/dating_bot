from django.db import models


class TimeBasedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        abstract = True


class Users(TimeBasedModel):
    telegram_id = models.CharField(verbose_name="ID в телеграмме", max_length=20)
    name = models.CharField(verbose_name="Имя", max_length=255)
    age = models.CharField(verbose_name="Возраст", max_length=2)
    nationality = models.CharField(verbose_name="Национальность", max_length=255)
    education = models.CharField(verbose_name="Образование", max_length=255)
    education_city = models.CharField(verbose_name="Город, где получал образование", max_length=255)
    city = models.CharField(verbose_name="Город текущего проживания", max_length=255)
    profession = models.CharField(verbose_name="Профессия", max_length=255)
    marital_status = models.CharField(verbose_name="Семейное положение", max_length=255)
    has_car = models.CharField(verbose_name="Есть ли автомобиль", max_length=255)
    has_own_housing = models.CharField(verbose_name="Есть ли собственное жилье", max_length=255)
    has_children = models.CharField(verbose_name="Есть ли дети", max_length=255)

    def __str__(self):
        return self.telegram_id

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Questions(TimeBasedModel):
    question = models.CharField(verbose_name="Вопрос", max_length=255)
    answer_options = models.TextField(verbose_name="Варианты ответа. Каждая строка - новый вариант ответа "
                                                   "(точно так же будет выглядеть инлайн меню). "
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


class Questionnaires(TimeBasedModel):
    user = models.ForeignKey(Users, verbose_name="Пользователь", on_delete=models.CASCADE)
    age_range = models.CharField(verbose_name="Диапазон возраста", max_length=7)
    nationality = models.CharField(verbose_name="Национальность", max_length=255)
    education = models.CharField(verbose_name="Образование", max_length=255)
    education_city = models.CharField(verbose_name="Город, где получал образование", max_length=255)
    city = models.CharField(verbose_name="Город текущего проживания", max_length=255)
    profession = models.CharField(verbose_name="Чем должен заниматься", max_length=255)
    marital_status = models.CharField(verbose_name="Семейное положение", max_length=255)
    has_car = models.CharField(verbose_name="Должен ли быть автомобиль", max_length=255)
    has_own_housing = models.CharField(verbose_name="Должно ли быть собственное жилье", max_length=255)
    has_children = models.CharField(verbose_name="Могут ли быть дети", max_length=255)

    def __str__(self):
        return f"Анкета пользователя {self.user}"

    class Meta:
        verbose_name = "Анкета для поиска"
        verbose_name_plural = "Анкеты для поиска"




