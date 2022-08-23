import random
from telegram.ext import Filters
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackContext
import datetime

def start_game(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Привет, {update.effective_user.first_name}! Мы начинаем игру 'камень ножницы бумага'!\n Загадывай первый!\n Если камень - пиши 'к'\n Если ножницы - пиши 'н'\n Если бумага - пиши 'б'\n Если хочешь увидеть счет - пиши 'с'\n Если хочешь закончить игру - пиши '-'")

def log(update1: Update, update2: Update):
    file = open("db.csv", "a")
    file.write(f'{datetime.datetime.now().time()}, Opponent points - {update1}, your points - {update2}\n')
    file.close()
            
user_ball = 0
rand_ball = 0      
def UserMessage(update: Update, context: CallbackContext):
    global user_ball, rand_ball
    
    list_play = ['к', 'н', 'б']
    
    if update.message.text in list_play:
        rand = random.choice(list_play)
        update.message.reply_text(f"{rand}")
        if rand == 'к' and update.message.text == 'н':
            rand_ball += 1
        if rand == 'к' and update.message.text == 'б':
            user_ball += 1
        if rand == 'н' and update.message.text == 'к':
            user_ball += 1
        if rand == 'н' and update.message.text == 'б':
            rand_ball += 1
        if rand == 'б' and update.message.text == 'н':
            user_ball += 1
        if rand == 'б' and update.message.text == 'к':
            rand_ball += 1
    
    elif update.message.text == 'с':
        update.message.reply_text(f"Ваши баллы - {user_ball}, Баллы вашего соперника - {rand_ball}")
    elif update.message.text == '-':
        update.message.reply_text(f"Конец игры!\nВаши баллы - {user_ball}, Баллы вашего соперника - {rand_ball}")
        if user_ball> rand_ball:
            update.message.reply_text(f"{update.effective_user.first_name} - Вы выиграли!!!")
        elif user_ball == rand_ball:
            update.message.reply_text(f"Ничья")    
        else:
            update.message.reply_text(f"Вы проиграли :(((")        
        update.message.reply_text('Заходите ещё!')
        rand_ball=0
        user_ball=0
    else:
        update.message.reply_text('Вводите к, н или б')
    log(rand_ball, user_ball)
    return rand_ball, user_ball

updater = Updater("KEY")
updater.dispatcher.add_handler(CommandHandler("game", start_game))
updater.dispatcher.add_handler(MessageHandler(Filters.text, UserMessage))


print('Server start')
updater.start_polling()
updater.idle()