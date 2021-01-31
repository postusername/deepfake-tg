import sys

from bot import Bot
b = Bot()

if len(sys.argv) > 1:
    b = Bot(sys.argv[1])
else:
    print("Укажите ключ аутентификации.")
    sys.exit()

b.startBot()