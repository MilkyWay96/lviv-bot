from commands import start
from commands import help
from commands import attacks
from commands import warban

from aiogram import Dispatcher

def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(attacks.router)
    dp.include_router(warban.router)