import sys
import logging

from bot import Bot
b = Bot()

if len(sys.argv) > 1:
    b = Bot(sys.argv[1])
else:
    print("Укажите ключ аутентификации.")
    sys.exit()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


b.startBot()