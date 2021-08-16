from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())



# from loader import dp
# from .throttling import ThrottlingMiddleware
#
#
# if __name__ == "middlewares":
#     dp.middleware.setup(ThrottlingMiddleware())
