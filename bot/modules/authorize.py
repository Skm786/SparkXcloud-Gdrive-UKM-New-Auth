# import os.path
# import pickle

# from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
# from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler

# import bot
from bot import AUTHORIZED_CHATS, SUDO_USERS, dispatcher, DB_URI
# from bot import LOGGER
# from bot.helper.button_builder import ButtonMaker
from bot.helper.ext_utils.db_handler import DbManger
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage
# from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper

# OAUTH_SCOPE = "https://www.googleapis.com/auth/drive"
# REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
# G_DRIVE_CLIENT_ID = "335100795592-igtq8vbkcoer77aqccb3l83uco4ku46d.apps.googleusercontent.com"
# G_DRIVE_CLIENT_SECRET = "X2IUV5dFwbapte07mVapE5cl"
# AUTH_SUCCESSFULLY = '🔐 Authorized Google Drive account Successfully.'
# ALREADY_AUTH = "🔒 Already authorized your Google Drive Account.\nUse /revoke to revoke the current account.\nSend me a direct link or File to Upload on Google Drive"
# AUTH_TEXT = "⛓️To Authorize your Google Drive account visit this [URL]({}) and send the generated code here.\nVisit the URL > Allow permissions > you will get a code > copy it > Send it here"
# FLOW_IS_NONE = f"❗ Invalid Code\nRun /login first."
# INVALID_AUTH_CODE = '❗ Invalid Code\nThe code you have sent is invalid or already used before. Generate new one by the Authorization URL'
# REVOKED = f"🔓 Revoked current logged account successfully.\n__Use /login to authenticate again and use this bot."

# flow = None


# def _auth(update, context):
#     button = ButtonMaker()
#     creds = os.path.exists("creds.txt")
#     # creds = gDriveDB.search(user_id)
#     if creds is not False:
#         # creds.refresh(Http())
#         # gDriveDB._set(user_id, creds)
#         update.message.reply_text(ALREADY_AUTH, quote=True)
#     else:
#         global flow
#         try:
#             flow = OAuth2WebServerFlow(
#                 G_DRIVE_CLIENT_ID,
#                 G_DRIVE_CLIENT_SECRET,
#                 OAUTH_SCOPE,
#                 redirect_uri=REDIRECT_URI
#             )
#             auth_url = flow.step1_get_authorize_url()
#             LOGGER.info(f'AuthURL:{auth_url}')
#             button.buildbutton("Authorization URL", link=auth_url)
#             context.bot.sendMessage(
#                 chat_id=update.message.chat_id,
#                 text=AUTH_TEXT.format(auth_url),
#                 reply_markup=InlineKeyboardMarkup(button.build_menu(1))
#             )
#         except Exception as e:
#             update.message.reply_text(f"**ERROR:** ```{e}```", quote=True)


# def _token(update, context):
#     args = update.message.text.split(" ")
#     token = args[1]
#     print(token)
#     WORD = len(token)
#     print(WORD)
#     if WORD == 62:
#         creds = None
#         global flow
#         if flow:
#             try:
#                 user_id = update.message.from_user.id
#                 sendMessage(text="🕵️**Checking received code...**", bot=context.bot, update=update)
#                 creds = flow.step2_exchange(token)
#                 with open('creds.txt', 'wb') as file:
#                     pickle.dump(creds, file)
#                 print(creds)
#                 LOGGER.info(f'AuthSuccess: {user_id}')
#                 context.bot.edit_message_text(text=AUTH_SUCCESSFULLY, message_id=update.message.message_id + 1,
#                                               chat_id=update.message.chat_id)
#                 parent_id = GoogleDriveHelper.createParentFolder(GoogleDriveHelper())
#                 f = open("parent_folder.txt", "w+")
#                 print("Folder id " + parent_id)
#                 f.truncate(0)
#                 f.write(parent_id)
#                 bot.PARENT_FOLDER_ID = parent_id
#                 flow = None
#             except FlowExchangeError:
#                 context.bot.edit_message_text(text=INVALID_AUTH_CODE, message_id=update.message.message_id + 1,
#                                               chat_id=update.message.chat_id)
#             except Exception as e:
#                 context.bot.edit_message_text(f"**ERROR:** ```{e}```")
#         else:
#             sendMessage(text=FLOW_IS_NONE, bot=context.bot, update=update)


# def _revoke(update, context):
#     user_id = update.message.from_user.id
#     if os.path.exists("creds.txt"):
#         try:
#             os.remove("creds.txt")
#             if os.path.exists("parent_folder.txt"):
#                 os.remove("parent_folder.txt")
#             if os.path.exists("selected_folder.txt"):
#                 os.remove("selected_folder.txt")
#             LOGGER.info(f'Revoked:{user_id}')
#             update.message.reply_text(REVOKED, quote=True)
#         except Exception as e:
#             update.message.reply_text(f"**ERROR:** ```{e}```", quote=True)
#     else:
#         update.message.reply_text("Currently You Are Not Logged in\nUse /login to login", quote=True)

def authorize(update, context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id not in AUTHORIZED_CHATS:
            if DB_URI is not None:
                msg = DbManger().db_auth(user_id)
            else:
                with open('authorized_chats.txt', 'a') as file:
                    file.write(f'{user_id}\n')
                    AUTHORIZED_CHATS.add(user_id)
                    msg = 'User Authorized'
        else:
            msg = 'User Already Authorized'
    else:
        if reply_message is None:
            # Trying to authorize a chat
            chat_id = update.effective_chat.id
            if chat_id not in AUTHORIZED_CHATS:
                if DB_URI is not None:
                    msg = DbManger().db_auth(chat_id)
                else:
                    with open('authorized_chats.txt', 'a') as file:
                        file.write(f'{chat_id}\n')
                        AUTHORIZED_CHATS.add(chat_id)
                        msg = 'Chat Authorized'
            else:
                msg = 'Chat Already Authorized'

        else:
            # Trying to authorize someone by replying
            user_id = reply_message.from_user.id
            if user_id not in AUTHORIZED_CHATS:
                if DB_URI is not None:
                    msg = DbManger().db_auth(user_id)
                else:
                    with open('authorized_chats.txt', 'a') as file:
                        file.write(f'{user_id}\n')
                        AUTHORIZED_CHATS.add(user_id)
                        msg = 'User Authorized'
            else:
                msg = 'User Already Authorized'
    sendMessage(msg, context.bot, update)


def unauthorize(update, context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id in AUTHORIZED_CHATS:
            if DB_URI is not None:
                msg = DbManger().db_unauth(user_id)
            else:
                AUTHORIZED_CHATS.remove(user_id)
                msg = 'User Unauthorized'
        else:
            msg = 'User Already Unauthorized'
    else:
        if reply_message is None:
            # Trying to unauthorize a chat
            chat_id = update.effective_chat.id
            if chat_id in AUTHORIZED_CHATS:
                if DB_URI is not None:
                    msg = DbManger().db_unauth(chat_id)
                else:
                    AUTHORIZED_CHATS.remove(chat_id)
                    msg = 'Chat Unauthorized'
            else:
                msg = 'Chat Already Unauthorized'
        else:
            # Trying to authorize someone by replying
            user_id = reply_message.from_user.id
            if user_id in AUTHORIZED_CHATS:
                if DB_URI is not None:
                    msg = DbManger().db_unauth(user_id)
                else:
                    AUTHORIZED_CHATS.remove(user_id)
                    msg = 'User Unauthorized'
            else:
                msg = 'User Already Unauthorized'
    with open('authorized_chats.txt', 'a') as file:
        file.truncate(0)
        for i in AUTHORIZED_CHATS:
            file.write(f'{i}\n')
    sendMessage(msg, context.bot, update)


def addSudo(update, context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id not in SUDO_USERS:
            if DB_URI is not None:
                msg = DbManger().db_addsudo(user_id)
            else:
                with open('sudo_users.txt', 'a') as file:
                    file.write(f'{user_id}\n')
                    SUDO_USERS.add(user_id)
                    msg = 'Promoted as Sudo'
        else:
            msg = 'Already Sudo'
    else:
        if reply_message is None:
            msg = "Give ID or Reply To message of whom you want to Promote"
        else:
            # Trying to authorize someone by replying
            user_id = reply_message.from_user.id
            if user_id not in SUDO_USERS:
                if DB_URI is not None:
                    msg = DbManger().db_addsudo(user_id)
                else:
                    with open('sudo_users.txt', 'a') as file:
                        file.write(f'{user_id}\n')
                        SUDO_USERS.add(user_id)
                        msg = 'Promoted as Sudo'
            else:
                msg = 'Already Sudo'
    sendMessage(msg, context.bot, update)


def removeSudo(update, context):
    reply_message = None
    message_ = None
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
        user_id = int(message_[1])
        if user_id in SUDO_USERS:
            if DB_URI is not None:
                msg = DbManger().db_rmsudo(user_id)
            else:
                SUDO_USERS.remove(user_id)
                msg = 'Demoted'
        else:
            msg = 'Not a Sudo'
    else:
        if reply_message is None:
            msg = "Give ID or Reply To message of whom you want to remove from Sudo"
        else:
            user_id = reply_message.from_user.id
            if user_id in SUDO_USERS:
                if DB_URI is not None:
                    msg = DbManger().db_rmsudo(user_id)
                else:
                    SUDO_USERS.remove(user_id)
                    msg = 'Demoted'
            else:
                msg = 'Not a Sudo'
    if DB_URI is None:
        with open('sudo_users.txt', 'a') as file:
            file.truncate(0)
            for i in SUDO_USERS:
                file.write(f'{i}\n')
    sendMessage(msg, context.bot, update)


def sendAuthChats(update, context):
    user = sudo = ''
    user += '\n'.join(str(id) for id in AUTHORIZED_CHATS)
    sudo += '\n'.join(str(id) for id in SUDO_USERS)
    sendMessage(f'<b><u>Authorized Chats</u></b>\n<code>{user}</code>\n<b><u>Sudo Users</u></b>\n<code>{sudo}</code>',
                context.bot, update)


send_auth_handler = CommandHandler(command=BotCommands.AuthorizedUsersCommand, callback=sendAuthChats,
                                   filters=CustomFilters.owner_filter | CustomFilters.sudo_user
                                   and CustomFilters.login_user, run_async=True)
authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter | CustomFilters.sudo_user
                                   and CustomFilters.login_user, run_async=True)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user
                                     and CustomFilters.login_user, run_async=True)
addsudo_handler = CommandHandler(command=BotCommands.AddSudoCommand, callback=addSudo,
                                 filters=CustomFilters.owner_filter
                                 and CustomFilters.login_user, run_async=True)
removesudo_handler = CommandHandler(command=BotCommands.RmSudoCommand, callback=removeSudo,
                                    filters=CustomFilters.owner_filter
                                    and CustomFilters.login_user, run_async=True)

# login_handler = CommandHandler(command="login", callback=_auth,
#                                filters=CustomFilters.owner_filter, run_async=True)

# dispatcher.add_handler(login_handler)

# auth_token_handler = CommandHandler(command="token", callback=_token,
#                                     filters=CustomFilters.owner_filter, run_async=True)

# dispatcher.add_handler(auth_token_handler)

# revoke_handler = CommandHandler(command="revoke", callback=_revoke,
#                                 filters=CustomFilters.owner_filter, run_async=True)

# dispatcher.add_handler(revoke_handler)

dispatcher.add_handler(send_auth_handler)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)
dispatcher.add_handler(addsudo_handler)
dispatcher.add_handler(removesudo_handler)
