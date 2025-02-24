import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Visit
import telegram
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
# Токен вашего бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# ID чата, куда отправлять уведомления
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


@receiver(post_save, sender=Visit)
def send_telegram_notification(sender, instance, created, **kwargs):
    """
    Отправляет уведомление в Telegram при создании новой записи.
    """
    if created:  # Проверяем, что запись создана, а не обновлена
        asyncio.run(send_telegram_message(instance))


async def send_telegram_message(instance):
    """Отправляет уведомление в Telegram асинхронно."""

    bot = telegram.Bot(token=BOT_TOKEN)
    message = (
        f"Новая запись!\n"
        f"Имя: {instance.name}\n"
        f"Телефон: {instance.phone}\n"
        f"Мастер: {instance.master.first_name} {instance.master.last_name}\n"
        f"Услуга: {instance.service.name}\n"
        f"Дата и время: {instance.date}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=message)
