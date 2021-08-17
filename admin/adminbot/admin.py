from django.contrib import admin
from . import models


class UserQuestionsAdmin(admin.ModelAdmin):
    pass


class SearchQuestionsAdmin(admin.ModelAdmin):
    pass


class UsersAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.UserQuestions, UserQuestionsAdmin)
admin.site.register(models.SearchQuestions, SearchQuestionsAdmin)
admin.site.register(models.Users, UsersAdmin)