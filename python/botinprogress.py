from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import main
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import mimetypes

# Define constants for file upload and Google Drive integration
SCOPES = ['https://www.googleapis.com/auth/drive']
SAF="sfn.json"
SERVICE_ACCOUNT_FILE = SAF  # Your Google Drive service account credentials file
DRIVE_FOLDER_ID = '1x7oZeHABu5ImkULojVbd8IkpMNM7FCmC'  # ID of the folder in Google Drive where files will be uploaded

token = main.token

class Commands:
    def __init__(self):
        self.drive_service = self._get_drive_service()

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
        update.message.reply_text(f'Hello Ing.{name}')
        update.message.reply_text(f"{name} 😎. What program are you offering?(CE/MC/EL)")
        return 'get_program'

    def handle_program_input(self, update, context):
        program = update.message.text
        update.message.reply_text(f'{program} ! , That is really good')
        update.message.reply_text("Go to menu and let me know how I can assist you OR begin typing with / to access my menu")
        update.message.reply_text(" select ANY command")

    def command1(self, update, context):
        update.message.reply_text('''This is tech@10 visit the site if you need assistance with ordinary computer problems''')
        keyboard = [[InlineKeyboardButton("Open Website", url="https://jhaguar.unaux.com/?i=1")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("URL ", reply_markup=reply_markup)



    def command2(self, update, context):
        program = update.message.text
        if program == 'CE':
            keyboard = [[InlineKeyboardButton('Computer Engineering', url="https://t.me/UMATCOURSEFILES")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Link", reply_markup=reply_markup)
        elif program == "MC":
            keyboard = [[InlineKeyboardButton('MECHANICAL ENGINEERING', url="https://t.me/houseofquest")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("Link", reply_markup=reply_markup)
        elif program == 'EL':
            keyboard = [[InlineKeyboardButton('ELECTRICAL ENGINEERING', url="https://t.me/SmileyKay_01")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('HELLO ELECTRICIAN', reply_markup=reply_markup)
        else:
            update.message.reply_text("SORRY WE DON'T HAVE THIS PROGRAM ON OUR LIST")

    def command3(self, update, bot,context):
        group_chat_id = '1565012474'
        chat = bot.get_chat(group_chat_id)
        last_message = bot.get_message(group_chat_id, chat.last_message_id)
        if last_message:
            last_message_text = last_message.text
            update.message.reply_text(f"The last message in the group is:\n\n{last_message_text}")
        else:
            update.message.reply_text("There are no messages in this group.")
        return ConversationHandler.END

    def error(self, update, context):
        print(f"Update {update} caused error: {context.error}")





   
    def list_files_in_drive(self):
        try:
            files = self.drive_service.files().list(q="'{}' in parents".format(DRIVE_FOLDER_ID),
                                                    fields='files(id, name)').execute().get('files', [])
            return files
        except Exception as e:
            print('An error occurred: %s' % e)
            return []
    




    def command4(self, update, context):
        files = self.list_files_in_drive()

        enumerated_list = [f"{i + 1}. {file['name']}" for i, file in enumerate(files)]
        
        
        if files:
            update.message.reply_text("List of available files:")
            for item in enumerated_list:
                update.message.reply_text(item)
            update.message.reply_text('What file would you like to download?')  
            userInput=context.user_data
            if item==userInput:
                file_id=enumerated_list[files]
                try:

                            # Download the file
                        request = self.drive_service.files().get_media(fileId=file_id)
                        file_data = request.execute()
                        update.message.reply_text('A moment...')

                        # Send the file to the user
                        mime_type, _ = mimetypes.guess_type(item)
                        if mime_type is None:
                            mime_type = 'application/octet-stream'
                        
                            context.bot.send_document(chat_id=update.effective_chat.id, document=file_data,
                                                filename=item, caption=f"Here is your requested document: {item}")

                        else:
                            update.message.reply_text("No files found.")
                
                except Exception as e:
            
            
                        update.message.reply_text(f"An error occurred while downloading the file: {e}")
            else:
            
                update.message.reply_text("Invalid file name. Please provide a valid file name.")
                

                     
            
        else:
            update.message.reply_text("No files found in the storage.")

        
         
   
       
  
        
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
    
    



dp.add_handler(conv_handler1)
dp.add_error_handler(commands.error)
dp.add_handler(CommandHandler('command1', commands.command1))
dp.add_handler(CommandHandler('command2', commands.command2))
dp.add_handler(CommandHandler('command3', commands.command3))
dp.add_handler(CommandHandler('command4', commands.command4))
    


updater.start_polling()
updater.idle()
