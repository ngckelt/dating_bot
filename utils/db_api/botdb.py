from admin.adminbot.models import *


def add_user(**kwargs):
    try:
        Users.objects.create(**kwargs)
        return True
    except:
        return False


def get_user(user_telegram_id):
    return Users.objects.filter(telegram_id=user_telegram_id).first()


def get_user_questions():
    return UserQuestions.objects.all()


def get_search_questions():
    return SearchQuestions.objects.all()


def create_questionnaire(**kwargs):
    Questionnaires.objects.create(**kwargs)


def get_questionnaire_by_user(user):
    return Questionnaires.objects.filter(user=user).first()


def update_search_questionnaire(user, **kwargs):
    Questionnaires.objects.filter(user=user).update(**kwargs)


def get_search_question_by_id(question_id):
    return SearchQuestions.objects.filter(question_id=question_id).first()




