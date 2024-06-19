from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import main
from google.oauth2 import service_account
from googleapiclient.discovery import build
import mimetypes
import tempfile
import os

# Define constants for file upload and Google Drive integration
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'sfn.json'  # Your Google Drive service account credentials file
DRIVE_FOLDER_ID = '1x7oZeHABu5ImkULojVbd8IkpMNM7FCmC'  # ID of the folder in Google Drive where files will be uploaded

token = main.token

class Commands:
    def __init__(self):
        self.drive_service = self._get_drive_service()
        self.files = []

    def _get_drive_service(self):
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('drive', 'v3', credentials=credentials)

    def start_message(self, update, context):
        update.message.reply_text('Hello, I am kshelpbot;')
        update.message.reply_text("What should I call you?")
        return 'get_name'

    def handle_name_input(self, update, context):
        name = update.message.text
        context.user_data['name'] = name
        update.message.reply_text(f'Hello Ing. {name}')
        update.message.reply_text(f"{name} 😎. What program are you offering? (CE/MC/EL)")
        return 'get_program'

    def handle_program_input(self, update, context):
        program = update.message.text
        context.user_data['program'] = program
        update.message.reply_text(f'{program}! That is really good.')
        update.message.reply_text("Go to the menu and let me know how I can assist you OR begin typing with / to access my menu.")
        update.message.reply_text("Select ANY command.")
        return ConversationHandler.END

    def command1(self, update, context):
        update.message.reply_text('This is tech@10. Visit the site if you need assistance with ordinary computer problems.')
        keyboard = [[InlineKeyboardButton("Open Website", url="https://jhaguar.unaux.com/?i=1")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("URL:", reply_markup=reply_markup)

    def command2(self, update, context):
        program = context.user_data.get('program', '')
        if program == 'CE':
            keyboard = [[InlineKeyboardButton('Computer Engineering', url="https://t.me/UMATCOURSEFILES")]]
        elif program == "MC":
            keyboard = [[InlineKeyboardButton('Mechanical Engineering', url="https://t.me/houseofquest")]]
        elif program == 'EL':
            keyboard = [[InlineKeyboardButton('Electrical Engineering', url="https://t.me/SmileyKay_01")]]
        else:
            update.message.reply_text("SORRY, WE DON'T HAVE THIS PROGRAM ON OUR LIST")
            return

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Link:", reply_markup=reply_markup)

    def command3(self, update, context):
        group_chat_id = '1565012474'
        bot = context.bot
        try:
            chat = bot.get_chat(group_chat_id)
            last_message = bot.get_message(group_chat_id, chat.last_message_id)
            if last_message:
                last_message_text = last_message.text
                update.message.reply_text(f"The last message in the group is:\n\n{last_message_text}")
            else:
                update.message.reply_text("There are no messages in this group.")
        except Exception as e:
            update.message.reply_text(f"An error occurred: {e}")

    def error(self, update, context):
        print(f"Update {update} caused error: {context.error}")

    def list_files_in_drive(self):
        try:
            files = self.drive_service.files().list(q=f"'{DRIVE_FOLDER_ID}' in parents", fields='files(id, name)').execute().get('files', [])
            return files
        except Exception as e:
            print(f'An error occurred: {e}')
            return []

    def command4(self, update, context):
        self.files = self.list_files_in_drive()

        if self.files:
            file_list_message = "List of available files:\n"
            file_list_message += "\n".join([f"{i + 1}. {file['name']}" for i, file in enumerate(self.files)])
            update.message.reply_text(file_list_message)
            update.message.reply_text('Please enter the number of the file you would like to download:')
            return 'get_file_number'
        else:
            update.message.reply_text("No files found in the storage.")
            return ConversationHandler.END

    def handle_file_number(self, update, context):
        file_number = int(update.message.text) - 1
        if 0 <= file_number < len(self.files):
            file_id = self.files[file_number]['id']
            file_name = self.files[file_number]['name']
            try:
                request = self.drive_service.files().get_media(fileId=file_id)
                file_data = request.execute()

                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(file_data)
                    temp_file_path = temp_file.name

                update.message.reply_text('A moment...')
                with open(temp_file_path, 'rb') as file:
                    context.bot.send_document(chat_id=update.effective_chat.id, document=file, filename=file_name, caption=f"Here is your requested document: {file_name}")

                os.remove(temp_file_path)  # Clean up the temporary file

            except Exception as e:
                update.message.reply_text(f"An error occurred while downloading the file: {e}")
        else:
            update.message.reply_text("Invalid file number. Please try again.")
            return 'get_file_number'

        return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token)
    dp = updater.dispatcher

    commands = Commands()

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('start', commands.start_message)],
        states={
            'get_name': [MessageHandler(Filters.text & ~Filters.command, commands.handle_name_input)],
            'get_program': [MessageHandler(Filters.text & ~Filters.command, commands.handle_program_input)],
        },
        fallbacks=[]
    )

    conv_handler4 = ConversationHandler(
        entry_points=[CommandHandler('command4', commands.command4)],
        states={
            'get_file_number': [MessageHandler(Filters.text & ~Filters.command, commands.handle_file_number)],
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler1)
    dp.add_handler(conv_handler4)
    dp.add_error_handler(commands.error)
    dp.add_handler(CommandHandler('command1', commands.command1))
    dp.add_handler(CommandHandler('command2', commands.command2))
    dp.add_handler(CommandHandler('command3', commands.command3))

    updater.start_polling()
    updater.idle()
