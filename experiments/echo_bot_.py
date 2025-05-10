# echo_bot.py
"""
Эхо-бот: отвечает тем же типом сообщений, что получил (текст, голос, фото, видео и т.п.)
"""

import os
import telebot

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo_text(message):
    bot.reply_to(message, message.text)

# Голосовые сообщения
@bot.message_handler(content_types=['voice'])
def echo_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    voice_file = bot.download_file(file_info.file_path)
    bot.send_voice(message.chat.id, voice_file)

# Фото
@bot.message_handler(content_types=['photo'])
def echo_photo(message):
    file_id = message.photo[-1].file_id  # самое большое по размеру
    bot.send_photo(message.chat.id, file_id)

# Видео
@bot.message_handler(content_types=['video'])
def echo_video(message):
    file_id = message.video.file_id
    bot.send_video(message.chat.id, file_id)

# Аудио (не голосовое, а music/mp3 и т.п.)
@bot.message_handler(content_types=['audio'])
def echo_audio(message):
    file_id = message.audio.file_id
    bot.send_audio(message.chat.id, file_id)

# Стикеры
@bot.message_handler(content_types=['sticker'])
def echo_sticker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)

# Видео заметки (кружочки)
@bot.message_handler(content_types=['video_note'])
def echo_video_note(message):
    file_id = message.video_note.file_id
    bot.send_video_note(message.chat.id, file_id)

print("[INFO] Эхо-бот расширенной версии запущен...")
bot.polling(none_stop=True)
