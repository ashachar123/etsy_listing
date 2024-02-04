import os.path
import time
import random
import telebot
from main import sort_files, create_dirs, config
from datetime import datetime
import threading

TOKEN = config().get("telegram_token")
bot = telebot.TeleBot(TOKEN)
counter = 0
project_path = None
images = []


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi! Send me an image with a caption!")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, "Please send me an image, not text.")



@bot.message_handler(content_types=['photo'])
def handle_image(message):
    global counter, project_path, images

    if not images:
        project_path = create_dirs()

    if len(images) <= 4:
        images.append(message)
        caption = images[-1].caption if images[-1].caption is not None else '_No caption'
        filename = extract_data(images[-1].photo[-1], caption)
        sort_files(filename, project_path)
        time.sleep(5)
    if len(images) == 4:
        bot.reply_to(message, "Starting to generate product...")
        threading.Thread(target=send_video, args=(project_path, message.chat.id, 500)).start()

        images = []
        project_path = None


def send_video(product_path, chatid, cap=60):
    counter = 0
    while True:
        if os.path.isfile(f"{product_path}/Mockup/output_video_rdy.mp4"):
            bot.send_video(chatid, open(f"{product_path}/Mockup/output_video_rdy.mp4", "rb"))
            return
        if counter == cap:
            bot.send_message(chatid, "could not generate video")
            return
        counter +=1
        time.sleep(1)

def extract_data(photo, caption):
    file_id = photo.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # Open the image using Pillow
    # image = Image.open(BytesIO(downloaded_file))
    caption = caption if caption is not None else None
    tmptime = str(datetime.now()).replace(':', '.').replace(' ', '')
    filename = f"{caption.replace(' ', '_') if caption else '_' + tmptime + str(counter)}.jpg"
    with open("stock" + "/" + filename, "wb") as image:
        image.write(downloaded_file)
    return filename


def start_bot():
    bot.polling()


if __name__ == '__main__':
    start_bot()
