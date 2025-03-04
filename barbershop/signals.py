import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Visit, MasterReview
import os
from dotenv import load_dotenv
from .src.utils.mistral_utils import MistralAI
from .src.utils.telegram_bot import TelegramBot

# Загружаем переменные окружения из .env
load_dotenv()
# Токен вашего бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# ID чата, куда отправлять уведомления
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# API ключ для Mistral
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
# Модель Mistral для использования
MISTRAL_MODEL = os.getenv('MISTRAL_MODEL')


async def send_telegram_message(message: str) -> bool:
    """
    Асинхронная функция для отправки сообщений в Telegram
    """
    bot = TelegramBot(BOT_TOKEN)
    return await bot.send_message(CHAT_ID, message)


@receiver(post_save, sender=Visit)
def send_telegram_notification(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Новая запись!\n"
            f"Имя: {instance.name}\n"
            f"Телефон: {instance.phone}\n"
            f"Мастер: {instance.master.first_name} {instance.master.last_name}\n"
            f"Услуга: {instance.service.name}\n"
            f"Дата и время: {instance.date}"
        )
        asyncio.run(send_telegram_message(message))


@receiver(post_save, sender=MasterReview)
def notify_admin_about_new_review(sender, instance, created, **kwargs):
    if created:
        message = f'Получен новый отзыв от {instance.author} о мастере {instance.master}.\nТекст: {instance.text}\nОценка: {instance.rating}'
        mistral_ai = MistralAI(MISTRAL_API_KEY, MISTRAL_MODEL)
        is_approved = asyncio.run(mistral_ai.check_for_profanity(instance.text))

        instance.is_approved = is_approved
        instance.save()

        status = "одобрен" if is_approved else "отклонен"
        telegram_message = f"{message}\nСтатус: {status}"
        asyncio.run(send_telegram_message(telegram_message))
