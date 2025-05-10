# main.py
"""
Telegram Bot: Распознаёт голосовые сообщения и видеосообщения (кружочки) в Telegram
и преобразует их в текст, а также может озвучивать текст в аудио.

Функциональность:
- Поддержка аудио (voice) и видео сообщений (video_note)
- Распознавание с помощью Whisper
- Синтез речи с помощью TTS (gTTS)
"""

import os
import telebot
import torch
import tempfile
from moviepy.editor import VideoFileClip
import whisper
from gtts import gTTS

# Инициализация
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")  # Переменная окружения
bot = telebot.TeleBot(API_TOKEN)
model = whisper.load_model("small")  # Или 'base', 'medium', в зависимости от устройства


# Функция для обработки и распознавания файла
def transcribe_audio(file_path):
    print(f"[INFO] Распознавание файла: {file_path}")
    result = model.transcribe(file_path)
    return result["text"]


# Функция для синтеза речи
def text_to_speech(text, lang='ru'):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name


# Обработка voice сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio:
        temp_audio.write(downloaded_file)
        temp_audio_path = temp_audio.name

    # Распознавание
    text = transcribe_audio(temp_audio_path)
    bot.reply_to(message, text)


# Обработка видео-сообщений (кружочки)
@bot.message_handler(content_types=['video_note'])
def handle_video_note(message):
    file_info = bot.get_file(message.video_note.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(downloaded_file)
        temp_video_path = temp_video.name

    # Извлекаем аудио из видео
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        clip = VideoFileClip(temp_video_path)
        clip.audio.write_audiofile(temp_audio.name)
        temp_audio_path = temp_audio.name

    # Распознавание
    text = transcribe_audio(temp_audio_path)
    bot.reply_to(message, text)



# Озвучка текста (по команде /say)
@bot.message_handler(commands=['say'])
def handle_say(message):
    text = message.text[len("/say "):]
    if not text:
        bot.reply_to(message, "Пожалуйста, напиши текст после команды /say")
        return

    audio_path = text_to_speech(text)
    with open(audio_path, 'rb') as audio:
        bot.send_audio(message.chat.id, audio)


# Старт
print("[INFO] Бот запущен...")
bot.polling(none_stop=True)