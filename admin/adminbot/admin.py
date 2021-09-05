from django.contrib import admin
from . import models


class UserQuestionsAdmin(admin.ModelAdmin):
    pass


class SearchQuestionsAdmin(admin.ModelAdmin):
    pass


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username', 'telegram_id']

    class Meta:
        model = models.Users


class QuestionnairesAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__telegram_id']

    class Meta:
        model = models.Questionnaires


admin.site.register(models.UserQuestions, UserQuestionsAdmin)
admin.site.register(models.SearchQuestions, SearchQuestionsAdmin)
admin.site.register(models.Users, UsersAdmin)
admin.site.register(models.Questionnaires, QuestionnairesAdmin)

admin.site.register(models.WaitingQuestionnaires)

