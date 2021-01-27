import sys

if len(sys.argv) > 1:
    print("Привет, {}!".format(sys.argv[1]))
else:
    print("Укажите ключ аутентификации.")
    sys.exit()