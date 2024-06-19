from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import main
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

token = main.token

class Commands:
    def start_message(self, update, context):
        update.message.reply_text('Hello, I am kshelpbot;')
        update.message.reply_text("What should I call you?")
        return 'get_name'

    def handle_name_input(self, update, context):
        name = update.message.text
        context.user_data['name'] = name
        update.message.reply_text(f'Hello Ing.{name}')
        update.message.reply_text(f"{name} 😎. What program are you offering?(CE/MC/EL)")
        return 'get_program'

    def handle_program_input(self, update, context):
        program = update.message.text
        context.user_data['program'] = program
        update.message.reply_text(f'{program} ! , That is really good')
        update.message.reply_text("Go to menu and let me know how I can assist you OR begin typing with / to access my menu")
        update.message.reply_text("And select ANY command")

    def command1(self, update, context):
        update.message.reply_text('''This is tech@10 visit the site if you need assistance with ordinary computer problems''')
        keyboard = [[InlineKeyboardButton("Open Website", url="http://jhaguar.unaux.com/?i=1")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("URL ", reply_markup=reply_markup)

    def command2(self, update, context):
        program = context.user_data.get('program')
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
        # Add similar code for other programs

    def command3(self, update, context):
        group_chat_id = '1565012474'
        chat = context.bot.get_chat(group_chat_id)
        last_message = context.bot.get_message(group_chat_id, chat.last_message_id)
        if last_message:
            last_message_text = last_message.text
            update.message.reply_text(f"The last message in the group is:\n\n{last_message_text}")
        else:
            update.message.reply_text("There are no messages in this group.")
        return ConversationHandler.END

    def error(self, update, context):
        print(f"Update {update} caused error: {context.error}")

if __name__ == '__main__':
    updater = Updater(token)
    dp = updater.dispatcher

    commands = Commands()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', commands.start_message)],
        states={
            'get_name': [MessageHandler(Filters.text & ~Filters.command, commands.handle_name_input)],
            'get_program': [MessageHandler(Filters.text & ~Filters.command, commands.handle_program_input)]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(commands.error)
    dp.add_handler(CommandHandler('command1', commands.command1))
    dp.add_handler(CommandHandler('command2', commands.command2))
    dp.add_handler(CommandHandler('command3', commands.command3))

    updater.start_polling()
    updater.idle()
