import telebot
import requests
import io

photos = []
i = 0

bot = telebot.TeleBot('')

unsplash_client_id = ''

def get_random_photo_urls():
    response = requests.get('https://api.unsplash.com/photos/random', params={'client_id': unsplash_client_id}).json()['urls']
    return response

def set_photos_query(query):
    response = requests.get('https://api.unsplash.com/search/photos', params={'client_id': unsplash_client_id, 'query': query}).json()['results']
    global photos,i
    photos = response
    i = 0

button_captions = {
    "random": "Випадкове зображення",
    "search": "Ще за останім запитом"
}

start_keyboard = telebot.types.ReplyKeyboardMarkup(True,True)
start_keyboard.row(button_captions["random"],button_captions["search"])

search_keyboard = telebot.types.ReplyKeyboardMarkup(True,True)
search_keyboard.row(button_captions["random"],button_captions["search"])

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.send_message(message.chat.id,"Вітаю!",reply_markup=start_keyboard)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global photos,i
    if message.text == button_captions["random"]:
        urls = get_random_photo_urls()
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Посилання",url=urls['raw'])
        keyboard.add(url_button)
        bot.send_photo(message.chat.id,photo=requests.get(urls['small']).content)
        bot.send_message(message.chat.id,'Випадкове зображення',reply_markup=keyboard)
    elif message.text == button_captions["search"]:
        if photos != []:
            keyboard = telebot.types.InlineKeyboardMarkup()
            i = i + 1
            url_button = telebot.types.InlineKeyboardButton(text="Посилання",url=photos[i]['urls']['raw'])
            keyboard.add(url_button)
            bot.send_photo(message.chat.id,photo=requests.get(photos[i]['urls']['small']).content)
            bot.send_message(message.chat.id,'Зображення по останьому запиту',reply_markup=keyboard)
    else:
        set_photos_query(message.text)
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Посилання",url=photos[0]['urls']['raw'])
        keyboard.add(url_button)
        bot.send_photo(message.chat.id,photo=requests.get(photos[0]['urls']['small']).content)
        bot.send_message(message.chat.id,'Зображення по запиту '+message.text,reply_markup=keyboard)
bot.polling()