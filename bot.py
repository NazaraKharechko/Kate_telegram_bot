import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('stiker/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомне число")
    item2 = types.KeyboardButton("😊 Як життя?")
    item3 = types.KeyboardButton("Хочу смайл?")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Привіт, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот створиний щоб бути "
                     "тестовим кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомне число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😊 Як життя?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Супер", callback_data='good')
            item2 = types.InlineKeyboardButton("Такоє собі", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Добре, сам як?', reply_markup=markup)
        elif message.text == 'Хочу смайл?':
            sti2 = open('stiker/sticker.webp', 'rb')
            bot.send_sticker(message.chat.id,  sti2)
        else:
            bot.send_message(message.chat.id, 'Я не знаю що сказати 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот і чудово 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Буває не кисне 😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Як життя?",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                      text="Це тестове повідомленя просто цикне ОК)")

    except Exception as e:
        print(repr(e))


# RUn
bot.polling(none_stop=True)
