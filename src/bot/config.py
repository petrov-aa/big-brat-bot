import os

from bot.messages import t

# Токен бота
ENV_VAR_BOT_TOKEN = "APP_BOT_TOKEN"
if ENV_VAR_BOT_TOKEN not in os.environ:
    raise Exception(t("bot.config.token_not_specified"))
APP_BOT_TOKEN = os.environ[ENV_VAR_BOT_TOKEN]

# Идентификатор чата канал - нужен только для того чтобы бот писал привет в чат, когда включается
ENV_VAR_APP_CHAT_ID = "APP_CHAT_ID"
if ENV_VAR_APP_CHAT_ID not in os.environ:
    raise Exception(t("bot.config.chat_id_not_specified"))
APP_CHAT_ID = os.environ[ENV_VAR_APP_CHAT_ID]

# Пользователи-админы
ENV_VAR_APP_USERS = "APP_USERS"
if ENV_VAR_APP_USERS not in os.environ:
    raise Exception(t("bot.config.users_not_specified"))
APP_USERS = [int(user_id) for user_id in os.environ[ENV_VAR_APP_USERS].split(',')]

# Способ запуска: вебхук или полинг
ENV_VAR_APP_RUN_METHOD = "APP_RUN_METHOD"
if ENV_VAR_APP_RUN_METHOD not in os.environ:
    raise Exception(t("bot.config.run_method_not_specified"))
APP_RUN_METHOD = os.environ[ENV_VAR_APP_RUN_METHOD]

# Прокси
ENV_VAR_PROXY = "APP_BOT_PROXY"
APP_BOT_PROXY = None
if ENV_VAR_PROXY in os.environ:
    APP_BOT_PROXY = os.environ[ENV_VAR_PROXY]
