from telebot import types
from doctors import logic

import telebot


doctors_name = {
    'Иванов И.И' : 'ivanov' ,
    'Петров П.П' : 'petrov',
    'Сидоров В.Г': 'sidorov'
}


client = {

}

doctors_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

ivn_btn = types.KeyboardButton("Иванов И.И") 
per_btn = types.KeyboardButton("Петров П.П")
sid_btn = types.KeyboardButton("Сидоров В.Г")

doctors_keyboard.add(ivn_btn, per_btn, sid_btn)


accept_keyboard =  types.ReplyKeyboardMarkup(resize_keyboard=True)

yes_btn = types.KeyboardButton("Да!")
no_btn = types.KeyboardButton("Нет!")

accept_keyboard.add(yes_btn, no_btn)



company_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

about_btn = types.KeyboardButton("Об организации")
doctor_btn = types.KeyboardButton("Записаться на прием")
call_operator_btn = types.KeyboardButton("Позвонить опрератору")

company_keyboard.add(doctor_btn)

def BotInit(token: str):    
    if token:
        bot = telebot.TeleBot(token)
    else:
        return
    
    @bot.message_handler(commands=['start'])
    def start_button(message):
        bot.send_message(message.chat.id, "Ввидите ваше имя!")
        client[message.chat.id] = dict(state='new')

    @bot.message_handler(func=lambda message: message.chat.id in client and 'name' not in client[message.chat.id], )
    def get_name(message):
        client[message.chat.id]['name'] = message.text
        bot.send_message(message.chat.id, f"Отлично! {client[message.chat.id]['name']}! А теперь выберете интересующую Вас опцию!", reply_markup=company_keyboard)


    @bot.message_handler(func=lambda message: message.chat.id in client and 'name' in client[message.chat.id] and client[message.chat.id]['state'] == 'register'  and 'target' not in client[message.chat.id])
    def set_target(message):
        client[message.chat.id]['target'] = message.text
        bot.send_message(message.chat.id, f"Благодарим Вас, {client[message.chat.id]['name']}, что вы записали {client[message.chat.id]['target']}  к нам на прием!\nОсталось выбрать врача и дату!", reply_markup=doctors_keyboard)


    @bot.message_handler(content_types=['text'], func=lambda messages: messages.chat.id in client and 'target_doctor' in client[messages.chat.id] and 'target_date' in client[messages.chat.id] and client[messages.chat.id]['state'] == 'end')
    def save_result(message):

        time = message.text
        
        client[message.chat.id]['target_time'] = time
        client[message.chat.id]['state'] = 'full'
        
        bot.send_message(message.chat.id, f"Все данные заполнены успешно. Давайте все проверим!\nВрач: {client[message.chat.id]['target_doctor']} \nДата: {client[message.chat.id]['target_date']} \nВремя: {client[message.chat.id]['target_time']}\nВсе верно?", reply_markup=accept_keyboard)
        

    
    @bot.message_handler(content_types=['text'], func=lambda message: message.chat.id in client and 'target_doctor' in client[message.chat.id] and 'target_date' not in client[message.chat.id])
    def set_time(message):
        
        date = message.text

        client[message.chat.id]['target_date'] = date
        client[message.chat.id]['state'] = 'end'
        
        name = client[message.chat.id]['target_doctor']
        
        timetable_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        

        for day in logic.GetPlanAllDoctor()[name]['plan']:
            if day['day'] == date:
                for item in day['timetable']:
                    if item['state'] == False:
                        timetable_keyboard.add(item['time']) 
                
        bot.send_message(message.chat.id, "Выберите свбодное время", reply_markup=timetable_keyboard)
        

    @bot.message_handler(content_types=['text'], func=lambda message: message.chat.id in client and 'target_doctor' in client[message.chat.id] and 'target_date' in client[message.chat.id] and 'target_time' in client[message.chat.id])
    def save(message):   
        if message.text == "Да!":
            doctor = client[message.chat.id]['target_doctor']
            date = client[message.chat.id]['target_date']
            time = client[message.chat.id]['target_time']

            logic.Save(doctor, date, time, True)

            bot.send_message(message.chat.id, "Спасибо, ваши данные успешно сохранены")
        
     
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "Записаться на прием":
            if 'state' in client[message.chat.id]:
                client[message.chat.id]['state'] = 'register'
                bot.send_message(message.chat.id, f"{client[message.chat.id]['name']}, ввидите ФИО кого Вы хотите записать на прием")

        if message.text in doctors_name:
            client[message.chat.id]['state'] = 'choose'
        
            name = doctors_name[message.text]
                        
            client[message.chat.id]['target_doctor'] = name
                    
            plan = logic.GetPlanAllDoctor()[name]['plan']
            
            days_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

            for day in plan:
                days_keyboard.add(day['day'])
                
            bot.send_message(message.chat.id, "Выберите дату", reply_markup=days_keyboard)
    
    return bot

