import telegram


class TelegramBot:
    """
    Класс для взаимодействия с Telegram ботом.
    """

    def __init__(self, token: str):
        """
        Инициализирует объект TelegramBot.
        :param token: Токен бота.
        """
        self.bot = telegram.Bot(token=token)

    async def send_message(self, chat_id: int | str, message: str) -> bool:
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
            return True
        except Exception as e:
            print(f"Ошибка отправки сообщения в Telegram: {e}")
            return False
