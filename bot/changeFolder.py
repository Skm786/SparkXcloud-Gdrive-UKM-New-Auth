from time import sleep

from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler

import bot
from bot import dispatcher
from bot.helper.button_builder import ButtonMaker
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper

delete_Message_id = ''
upload_folder_id = bot.UPLOAD_FOLDER_ID
upload_folder_name = bot.UPLOAD_FOLDER_NAME


def list_folders(update, context):
    global delete_Message_id
    global upload_folder_id
    global upload_folder_name
    delete_Message_id = update.message.message_id
    print("Message id: " + str(update.message.message_id))
    button = ButtonMaker()
    print("Current Folder Name: " + upload_folder_name)
    print("Current Folder Name: " + upload_folder_id)
    if not upload_folder_id:
        upload_folder_id = bot.parent_id
        upload_folder_name = "Parent"
    files = GoogleDriveHelper.getFilesByFolderId(GoogleDriveHelper(), bot.parent_id)
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
    #print(f"Current Folder Id {current_folder_id}")
    with open('selected_folder.txt', 'w') as file:
        file.truncate(0)
        file.write(str(query.data))
        bot.UPLOAD_FOLDER_ID = current_folder_id
        bot.UPLOAD_FOLDER_NAME = current_folder_name
    context.bot.deleteMessage(chat_id=bot.OWNER_ID, message_id=int(delete_Message_id) + 1)
    context.bot.sendMessage(text=f"Successfully Changed Folder To {current_folder_name}", chat_id=bot.OWNER_ID)
    query.answer("Successfully Changed The Folder")
    GoogleDriveHelper()


list_handler = CommandHandler(command="dir", callback=list_folders, run_async=True)
dispatcher.add_handler(CallbackQueryHandler(callback=select_folder))
dispatcher.add_handler(list_handler)
