from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
from setting import Token
import json
from apscheduler.schedulers.background import BackgroundScheduler


def reg_user_in_db(user):
    user_json = {
        "name": user,
        "ВС": 0,
        "НВС": 0,
        "КК": 0,
        "ДК": 0,
        "ТИ": 0,
        "МБ": 0,
        "СИМ": 0,
        "МНП": 0,
        "ПД": 0,
        "ТПРО": 0,
        "ОЛЕГ": 0,
        "ЗК": 0,
    }
    try:
        with open('db_users.json', encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []
    if not user in data:
        data.append(user_json)
    else:
        print(1)

    with open('db_users.json', "w", encoding="utf-8") as f:
        json.dump(data, f)


def update_user_in_db(user, message):
    try:
        with open("db_users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        print("Ошибка чтения файла")
        data = []

    for item in data:
        if item['name'] == user:
            add_offers(item, message)

    with open('db_users.json', "w", encoding="utf-8") as f:
        json.dump(data, f)


def start_new_month():
    with open("db_users.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        item['sales'] = 0

    with open('db_users.json', "w", encoding="utf-8") as f:
        json.dump(data, f)


def add_offers(item, message):
    if "ВС" in message:
        item['ВС'] += int(message[message.index("ВС") + 1])
    if "КК" in message:
        item["КК"] += int(message[message.index("КК") + 1])
    if "ДК" in message:
        item["ДК"] += int(message[message.index("ДК") + 1])
    if "ТИ" in message:
        item["ТИ"] += int(message[message.index("ТИ") + 1])
    if "СИМ" in message:
        item["СИМ"] += int(message[message.index("СИМ") + 1])
    if "МНП" in message:
        item["МНП"] += int(message[message.index("МНП") + 1])
    if "ПД" in message:
        item["ПД"] += int(message[message.index("ПД") + 1])
    if "НВС" in message:
        item["НВС"] += int(message[message.index("НВС") + 1])
    if "МБ" in message:
        item["МБ"] += int(message[message.index("МБ") + 1])
    if "ТПРО" in message:
        item["ТПРО"] += int(message[message.index("ТПРО") + 1])
    if "ОЛЕГ" in message:
        item["ОЛЕГ"] += int(message[message.index("ОЛЕГ") + 1])
    if "ЗК" in message:
        item["ЗК"] += int(message[message.index("ЗК") + 1])


def static():
    with open("db_users.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        print(data)


async def update_sales(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    update_user_in_db(user.username, update.message.text.split())
    print(update.message.text.split())
    with open("db_users.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    curr = list(filter(lambda x: x["name"] == user.username, data))
    text = ''
    for key, value in curr[0].items():
        text += f'{key}: {value}\n'
    await update.message.reply_text(text=text)


async def reg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user

    reg_user_in_db(user.username)
    await update.message.reply_text(text="Привет, " + user.username + "! В  ведите ваше имя и количество продаж")


def main() -> None:
    app = Application.builder().token(Token).build()

    app.add_handler(CommandHandler("reg", reg))
    app.add_handler(CommandHandler("send", update_sales))
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_new_month, 'cron', day='1')
    scheduler.start()

    app.run_polling()


if __name__ == "__main__":
    try:
        main()
    except:
        pass
