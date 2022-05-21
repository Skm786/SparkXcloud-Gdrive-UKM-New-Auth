from email import message
import requests
from bot import dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters

def changeImage(update, context):
    image_url = update.message.text.split(" ")
    if len(image_url) > 1:
        if "http" not in image_url[1]:
            context.bot.sendMessage(update.message.chat_id,
                                reply_to_message_id=update.message.message_id,
                                text=f"Please Provide A Valid Image Url",
                                allow_sending_without_reply=True,
                                parse_mode='HTMl', disable_web_page_preview=True)
            return
        if is_url_image(image_url=image_url[1]):
            f = open("image_url.txt", "w+")
            f.truncate(0)
            f.write(image_url[1])
            f.close()
            context.bot.sendMessage(update.message.chat_id,
                                reply_to_message_id=update.message.message_id,
                                text=f"Successfully Updated The Image",
                                allow_sending_without_reply=True,
                                parse_mode='HTMl', disable_web_page_preview=True)
        else:
            context.bot.sendMessage(update.message.chat_id,
                                reply_to_message_id=update.message.message_id,
                                text=f"Please Provide A Valid Image Url",
                                allow_sending_without_reply=True,
                                parse_mode='HTMl', disable_web_page_preview=True)
    else:
        context.bot.sendMessage(update.message.chat_id,
                                reply_to_message_id=update.message.message_id,
                                text=f"Send Direct Image Url With /image Command",
                                allow_sending_without_reply=True,
                                parse_mode='HTMl', disable_web_page_preview=True)
    

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

change_image_handler = CommandHandler(command="image", callback=changeImage,
                                filters=CustomFilters.owner_filter, run_async=True)

dispatcher.add_handler(change_image_handler)