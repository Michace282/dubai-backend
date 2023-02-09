from telegram.bot import Bot

TOKEN = '1678733652:AAGScC8WJtsIXq--nhtXT4eG477xUtXdk5s'
GROUP_ID = '-580988581'

bot = Bot(token=TOKEN)


def send_message(text):
    try:
        bot.send_message(GROUP_ID, text, parse_mode='html')
    except:
        pass
