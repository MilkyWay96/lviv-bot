import os
from dotenv import load_dotenv

# Отримує данні конфігурації для телеграм бота та Clash Of Clans API
# На GitHub нема цього файлу оскільки у ньому конфіденційні данні
# Щоб запустити, створіть файл config.env у робочій папці
# Та задайте у ньому змінні, які читаються нище:

load_dotenv("config.env")
EMAIL = os.getenv("EMAIL")          # Пошта з якою ви зареєструвались на офійійному сайті Clash Of Clans API
PASSWORD = os.getenv("PASSWORD")    # Пароль від вашого акаунту Clash Of Clans API
CLAN_TAG = os.getenv("CLAN_TAG")    # Тег клану з яким працює бот
TOKEN = os.getenv("BOT_TOKEN")      # Токен телеграм бота

# Приклад файлу config.env

# ------config.env------
# EMAIL=john.doe@gmail.com
# PASSWORD=Qwerty123!
# CLAN_TAG=#69696969
# TOKEN=231249042:DWOIJDjiwdjDWJOIWdDwdwjidNDWDJdwj
# ------config.env------

# EMail та пароль від вашого акаунта на сайті https://developer.clashofclans.com