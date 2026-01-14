import telebot
from telebot import types
from openai import OpenAI
from config import TOKEN
from config import TELETOKEN
import database


#Init
bot = telebot.TeleBot(TELETOKEN)
database.create_tables()

# временное хранилище состояний (DEMO)
user_states = {}


#Keyboard
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Fill questionnaire")
    keyboard.add("Get career ideas")
    return keyboard


#Start
@bot.message_handler(commands=["help", "start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hi! I'm CareerPath Bot.\n"
        "I help you explore new career directions.\n\n"
        "Choose an option below:",
        reply_markup=main_menu()
    )


#Questionare
@bot.message_handler(func=lambda m: m.text == "Fill questionnaire")
def fill_questionnaire(message):
    user_states[message.from_user.id] = {"step": "age"}
    bot.send_message(message.chat.id, "How old are you?")


@bot.message_handler(func=lambda m: True)
def handle_answers(message):
    user_id = message.from_user.id

    if user_id not in user_states:
        return

    step = user_states[user_id]["step"]

    if step == "age":
        user_states[user_id]["age"] = message.text
        user_states[user_id]["step"] = "interests"
        bot.send_message(
            message.chat.id,
            "What are you interested in?\n"
            "(technology, art, people, business)"
        )

    elif step == "interests":
        user_states[user_id]["interests"] = message.text
        user_states[user_id]["step"] = "goal"
        bot.send_message(
            message.chat.id,
            "What is your main goal?\n"
            "(money / interest / freedom)"
        )

    elif step == "goal":
        user_states[user_id]["goal"] = message.text

        database.add_user(
            user_id = user_id,
            age = user_states[user_id]["age"],
            interests = user_states[user_id]["interests"],
            goal = user_states[user_id]["goal"]
        )

        user_message = "age:" + user_states[user_id]["age"] + ", interests:" + user_states[user_id]["interests"] + ", goal:" + user_states[user_id]["goal"]

        user_states.pop(user_id)

        user_id = message.chat.id
        bot.send_chat_action(user_id, 'typing')
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= TOKEN,
        )

        completion = client.chat.completions.create(
        extra_headers={
            
        },
        extra_body={},
        model="deepseek/deepseek-r1-0528:free",

        messages=[
            {
                "role": "system",
                "content": "Your name is Bot26,you are an artificial intelligence assistant created by T6UGGER,you help users by finding them the hobbies,activites etc. by their preferations"
            },
            {
            "role": "user",
            "content": user_message
            }
        ]
        )
        bot.reply_to(message, completion.choices[0].message.content)

        bot.send_message(
            message.chat.id,
            "Your profile is saved!\n"
            "Now I can suggest career ideas.",
            reply_markup=main_menu()
        )



#Bot run
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling()


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user_id = message.chat.id
    bot.send_chat_action(user_id, 'typing')
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= TOKEN,
    )

    completion = client.chat.completions.create(
    extra_headers={
        
    },
    extra_body={},
    model="deepseek/deepseek-chat-v3.1:free",

    messages=[
        {
            "role": "system",
            "content": "Your name is T6BOTI,you are an artificial intelligence assistant created by T6UGGER,you help users by solving their tasks,problems and other stuff"
        },
        {
        "role": "user",
        "content": message.text
        }
    ]
    )
    bot.reply_to(message, completion.choices[0].message.content)