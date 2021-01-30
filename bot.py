from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

class Bot:
    def __init__(self, token = ''):
        if token == '':
            return
        
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        
        self.dispatcher.add_handler(CommandHandler('start', self.handle_start))
        self.dispatcher.add_handler(CommandHandler('help', self.handle_help))
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_button))
    
    def startBot(self):
        self.updater.start_polling(poll_interval=0.5)
        self.updater.idle()

    def handle_start(self, update: Update, context: CallbackContext) -> None:
        keyboard = [
            [InlineKeyboardButton("Попасть в фильм", callback_data='/vid')],
            [InlineKeyboardButton("О боте", callback_data='/about')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)
    
    def handle_button(self, update: Update, context: CallbackContext):
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()
    
        query.edit_message_text(text=f"Selected option: {query.data}")
    
    def handle_help(self, update: Update, context: CallbackContext):
        update.message.reply_text("Use /start to test this bot.")
