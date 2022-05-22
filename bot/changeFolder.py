import os

from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
import bot
from bot import dispatcher
from bot.helper.button_builder import ButtonMaker
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.telegram_helper.filters import CustomFilters

delete_Message_id = ''
upload_folder_id = bot.UPLOAD_FOLDER_ID
upload_folder_name = bot.UPLOAD_FOLDER_NAME


def createFolder(update, context):
    folder_name = update.message.text.split(" ")
    if not len(folder_name) > 1:
        context.bot.sendMessage(update.message.chat_id,
                                reply_to_message_id=update.message.message_id,
                                text=f"Please Provide a Folder Name With Command",
                                allow_sending_without_reply=True,
                                parse_mode='HTMl', disable_web_page_preview=True)
    else:
        response = GoogleDriveHelper.createNewFolder(GoogleDriveHelper(), folder_name=folder_name[1])
        if not response:
            context.bot.sendMessage(update.message.chat_id,
                                    reply_to_message_id=update.message.message_id,
                                    text=f"Folder With Name {folder_name[1]} Already Exist",
                                    allow_sending_without_reply=True,
                                    parse_mode='HTMl', disable_web_page_preview=True)
        else:
            context.bot.sendMessage(update.message.chat_id,
                                    reply_to_message_id=update.message.message_id,
                                    text=f"Successfully Created New Folder : {folder_name[1]}",
                                    allow_sending_without_reply=True,
                                    parse_mode='HTMl', disable_web_page_preview=True)


def list_folders(update, context):
    global delete_Message_id
    global upload_folder_id
    global upload_folder_name
    delete_Message_id = update.message.message_id
    print("Message id: " + str(update.message.message_id))
    button = ButtonMaker()
    if not upload_folder_id:
        upload_folder_id = bot.PARENT_FOLDER_ID
        upload_folder_name = "SparkX Bot Uploads"
    print("Current Folder Name: " + upload_folder_name)
    print("Current Folder id: " + upload_folder_id)
    files = GoogleDriveHelper.getFilesByFolderId(GoogleDriveHelper(), bot.PARENT_FOLDER_ID)
    # print(json.dumps(files))
    for file in files:
        if "application/vnd.google-apps.folder" in file['mimeType']:
            button.sbutton(file['name'], file['id'] + " " + file['name'])
    context.bot.sendMessage(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=f"List Of Google Drive Folders \nCurrent Folder: {upload_folder_name}",
                            reply_markup=InlineKeyboardMarkup(button.build_menu(2)),
                            allow_sending_without_reply=True,
                            parse_mode='HTMl', disable_web_page_preview=True)


def select_folder(update, context):
    global upload_folder_id
    global upload_folder_name
    query = update.callback_query
    args = str({query.data}).split(" ")
    current_folder_name = args[1].strip("'}")
    current_folder_id = args[0].strip("{'")
    upload_folder_id = current_folder_id
    upload_folder_name = current_folder_name
    print(f"Current Folder Name {current_folder_name}")
    # print(f"Current Folder Id {current_folder_id}")
    f = open("selected_folder.txt", "w+")
    f.truncate(0)
    f.write(str(query.data))
    f.close()
    bot.UPLOAD_FOLDER_ID = current_folder_id
    bot.UPLOAD_FOLDER_NAME = current_folder_name
    context.bot.deleteMessage(chat_id=bot.OWNER_ID, message_id=int(delete_Message_id) + 1)
    context.bot.sendMessage(text=f"Successfully Changed Folder To {current_folder_name}", chat_id=bot.OWNER_ID)
    query.answer("Successfully Changed The Folder")
    GoogleDriveHelper()


list_handler = CommandHandler(command="dir", callback=list_folders,
                              filters=CustomFilters.owner_filter and CustomFilters.login_user and CustomFilters.parent_folder_filter, run_async=True)
create_handler = CommandHandler(command="add", callback=createFolder,
                                filters=CustomFilters.owner_filter and CustomFilters.login_user and CustomFilters.parent_folder_filter, run_async=True)
dispatcher.add_handler(CallbackQueryHandler(callback=select_folder))
dispatcher.add_handler(list_handler)
dispatcher.add_handler(create_handler)
