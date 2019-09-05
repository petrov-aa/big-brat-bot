from telebot import TeleBot, apihelper
from bot import config
from bot.messages import t

if config.APP_BOT_PROXY is not None:
    apihelper.proxy = {"https": config.APP_BOT_PROXY}

bot = TeleBot(config.APP_BOT_TOKEN)
me = bot.get_me()

bot.send_message(config.APP_CHAT_ID, t('bot.bot.hi'))


def get_my_rights(chat_id):
    """
    Возвращает словарь прав, которыми обладает бот в чате

    :param chat_id: Идентификатор чата
    :return: Словарь прав
    """
    chat_member = bot.get_chat_member(chat_id, me.id)

    # Перечень свойств, содержащих права объекта ChatMember
    right_properties = {
        'can_change_info',
        'can_delete_messages',
        'can_restrict_members',
        'can_invite_users',
        'can_pin_messages',
        'can_promote_members'
    }

    chat_member_properties = vars(chat_member)

    return {k: chat_member_properties[k] for k in chat_member_properties.keys() & right_properties}


@bot.message_handler(commands=['start', 'help'])
def on_start_or_help(message):
    """
    По правилам Телеграма бот должен реализовывать методы start и help
    """
    bot.send_message(message.chat.id, t('bot.bot.start'))


@bot.message_handler(content_types=["new_chat_members"])
def on_new_member(message):

    # Получаем набор прав, которыми обладает бот - бот сможет выдавать только эти же права
    rights = get_my_rights(message.chat.id)
    if not rights['can_promote_members']:
        # У бота нет возможности выдавать админку
        return
    # В последствии этот же словарь будет использоваться для выдачи админки, и чтобы при
    # этом пользователь не получил возможность выдавать админки исключаем это правило
    rights['can_promote_members'] = False

    for user in message.new_chat_members:
        if user.id == me.id:
            # В чат добавлен сам бот
            continue
        if user.id not in config.APP_USERS:
            # Пользователь не входит в перечень пользователей-админов
            continue
        chat_member = bot.get_chat_member(message.chat.id, user.id)
        if chat_member.status == 'creator':
            # Если это создатель чата, то в правах его восстановит сам телеграм
            continue
        if chat_member.can_be_edited is not None:
            # Пользователь либо уже администратор - в этом случае его права не редактируем
            continue
        # Выдаем админку
        bot.promote_chat_member(message.chat.id, user.id, **rights)
        bot.reply_to(message, t('bot.bot.admin_restored'))
