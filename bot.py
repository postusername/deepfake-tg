import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


SEND_VIDEO_TIMEOUT = 300
TEXT_START = 'Привет! Выбери действия из списка ниже:'
TEXT_KEYBOARD_VID = 'Сделать DeepFake'
TEXT_KEYBOARD_ABOUT = 'О боте'
TEXT_UNKNOWN_BUTTON = 'Неизвестная команда с кнопки бота. Пожалуйста, напишите нам об этом —> /feedback'
TEXT_ABOUT = 'Данный бот является дипломным проектом группы НР-У-22. В процессе разработки были изучены такие методы как Face Recognition & Encoding, а также методы создания Telegram-ботов. Мы много трудились над созданием этого проекта, поэтому, пожалуйста, оставьте обратную связь командой /feedback'
TEXT_SEND_PHOTO = 'Отправьте свою фотографию:'
TEXT_SEND_VIDEO = 'Теперь видеоролик (для наилучших результатов лицо должно быть ничем не перекрыто и занимать большую часть экрана):'
TEXT_ERROR_TOO_LONG = 'Ваш видеоролик слишком долгий! Пожалуйста, постарайтесь уложиться в 30 секунд.'
TEXT_ERROR_TOO_WIDE = 'Упс! Кажется, ваше видео *слишком* хорошего качества — в процессе обработки оно было бы сжато до 256 пикселей по большей стороне, так что полезная информация вряд-ли бы сохранилась. Попробуйте обрезать лицо чуть крупнее или отправить ролик не в таком большом разрешении.'
TEXT_START_SEND_VIDEO = 'Начинаю отправку...'
TEXT_VIDEO_CAPTION = 'Ролик готов! Если что-то пошло не так, напишите нам —> /feedback'
TEXT_KEYBOARD_BACK = 'Назад в меню'

keyboard = [[InlineKeyboardButton(TEXT_KEYBOARD_VID, callback_data='/vid')],
            [InlineKeyboardButton(TEXT_KEYBOARD_ABOUT, callback_data='/about')]]
start_keyboard = InlineKeyboardMarkup(keyboard)
back_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(TEXT_KEYBOARD_BACK, callback_data='/menu')]])


class Bot:
    def __init__(self, token = ''):
        if token == '':
            return
        
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        
        self.dispatcher.add_handler(CommandHandler('start', self.handle_start))
        self.dispatcher.add_handler(CommandHandler('menu', self.handle_start))
        self.dispatcher.add_handler(CommandHandler('help', self.handle_help))
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_button))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.handle_photo))
        self.dispatcher.add_handler(MessageHandler(Filters.video | Filters.animation, self.handle_video))
        self.dispatcher.add_handler(CommandHandler('about', self.handle_about))
        self.dispatcher.add_handler(CommandHandler('vid', self.handle_gen))
        
    def startBot(self):
        self.updater.start_polling()
        self.updater.idle()

    def handle_start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(TEXT_START, reply_markup=start_keyboard)
    
    def handle_help(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Use /start to test this bot.")
    
    def handle_about(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(text=TEXT_ABOUT, reply_markup=back_keyboard)
        
    def handle_gen(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(text=TEXT_SEND_PHOTO)
        
    def handle_button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        if query.data == '/about':
            query.edit_message_text(text=TEXT_ABOUT, reply_markup=back_keyboard)
        elif query.data == '/vid':
            query.edit_message_text(text=TEXT_SEND_PHOTO)
        elif query.data == '/menu':
            query.edit_message_text(text=TEXT_START, reply_markup=start_keyboard)
        else:
            query.edit_message_text(text=TEXT_UNKNOWN_BUTTON)
    
    def handle_photo(self, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user
        photo_file = update.message.photo[-1].get_file()
        
        os.system('mkdir photos') # Platform-independent
        photo_file.download(r'./photos/photo' + str(user.id) + r'.jpg')
        logger.info("Photo of %s: %s", user.first_name, r'./photos/photo' + str(user.id) + r'.jpg')
        
        update.message.reply_text(text=TEXT_SEND_VIDEO)
        
    def handle_video(self, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user
        anim_file = update.message.animation
        video_file = update.message.video if anim_file is None else anim_file
        
        if video_file.duration > 30:
            update.message.reply_text(TEXT_ERROR_TOO_LONG)
        elif video_file.width > 1024 or video_file.height > 1024:
            update.message.reply_text(TEXT_ERROR_TOO_WIDE)
        else:
            os.system('mkdir videos') # Platform-independent
            video_file.get_file().download(r'./videos/vid' + str(user.id) + r'.mp4', timeout=60)
            logger.info("Video of %s: %s", user.first_name, r'./videos/vid' + str(user.id) + r'.mp4')
        
            update.message.reply_text(TEXT_START_SEND_VIDEO)
            vid = open(r'./demo.mp4', 'rb')
            update.message.reply_video(video=vid, duration=video_file.duration, width=640, height=360, timeout=SEND_VIDEO_TIMEOUT)
            update.message.reply_text(TEXT_VIDEO_CAPTION, reply_markup=back_keyboard)