#загрузка необходимых библиотек и модулей
import logging
import time 
import gspread
from aiogram import Bot, Dispatcher, executor, types,exceptions

# предварительная работа с google таблицами: подключение и определение места записи 

gc = gspread.service_account(filename='project-for-cafe-sunrise-9b017f6c5ba6.json')
bd_orders = gc.open("experemental01")
first_free_string = 1

try:
    while  len ((bd_orders.sheet1.get('A' + str(first_free_string)))[0][0])  > 0:
        first_free_string +=1
except:
    ...

# инициализация бота в телеграмме 

API_TOKEN = '6172045840:AAF61QxxP7-1WsX99HpwL2DrbxPDWkBhApE'
logging.basicConfig(level=logging.INFO) 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
outchat_id = -848730589

# определение классов

class Product():

    def __init__(self, name = '', price_tag = 0, size = '', supplements  = [], way = str):
        self.name = name
        self.price_tag = price_tag
        self.size = size
        self.supplements = supplements
        self.way = way

    def clean(self):
        if self.name in drinks_there_must_add_supplements: 
            self.supplements = [self.supplements[0]]
        else:
            self.supplements = []

    def get_price(self):
        price = 0 + self.price_tag
        for sup in self.supplements:
            price += sup.price_tag
        return price

class Order:
    def __init__(self, user):
        self.user = user
        self.product_list = []
        self.status = 'open'
        text = time.ctime(time.time())[4:].split(' ')
        self.last_action = time.time()
        morth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        text[0] = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'][morth.index(text[0])]
        print(text)
        self.number = text[-1] + ':' + text[0] + ':' + [text[2], '0'+text[2]][len(text[2]) == 1] + ':' +text[3]
        self.delivery_trigger = False
        self.comment_trigger = False
        self.comment = ''

    def set_comment(self, comment):
        self.comment = comment

    def add(self, way):
        directory = open_directory(menu[0], way[:-2], '🗒Меню')
        for item in directory[0]:
            if item.split('&')[0] == way[-2]:
                    directory[1] = item.split('&')[-1]
                    directory[0] = directory[0][item][int(way[-1])]
        self.product_list.append(Product(name=directory[1], price_tag=directory[0][1], size= directory[0][0], supplements= [], way = way[2]))

    def out(self):
        order_text = 'Заказ №' + self.number +'\nОт пользователя @' + str(self.user) +'\nАдрес ' + self.address + ' :'
        for p in self.product_list:
            supplements_text = ''
            for s in p.supplements:
                supplements_text += s.name  + ' '
            order_text += '\n - ' + p.name + ' ' + p.size + [' c ',''][len(p.supplements) == 0] + supplements_text 
        if len(self.comment) == 0:
            return order_text +'\nВремя получения заказа: ' + self.close_time[11:19]
        else:
            return order_text +'\nВремя получения заказа: ' + self.close_time[11:19] + '\nКомментарий к заказу:\n -"' + self.comment + '"'
        
    def refresh(self):
        self.last_action = time.time()

    def get_price(self):
        return sum(map(lambda product: product.get_price(), self.product_list))

    def close(self):
        self.status = 'in queue'
        self.product_list = tuple(self.product_list)
        self.close_time = time.ctime(time.time())

    def set_address(self, address):
        self.address = address
    
    def arhivate(self):
        global first_free_string
        bd_orders.sheet1.update_cell(first_free_string, 1, self.number)
        bd_orders.sheet1.update_cell(first_free_string, 2, '=ДАТА(' + self.number.split(':')[0] + ';' + self.number.split(':')[1] + ';' + self.number.split(':')[2] + ')' )
        products_in_order = ''
        for p in self.product_list:
            supplements_text = ''
            for s in p.supplements:
                supplements_text += s.name + '; '
            products_in_order += p.name + ' ' + p.size + [' c ',''][len(p.supplements) == 0] + supplements_text
        bd_orders.sheet1.update_cell(first_free_string, 3, products_in_order)
        bd_orders.sheet1.update_cell(first_free_string, 4, self.get_price())  
        first_free_string += 1
        ... #скрипт архивации в ексель таблице


# стартовые настройки: дерево меню, словарь пользователей, список добавок к напиткам, список напитков с обязательным сиропом и список с возможным
pay_contacts = ' по номеру: 8-916-533-65-58 \n'

menu = ({
        '0&еда':{
                '0&Пиццы':{
                            '0&Маргарита':[['25см', 260],['40см', 430],['1/6 от 40см', 70]],
                            '1&Пеперони':[['25см', 290],['40см', 490],['1/6 от 40см', 80]],
                            '2&Куриная':[['25см', 290],['40см', 490],['1/6 от 40см', 80]],
                            '3&4 сыра':[['25см', 290],['40см', 490],['1/6 от 40см', 80]],
                            '4&Салями':[['25см', 290],['40см', 490],['1/6 от 40см', 80]],
                            '5&Грибы ветчина':[['25см', 290],['40см', 490],['1/6 от 40см', 80]],
                            '6&Цезарь':[['25см', 290],['40см', 490],['1/6 от 40см', 80]],
                            '7&Жульен':[['25см', 290],['40см', 490],['1/6 от 40см', 80]]
                            },
                '1&Торты':{
                            '0&Чизкейк':[['', 150]],
                            '1&Торт шоколадный':[['', 150]]
                            },
                '2&Сэндвичи':{
                            '0&Сендвич с ветчиной и сыром':[['', 130]],
                            '1&Сендвич с курицей':[['', 130]]
                            }
                },
        '1&напитки':{
                    '0&Летние':{
                                '0&Ice латте':[['0,4л', 190]],
                                '1&Бамбл':[['0,4л', 190]],
                                '2&Эспрессо-тоник':[['0,4л', 190]],
                                '3&Ice американо':[['0,4л', 160]],
                                '4&Ice какао':[['0,4л', 160]],
                                '5&Ice раф':[['0,4л', 210]],
                                '6&Мохито':[['0,4л', 170]],
                                '7&Лимонад':[['0,4л', 130]],
                                '8&Ice tea':[['0,4л', 150]],
                                '9&Фраппучино':[['0,4л', 230]]
                                },
                    '1&Классика':{
                                '0&Эспрессо':[['0,2л', 100]],
                                '1&Американо':[['0,2л',100],['0,3л',130],['0,4л',150]],
                                '2&Капучино':[['0,2л',120],['0,3л',150],['0,4л',170]],
                                '3&Латте':[['0,2л',120],['0,3л',150],['0,4л',170]],
                                '4&Раф':[['0,2л',140],['0,3л',180],['0,4л',200]],
                                '5&Моккачино':[['0,2л',130],['0,3л',160],['0,4л',180]],
                                '6&Флэт уайт':[['0,2л',140]],
                                '7&Какао':[['0,2л',100],['0,3л',130],['0,4л',150]],
                                '8&Горячий шоколад':[['0,2л',120],['0,3л',140],['0,4л',190]],
                                '9&Чай на выбор':{
                                                '0&Черный Ассам':[['0,2л',80],['0,3л',100],['0,4л',130]],
                                                '1&Чёрныц Эрл грей':[['0,2л',80],['0,3л',100],['0,4л',130]],
                                                '2&Зелёная Сенча':[['0,2л',80],['0,3л',100],['0,4л',130]],
                                                '3&Зелёный Жасмин':[['0,2л',80],['0,3л',100],['0,4л',130]],
                                                '4&Фруктовый Каркаде':[['0,2л',80],['0,3л',100],['0,4л',130]],
                                                '5&Травяной Иван-чай':[['0,2л',80],['0,3л',100],['0,4л',130]]
                                                }
                                },
                    '2&Авторские':{
                                '0&Раф нат':[['0,4л', 230]],
                                '1&Раф цитрус':[['0,4л', 230]],
                                '2&Пряный чай':[['0,2л',140],['0,3л',190],['0,4л',220]],
                                '3&Облепиховый чай':[['0,4л', 220]],
                                '4&Имбирный чай':[['0,4л', 200]],
                                '5&Глинтвейн':[['0,4л', 210]],
                                '6&Матча латте':[['0,2л',130],['0,3л',180],['0,4л',210]],
                                '7&Глясе':[['0,4л', 190]]
                                    },
                    '3&Молочные коктейли':{
                                            '0&Клубника':[['0,4л', 230]],
                                            '1&Шоколад':[['0,4л', 230]],
                                            '2&Ваниль':[['0,4л', 230]]
                                            },
                    '4&Смузи':{
                                '0&Огурец сельдерей':[['0,4л', 200]],
                                '1&Клубника':[['0,4л', 200]],
                                '2&Банан шоколад':[['0,4л', 220]],
                                '3&Мята':[['0,4л', 200]]
                                },
                    '5&Фреш':{
                            '0&Апельсин':[['0,4л', 190]],
                            '1&Грейпфрут':[['0,4л', 220]]
                            },
                    '6&Холодильник':{
                                    '0&РЭД Булл':[['0,25л', 110],['0,5л', 210]],
                                    '1&Адреналин':[['0,25л', 80],['0,5л', 100]],
                                    '2&Кола':[['0,5л', 80],['1л', 150],['2л', 200]],
                                    '3&Фанта':[['0,5л', 80]],
                                    '4&Липтон':[['0,5л', 80]],
                                    '5&Вода':[['0,5л', 35]],
                                    '6&Горилла':[['0,5л', 100]],
                                    '7&Монстр':[['0,5л', 100]]
                                    }    
                    }
        },)

users_online = {}

supplements = [Product('альт.молоко', 50, '0.2л'), Product('альт.молоко', 70, '0.3л'), Product('альт.молоко', 90, '0.4л')]

acceptable_drinks_for_supplements = ['Ice латте','Бамбл','Эспрессо-тоник','Ice американо','Ice какао',
                                     'Ice раф','Мохито','Лимонад','Ice tea','Фраппучино',
                                     'Эспрессо','Американо','Капучино','Латте','Раф',
                                     'Моккачино','Флэт уайт','Какао','Горячий шоколад','Черный Ассам',
                                     'Чёрныц Эрл грей','Зелёная Сенча','Зелёный Жасмин','Фруктовый Каркаде','Травяной Иван-чай',
                                     'Раф нат','Раф цитрус','Пряный чай','Облепиховый чай','Имбирный чай',
                                     'Глинтвейн','Матча латте','Глясе']         #список напитков куда можно добавки

names_for_supplements = ['Карамель','Соленая карамель','Шоколадный',  #название сиропов
                         'Мята','Клубника','Малина',
                         'Ежевика','Кокос','Фундук',
                         'Ваниль','Мёд','Клён',
                         'Айриш']

drinks_there_must_add_supplements = ['Ice латте', 'Ice раф', 'Лимонад', 'Ice tea', 'Раф']

for i in names_for_supplements:                 #заполнение списка добавок к напиткам сиропами
    supplements.append(Product(i, 30, '', []))



# функции 
        #открытие вложенного словоря по id в названии
def open_directory(directory, way, name=''):    #открытие раздела в формате листа [содержимое; ключ]
    if len(way) < 1:                            #проверка ссылки на окончание пути
        return [directory, name]                #вывод содержимого раздела и его название
    for key in directory:                       #поиск нужного подраздела раздела по его id
        if way[0] == key.split('&')[0]:
            return open_directory(directory[key], way[1:], key.split('&')[-1])              #вызов функции для подраздела, если таковой определен
    return [directory, name]                    #вывод содержимого последнего найденного подраздела в случае если по ссылке дальше не удается пройти

        #сборщик мусора
deadline = 3600
extra_deadline = 600
last_clear = time.time()

def trash_collector(dline):
    global last_clear
    if time.time() - last_clear > dline:
        black_list = []
        last_clear = time.time() 
        for order in users_online:
            if time.time() - users_online[order].last_action > dline and users_online[order] == 'open':
                black_list.append(order)
        outdated_list = []
        for outdated in black_list:
            outdated_list.append(outdated)
            del users_online[order]
        return outdated_list
    else: return []

#стартовый обработчик сообщения

@dp.message_handler(commands=['start'])             #перехват сообщения запуска
async def send_welcome(message: types.Message):
    if message.chat.id != outchat_id:
        InlineKeyboard = types.InlineKeyboardMarkup()
        inlineKeyboard = types.InlineKeyboardMarkup()
        try:             
            users_online[message.from_user.id] = Order(message.from_user.id)          # корзина для каждого онлайн пользователя
        except MemoryError:
            trash_collector_memory = trash_collector(deadline)
            if len(trash_collector_memory) > 0:
                inlineKeyboard.add(types.InlineKeyboardButton(text= 'Начать заново', callback_data='start'))
                for order in trash_collector:
                    await bot.send_message(order, 'Ваши данные были стёрты из-за длительной неактивности.', reply_markup=inlineKeyboard)
        InlineKeyboard.add(types.InlineKeyboardButton(text='🗒 Меню 🗒', callback_data='open$menu')) # -кнопка с вызовом корневой вершины дерева-меню
        await message.answer("Привет!\nЯ бот от кафе Рассвет!\nОзнакомьтесь с нашим... ", reply_markup=InlineKeyboard)

#основной обработчик кнопок

@dp.callback_query_handler(lambda call:True)            #перехват любого сообщения с кнопок
async def start_hub_menu(call: types.CallbackQuery):    
    inlineKeyboard = types.InlineKeyboardMarkup()
    orderInlineKeyboard = types.InlineKeyboardMarkup()
    trash_collector_memory = trash_collector(deadline)
    if len(trash_collector_memory) > 0:
        inlineKeyboard.add(types.InlineKeyboardButton(text= 'Начать заново', callback_data='open$menu'))
        for order in trash_collector:
            await bot.send_message(order, 'Ваши данные были стёрты из-за длительной неактивности.', reply_markup=inlineKeyboard)
    commandList = call.data.split('$') 

    try:
        if commandList[0] != 'start':
            users_online[call.from_user.id].comment_trigger = False
            users_online[call.from_user.id].delivery_trigger = False
        if commandList[0] == 'order':
            if commandList[2] == 'cook':
                if commandList[3] == 'start' and users_online[int(commandList[1])].status == 'in queue':
                    orderInlineKeyboard.add(types.InlineKeyboardButton('Готов', callback_data='order$'+commandList[1] +'$cook$ready'))
                    users_online[int(commandList[1])].status = 'cooking'
                    await bot.send_message(int(commandList[1]), 'Ваш заказ начали готовить.' )
                    await bot.send_message(outchat_id, users_online[int(commandList[1])].out(), reply_markup=orderInlineKeyboard)

                elif commandList[3] == 'ready' and users_online[int(commandList[1])].status == 'cooking':
                    if users_online[int(commandList[1])].address in ['"В зале"', '"С собой"']:
                        orderInlineKeyboard.add(types.InlineKeyboardButton('Закрыть', callback_data='order$'+commandList[1] +'$cook$end'))
                        users_online[int(commandList[1])].status = 'ready'
                        await bot.send_message(int(commandList[1]), 'Ваш заказ готов. Можете подойти и забрать его.' )
                        await bot.send_message(outchat_id, users_online[int(commandList[1])].out(), reply_markup=orderInlineKeyboard)  
                    else:
                        orderInlineKeyboard.add(types.InlineKeyboardButton('Доставить', callback_data='order$'+commandList[1] +'$cook$dlvr'))
                        users_online[int(commandList[1])].status = 'deliver'
                        await bot.send_message(int(commandList[1]), 'Ваш заказ готов. Первый освободившийся курьер возьмёт его.' )
                        await bot.send_message(outchat_id, users_online[int(commandList[1])].out(), reply_markup=orderInlineKeyboard)

                elif commandList[3] == 'dlvr' and users_online[int(commandList[1])].status == 'deliver':
                    orderInlineKeyboard.add(types.InlineKeyboardButton('Закрыть', callback_data='order$'+commandList[1] +'$cook$dend'))
                    users_online[int(commandList[1])].status = 'dready'
                    await bot.send_message(int(commandList[1]), 'Ваш заказ готов и уже в пути.' )
                    await bot.send_message(outchat_id, users_online[int(commandList[1])].out(), reply_markup=orderInlineKeyboard)
                    
                elif commandList[3] == 'end' and users_online[int(commandList[1])].status == 'ready':
                    users_online[int(commandList[1])].status = 'close'
                    users_online[int(commandList[1])].arhivate()
                    del users_online[int(commandList[1])]
                    inlineKeyboard.add(types.InlineKeyboardButton('Открыть новый заказ', callback_data='start'))
                    await bot.send_message(int(commandList[1]), 'Спасибо за посещение нашего кафе. Делитесь впечатлениями с друзьями и приходите ещё. Ждём вас.', reply_markup=inlineKeyboard)
                    await bot.send_message(outchat_id, 'Заказ был перенесён в архив.', reply_markup=orderInlineKeyboard)

                elif commandList[3] == 'dend' and users_online[int(commandList[1])].status == 'dready':
                    users_online[int(commandList[1])].status = 'close'
                    users_online[int(commandList[1])].arhivate()
                    del users_online[int(commandList[1])]
                    inlineKeyboard.add(types.InlineKeyboardButton('Открыть новый заказ', callback_data='start'))
                    await bot.send_message(int(commandList[1]), 'Спасибо за посещение нашего кафе. Делитесь впечатлениями с друзьями и приходите ещё. Ждём вас.', reply_markup=inlineKeyboard)
                    await bot.send_message(outchat_id, 'Заказ был перенесён в архив.', reply_markup=orderInlineKeyboard)

            elif commandList[2] == 'waiver':
                if commandList[3] == 'write':
                    orderInlineKeyboard.add(types.InlineKeyboardButton('Нет возможности приготовить', callback_data='order$'+commandList[1] +'$waiver$pnf'))
                    orderInlineKeyboard.add(types.InlineKeyboardButton('Вернуться', callback_data='order$'+commandList[1] +'$waiver$remove'))
                    users_online[int(commandList[1])].status = 'rejection'
                    await bot.send_message(outchat_id, 'Укажите причину отказа от заказа №'+ users_online[int(commandList[1])].number +':', reply_markup=orderInlineKeyboard)

                elif commandList[3] == 'pnf' and users_online[int(commandList[1])].status == 'rejection':
                    del users_online[int(commandList[1])]
                    await bot.send_message(int(commandList[1]), 'По причине отсутствия некоторых ингридиентов ваш заказ был отклонён, просим прощения.')   

                elif commandList[3] == 'remove' and users_online[int(commandList[1])].status == 'rejection':
                    users_online[int(commandList[1])].status = 'in queue'
                    await bot.send_message(outchat_id, users_online[call.from_user.id].out(), reply_markup=orderInlineKeyboard)       

        elif commandList[0] == 'open' and call.message.chat.id != outchat_id:
            if commandList[1] == 'menu':
                directory = open_directory(menu[0], commandList[2:], '🗒 Меню 🗒')
                for obj in directory[0]:
                    if type(directory[0][obj]) == list:
                        inlineKeyboard.add( types.InlineKeyboardButton(text= obj.split('&')[-1] , callback_data= 'open$objmenu$'+'$'.join(commandList[2:])+'$'+obj.split('&')[0]))
                    else:
                        inlineKeyboard.add( types.InlineKeyboardButton(text= obj.split('&')[-1] , callback_data= '$'.join(commandList)+'$'+obj.split('&')[0]))

                await call.message.answer(directory[1]+":", reply_markup=inlineKeyboard)

            elif commandList[1] == 'objmenu':
                directory = open_directory(menu[0], commandList[2:-1], '🗒 Меню 🗒')
                for item in directory[0]:
                    if item.split('&')[0] == commandList[-1]:
                        directory[1] = item.split('&')[-1]
                        directory[0] = directory[0][item]
                message_text = ''
                way_to_add = 'cart$add$'
                if directory[1] in drinks_there_must_add_supplements:
                    way_to_add = 'sup$nec$'
                if len(directory[0]) == 1:
                    message_text = directory[1] + ' ' + directory[0][0][0] + ' за ' + str(directory[0][0][1]) + '₽'
                    inlineKeyboard.add(types.InlineKeyboardButton(text = 'Добавить ', callback_data= 'open$' + way_to_add +'$'.join(commandList[2:]) +'$0'))
                else:
                    message_text = 'Добавить' + directory[1] + ':'
                    instance_number = 0
                    for instance in directory[0]:
                        inlineKeyboard.add(types.InlineKeyboardButton(text = directory[0][instance_number][0] + ' за ' + str(directory[0][instance_number][1])+ '₽',
                                                                       callback_data= 'open$' + way_to_add +'$'.join(commandList[2:])+'$' + str(instance_number)))
                        instance_number += 1

                await call.message.answer(message_text, reply_markup=inlineKeyboard)
            
            elif commandList[1] == 'sup':
                if commandList[2] == 'nec':
                    for sup in range(3, len(supplements)):
                        inlineKeyboard.add(types.InlineKeyboardButton( text = supplements[sup].name + ' | +' + str(supplements[sup].price_tag - 30) + '₽',
                                                                       callback_data= 'open$cart$add$' + '$'.join(commandList[3:]) + '$sup$' + str(sup)))
                    await call.message.answer("К данному напитку обязательно идёт сироп, который включен в цену:", reply_markup=inlineKeyboard)
                                                        #эту команду не включил к $red or $add or... из-за масштабности кода и отдельного сообщения для неё
                elif commandList[3] == 'addmenu':        #commandList[0] = open; commandList[1] = sup; commandList[2] = product number in order.product_list  ; commandList[3] = command 
                    if users_online[call.from_user.id].product_list[int(commandList[2])].size == '0,2л':
                        inlineKeyboard.add( types.InlineKeyboardButton(text=supplements[0].name + '| +' + str(supplements[0].price_tag) +'₽', callback_data = 'open$sup$' + commandList[2] + '$add$0'))
                    elif users_online[call.from_user.id].product_list[int(commandList[2])].size == '0,3л':
                        inlineKeyboard.add( types.InlineKeyboardButton(text=supplements[1].name + '| +' + str(supplements[1].price_tag) +'₽', callback_data = 'open$sup$' + commandList[2] + '$add$1'))
                    elif users_online[call.from_user.id].product_list[int(commandList[2])].size == '0,4л':
                        inlineKeyboard.add( types.InlineKeyboardButton(text=supplements[2].name + '| +' + str(supplements[2].price_tag) +'₽', callback_data = 'open$sup$' + commandList[2] + '$add$2'))
                    for supplement_number in range(3, len(supplements)):
                        inlineKeyboard.add( types.InlineKeyboardButton(text=supplements[supplement_number].name + '| +' + str(supplements[supplement_number].price_tag) +'₽',
                                                                        callback_data = 'open$sup$' + commandList[2] + '$add$' + str(supplement_number)))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🛒 вернуться 🛒', callback_data = 'open$cart$red$' + commandList[2]))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🗒 меню 🗒', callback_data = 'open$menu'))
                    await call.message.answer("Список возможных добавок к напитку:", reply_markup=inlineKeyboard)

                elif commandList[2] == 'removeexc':
                    await  call.message.answer("Это обязательная добавка, её нельзя убрать.")

                elif commandList[3] in ['red','add','remove']:     #commandList[0] = open; commandList[1] = sup; commandList[2] = product number in order.product_list  ; commandList[3] = command ; commandList[4] = supplement number in supplements 
                                                                       #включил сюда маленькие команды с похожим каркасом commandList, для экономии, наглядности и уменьшения промежуточных окон
                    if commandList[3] == 'add':
                        users_online[call.from_user.id].product_list[int(commandList[2])].supplements.append(supplements[int(commandList[4])])
                    elif commandList[3] == 'remove':
                        del users_online[call.from_user.id].product_list[int(commandList[2])].supplements[int(commandList[4])]
                    elif commandList[3] == 'clean':
                        users_online[call.from_user.id].product_list[int(commandList[2])].clean()
                    


                    for index_sup in range(len(users_online[call.from_user.id].product_list[int(commandList[2])].supplements)):
                        if users_online[call.from_user.id].product_list[int(commandList[2])].supplements[index_sup].price_tag == 0:
                            inlineKeyboard.add(types.InlineKeyboardButton(text='🪨' + users_online[call.from_user.id].product_list[int(commandList[2])].supplements[index_sup].name +
                                                                           ' | +' + str(users_online[call.from_user.id].product_list[int(commandList[2])].supplements[index_sup].price_tag) +
                                                                            '₽', callback_data= 'open$sup$removeexc$'))
                        else:
                            inlineKeyboard.add(types.InlineKeyboardButton(text=users_online[call.from_user.id].product_list[int(commandList[2])].supplements[index_sup].name +
                                                                           ' | +' + str(users_online[call.from_user.id].product_list[int(commandList[2])].supplements[index_sup].price_tag) +
                                                                            '₽', callback_data= 'open$sup$' + commandList[2] + '$remove$'+str(index_sup)))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='добавить', callback_data = 'open$sup$' + commandList[2] + '$addmenu'))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='убрать все добавки', callback_data = 'open$sup$' + commandList[2] + '$clean'))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🛒 вернуться 🛒', callback_data = 'open$cart$red$' + commandList[2]))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🗒 меню 🗒', callback_data = 'open$menu'))
                    await call.message.answer("Список добавок к напитку:", reply_markup=inlineKeyboard)
            

            elif commandList[1] == 'cart':
                if commandList[2] == 'add':
                    if commandList[-2] == 'sup':
                        users_online[call.from_user.id].add(commandList[3:-2])
                        users_online[call.from_user.id].product_list[-1].supplements.append(supplements[int(commandList[-1])])
                        users_online[call.from_user.id].product_list[-1].supplements[-1].price_tag = 0
                    else:
                        users_online[call.from_user.id].add(commandList[3:])
                    inlineKeyboard.add( types.InlineKeyboardButton( text = '🛒 Корзина 🛒', callback_data = 'open$cart$show') )
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🗒 меню 🗒', callback_data = 'open$menu'))
                    await call.message.answer('Успешно добавленно в вашу корзину.' , reply_markup=inlineKeyboard)

                elif commandList[2] == 'show':
                    if len(commandList) == 5:
                        if commandList[3] =='del':
                            del users_online[call.from_user.id].product_list[int(commandList[4])] 
                    item_number = 0
                    for item in users_online[call.from_user.id].product_list:
                        print(item)
                        inlineKeyboard.add( types.InlineKeyboardButton( text = item.name + ' | ' + str(item.get_price()), callback_data = 'open$cart$red$' + str(item_number)) )
                        item_number +=1
                    
                    inlineKeyboard.add( types.InlineKeyboardButton( 'Всего | ' + str (users_online[call.from_user.id].get_price()), callback_data= 'open$preend') )
                    inlineKeyboard.add( types.InlineKeyboardButton(text='-----------------------------', callback_data= 'none') )
                    if len(users_online[call.from_user.id].comment) == 0:
                        inlineKeyboard.add( types.InlineKeyboardButton(text='✏️ добавить комментарий к заказу  ✏️', callback_data = 'open$addcomment'))
                    else:
                        inlineKeyboard.add( types.InlineKeyboardButton(text='комментарий:', callback_data = 'open$addcomment'))
                        inlineKeyboard.add( types.InlineKeyboardButton(text='"' + users_online[call.from_user.id].comment + '"', callback_data = 'open$addcomment'))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🗒 меню 🗒', callback_data = 'open$menu'))
                    await call.message.answer('🛒        Ваша корзина:        🛒', reply_markup=inlineKeyboard)

                elif commandList[2] == 'red':
                         
                    if users_online[call.from_user.id].product_list[int(commandList[3])].name in acceptable_drinks_for_supplements:
                        inlineKeyboard.add( types.InlineKeyboardButton(text='🧴 добавки 🧴', callback_data = 'open$sup$' + commandList[3] + '$red'))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🗑️ убрать 🗑️', callback_data = 'open$cart$show$del$' + commandList[3]))
                    inlineKeyboard.add( types.InlineKeyboardButton(text='🛒 вернуться 🛒', callback_data = 'open$cart$show'))
                    await call.message.answer(users_online[call.from_user.id].product_list[int(commandList[3])].name, reply_markup=inlineKeyboard)

            elif commandList[1] == 'preend':
                inlineKeyboard.add( types.InlineKeyboardButton(text='Вернуться', callback_data='open$cart$show'))
                inlineKeyboard.add( types.InlineKeyboardButton(text='В зале', callback_data='open$pay_order$in_cafe'))
                inlineKeyboard.add( types.InlineKeyboardButton(text='С собой', callback_data='open$pay_order$with_myself'))
                if users_online[call.from_user.id].get_price() < 750:
                    inlineKeyboard.add( types.InlineKeyboardButton(text='Доставка недоступна', callback_data='open$dlvr$break'))
                else:
                    inlineKeyboard.add( types.InlineKeyboardButton(text='Доставка', callback_data='open$dlvr$start'))
                await call.message.answer('Как вам хочется получить заказ? \nОбратите внимание, редактировать заказ после оправления нельзя.', reply_markup=inlineKeyboard)
            
            elif commandList[1] == 'pay_order':
                users_online[call.from_user.id].close()
                orderInlineKeyboard.add(types.InlineKeyboardButton(text='Начать готовить', callback_data= 'order$'+str(call.from_user.id)+'$cook$start'))
                orderInlineKeyboard.add(types.InlineKeyboardButton(text='Отказаться', callback_data= 'order$'+str(call.from_user.id)+'$waiver$write'))
                if commandList[2] == 'in_cafe':
                    users_online[call.from_user.id].set_address('"В зале"')
                elif commandList[2] == 'with_myself':
                    users_online[call.from_user.id].set_address('"С собой"')
                elif commandList[2] == 'dlvr_close':
                    ...
                await call.message.answer("Мы будем уведомлять вас на какой стадии ваш заказ.\nНомер вашего заказа: №" + users_online[call.from_user.id].number)
                await call.message.answer("Пока можете оплатить заказ переводом " + str(users_online[call.from_user.id].get_price()) + "₽ сюда: \n" + pay_contacts)
                await bot.send_message(outchat_id, users_online[call.from_user.id].out(), reply_markup=orderInlineKeyboard)       

            elif commandList[1] == 'dlvr':
                if commandList[2] == 'start':
                    await call.message.answer("Напишите пожалуйста адрес доставки.")
                    users_online[call.from_user.id].delivery_trigger = True
                elif commandList[2] == 'break':
                    await call.message.answer("Доставка доступна при общей стоимости корзины более 750₽")

            elif commandList[1] == 'addcomment':
                await call.message.answer("Напишите сюда свои пожелания к заказу или уточнения:")
                users_online[call.from_user.id].comment_trigger = True

        elif commandList[0] == 'start':
            users_online[call.from_user.id] = Order(call.from_user.id)
            inlineKeyboard.add(types.InlineKeyboardButton(text='🗒 Меню 🗒', callback_data='open$menu')) # -кнопка с вызовом корневой вершины дерева-меню
            await call.message.answer("Привет!\nЯ бот от кафе Рассвет!\nОзнакомьтесь с нашим... ", reply_markup=inlineKeyboard)

        elif commandList[0] == 'none':
            ...    


    except exceptions.ButtonDataInvalid:
        print('CritError: Command List drop out of limit 64 byte memory.')
        await bot.send_message(outchat_id, 'CommandList drop out of limit of 64 byte memory. Some buttons break a work and can critical go out a telegram-bot . Telegram-bot was stop take orders.')
    except MemoryError:
            trash_collector_memory = trash_collector(extra_deadline)
            if len(trash_collector_memory) > 0:
                inlineKeyboard.add(types.InlineKeyboardButton(text= 'Начать заново', callback_data='open$menu'))
            for order in trash_collector:
                await bot.send_message(order, 'Ваши данные были стёрты из-за длительной неактивности.', reply_markup=inlineKeyboard)
    except KeyError:
        inlineKeyboard.add( types.InlineKeyboardButton(text='🗒меню🗒', callback_data='open$menu'))
        users_online[call.from_user.id] = Order(call.from_user.id)
        await call.message.answer("Сведения о вашем заказе не были найдены. Возможно это связано с взаимодействием с кнопками из предыдущих заказов. Мы открыли для вас новый заказ.", reply_markup=inlineKeyboard)
        
    except AttributeError:    
        await call.message.answer("К сожалению после отправления заказа в Кафе редактировать его нельзя. Если вы хотите заказать ещё что-нибудь, дождитесь выполнения предыдущего заказа.", reply_markup=inlineKeyboard)


@dp.message_handler(lambda message:True)             #перехват сообщений при заполнении комментария к заказу или адреса
async def send_welcome(message: types.Message):   
    inlineKeyboard = types.InlineKeyboardMarkup()

    if users_online[message.from_user.id].delivery_trigger == True:
        users_online[message.from_user.id].set_address(message.text)
        inlineKeyboard.add( types.InlineKeyboardButton(text='Адрес точный', callback_data='open$pay_order$dlvr_close'))
        inlineKeyboard.add( types.InlineKeyboardButton(text='Хочу вернуться к корзине', callback_data='open$cart$show'))
        await message.answer('Убедитесь пожалуйста в верности адреса. Если адрес неверный просто напишите его заново.', reply_markup=inlineKeyboard)    
    if users_online[message.from_user.id].comment_trigger == True:
        users_online[message.from_user.id].set_comment(message.text)
        inlineKeyboard.add( types.InlineKeyboardButton(text='🗒 Меню 🗒', callback_data='open$menu'))
        inlineKeyboard.add( types.InlineKeyboardButton(text='Вернуться к корзине', callback_data='open$cart$show'))
        await message.answer('Комментарий:\n" - '+ message.text +'"\n прикреплён к заказу.', reply_markup=inlineKeyboard)   
                
                        
                


                    
                     
                

                    

    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)